# -*- coding: utf-8 -*-
import asyncio
import logging
from typing import List, Tuple

import aiohttp

from settings import CHANNELS, CLIENT_ID, GAMES, MAX_CONNECTIONS, MAX_VIEWERS, MIN_VIEWERS, NEW_API_URL, BEARER

from sources.irc import connected_to, join_channels, part_channels


LOG = logging.getLogger(__name__)


async def get_inactive_streams(session: aiohttp.ClientSession) -> List[Tuple[int, str]]:
    user_ids = list(connected_to.keys())
    online = []
    for i in range(0, len(user_ids), 100):
        params = [
            ('user_id', user_id)
            for user_id in user_ids[i:i+100]
        ]
        async with session.get(f'{NEW_API_URL}streams', params=params) as resp:
            streams = await resp.json()
        online += [
            stream['user_id']
            for stream in streams['data']
        ]
    streamers = [
        stream
        for stream in connected_to.items()
        if stream[0] not in online
    ]
    LOG.info(f'Found {len(streamers)} inactive streamers')
    LOG.debug(streamers)
    return streamers


async def get_active_streams(session: aiohttp.ClientSession) -> List[Tuple[int, str]]:
    cursor = ''
    streamers = []

    if CHANNELS:
        while len(streamers) + len(connected_to) < MAX_CONNECTIONS:
            params = [
                ('first', 100),
                ('after', cursor),
            ]
            params += [('user_login', user) for user in CHANNELS]
            async with session.get(f'{NEW_API_URL}streams', params=params) as resp:
                streams = await resp.json()
            streamers += [
                (stream['user_id'], stream['user_login'])
                for stream in streams['data']
                if stream['user_id'] not in connected_to
            ]
            # streamers.extend(await get_logins(session, streamer_ids))
            cursor = streams['pagination'].get('cursor', None)
            if cursor is None:
                break

    cursor = ''
    while len(streamers) + len(connected_to) < MAX_CONNECTIONS:
        params = [
            ('first', 100),
            ('after', cursor),
        ]
        if GAMES:
            params += [('game_id', game_id) for game_id in GAMES]
        async with session.get(f'{NEW_API_URL}streams', params=params) as resp:
            streams = await resp.json()
        if not streams['data']:
            break
        if streams['data'][0]['viewer_count'] < MIN_VIEWERS:
            break
        streamers += [
            (stream['user_id'], stream['user_login'])
            for stream in streams['data']
            if stream['user_id'] not in connected_to
            if MIN_VIEWERS <= stream['viewer_count'] <= MAX_VIEWERS
        ]
        cursor = streams['pagination'].get('cursor', None)
        if cursor is None:
            break
    channels_needed = MAX_CONNECTIONS - len(connected_to)
    streamers = streamers[:channels_needed]
    LOG.info(f'Collected {len(streamers)} channels to connect to')
    LOG.debug(streamers)
    return streamers


async def idle(writer):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {BEARER}',
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            offline_streamers = await get_inactive_streams(session)
            if offline_streamers:
                await part_channels(writer, offline_streamers)
            if len(connected_to) < MAX_CONNECTIONS:
                streamers = await get_active_streams(session)
                await join_channels(writer, streamers)
            await asyncio.sleep(20*60)
