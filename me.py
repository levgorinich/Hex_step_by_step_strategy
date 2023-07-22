import pygame
import pygame as pg
import sys


class Hex(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("hex.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = (x, y)
    def onClick(self):
        print("Clicked")


pg.init()
screen = pg.display.set_mode((1280,720))
hex = Hex(100,100)
hex_group = pg.sprite.Group()
hex_group.add(hex)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((235,255,255))

    hex_group.draw(screen)

    pygame.display.flip()
