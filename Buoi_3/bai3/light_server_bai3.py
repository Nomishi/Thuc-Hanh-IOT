import asyncio
import json

import aiocoap
import aiocoap.resource as resource

# Dia chi server. Chay 2 may khac nhau thi doi thanh IP cua may chay Server.
# Luu y: tren Windows server phai bind vao mot dia chi cu the (khong dung 0.0.0.0).
HOST = "127.0.0.1"
PORT = 5683
DEVICE_ID = "light01"
JSON_FORMAT = 50  # Content-Format cua application/json


class LightStatusResource(resource.ObservableResource):
    """Tai nguyen /iot/lab/light01/status: GET, PUT va Observe."""

    def __init__(self):
        super().__init__()
        self.status = "OFF"  # trang thai ban dau
        self.observers = 0

    def status_payload(self):
        data = {"device_id": DEVICE_ID, "status": self.status}
        return json.dumps(data, separators=(",", ":")).encode("utf-8")

    def update_observation_count(self, newcount):
        # Duoc aiocoap goi khi so Client dang Observe thay doi
        if newcount > self.observers:
            print("New Observe registration received\n")
        elif newcount < self.observers:
            print("Mot Client da huy Observe\n")
        self.observers = newcount

    async def render_get(self, request):
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=self.status_payload(),
            content_format=JSON_FORMAT,
        )

    async def render_put(self, request):
        # Doc va kiem tra payload JSON: {"device_id": "light01", "command": "ON"}
        try:
            data = json.loads(request.payload.decode("utf-8"))
            device = data["device_id"]
            command = str(data["command"]).strip().upper()
        except (ValueError, KeyError, TypeError, AttributeError):
            print("PUT request khong hop le (payload sai dinh dang)\n")
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Payload phai la JSON co device_id va command".encode("utf-8"),
            )

        print("PUT request received:")
        print("Device:", device)
        print("Command:", command)

        if device != DEVICE_ID:
            print("Loi: sai ma thiet bi\n")
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Sai ma thiet bi".encode("utf-8"),
            )
        if command not in ("ON", "OFF"):
            print("Loi: lenh khong hop le\n")
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Lenh khong hop le, chi nhan ON hoac OFF".encode("utf-8"),
            )

        if command != self.status:
            old = self.status
            self.status = command
            print(f"Light state changed: {old} -> {self.status}")
            print(f"Notify observers: {self.status}\n")
            self.updated_state()  # thong bao cho tat ca Client dang Observe
        else:
            print(f"Trang thai khong doi (den dang {self.status}), khong thong bao\n")

        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload=self.status_payload(),
            content_format=JSON_FORMAT,
        )


async def main():
    site = resource.Site()
    site.add_resource(
        [".well-known", "core"],
        resource.WKCResource(site.get_resources_as_linkheader),
    )
    site.add_resource(["iot", "lab", "light01", "status"], LightStatusResource())

    context = await aiocoap.Context.create_server_context(site, bind=(HOST, PORT))
    print("CoAP Smart Light Server started...")
    print(f"Resource: /iot/lab/light01/status (coap://{HOST}:{PORT})")
    print("Bam Ctrl+C de dung.\n")
    try:
        await asyncio.Event().wait()
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Da dung Smart Light Server")
