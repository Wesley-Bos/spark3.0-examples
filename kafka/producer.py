from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

print("Please insert a number --> 'stop' to exit")
input_user = input()
index = 0

while input_user != "stop":
    data = {"id": "PXL"+str(index), "number" : input_user}
    producer.send("pxl_data", value=data)
    
    print(f"Sending data: {data}")
    
    index += 1
    
    print("Insert new data (stop to exit)")
    input_user = input()
