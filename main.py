from contextlib import asynccontextmanager
from asyncio import get_running_loop
import logging
from fastapi import FastAPI
import uvicorn

from constants import API_PORT, UDP_PORT
from server import Server
from udp import UdpDiscoveryServer

@asynccontextmanager
async def lifespan(_app: FastAPI):
  loop = get_running_loop()
  transport, _ = await loop.create_datagram_endpoint(
    protocol_factory=UdpDiscoveryServer,
    local_addr=("0.0.0.0", UDP_PORT),
  )
  try:
    yield
  finally:
    transport.close()

app = Server(lifespan=lifespan)

if __name__ == "__main__":
  logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
  )
  uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=API_PORT,
    limit_concurrency=30,
    backlog=16,
    timeout_keep_alive=5,
    timeout_graceful_shutdown=3,
    log_config=None
  )