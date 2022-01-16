import asyncio
import websockets
import logging
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import *
from ocpp.v16 import call_result, call

#logger
logging.getLogger('ocpp').setLevel(level=logging.DEBUG)
#rejestrowanie danych wyjsciowych
logging.getLogger('ocpp').addHandler(logging.StreamHandler()) 

#config
IP_ADDRESS = '0.0.0.0'
PORT = 9000

class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor, charge_point_model, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=15,
            status=RegistrationStatus.pending
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self, **kwargs):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

    async def send_trigger_message(self):
        request = call.TriggerMessagePayload(
            message='BootNotification' 
        )

        response = await self.call(request)
        if response.status == TriggerMessageStatus.accepted:
            print("Trigger message will be sent.")

        elif response.status == TriggerMessageStatus.rejected:
            print("Trigger message will not be sent.")

#nasluchiwanie
async def on_connect(websocket, path):
    charge_point_id = path.strip('/')
    print(f'{charge_point_id} connected')

    cp = ChargePoint(charge_point_id, websocket)
    await cp.start()

async def main():
    server = await websockets.serve(
        on_connect,
        IP_ADDRESS,
        PORT,
        subprotocols=['ocpp1.6']
    )
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
