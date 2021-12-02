import time
import asyncio
import logging

L = logging.getLogger(__name__)

class Player(object):
    def __init__(self, name):
        self.name = name
        self.player_is_done = asyncio.Event()
        self.master_is_done = asyncio.Event()
        self.player_is_busy = asyncio.Lock()

    async def think_and_play(self, round: "Round", opponent: "Player"):
        await self.master_is_done.wait()
        self.master_is_done.clear()
        async with self.player_is_busy:
            L.info(f'{self.name} is thinking')
            await asyncio.sleep(2)
            L.info(f'{self.name} plays')
            self.player_is_done.set()
