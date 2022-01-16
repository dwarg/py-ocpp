import asyncio
import logging
import datetime
import websockets

from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import *

logging.basicConfig(level=logging.INFO)

URL = 'ws://localhost:9000/CP_1'

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Test1",
            charge_point_vendor="Test2",
            firmware_version="69",
        )

        response = await self.call(request)
        if response.status == RegistrationStatus.pending:
            logging.info("Status: Pending (?)")

async def main():
    async with websockets.connect(
        URL,
        subprotocols=['ocpp1.6']
    ) as ws:
        cp = ChargePoint('CP_1', ws)
        await asyncio.gather(cp.start(), cp.send_boot_notification())

if __name__ == '__main__':
    asyncio.run(main())