import json
import random
import time
from datetime import datetime
import pika

HOST = "localhost"
PORT = 5672
QUEUE = "sensor_data_queue"

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT)
    )
except pika.exceptions.AMQPConnectionError:
    print(f"Khong ket noi duoc RabbitMQ tai {HOST}:{PORT}")
    raise SystemExit(1)

channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)

print(f"Sensor dang gui du lieu vao queue '{QUEUE}' moi 3 giay. Bam Ctrl+C de dung.")
try:
    while True:
        data = {
            "device_id": "sensor01",
            "temperature": round(random.uniform(25, 40), 1),
            "humidity": round(random.uniform(30, 80), 1),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        body = json.dumps(data)  # dict -> chuoi JSON
        channel.basic_publish(exchange="", routing_key=QUEUE, body=body)
        print("Da gui:", body)
        time.sleep(3)
except KeyboardInterrupt:
    print("Da dung sensor")
connection.close()
