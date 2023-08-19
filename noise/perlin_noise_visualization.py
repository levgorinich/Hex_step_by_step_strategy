import random

import matplotlib.pyplot as plt
import numpy as np

from some_russian_gay_m.noise.perlin_noise import Perlin1D, Perlin2D


octaves = 4
persistance = 0.5
lacanarity = 7
Perlin = Perlin2D()
values = np.zeros((200,200))
for i in range(200):
    for j in range(200):
        print(i,j)
        values[i][j] = Perlin.calcStandartNoiseForPoint((i/100,j/100))
print(values)
arr = [Perlin.calcStandartNoiseForPoint(i)for i in values]


#
plt.title("Perlin Noise")
plt.xlabel("Time")
plt.ylabel("Value")
plt.imshow(values)
plt.show()