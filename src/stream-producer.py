"""
Keep producing events continously 
run `python3 stream-producer.py --count 1000 --cycle 10` 
This will produce `1000*10=10000 events
"""
import argparse
import datetime
import io
import random

import avro.io
from confluent_kafka import Producer

# broker information
broker_servers = 'localhost:9092'


def flush(this_producer):
    this_producer.flush()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate simulated NetFlow streams')
    parser.add_argument('--topic-name', dest='topic', action='store',
                        default='avro_topic', help='netflow', required=False)
    parser.add_argument('--client-id', dest='clientid', action='store',
                        default='my-app', help='Kafka-P01', required=False)
    parser.add_argument('--cycle', dest='cy', action='store', type=int,
                        default=1, help='Number if iteration [1-100]', required=False, )
    parser.add_argument("--count", dest='count', type=int, default=10,
                        help="Number of messages to send")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    # Producer Definition
    producer_config = {
        'bootstrap.servers': broker_servers,
        'batch.size': 262144,  # num of bytes
        'linger.ms': 10,  # after 10 millisecond send the package
        'acks': 1,
        'client.id': args.clientid,
        'compression.codec': 'snappy',
    }

    producer = Producer(producer_config)

    # Base Data template
    base_data = {"id": 1, "firstname": "James "}

    # Avro encoding setup using the in-line schema
    avro_schema = '''{
          "namespace": "com.rupesh.spark.example.types",
          "type": "record",
          "name": "person",    
          "fields": [
            {"name": "id","type": ["int", "null"]},
            {"name": "firstname","type": ["string", "null"]}
          ]
        }'''
    schema = avro.schema.parse(avro_schema)
    writer = avro.io.DatumWriter(schema)

    topic = args.topic
    msgArr = []
    msgCount = args.count
    for i in range(msgCount):
        data = base_data
        data['id'] = random.randint(1, 99999)
        data['firstname'] = random.choice(
            ["Rupesh", "Ritesh", "Rakesh", "Rajnish", "Nisha", "Sheetal", "Preeti", "Shobha", "Rajkumar"])
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(data, encoder)
        raw_bytes = bytes_writer.getvalue()
        msgArr.append(raw_bytes)

    # Make this run forever
    print(
        f'Start of data pub: topic={topic} time={str(datetime.datetime.now())}')
    cycled = 0
    cy = args.cy
    while 1:
        if cy != 0 and cycled >= cy:
            print('End of data pub - ', str(datetime.datetime.now()),
                  'Message Count - ', cy*msgCount)
            break

        cycled += 1
        messages_to_retry = 0
        i = 0
        for msg in msgArr:
            try:
                i = i + 1
                producer.produce(topic=topic, value=msg)
                if (i % 100000) == 0:
                    flush(producer)
                    i = 0
            except BufferError as e:
                messages_to_retry += 1

        for msg in msgArr[:messages_to_retry]:
            producer.poll(0)  # check if kafka is there
            try:
                producer.produce(topic=topic, value=msg)
            except BufferError as e:
                producer.poll(0)
                producer.produce(topic=topic, value=msg)

        flush(producer)
