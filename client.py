import asyncio
import datetime
import logging
import websockets
import datetime

from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus
from config import Config as cfg

#logger
logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model=cfg.model,
            charge_point_vendor=cfg.vendor,
            firmware_version="69",
        )

        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            logging.info(self.id + " accepted.")
            await self.send_heartbeat()
        if response.status == RegistrationStatus.rejected:
            logging.info(self.id + " rejected.")
        if response.status == RegistrationStatus.pending:
            logging.info(self.id + " pending.")

    async def send_heartbeat(self):
        while True:
            try:
                request = call.HeartbeatPayload()                              
                await self.call(request)
                #pingowanie
                await asyncio.sleep(15)
            except:
                raise

async def main():
    async with websockets.connect(
        f'ws://{cfg.host}:{cfg.port}/{cfg.name}',
        subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)
        
        #ponizsza funkcja zwraca instancje oraz pozwala na grupowanie zadan
        await asyncio.gather(cp.start(), cp.send_boot_notification())

if __name__ == '__main__':
    asyncio.run(main())