
class Game:
    def __init__(self, id, seed, max_players=2, size = (20,20)):
        self.id = id
        self.seed = seed
        self.players = []
        self.max_players = max_players
        self.size = size
        self.places = [x for x in reversed(range(self.max_players))]
        self.comands = {x:"" for x in range(self.max_players)}

    def add_player(self, ):
        if self.places:
            player= self.places.pop()
            self.players.append(player)
            return player
        else:
            return False


    def remove_player(self, player):
        self.players.remove(player)
        self.places.append(player)

    def get_dict_for_client(self):
        return {"seed": self.seed, "max_players": self.max_players, "size":self.size}

    def get_dict_for_room_selection(self):
        return {"id":self.id, "max_players": self.max_players, "players":self.players,}
