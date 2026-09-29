import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/lab/message"

MEMBERS = [
    "B23DCCN584 - Nguyen Hoang Nam",
    "B23DCCN486 - Nguyen Khanh Linh",
    "B23DCCN500 - Le Hien Long",
]

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

# Moi thanh vien gui 1 tin, moi tin gom ma SV, ho ten va loi chao
for member in MEMBERS:
    message = f"Xin chao tu client Python MQTT - {member}"
    info = client.publish(TOPIC, message)
    info.wait_for_publish()
    print("Da gui:", message)
    time.sleep(1)

client.loop_stop()
client.disconnect()