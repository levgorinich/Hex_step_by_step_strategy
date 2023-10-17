import pygame

from math import *

from game_content.Groups import HexesGroup
from game_content.Sprites import Hexagon, Hexagon_mountain, Hexagon_sea, Hexagon_land
from player_actions.Spawner import Spawner
from noise.Noise import Noise
import random


class Map:

    def __init__(self, rows, columns, player_id, seed, players_amount = 2, Offline=False):
        self.seed = seed
        random.seed(self.seed)

        self.rows = rows
        self.columns = columns
        self.players_amount = players_amount

        self.player_id = player_id
        self.actions=[]
        self.spawn_point = None
        self.offline = Offline
        self.offline_spawn_point = {0: (2,3), 1: (4,4)}

        self.hex_width = 30* sqrt(3)
        self.hex_height = self.hex_width*sqrt(3)/2
        self.hexes   = self.create_tiles()

        self.units =  pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.Spawner = Spawner(self)
        self.create_mines()


        # self.spawner = Spawner(self)

    def get_hex_by_coord(self, grid_pos):
        if grid_pos[0] in range(0, self.columns + 1) and grid_pos[0] in range(0, self.rows + 1):

            return self.hexes[grid_pos]
        return False
    def get_cube_coords(self, hex):
        return self.hexes.get_hex_cube_coords(hex)

    def calculate_distance(self, hex1, hex2):


        cube_coords1 = self.get_cube_coords(hex1)
        cube_coords2 = self.get_cube_coords(hex2)

        return int((abs(cube_coords1[0] - cube_coords2[0]) + abs(cube_coords1[1] - cube_coords2[1])+abs(cube_coords1[2] - cube_coords2[2]))//2)


    def __str__(self):
        return f"map with {self.rows} rows and {self.columns} columns"


    def create_tiles(self):
        noise = Noise(self.rows, self.columns,seed=self.seed)
        hexes = noise.create_tiles()
        return hexes

    def create_mines(self, ):
        land_hexes = []
        for hex in self.hexes:
            if isinstance(hex, Hexagon_land):
                land_hexes.append(hex.grid_pos)

        for hex in land_hexes:

            a = random.random()
            if a < 0.03:
                self.Spawner.spawn_building("Mine",hex)


        for i in range(self.players_amount):
            print("amount of players in this game ", self.players_amount)
            base1 = random.choice(land_hexes)
            print("base1 ",base1)

            if self.player_id == i:
                self.spawn_point = base1[0], base1[1]+1

            print("spawn point in map ",self.spawn_point,i, self.player_id)


            self.Spawner.spawn_unit("WarBase",base1,player_id=i)



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
        if radius >0:
            for dir in range(6):
                neighbor = self.oddq_offset_neighbor(start,dir)
                neighbor_hex = self.get_hex_by_coord(neighbor)
                if neighbor_hex and isinstance(neighbor_hex, Hexagon_sea) and not isinstance(star, Hexagon_sea) or\
                        not isinstance(neighbor_hex, (Hexagon_mountain, Hexagon_sea)) and isinstance(star, Hexagon_sea):
                    visited.add(neighbor)

            for mov in range(1,radius+1):

                for hex in fringes[mov-1]:
                    fringes.append([])
                    for dir in range(0,6):

                        neighbor  = self.oddq_offset_neighbor(hex,dir)
                        neighbor_hex = self.get_hex_by_coord(neighbor)

                        if not isinstance(star, Hexagon_sea) and not isinstance(neighbor_hex, (Hexagon_mountain, Hexagon_sea)) or\
                                isinstance(star, Hexagon_sea) and isinstance(neighbor_hex, Hexagon_sea) and neighbor_hex:

                            if neighbor not in visited and  self.check_coord_validity(neighbor):
                                visited.add(neighbor)
                                fringes[mov].append(neighbor)

        return tuple(visited)

    def coordinate_range(self, hex, distance):
        hexes=[]
        distance = int(distance)
        qs,rs,ss = map(int,self.get_cube_coords(hex))
        for q in range(qs - distance, qs + distance + 1):

            for r in range(rs - distance, rs + distance + 1):
                for s in range(ss - distance, ss + distance + 1):

                    if q + r + s == 0 and q >= 0 and q < self.columns and r > -self.rows  and s <=0:

                        hex = self.hexes[(q,r,s)]
                        if hex:
                            hexes.append(hex)
        return hexes

    def view_range(self, hex, distance):
        hexes = []
        distance = int(distance)
        qs,rs,ss = map(int,self.get_cube_coords(hex))

        for q in range(qs - distance, qs + distance + 1):
            for r in range(rs - distance, rs + distance + 1):
                for s in range(ss - distance, ss + distance + 1):

                    if q + r + s == 0 and q >= 0 and q < self.columns and r > -self.rows  and s <=0:
                        hex = self.hexes[(q,r,s)]
                        if hex and hex.is_discovered:
                            hex.view_hex()
                            hexes.append(hex)
        return hexes
    def qoffset_from_cube(self,q,r,s,offset):
        col = q
        if offset == -1:
            row = -col - s + (col - (col & 1)) / 2 + 1
        else:
            row = -col - s + (col - (col & 1)) / 2
        return (col, row)

    def end_turn(self):
        for unit in self.units:
            unit.restore_stamina()
        string = "<end_turn" + str(self.player_id) + ">"
        self.actions.append(string)













