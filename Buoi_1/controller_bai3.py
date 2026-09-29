import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
DEVICE_ID = "light01"
TOPIC_CMD = f"iot/lab/{DEVICE_ID}/cmd"
TOPIC_STATUS = f"iot/lab/{DEVICE_ID}/status"

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(TOPIC_STATUS)

def on_message(client, userdata, msg):
    print("\nTrang thai nhan duoc:")
    print(msg.payload.decode())
    print()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()          # nhận tin ở luồng nền, luồng chính để nhập lệnh
time.sleep(1)                # chờ kết nối + nhận trạng thái ban đầu

while True:
    cmd = input("Nhap lenh (ON/OFF/EXIT): ").strip().upper()
    if cmd == "EXIT":
        break
    if cmd == "ON" or cmd == "OFF":
        client.publish(TOPIC_CMD, cmd)
        print(f"Da gui lenh {cmd} toi {DEVICE_ID}")
        time.sleep(0.5)      # chờ thiết bị phản hồi rồi mới hỏi lệnh tiếp
    else:
        print("Loi: chi nhan ON, OFF hoac EXIT")

client.loop_stop()
client.disconnect()
print("Da thoat controller")