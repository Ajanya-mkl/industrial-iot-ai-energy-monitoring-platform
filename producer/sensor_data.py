from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

while True:
    data = {
        "voltage": random.randint(210, 240),
        "current": random.uniform(5, 15),
        "temperature": random.uniform(30, 80),
        "machine_status": random.choice([0,1])
    }
    producer.send("factory_data", value=data)
    print("Sent:", data)
    time.sleep(1)