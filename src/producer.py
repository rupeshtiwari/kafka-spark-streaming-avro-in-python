"""
python3 producer.py
"""
import argparse
import io

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
    parser.add_argument("-c", "--count", type=int, default=10,
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
    data = {"id": 1, "firstname": "James "}

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
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    topic = args.topic
    writer.write(data, encoder)
    raw_bytes = bytes_writer.getvalue()
    producer.produce(topic=topic, value=raw_bytes)
    print('message sent', data, 'topic-', topic)
    flush(producer)
