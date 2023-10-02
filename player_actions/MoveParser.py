
class Parser:
    def __init__(self, mover, spawner, player ):
        self.mover = mover
        self.spawner = spawner
        self.player = player
    def parse_moves(self, move):
        print(move, "string to parse")

        if move.startswith("spawn"):
            self.parse_spawn(move)
        elif move.startswith("move"):
            self.parse_moving(move)
        elif move.startswith("end_turn"):
            self.parse_end_turn(move)

    def parse_spawn(self, move):

        move = move.replace("spawn", "")
        idx = move.find("(")
        type = move[:idx]
        move = move[idx+1:]
        coords = move.replace("(", "").replace(")", "")

        coords = coords.split(",")
        spawn = tuple(map(int, coords[:2]))
        # print("player_id in parser  ", coords[2])
        self.spawner.spawn_unit(type, spawn, coords[2])
        # print("finished spawn parsing")

    def parse_moving(self, move):

        move = move.replace("move", "")
        move = move.replace("(", "")
        move = move.replace(")", "")
        coords = move.split(",")

        coords = list(map(int, coords))
        self.mover.move((coords[0], coords[1]), (coords[2], coords[3]))
    def parse_end_turn(self, move):
        move = move.replace("end_turn", "")
        self.player.start_turn()
