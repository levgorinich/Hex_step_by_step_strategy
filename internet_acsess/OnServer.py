
class Game:
    def __init__(self, id, seed, max_players=2):
        self.id = id
        self.seed = seed
        self.players = []
        self.max_players = max_players

        self.comands = {0: "", 1: "",}

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)
