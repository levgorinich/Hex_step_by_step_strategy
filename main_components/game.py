class OnlineGame:
    def __init__(self, id, players, max_players=2,  size = (20,20)):
        self.id = id
        self.players = players
        self.players_amount = len(players)
        self.max_players = max_players

        self.size = size