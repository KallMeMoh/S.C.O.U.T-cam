import asyncio
from typing import override
import logging
from constants import DISCOVERY_MAGIC, REPLY_MAGIC

logger = logging.getLogger(__name__)

class UdpDiscoveryServer(asyncio.DatagramProtocol):
  transport: asyncio.DatagramTransport | None = None

  @override
  def connection_made(self, transport: asyncio.DatagramTransport) -> None:
    self.transport = transport

  @override
  def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
    logger.debug("received %r from %s", data, addr)
    if data == DISCOVERY_MAGIC:
      assert self.transport is not None
      self.transport.sendto(REPLY_MAGIC, addr)
      logger.debug("replied to %s", addr)
    else:
      logger.debug("ignored %r from %s", data, addr)