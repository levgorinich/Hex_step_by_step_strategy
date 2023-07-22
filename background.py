import pygame as pg
from math import *

class Hexagon:
    def __init__(self,radius,width):
        self.x = 10
        self.y = 10
        self.r = radius
        self.w = width

    def draw(self,x,y):
        self.x = x
        self.y = y
        l1 = pg.draw.line(screen,WHITE, [self.x+self.r/2,y],
                          [self.x+self.r/2+self.r, self.y],self.w)
        l2 = pg.draw.line(screen,WHITE,[self.x+self.r/2+self.r,self.y],
                          [self.x+self.r/2+self.r+self.r/2, sqrt(3)/2*self.r+self.y],self.w)
        l3 = pg.draw.line(screen,WHITE,[self.x+self.r/2+self.r+self.r/2, sqrt(3)/2*self.r+self.y],
                          [self.x+self.r/2+self.r, 2*sqrt(3)/2*self.r+self.y],self.w)
        l4 = pg.draw.line(screen,WHITE,[self.x+self.r/2+self.r, 2*sqrt(3)/2*self.r+self.y],
                          [self.x+self.r/2, 2*sqrt(3)/2*self.r+self.y],self.w)
        l5 = pg.draw.line(screen,WHITE,[self.x+self.r/2, 2*sqrt(3)/2*self.r+self.y],
                          [self.x+self.r/2-self.r/2, sqrt(3)/2*self.r+self.y],self.w)
        l6 = pg.draw.line(screen,WHITE,[self.x+self.r/2-self.r/2, sqrt(3)/2*self.r+self.y],
                          [self.x+self.r/2,self.y],self.w)


    





pg.init()
clock = pg.time.Clock()
FPS = 10
WINDOW_SIZE = (700, 700)
WHITE = (255,255,255)
BACKGROUND = (150, 90, 30)
screen = pg.display.set_mode(WINDOW_SIZE)

screen.fill(BACKGROUND)
a = 20
x = 20
y = 60
w = 5
hex = Hexagon(20,1)
for i in range(100):
    k = -10
    for j in range(100):
        hex.draw(-10+j*3*a,2*i*sqrt(3)/2*a+k)
        hex.draw(-10+3/2*a+j*3*a,2*i*sqrt(3)/2*a+sqrt(3)/2*a+k)
    
# l1 = pg.draw.line(screen,WHITE, [x+a/2,y], [x+a/2+a, y],w)
# l2 = pg.draw.line(screen,WHITE,[x+a/2+a,y],[x+a/2+a+a/2, sqrt(3)/2*a+y],w)
# l3 = pg.draw.line(screen,WHITE,[x+a/2+a+a/2, sqrt(3)/2*a+y],[x+a/2+a, 2*sqrt(3)/2*a+y],w)
# l4 = pg.draw.line(screen,WHITE,[x+a/2+a, 2*sqrt(3)/2*a+y],[x+a/2, 2*sqrt(3)/2*a+y],w)
# l5 = pg.draw.line(screen,WHITE,[x+a/2, 2*sqrt(3)/2*a+y],[x+a/2-a/2, sqrt(3)/2*a+y],w)
# l6 = pg.draw.line(screen,WHITE,[x+a/2-a/2, sqrt(3)/2*a+y],[x+a/2,y],w)


pg.display.update()

run = True

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
    clock.tick(FPS)
