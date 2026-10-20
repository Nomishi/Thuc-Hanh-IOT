import asyncio
import json
import time
from datetime import datetime

import aiocoap
import aiocoap.error
from aiocoap import GET, Message

# Dia chi server. Chay 2 may khac nhau thi doi thanh IP cua may chay Server.
SERVER = "127.0.0.1"
PORT = 5683
URI = f"coap://{SERVER}:{PORT}/iot/lab/sensor01/data"
INTERVAL = 3  # giay giua 2 lan GET
TIMEOUT = 5  # giay cho phan hoi

TEMP_LIMIT = 35
HUMIDITY_LIMIT = 40


def now():
    return datetime.now().strftime("%H:%M:%S")


def show_data(data):
    print(f"[{now()}] Received sensor data\n")
    print("Device:", data["device_id"])
    print("Temperature:", data["temperature"], "C")
    print("Humidity:", data["humidity"], "%")
    print()
    warned = False
    if data["temperature"] > TEMP_LIMIT:
        print("CANH BAO: Nhiet do cao")
        warned = True
    if data["humidity"] < HUMIDITY_LIMIT:
        print("CANH BAO: Do am thap")
        warned = True
    if not warned:
        print("Trang thai: Binh thuong")
    print("\n------------------------------\n")


async def main():
    context = await aiocoap.Context.create_client_context()
    count = 0
    total_time = 0.0
    print(f"Monitoring Client: GET {URI} moi {INTERVAL} giay. Bam Ctrl+C de dung.\n")
    try:
        while True:
            request = Message(code=GET, uri=URI)
            start = time.perf_counter()
            try:
                response = await asyncio.wait_for(
                    context.request(request).response, TIMEOUT
                )
            except asyncio.TimeoutError:
                print(f"[{now()}] Loi: Server khong phan hoi (timeout)\n")
            except (aiocoap.error.Error, OSError) as e:
                print(f"[{now()}] Loi ket noi: {e!r}\n")
            else:
                count += 1
                total_time += time.perf_counter() - start
                if response.code.is_successful():
                    try:
                        data = json.loads(response.payload.decode("utf-8"))
                        show_data(data)
                    except (ValueError, KeyError):
                        print(f"[{now()}] Loi: payload JSON khong hop le\n")
                else:
                    print(f"[{now()}] Server tra ve loi: {response.code}\n")
            await asyncio.sleep(INTERVAL)
    finally:
        await context.shutdown()
        if count:
            avg_ms = total_time / count * 1000
            print(f"So lan GET thanh cong: {count}")
            print(f"Thoi gian phan hoi trung binh: {avg_ms:.1f} ms")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Da dung Monitoring Client")
