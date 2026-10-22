from asyncio import run, get_running_loop, Event
import logging

from constants import UDP_PORT
from udp import UdpDiscoveryServer

async def main():
  loop = get_running_loop()
  transport, _ = await loop.create_datagram_endpoint(
    UdpDiscoveryServer, 
    local_addr=("0.0.0.0", UDP_PORT)
  )

  try:
    print('uvicorn serves the fastapi here')
    __ = await Event().wait()
  finally:
    transport.close()

if __name__ == "__main__":
  logging.basicConfig(
    level=logging.DEBUG, # we need to change this in production
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
  )
  run(main())
