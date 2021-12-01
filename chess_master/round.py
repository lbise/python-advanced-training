class Round(object):
    def __init__(self, master, players):
        self.master = master
        self.players = players

    def play(self, opponent_id: int):
        player = self.players[opponent_id]
        player.think_and_play(self, self.master)
        self.master.think_and_play(self, player)

