from math import sqrt

import pygame

from some_russian_gay_m.Sprites import Hexagon
class HexesGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.hexes_dict =Grid()


    def add(self, *hexes, **kwargs):
        for hex in hexes:
            super().add(hex, **kwargs)  # Add sprite to the standard Group
            self.hexes_dict[hex.grid_pos] = hex  # Add sprite to the lookup dictionary


class Grid(dict):
    # """An extension of a basic dictionary with a fast, consistent lookup by value implementation."""
    def __init__(self, default=None, *args, **kwargs):
        super(Grid, self).__init__(*args, **kwargs)
        self.default = default

    def __getitem__(self, key):
        return super(Grid, self).get(key, self.default)

    def find(self, pos):
        for key, value in self.items():
            if value == pos:
                return key
        return None




