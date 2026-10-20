import asyncio
from datetime import datetime

import aiocoap
import aiocoap.resource as resource

# Dia chi server. Chay 2 may khac nhau thi doi thanh IP cua may chay Server.
# Luu y: tren Windows server phai bind vao mot dia chi cu the (khong dung 0.0.0.0).
HOST = "127.0.0.1"
PORT = 5683
WELCOME = "Xin chao tu CoAP Server"


class MessageResource(resource.Resource):
    """Tai nguyen /iot/lab/message: GET tra loi chao, POST nhan thong diep."""

    def __init__(self):
        super().__init__()
        self.last_message = None  # thong diep POST gan nhat

    async def render_get(self, request):
        print("GET request received: /iot/lab/message\n")
        if self.last_message is None:
            text = WELCOME
        else:
            text = f"{WELCOME} | Thong diep gan nhat: {self.last_message}"
        return aiocoap.Message(
            code=aiocoap.CONTENT, payload=text.encode("utf-8"), content_format=0
        )

    async def render_post(self, request):
        payload = request.payload.decode("utf-8", errors="replace")
        time_now = datetime.now().strftime("%H:%M:%S")
        self.last_message = payload
        print("POST request received:")
        print("Payload:", payload)
        print("Time:", time_now)
        print()
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload="Server da nhan thong diep".encode("utf-8"),
            content_format=0,
        )


async def main():
    site = resource.Site()
    site.add_resource(
        [".well-known", "core"],
        resource.WKCResource(site.get_resources_as_linkheader),
    )
    site.add_resource(["iot", "lab", "message"], MessageResource())

    context = await aiocoap.Context.create_server_context(site, bind=(HOST, PORT))
    print(f"CoAP Server started on port {PORT}")
    print(f"Resource: coap://{HOST}:{PORT}/iot/lab/message")
    print("Bam Ctrl+C de dung.\n")
    try:
        await asyncio.Event().wait()  # chay mai cho den khi Ctrl+C
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Da dung CoAP Server")
