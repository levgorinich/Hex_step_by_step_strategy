from Sprites import *
class Spawner:
    def __init__(self, game_map):
        self.game_map = game_map
        self.player_id = game_map.player_id

    def create_start_unit(self):
        print(self.player_id,"player", self.game_map.player_id)
        if self.player_id == 0:
            "here"
            self.spawn_unit("Triangular", (5, 2))
            self.spawn_unit("Square", (6, 2))
            self.spawn_unit("Circle", (7, 2))
        else:
            self.spawn_unit("Square", (20, 2))
            self.spawn_unit("Circle", (15, 3))
            self.spawn_unit("Triangular", (15, 2))
    def spawn_unit(self, type, spawn_point, player_id=None):

        if player_id is None:
            player_id = self.player_id

        # idx = self.player_id
        if type == "Triangular":
            unit = TriangularUnit(spawn_point, player_id)
        elif type == "Square":
            unit = SquareUnit(spawn_point, player_id)
        elif type == "Circle":
            unit = CircleUnit(spawn_point, player_id)
        string = "<spawn"+type+"("+str(spawn_point[0])+","+str(spawn_point[1])+"),"+str(player_id)+">"


        hexagon = self.game_map.hexes.hexes_dict[spawn_point]
        # print(hexagon)
        if not hexagon.unit_on_hex:

            hexagon.add_unit(unit)
            self.game_map.units.add(unit)
            if player_id == self.player_id:
                self.game_map.actions.add(string)