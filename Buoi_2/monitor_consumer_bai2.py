import json
import pika

HOST = "localhost"
PORT = 5672
QUEUE = "sensor_data_queue"

def callback(ch, method, properties, body):
    data = json.loads(body.decode())  # chuoi JSON -> dict
    print("Device:", data["device_id"])
    print("Temperature:", data["temperature"])
    print("Humidity:", data["humidity"])
    if data["temperature"] > 35:
        print("CANH BAO: Nhiet do cao")
    if data["humidity"] < 40:
        print("CANH BAO: Do am thap")
    print()
    ch.basic_ack(delivery_tag=method.delivery_tag)

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT)
    )
except pika.exceptions.AMQPConnectionError:
    print(f"Khong ket noi duoc RabbitMQ tai {HOST}:{PORT}")
    raise SystemExit(1)

channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)

print(f"Dang theo doi queue '{QUEUE}'. Bam Ctrl+C de thoat.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Da thoat monitor")
    channel.stop_consuming()
connection.close()
