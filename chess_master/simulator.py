#!/usr/bin/env python3
import logging
import asyncio

from chessmaster import Chessmaster
from player import Player
from round import Round

L = logging.getLogger(__name__)

def setup_logger(name, level):
    sim = logging.getLogger(name)
    strm = logging.StreamHandler()
    frmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    strm.setFormatter(frmt)
    sim.addHandler(strm)
    sim.setLevel(level)

master_is_done = asyncio.Event()

class Simulator(object):
    def __init__(self):
        self.nb_rounds = 2
        self.nb_players = 3
        self.master = Chessmaster()
        self.players = [Player(f'Player{i}') for i in range(self.nb_players)]
        self.rounds = [Round(self.master, self.players) for i in range(self.nb_rounds)]

    async def main(self):
        L.info('*** Start simulation')
        for round_id, round in enumerate(self.rounds):
            for player_id, player in enumerate(self.players):
                # Authorize player to play beginning of first round
                if round_id == 0:
                    player.master_is_done.set()
                await round.play(player_id)

        for round_id, round in enumerate(self.rounds):
            await asyncio.wait(round.tasks)

        L.info('*** End simulation')

if __name__ == '__main__':
    setup_logger('__main__', logging.DEBUG)
    setup_logger('chessmaster', logging.DEBUG)
    setup_logger('player', logging.DEBUG)
    setup_logger('round', logging.DEBUG)

    s = Simulator()
    asyncio.run(s.main())
