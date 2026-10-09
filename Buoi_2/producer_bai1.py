import time
import pika

HOST = "localhost"
PORT = 5672
QUEUE = "iot_lab_queue"

# Thanh vien nhom
MEMBERS = [
    "B23DCCN584 - Nguyen Hoang Nam",
    "B23DCCN486 - Nguyen Khanh Linh",
    "B23DCCN500 - Le Hien Long",
]

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT)
    )
except pika.exceptions.AMQPConnectionError:
    print(f"Khong ket noi duoc RabbitMQ tai {HOST}:{PORT}")
    raise SystemExit(1)

channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)  # tao queue neu chua co

# Moi message chua thong tin ca 3 thanh vien; gui 3 message lien tiep
members_text = " | ".join(MEMBERS)
for i in range(1, 4):
    message = f"Xin chao tu ung dung Python AMQP - {members_text} - lan {i}"
    channel.basic_publish(exchange="", routing_key=QUEUE, body=message)
    print("Da gui:", message)
    time.sleep(1)

connection.close()