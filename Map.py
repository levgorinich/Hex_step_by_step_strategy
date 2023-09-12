import pygame

from math import *

from Groups import HexesGroup, Grid
from Sprites import *
from Spawner import Spawner

class Map:

    def __init__(self, rows, columns, player_id):
        self.rows = rows
        self.columns = columns
        self.player_id = player_id
        self.actions=set()
        self.hex_width = 30* sqrt(3)
        self.hex_height = self.hex_width*sqrt(3)/2
        self.hexes = self.create_tiles()
        self.units =  pygame.sprite.Group()
        self.spawner = Spawner(self)
        self.spawner.create_start_unit()


    def __str__(self):
        return f"map with {self.rows} rows and {self.columns} columns"


    def create_tiles(self):
        hexes = HexesGroup()

        for col in range(self.columns):
            for row in range(self.rows):
                grid_pos =  col, row
                # print(current_y,current_x)
                hex = Hexagon( grid_pos)
                hexes.add(hex)
        return hexes






# class UnitPlacer:
#     def __init__(self, map):
#         self.map = map
#
#     def place_unit_and_add_it_to_player(self, unit, player):
#         self.map.hexes.hexes_dict[unit.grid_pos]
#         player.







