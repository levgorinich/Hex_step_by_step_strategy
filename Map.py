import pygame

from math import *

from some_russian_gay_m.Groups import HexesGroup, Grid
from some_russian_gay_m.Sprites import Hexagon, Unit

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
                grid_pos_x = row+col//2+col%2
                grid_pos_y = col
                # print(current_y,current_x)
                hex = Hexagon( grid_pos_x, grid_pos_y,current_x, current_y)
                current_y += self.hex_height
                hexes.add(hex)
                self.hexes_grid[grid_pos_x,grid_pos_y] = hex
            current_x += self.hex_width*3/4
            current_y= self.hex_height/2
        return hexes

    def create_units(self):
        Units = pygame.sprite.Group()
        unit = Unit(15,2)
        Units.add(unit)
        self.hexes.hexes_dict[15,2].add_unit(unit)
        return Units





