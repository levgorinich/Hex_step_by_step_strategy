import random

import matplotlib.pyplot as plt
import numpy as np

from some_russian_gay_m.noise.perlin_noise import Perlin1D, Perlin2D


octaves = 4
persistance = 0.5
lacanarity = 7
Perlin = Perlin2D()
values = np.zeros((100,100))
for i in range(100):
    for j in range(100):
        values[i][j] = Perlin.calcStandartNoiseForPoint((i/100,j/100))
print(values)
arr = [Perlin.calcStandartNoiseForPoint(i)for i in values]


#
plt.title("Perlin Noise")
plt.xlabel("Time")
plt.ylabel("Value")
plt.imshow(values)
plt.show()