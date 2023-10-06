import pygame

from math import *

from game_content.Groups import HexesGroup
from game_content.Sprites import Hexagon, Hexagon_mountain, Hexagon_sea
from player_actions.Spawner import Spawner
from noise.Noise import Noise
import random


class Map:

    def __init__(self, rows, columns, player_id, seed, Offline=False):
        self.seed = seed
        random.seed(self.seed)

        self.rows = rows
        self.columns = columns

        self.player_id = player_id
        self.actions=[]
        self.spawn_point = None
        self.offline = Offline
        self.offline_spawn_point = {0: (2,2), 1: (4,4)}

        self.hex_width = 30* sqrt(3)
        self.hex_height = self.hex_width*sqrt(3)/2
        self.hexes   = self.create_tiles()

        self.units =  pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.Spawner = Spawner(self)
        self.create_mines([(1,1)])


        # self.spawner = Spawner(self)

    def get_hex_by_coord(self, grid_pos):
        return self.hexes.hexes_dict[grid_pos]


    def __str__(self):
        return f"map with {self.rows} rows and {self.columns} columns"


    def create_tiles(self):
        noise = Noise(self.rows, self.columns,seed=self.seed)
        hexes = noise.create_tiles()
        return hexes

    def create_mines(self, land_hexes):
        for hex in land_hexes:

            a = random.random()
            if a < 0.03:
                self.Spawner.spawn_building("Mine",hex)
        if self.offline:
            base1 = (2,2)
            base2 = (3,2)
            self.spawn_point= self.offline_spawn_point[self.player_id]
        else:
            base1 = random.choice(land_hexes)
            base2 = random.choice(land_hexes)
            if self.player_id == 0:
                self.spawn_point = base1
            else:
                self.spawn_point = base2

        self.Spawner.spawn_unit("WarBase",base1,player_id=0)
        self.Spawner.spawn_unit("WarBase",base2,player_id=1)


    def check_coord_validity(self,cords):
        return cords[0] >= 0 and cords[1] >= 0 and cords[0] < self.rows and cords[1] < self.columns

    def oddq_offset_neighbor(self,hex,direction):
        oddq_direction_differences = [
            # even cols
            [[+1,  0], [+1, -1], [ 0, -1],
             [-1, -1], [-1,  0], [ 0, +1]],
            # odd cols
            [[+1, +1], [+1,  0], [ 0, -1],
             [-1,  0], [-1, +1], [ 0, +1]],
        ]


        parity = hex[0] & 1
        diff = oddq_direction_differences[parity][direction]
        return (hex[0] + diff[0], hex[1]+ diff[1])

    def reachable_hexes(self,start, radius):
        print(start)
        visited = set() # set of hexes
        visited.add(start)
        star = self.get_hex_by_coord(start)
        fringes = [] # array of arrays of hexes
        fringes.append([start])

        for dir in range(6):
            neighbor = self.oddq_offset_neighbor(start,dir)
            neighbor_hex = self.get_hex_by_coord(neighbor)
            if isinstance(neighbor_hex, Hexagon_sea) and not isinstance(star, Hexagon_sea) or\
                    not isinstance(neighbor_hex, (Hexagon_mountain, Hexagon_sea)) and isinstance(star, Hexagon_sea):
                visited.add(neighbor)

        for mov in range(1,radius+1):

            for hex in fringes[mov-1]:
                fringes.append([])
                for dir in range(0,6):

                    neighbor  = self.oddq_offset_neighbor(hex,dir)
                    neighbor_hex = self.get_hex_by_coord(neighbor)

                    if not isinstance(star, Hexagon_sea) and not isinstance(neighbor_hex, (Hexagon_mountain, Hexagon_sea)) or\
                            isinstance(star, Hexagon_sea) and isinstance(neighbor_hex, Hexagon_sea):

                        if neighbor not in visited and  self.check_coord_validity(neighbor):
                            visited.add(neighbor)
                            fringes[mov].append(neighbor)

        return tuple(visited)

    def qoffset_from_cube(self,q,r,s,offset):
        col = q
        if offset == -1:
            row = -col - s + (col - (col & 1)) / 2 + 1
        else:
            row = -col - s + (col - (col & 1)) / 2
        return (col, row)











