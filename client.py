import asyncio
import logging
import websockets

from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus

#logger
logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Test1",
            charge_point_vendor="Test2",
            firmware_version="69"
        )

        response = await self.call(request)
        if response.status == RegistrationStatus.pending:
            logging.info("STATUS: Pending (?)")
        await self.send_heartbeat()

    async def send_heartbeat(self):
        while True:
            try:
                request = call.HeartbeatPayload()                              
                await self.call(request)
                await asyncio.sleep(10)
            except:
                raise

async def main():
    async with websockets.connect(
        'ws://127.0.0.1:9000/CP_1',
        subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())

if __name__ == '__main__':
    asyncio.run(main())