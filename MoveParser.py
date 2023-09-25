
class Parser:
    def __init__(self, mover, spawner):
        self.mover = mover
        self.spawner = spawner
    def parse_moves(self, move):
        print(move, "string to parse")

        if move.startswith("spawn"):
            self.parse_spawn(move)
        elif move.startswith("move"):
            self.parse_moving(move)

    def parse_spawn(self, move):

        move = move.replace("spawn", "")
        idx = move.find("(")
        type = move[:idx]
        move = move[idx+1:]
        coords = move.replace("(", "").replace(")", "")

        coords = coords.split(",")
        spawn = tuple(map(int, coords[:2]))
        print("player_id in parser  ", coords[2])
        self.spawner.spawn_unit(type, spawn, coords[2])

    def parse_moving(self, move):

        move = move.replace("move", "")
        move = move.replace("(", "")
        move = move.replace(")", "")
        coords = move.split(",")

        coords = list(map(int, coords))
        self.mover.move((coords[0], coords[1]), (coords[2], coords[3]))
