from game_content.Sprites import *


class Spawner:
    def __init__(self, game_map):
        self.game_map = game_map
        self.player_id = 1
        self.id_colors= {0 : (255, 0, 0), 1: (0, 125, 255), 2:(125, 125,0), 3:(125, 0, 125),4:(66,66,66),5:(150,50,50)}
        self.create_start_unit()

    def create_start_unit(self):
        pass
    def spawn_unit(self, type, spawn_point, player_id=None):

        if player_id is None:
            player_id = self.game_map.player_id
        color = self.id_colors[int(player_id)]

        # idx = self.player_id
        if type == "Triangular":
            unit = TriangularUnit(spawn_point, player_id, color)
        elif type == "Square":
            unit = SquareUnit(spawn_point, player_id, color)
        elif type == "Circle":
            print("got to spwawn circle")
            unit = CircleUnit(spawn_point, player_id, color)
        elif type == "WarBase":
            unit = WarBase(spawn_point, player_id, color)

        string = "<spawn"+type+"("+str(spawn_point[0])+","+str(spawn_point[1])+"),"+str(player_id)+">"


        hexagon = self.game_map.get_hex_by_coord(spawn_point)
        # print(hexagon)
        if not hexagon.unit_on_hex:

            hexagon.add_unit(unit)
            if unit.player_id == self.game_map.player_id:
                discovered_hexes = self.game_map.coordinate_range(hexagon, unit.discovery_range)
                [hex.reveal_hex() for hex in discovered_hexes]
                unit.hexes_viewed = self.game_map.view_range(hexagon, unit.view_range)
                unit.view_hexes()
            self.game_map.units.add(unit)
            if player_id == self.player_id:
                self.game_map.actions.append(string)

    def spawn_building (self, type, spawn_point, player_id=None):
        if type == "Mine":
            building = Mine(spawn_point,)
        if type == "WarBase":
            building = WarBase(spawn_point,player_id, color=(0,0,0))
        # string = "<spawn"+type+"("+str(spawn_point[0])+","+str(spawn_point[1])+"),"+str(player_id)+">"
        # self.game_map.actions.add(string)

        hexagon = self.game_map.get_hex_by_coord(spawn_point)
        hexagon.add_building(building)
        print("building added")
        self.game_map.buildings.add(building)

