import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/lab/sensor01/data"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Ket noi broker:", reason_code)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Device:", data["device_id"])
    print("Temperature:", data["temperature"], "C")
    print("Humidity:", data["humidity"], "%")
    if data["temperature"] > 35:
        print("CANH BAO: Nhiet do cao")
    if data["humidity"] < 40:
        print("CANH BAO: Do am thap")
    print()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Da thoat monitor")
    client.disconnect()
    