import matplotlib.pyplot as plt
from some_russian_gay_m.noise.perlin_noise import Perlin1D


octaves = 4
persistance = 0.5
lacanarity = 7
Perlin = Perlin1D()
values = [i/100 for i in range(600)]
arr = [Perlin.getValueAt(i, octaves, lacanarity, persistance)for i in values]



plt.title("Perlin Noise")
plt.xlabel("Time")
plt.ylabel("Value")
plt.plot(values, arr)
plt.show()