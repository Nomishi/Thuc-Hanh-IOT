import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/lab/sensor01/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

try:
    while True:
        data = {
            "device_id": "sensor01",
            "temperature": round(random.uniform(25, 40), 1),
            "humidity": round(random.uniform(30, 80), 1),
        }
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print("Da gui:", payload)
        time.sleep(3)
except KeyboardInterrupt:
    print("Da dung sensor")
    client.loop_stop()
    client.disconnect()