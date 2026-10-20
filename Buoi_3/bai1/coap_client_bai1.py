import asyncio

import aiocoap
import aiocoap.error
from aiocoap import GET, POST, Message

# Dia chi server. Chay 2 may khac nhau thi doi thanh IP cua may chay Server.
SERVER = "127.0.0.1"
PORT = 5683
URI = f"coap://{SERVER}:{PORT}/iot/lab/message"
TIMEOUT = 5  # giay

MEMBERS = [
    "B23DCCN584 - Nguyen Hoang Nam",
    "B23DCCN486 - Nguyen Khanh Linh",
    "B23DCCN500 - Le Hien Long",
]


async def send(context, code, uri, text=None):
    """Gui 1 yeu cau, tra ve response hoac None neu loi."""
    payload = text.encode("utf-8") if text else b""
    request = Message(code=code, uri=uri, payload=payload)
    try:
        return await asyncio.wait_for(context.request(request).response, TIMEOUT)
    except asyncio.TimeoutError:
        print("Loi: het thoi gian cho (timeout), Server khong phan hoi\n")
    except (aiocoap.error.Error, OSError) as e:
        print(f"Loi ket noi: {e!r}\n")
    return None


def show(response):
    if response is None:
        return
    print("Response:")
    print("Code:", response.code)
    print("Payload:", response.payload.decode("utf-8", errors="replace"))
    print()


async def main():
    print("CoAP Client")
    context = await aiocoap.Context.create_client_context()
    try:
        # 1. GET
        print("Sending GET request...")
        print(f"URI: {URI}\n")
        show(await send(context, GET, URI))

        # 2. POST (gui 3 lan lien tiep, moi lan co thong tin ca 3 thanh vien)
        members_text = " | ".join(MEMBERS)
        for i in range(1, 4):
            message = f"Xin chao tu CoAP Client - {members_text} - lan {i}"
            print("Sending POST request...")
            print("Payload:", message)
            print()
            show(await send(context, POST, URI, message))
            await asyncio.sleep(1)

        # 3. GET lai: Server tra ve thong diep POST gan nhat
        print("Sending GET request (lay thong diep gan nhat)...")
        print(f"URI: {URI}\n")
        show(await send(context, GET, URI))

        # 4. Truy cap tai nguyen khong ton tai -> 4.04 Not Found
        wrong_uri = f"coap://{SERVER}:{PORT}/iot/lab/khong_ton_tai"
        print("Sending GET request toi tai nguyen khong ton tai...")
        print(f"URI: {wrong_uri}\n")
        show(await send(context, GET, wrong_uri))
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Da dung CoAP Client")
