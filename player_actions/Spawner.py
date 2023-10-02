from game_content.Sprites import *


class Spawner:
    def __init__(self, game_map):
        self.game_map = game_map
        self.player_id = game_map.player_id
        self.id_colors= {0 : (255, 0, 0), 1: (0, 125, 255)}

    def create_start_unit(self):
        print(self.player_id,"player", self.player_id)
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
        print("i spawning ")
        print(player_id, "this is inside parser")
        if player_id is None:
            player_id = self.player_id
        color = self.id_colors[int(player_id)]
        print(player_id, color, "this is inside parser")
        # idx = self.player_id
        if type == "Triangular":
            unit = TriangularUnit(spawn_point, player_id, color)
        elif type == "Square":
            unit = SquareUnit(spawn_point, player_id, color)
        elif type == "Circle":
            unit = CircleUnit(spawn_point, player_id, color)
        string = "<spawn"+type+"("+str(spawn_point[0])+","+str(spawn_point[1])+"),"+str(player_id)+">"


        hexagon = self.game_map.hexes.hexes_dict[spawn_point]
        # print(hexagon)
        if not hexagon.unit_on_hex:

            hexagon.add_unit(unit)
            self.game_map.units.add(unit)
            if player_id == self.player_id:
                self.game_map.actions.add(string)