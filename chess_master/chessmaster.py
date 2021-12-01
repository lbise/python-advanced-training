import time
import logging

L = logging.getLogger(__name__)

class Chessmaster(object):
    def __init__(self):
        pass

    def think_and_play(self, round: "Round", opponent: "Player"):
        L.info('Master is thinking')
        time.sleep(1)
        L.info('Master plays')
