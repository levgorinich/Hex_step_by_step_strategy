class Player:

    def __init__(self, id, ):
        self.id = id
        self.max_moves = 3
        self.moves = 0
        self.cur_turn = False

    def start_turn(self):
        self.cur_turn = True
        self.moves = self.max_moves

