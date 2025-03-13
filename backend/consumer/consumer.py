import pika
import json
import psycopg2
import redis
from datetime import datetime
import websockets
import asyncio

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASS = "guest"
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials
    ))
    channel = connection.channel()
    print("Connected to RabbitMQ.")
except pika.exceptions.AMQPConnectionError as e:
    print(f"Failed to connect to RabbitMQ: {e}")
    exit(1)

POSTGRES_HOST = "localhost"
POSTGRES_DB = "shipsdb"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "1234"

try:
    conn = psycopg2.connect(
        dbname=POSTGRES_DB, 
        user=POSTGRES_USER, 
        password=POSTGRES_PASSWORD, 
        host=POSTGRES_HOST
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL.")
except psycopg2.OperationalError as e:
    print(f"Failed to connect to PostgreSQL: {e}")
    exit(1)

REDIS_HOST = "localhost"
REDIS_PORT = 6379

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    print("Connected to Redis.")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
    exit(1)

channel.queue_declare(queue="ship_data")

WEBSOCKET_URL = "ws://localhost:8000/ws"

async def send_to_websocket(data):
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await websocket.send(json.dumps(data))
            print("Sent data to WebSocket:", data)
    except Exception as e:
        print(f"Error sending data to WebSocket: {e}")

def process_ship_data(ch, method, properties, body):
    try:
        ship_data = json.loads(body)
        timestamp = datetime.utcfromtimestamp(ship_data["timestamp"])
        
        cursor.execute("BEGIN;")
        cursor.execute(
            "INSERT INTO ship_tracks (ship_id, latitude, longitude, speed, heading, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
            (ship_data["ship_id"], ship_data["latitude"], ship_data["longitude"],
             ship_data["speed"], ship_data["heading"], timestamp)
        )
        conn.commit()

        redis_client.set(ship_data["ship_id"], json.dumps(ship_data))
        asyncio.run(send_to_websocket(ship_data))
        
        print(f"Processed ship data: {ship_data}")

    except Exception as e:
        print(f"Error processing ship data: {e}")
        conn.rollback()  

channel.basic_consume(queue="ship_data", on_message_callback=process_ship_data, auto_ack=True)

print("Waiting for ship data...")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Shutting down consumer.")
    channel.stop_consuming()
finally:
    if connection and connection.is_open:
        connection.close()
    if conn:
        cursor.close()
        conn.close()
    if redis_client:
        redis_client.close()
