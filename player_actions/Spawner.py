from game_content.Sprites import *


class Spawner:
    def __init__(self, game_map):
        self.game_map = game_map
        self.player_id = game_map.player_id
        self.id_colors= {0 : (255, 0, 0), 1: (0, 125, 255)}
        self.create_start_unit()

    def create_start_unit(self):
        pass
    def spawn_unit(self, type, spawn_point, player_id=None):

        if player_id is None:
            player_id = self.player_id
        color = self.id_colors[int(player_id)]

        # idx = self.player_id
        if type == "Triangular":
            unit = TriangularUnit(spawn_point, player_id, color)
        elif type == "Square":
            unit = SquareUnit(spawn_point, player_id, color)
        elif type == "Circle":
            unit = CircleUnit(spawn_point, player_id, color)
        elif type == "WarBase":
            unit = WarBase(spawn_point, player_id, color)

        string = "<spawn"+type+"("+str(spawn_point[0])+","+str(spawn_point[1])+"),"+str(player_id)+">"


        hexagon = self.game_map.hexes.hexes_dict[spawn_point]
        # print(hexagon)
        if not hexagon.unit_on_hex:

            hexagon.add_unit(unit)
            self.game_map.units.add(unit)
            if player_id == self.player_id:
                self.game_map.actions.add(string)

    def spawn_building (self, type, spawn_point, player_id=None):
        if type == "Mine":
            building = Mine(spawn_point,)
        if type == "WarBase":
            building = WarBase(spawn_point,player_id, color=(0,0,0))
        # string = "<spawn"+type+"("+str(spawn_point[0])+","+str(spawn_point[1])+"),"+str(player_id)+">"
        # self.game_map.actions.add(string)

        hexagon = self.game_map.hexes.hexes_dict[spawn_point]
        hexagon.add_building(building)
        print("building added")
        self.game_map.buildings.add(building)

