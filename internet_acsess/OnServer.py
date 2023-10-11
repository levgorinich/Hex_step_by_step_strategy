
class Game:
    def __init__(self, id, seed, max_players=2):
        self.id = id
        self.seed = seed
        self.players = []
        self.max_players = max_players

        self.comands = {x:"" for x in range(self.max_players)}

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)
