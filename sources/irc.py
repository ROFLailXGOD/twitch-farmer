# -*- coding: utf-8 -*-
import asyncio
import logging
import re

from settings import NICK, OAUTH

LOG = logging.getLogger(__name__)
connected_to = {}


async def send_credentials(writer):
    writer.write(bytes('PASS {}\r\n'.format(OAUTH), 'UTF-8'))
    writer.write(bytes('NICK {}\r\n'.format(NICK), 'UTF-8'))
    await writer.drain()


async def send_pong(writer):
    writer.write(bytes('PONG :tmi.twitch.tv\r\n', 'UTF-8'))
    await writer.drain()
    LOG.info('Sent PONG')


async def join_channels(writer, channels):
    for channel in channels:
        # sleep to make sure we won't exceed 50/15 limit
        await asyncio.sleep(0.4)
        writer.write(bytes('JOIN #{}\r\n'.format(channel[1]), 'UTF-8'))
        await writer.drain()
        connected_to[channel[0]] = channel[1]
        LOG.info(f'Joined {channel[1]}')


async def part_channels(writer, channels):
    for channel in channels:
        # sleep to make sure we won't exceed 50/15 limit
        await asyncio.sleep(0.4)
        writer.write(bytes('PART #{}\r\n'.format(channel[1]), 'UTF-8'))
        await writer.drain()
        del connected_to[channel[0]]
        LOG.info(f'Parted {channel[1]}')


async def read_info(writer, reader):
    prev_data = ''
    while True:
        try:
            data = await reader.read(16*1024)
            data = data.decode('UTF-8')
            if 'PING :tmi.twitch.tv' in prev_data + data:
                await send_pong(writer)
            messages = re.split(r'[~\r\n]+', prev_data + data)
            # for msg in messages:
            #     print(msg)
            prev_data = messages[-1]
        except Exception as exc:
            print(exc)
