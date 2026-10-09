import pika

HOST = "localhost"
PORT = 5672
EXCHANGE = "iot_alert_exchange"
QUEUE = "warning_queue"
ROUTING_KEY = "warning"

def callback(ch, method, properties, body):
    print(f"[{QUEUE}] Da nhan: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT)
    )
except pika.exceptions.AMQPConnectionError:
    print(f"Khong ket noi duoc RabbitMQ tai {HOST}:{PORT}")
    raise SystemExit(1)

channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct")
channel.queue_declare(queue=QUEUE, durable=True)
# Noi queue voi exchange: chi nhan message co routing key = "warning"
channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=ROUTING_KEY)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)

print(f"[{QUEUE}] Dang cho canh bao muc '{ROUTING_KEY}'. Bam Ctrl+C de thoat.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Da thoat warning consumer")
    channel.stop_consuming()
connection.close()
