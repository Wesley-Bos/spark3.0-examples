from json import loads
from kafka import KafkaConsumer

print("Connecting to consumer ...")
consumer = KafkaConsumer(
        'pxl_data',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
 print(f"{message.value}")
