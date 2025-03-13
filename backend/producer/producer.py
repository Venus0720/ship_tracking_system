import pika
import json
import random
import time

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST, 
    credentials=credentials
))
channel = connection.channel()
channel.queue_declare(queue="ship_data")

def generate_ship_data():
    while True:
        ship_data = {
            "ship_id": f"SHIP-{random.randint(100, 999)}",
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6),
            "speed": round(random.uniform(5, 30), 2),
            "heading": random.randint(0, 360),
            "timestamp": time.time()
        }
        
        channel.basic_publish(exchange="", routing_key="ship_data", body=json.dumps(ship_data))
        print(f"Sent: {ship_data}")

        time.sleep(2)  

if __name__ == "__main__":
    generate_ship_data()
