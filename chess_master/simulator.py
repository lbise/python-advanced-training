#!/usr/bin/env python3
import logging

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

class Simulator(object):
    def main(self):
        master = Chessmaster()
        players = [Player('Player1'), Player('Player2'), Player('Player3')]
        round_ = Round(master, players)
        for j in range(2):
            L.info(f'== Starting round {j} ==')
            for i, _ in enumerate(players):
                round_.play(i)

if __name__ == '__main__':
    setup_logger('__main__', logging.DEBUG)
    setup_logger('chessmaster', logging.DEBUG)
    setup_logger('player', logging.DEBUG)
    setup_logger('round', logging.DEBUG)

    s = Simulator()
    s.main()
