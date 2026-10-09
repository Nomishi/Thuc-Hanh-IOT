from datetime import datetime
import pika

HOST = "localhost"
PORT = 5672
QUEUE = "iot_lab_queue"

# Ham nay tu duoc goi moi khi co message tu queue
def callback(ch, method, properties, body):
    message = body.decode()
    time_now = datetime.now().strftime("%H:%M:%S")
    print("Da nhan message:", message)
    print("Thoi gian nhan:", time_now)
    print()
    ch.basic_ack(delivery_tag=method.delivery_tag)  # bao broker da xu ly xong

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

print(f"Dang cho message tu queue '{QUEUE}'. Bam Ctrl+C de thoat.")
try:
    channel.start_consuming()  # chay lien tuc
except KeyboardInterrupt:
    print("Da thoat consumer")
    channel.stop_consuming()
connection.close()
