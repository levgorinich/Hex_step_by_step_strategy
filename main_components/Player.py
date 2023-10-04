class Player:

    def __init__(self, id,game_map ):
        self.id = id
        self.max_moves = 8
        self.moves = 0
        self.cur_turn = False
        self.coins= 100
        self.income = 0
        self.map = game_map

    def start_turn(self):
        print("start turn")
        self.cur_turn = True
        self.moves = self.max_moves
        self.income = 10
        print(self.map.buildings)
        for building in self.map.buildings:
            grid_pos = building.grid_pos
            unit_on_hex = self.map.hexes.hexes_dict[grid_pos].unit_on_hex
            if unit_on_hex and unit_on_hex.player_id == self.id:
                self.income += 10
                print("increasing income")

        print(self.income)
        self.coins += self.income
        print(self.coins)


