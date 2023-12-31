from numpy import floor
from perlin_noise import PerlinNoise
# import matplotlib.pyplot as plt
import random

from game_content.Groups import HexesGroup
from game_content.Sprites import Hexagon, Hexagon_sea, Hexagon_mountain, Hexagon_land


class Noise():
    def __init__(self, rows, columns,seed =None, water_bound=-0.1, mountain_bound=0.5):
        self.rows = rows
        self.columns = columns

        if seed is None:
            self.seed = random.randint(0, 4000)
        else:
            self.seed = seed

        self.start = self.start_generation()
        self.mountain_bound = mountain_bound
        self.water_bound = water_bound

    def start_generation(self):
        # генерация основного шума и параметризация

        noise = PerlinNoise(octaves=8, seed=self.seed)
        amp = 2
        period = 24
        terrain_width = self.rows

        # генерация матрицы для представления ландшафта
        landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

        for position in range(terrain_width ** 2):
            # вычисление высоты y в координатах (x, z)
            x = floor(position / terrain_width)
            z = floor(position % terrain_width)
            y = (noise([x / period, z / period]) * amp)
            landscale[int(x)][int(z)] = y

        # чтобы можно было спавнить юнитов и прога не вылетала, устанавливаю для гекса (1,1) значение 1
        # landscale[1][1] = 0

        return landscale

    def create_tiles(self):

        hexes = HexesGroup()
        landscape = self.start_generation()
        for col in range(self.columns):
            for row in range(self.rows):
                if self.mountain_bound > landscape[col][row] > self.water_bound:
                    grid_pos = col, row
                    # print(current_y,current_x)
                    hex = Hexagon_land(grid_pos)
                    hexes.add(hex)

                elif landscape[col][row] <= self.water_bound:
                    grid_pos = col, row
                    # print(current_y,current_x)
                    hex = Hexagon_sea(grid_pos)
                    hexes.add(hex)

                    # self.empty_hexes.append((col,row))
                elif landscape[col][row] > self.mountain_bound:
                    grid_pos = col, row
                    # print(current_y,current_x)
                    hex = Hexagon_mountain(grid_pos)
                    hexes.add(hex)


        return hexes
