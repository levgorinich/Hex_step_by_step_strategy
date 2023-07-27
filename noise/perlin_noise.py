import random
import numpy as np
import math
import pprint

pp = pprint.PrettyPrinter(indent=4)
class Perlin1D:
    def __init__(self, ):
        self.gradients = []




    def assign_gradients(self,len):
        for i in range(int(len)-1):
            grad = random.random()*2-1
            self.gradients.append(grad)

    def getValueAt(self, point, octaves, laconarity, persistance):
        amplitude = 1
        frequency = 1
        noiseHeight = 0

        # With each octave< frequency increases the amplitude decreases
        for _ in range(octaves):
            point = point * frequency
            noiseHeight += self.calcStandartNoiseForPoint(point) *amplitude

            amplitude*=persistance
            frequency*=laconarity

        return noiseHeight

    def calcStandartNoiseForPoint(self, point):
        """Calculates the standart noise for a given point"""

        while point >= len(self.gradients)-1:
            grad = random.uniform(-1,1)
            self.gradients.append(grad)

        # Caclulate vectors from 0 and 1 to given point
        left_vector = point - math.floor(point)
        right_vector = left_vector-1

        # Dot product of random vectors and distance vectors
        lef_dot_product = left_vector*self.gradients[int(math.floor(point))]
        right_dot_product = right_vector*self.gradients[int(math.ceil(point))]

        amt = self.smooze(left_vector)
        return self.__lepr(lef_dot_product, right_dot_product, amt)
    def smooze(self, x):
        """ Smoothes the noise
        This function has first and second derivatives 0 in poins 1 and 0 """
        return 6*x**5 - 15*x**4 + 10*x**3

    def __lepr(self, start, stop, amt):
        "Do the interpolation"
        return amt * (stop - start) + start


class Perlin2D:
    def __init__(self):
        self.gradients = np.array([[self.chooseGradient()]])

    def chooseGradient(self):
        return random.choice([(1,1),(-1,1),(1,-1),(-1,-1)])
    def getVector(self, point):

        return self.gradients[point[1]][point[0]]
    def calcStandartNoiseForPoint(self, point):
        while point[1] >= len(self.gradients)-1:
            row = np.array([[self.chooseGradient()]])
            for _ in range(len(self.gradients[0])-1):
                grad = self.chooseGradient()
                row = np.append(row, np.array([[grad]]), axis=0)

            self.gradients = np.append(self.gradients, row, axis=0)

        while point[0] >= len(self.gradients[0])-1:
            column = np.array([[self.chooseGradient()]])
            for i in range(len(self.gradients)-1):
                grad = self.chooseGradient()
                column = np.append(column, np.array([[grad]]), axis=0)
            self.gradients = np.append(self.gradients, column, axis=1)

        vectTopLeft = self.getVector((math.floor(point[0]), math.floor(point[1])))
        vectTopRight = self.getVector((math.ceil(point[0]), math.floor(point[1])))
        vectBottomLeft = self.getVector((math.floor(point[0]), math.ceil(point[1])))
        vectBottomRight = self.getVector((math.ceil(point[0]), math.ceil(point[1])))


        x0y0 = (point[0] - math.floor(point[0]), point[1] - math.floor(point[1]))
        x0y1 =  (point[0] - math.ceil(point[0]), point[1] - math.ceil(point[1]))
        x1y0 = (point[0] - math.ceil(point[0]), point[1] - math.floor(point[1]))
        x1y1 = (point[0] - math.floor(point[0]), point[1] - math.ceil(point[1]))

        dotTopRight = np.dot(x0y1, vectTopRight)
        dotTopLeft = np.dot(x0y0, vectTopLeft)
        dotBottomRight = np.dot(x1y1, vectBottomRight)
        dotBottomLeft = np.dot(x1y0, vectBottomLeft)

        u = self.smooze(x0y0[0])
        v = self.smooze(x0y0[1])

        return self.__lepr(u, self.__lepr(v, dotBottomLeft, dotTopLeft),self.__lepr(v, dotBottomRight, dotTopRight))


    def smooze(self, x):
        """ Smoothes the noise
        This function has first and second derivatives 0 in poins 1 and 0 """
        return 6*x**5 - 15*x**4 + 10*x**3

    def __lepr(self, start, stop, amt):
        "Do the interpolation"
        return amt * (stop - start) + start






