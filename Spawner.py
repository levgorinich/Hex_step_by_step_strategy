from Sprites import *
class Spawner:
    def __init__(self, game_map):
        self.game_map = game_map

    def spawn_unit(self, unit_name, spawn_point):
        if unit_name == "Triangular":
            unit = TriangularUnit(spawn_point)
        elif unit_name == "Square":
            unit = SquareUnit(spawn_point)
        elif unit_name == "Circle":
            unit = CircleUnit(spawn_point)

        hexagon = self.game_map.hexes.hexes_dict[spawn_point]
        print(hexagon)
        if not hexagon.unit_on_hex:
            hexagon.add_unit(unit)
            self.game_map.units.add(unit)
