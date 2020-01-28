# -*- coding: utf-8 -*-
import asyncio
import logging

from settings import HOST, LOG_LEVEL, PORT

from sources.irc import read_info, send_credentials
from sources.new_api import idle


logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


async def run():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    await send_credentials(writer)

    await asyncio.gather(
        read_info(writer, reader),
        idle(writer),
    )


if __name__ == '__main__':
    asyncio.run(run())
