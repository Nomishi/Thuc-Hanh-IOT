import asyncio
import json
from datetime import datetime

import aiocoap
import aiocoap.error
from aiocoap import GET, Message

# Dia chi server. Chay 2 may khac nhau thi doi thanh IP cua may chay Server.
SERVER = "127.0.0.1"
PORT = 5683
URI = f"coap://{SERVER}:{PORT}/iot/lab/light01/status"
TIMEOUT = 5  # giay cho phan hoi dau tien


def now():
    return datetime.now().strftime("%H:%M:%S")


def show(title, response):
    try:
        data = json.loads(response.payload.decode("utf-8"))
        print(f"[{now()}] {title}")
        print("Device:", data["device_id"])
        print("Status:", data["status"])
        print()
    except (ValueError, KeyError):
        print(f"[{now()}] Loi: payload khong hop le\n")


async def main():
    context = await aiocoap.Context.create_client_context()
    print("Registering CoAP Observe...")

    # observe=0 -> dang ky theo doi tai nguyen (khong dung vong lap GET)
    request = Message(code=GET, uri=URI, observe=0)
    pending = context.request(request)
    try:
        try:
            first = await asyncio.wait_for(pending.response, TIMEOUT)
        except asyncio.TimeoutError:
            print("Loi: Server khong phan hoi (timeout)")
            return
        except (aiocoap.error.Error, OSError) as e:
            print(f"Loi ket noi: {e!r}")
            return

        if first.opt.observe is None:
            print("Server khong ho tro Observe cho tai nguyen nay")
            return
        print("Observe registration successful\n")
        show("Initial State", first)

        # Moi lan trang thai thay doi, Server tu day thong bao ve day
        try:
            async for notification in pending.observation:
                show("State Updated", notification)
        except (aiocoap.error.Error, OSError) as e:
            print(f"Mat ket noi Observe: {e!r}")
    finally:
        pending.observation.cancel()
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Da dung Light Monitor")
