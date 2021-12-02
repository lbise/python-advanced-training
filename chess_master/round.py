import asyncio

class Round(object):
    def __init__(self, master, players):
        self.master = master
        self.players = players
        self.tasks = []

    async def play(self, opponent_id: int):
        player = self.players[opponent_id]
        master_task = asyncio.create_task(self.master.think_and_play(self, player))
        player_task = asyncio.create_task(player.think_and_play(self, self.master))
        self.tasks = [master_task, player_task]
