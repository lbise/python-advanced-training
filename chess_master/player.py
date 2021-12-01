import time
import logging

L = logging.getLogger(__name__)

class Player(object):
    def __init__(self, name):
        self.name = name

    def think_and_play(self, round: "Round", opponent: "Player"):
        L.info(f'{self.name} is thinking')
        time.sleep(2)
        L.info(f'{self.name} plays')
