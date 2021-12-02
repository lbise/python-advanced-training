import time
import logging
import asyncio

L = logging.getLogger(__name__)

class Chessmaster(object):
    def __init__(self):
        self.master_is_busy = asyncio.Lock()

    async def think_and_play(self, round: "Round", opponent: "Player"):
        async with self.master_is_busy:
            await opponent.player_is_done.wait()
            opponent.player_is_done.clear()
            L.info('Master is thinking')
            await asyncio.sleep(1)
            L.info('Master plays')
            opponent.master_is_done.set()
