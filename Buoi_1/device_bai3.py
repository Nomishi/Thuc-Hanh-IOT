import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
DEVICE_ID = "light01"
TOPIC_CMD = f"iot/lab/{DEVICE_ID}/cmd"
TOPIC_STATUS = f"iot/lab/{DEVICE_ID}/status"

light_status = "OFF"   # trạng thái hiện tại của đèn

def publish_status(client):
    payload = json.dumps({"device_id": DEVICE_ID, "status": light_status},
                         separators=(",", ":"))
    client.publish(TOPIC_STATUS, payload)
    print("Da gui trang thai:", payload)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Ket noi broker:", reason_code)
    client.subscribe(TOPIC_CMD)
    publish_status(client)          # báo trạng thái ban đầu

def on_message(client, userdata, msg):
    global light_status
    cmd = msg.payload.decode().strip().upper()
    print("Nhan lenh:", cmd)
    if cmd == "ON" or cmd == "OFF":
        light_status = cmd
        publish_status(client)      # sau mỗi lệnh hợp lệ gửi trạng thái mới
    else:
        print("Lenh khong hop le, bo qua")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Da thoat device")
    client.disconnect()