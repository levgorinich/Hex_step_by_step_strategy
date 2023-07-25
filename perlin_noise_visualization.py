import matplotlib.pyplot as plt
from noise.perlin_noise import Perlin


octaves = 4
persistance = 0.7
lacanarity = 2
Perlin = Perlin()
values = [i/100 for i in range(600)]
arr = [Perlin.calc_octaves(i, octaves, lacanarity, persistance)for i in values]



plt.title("Perlin Noise")
plt.xlabel("Time")
plt.ylabel("Value")
plt.plot(values, arr)
plt.show()