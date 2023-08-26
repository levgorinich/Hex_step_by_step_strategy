import pygame

from math import *

from Groups import HexesGroup, Grid
from Sprites import *

class Map:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.hexes_grid = Grid()

        self.hex_width = 30* sqrt(3)
        self.hex_height = self.hex_width*sqrt(3)/2
        self.hexes = self.create_tiles()
        self.units = self.create_units()

    def __str__(self):
        return f"map with {self.rows} rows and {self.columns} columns"

    def create_tiles(self):
        hexes = HexesGroup()

        current_x = self.hex_width/2
        current_y = self.hex_height/2

        for col in range(self.columns):
            # each uneven column is moved down by hex_width/2
            if col %2 ==1:
                current_y+= self.hex_height/2
            for row in range(self.rows):
                grid_pos =  col, row

                # print(current_y,current_x)
                hex = Hexagon( grid_pos,(current_x, current_y))
                current_y += self.hex_height
                hexes.add(hex)
                # self.hexes_grid[grid_pos] = hex
            current_x += self.hex_width*3/4
            current_y= self.hex_height/2
        return hexes

    def create_units(self):
        Units = pygame.sprite.Group()
        unit = TriangularUnit((15,2))
        Units.add(unit)
        unit_2 = SquareUnit((20,2))
        Units.add(unit_2)
        unit_4 = SquareUnit((5,2))
        Units.add(unit_4)
        unit_5 = SquareUnit((12,2))
        Units.add(unit_5)
        unit_3 = CircleUnit((10,2))
        Units.add(unit_3)
        # print(self.hexes.hexes_dict)
        self.hexes.hexes_dict[(15,2)].add_unit(unit)
        self.hexes.hexes_dict[20,2].add_unit(unit_2)
        self.hexes.hexes_dict[10,2].add_unit(unit_3)
        self.hexes.hexes_dict[5,2].add_unit(unit_4)
        self.hexes.hexes_dict[12,2].add_unit(unit_5)
        return Units





