import asyncio
import json
import random
from datetime import datetime

import aiocoap
import aiocoap.resource as resource

# Dia chi server. Chay 2 may khac nhau thi doi thanh IP cua may chay Server.
# Luu y: tren Windows server phai bind vao mot dia chi cu the (khong dung 0.0.0.0).
HOST = "127.0.0.1"
PORT = 5683
JSON_FORMAT = 50  # Content-Format cua application/json
UPDATE_INTERVAL = 3  # giay


def now():
    return datetime.now().strftime("%H:%M:%S")


class SensorResource(resource.Resource):
    """Tai nguyen /iot/lab/sensor01/data: tra ve du lieu cam bien moi nhat."""

    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.data = self.generate()

    def generate(self):
        return {
            "device_id": self.device_id,
            "temperature": round(random.uniform(25, 40), 1),
            "humidity": round(random.uniform(30, 80), 1),
            "timestamp": now(),
        }

    def update(self):
        self.data = self.generate()

    async def render_get(self, request):
        print(f"[{now()}] GET request received: tra ve du lieu hien tai")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=json.dumps(self.data).encode("utf-8"),
            content_format=JSON_FORMAT,
        )


async def update_loop(sensor):
    """Tu dong cap nhat du lieu cam bien moi 3 giay."""
    while True:
        await asyncio.sleep(UPDATE_INTERVAL)
        sensor.update()
        print(
            f"[{now()}] Cap nhat cam bien: "
            f"{sensor.data['temperature']} C, {sensor.data['humidity']} %"
        )


async def main():
    sensor = SensorResource("sensor01")
    site = resource.Site()
    site.add_resource(
        [".well-known", "core"],
        resource.WKCResource(site.get_resources_as_linkheader),
    )
    site.add_resource(["iot", "lab", "sensor01", "data"], sensor)

    context = await aiocoap.Context.create_server_context(site, bind=(HOST, PORT))
    print(f"Sensor CoAP Server started on port {PORT}")
    print(f"Resource: coap://{HOST}:{PORT}/iot/lab/sensor01/data")
    print("Bam Ctrl+C de dung.\n")

    updater = asyncio.create_task(update_loop(sensor))
    try:
        await asyncio.Event().wait()
    finally:
        updater.cancel()
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Da dung Sensor Server")
