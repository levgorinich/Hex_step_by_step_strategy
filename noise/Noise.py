from numpy import floor
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import random

class Noise():
   def __init__(self,rows):
      self.rows = rows
      self.start = self.start_generation()
      

   def start_generation(self):
      # генерация основного шума и параметризация
      noise = PerlinNoise(octaves=8, seed = random.randint(0,4000))
      amp = 2
      period = 24
      terrain_width = self.rows

      #генерация матрицы для представления ландшафта 
      landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

      for position in range(terrain_width**2):
         # вычисление высоты y в координатах (x, z)
         x = floor(position / terrain_width)
         z = floor(position % terrain_width)
         y = floor(noise([x/period, z/period])*amp)
         landscale[int(x)][int(z)] = int(y) 
      # чтобы можно было спавнить юнитов и прога не вылетала, устанавливаю для гекса (1,1) значение 1
      landscale[1][1] = 0 

      return landscale


# noise = PerlinNoise(octaves=8, seed= random.randint(0,4000))
# amp = 2
# period = 24
# terrain_width = 25

# #генерация матрицы для представления ландшафта 
# landscale = [[0 for i in range(terrain_width)] for i in range(terrain_width)]

# for position in range(terrain_width**2):
#    # вычисление высоты y в координатах (x, z)
#    x = floor(position / terrain_width)
#    z = floor(position % terrain_width)
#    y = floor(noise([x/period, z/period])*amp)
#    landscale[int(x)][int(z)] = int(y) 
# # чтобы можно было спавнить юнитов и прога не вылетала, устанавливаю для гекса (1,1) значение 1
# print(landscale)
# plt.imshow(landscale)
# plt.show()
# # landscale[1][1] = 0