import asyncio
import json

import aiocoap
import aiocoap.error
from aiocoap import GET, PUT, Message

# Dia chi server. Chay 2 may khac nhau thi doi thanh IP cua may chay Server.
SERVER = "127.0.0.1"
PORT = 5683
DEVICE_ID = "light01"
URI = f"coap://{SERVER}:{PORT}/iot/lab/light01/status"
JSON_FORMAT = 50  # application/json
TIMEOUT = 5  # giay


async def send(context, request):
    """Gui yeu cau, tra ve response hoac None neu loi."""
    try:
        return await asyncio.wait_for(context.request(request).response, TIMEOUT)
    except asyncio.TimeoutError:
        print("Loi: het thoi gian cho (timeout), Server khong phan hoi\n")
    except (aiocoap.error.Error, OSError) as e:
        print(f"Loi ket noi: {e!r}\n")
    return None


async def send_command(context, command):
    body = json.dumps({"device_id": DEVICE_ID, "command": command})
    request = Message(
        code=PUT, uri=URI, payload=body.encode("utf-8"), content_format=JSON_FORMAT
    )
    print("\nSending PUT request...")
    response = await send(context, request)
    if response is None:
        return
    print("Response Code:", response.code)
    if response.code.is_successful():
        if command == "ON":
            print(f"Da bat den {DEVICE_ID}\n")
        else:
            print(f"Da tat den {DEVICE_ID}\n")
    else:
        print("Server tu choi:", response.payload.decode("utf-8", errors="replace"), "\n")


async def get_status(context):
    print("\nSending GET request...")
    response = await send(context, Message(code=GET, uri=URI))
    if response is None:
        return
    print("Response:")
    print(response.payload.decode("utf-8", errors="replace"), "\n")


async def main():
    context = await aiocoap.Context.create_client_context()
    try:
        while True:
            try:
                command = input("Nhap lenh (ON/OFF/STATUS/EXIT): ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if command == "EXIT":
                break
            elif command in ("ON", "OFF"):
                await send_command(context, command)
            elif command == "STATUS":
                await get_status(context)
            else:
                print("Loi: lenh khong hop le, chi nhan ON, OFF, STATUS hoac EXIT\n")
    finally:
        await context.shutdown()
        print("Da thoat Light Controller")


if __name__ == "__main__":
    asyncio.run(main())
