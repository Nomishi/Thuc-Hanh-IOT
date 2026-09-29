import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/lab/message"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Ket noi broker:", reason_code)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    time_now = datetime.now().strftime("%H:%M:%S")
    print("Nhan duoc message:")
    print("Topic:", msg.topic)
    print("Payload:", payload)
    print("Time:", time_now)
    print()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Da thoat subscriber")
    client.disconnect()