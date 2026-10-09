import time
import pika

HOST = "localhost"
PORT = 5672
EXCHANGE = "iot_alert_exchange"

# (routing key, noi dung canh bao)
ALERTS = [
    ("info", "He thong IoT hoat dong binh thuong muc info"),
    ("warning", "Nhiet do phong may vuot nguong muc warning"),
    ("critical", "Cam bien kho lanh mat ket noi muc critical"),
]

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT)
    )
except pika.exceptions.AMQPConnectionError:
    print(f"Khong ket noi duoc RabbitMQ tai {HOST}:{PORT}")
    raise SystemExit(1)

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct")

for routing_key, message in ALERTS:
    channel.basic_publish(exchange=EXCHANGE, routing_key=routing_key, body=message)
    print(f"Da gui [{routing_key}]: {message}")
    time.sleep(1)

connection.close()
