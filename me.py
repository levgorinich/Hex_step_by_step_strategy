import pygame
import pygame as pg
import sys
import math


class Hex(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("hex.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.topleft = (x, y)
    def onClick(self):
        print("Clicked")


sprite_x = 500
sprite_y = 200

pg.init()
screen = pg.display.set_mode((1280,720))
hex = Hex(sprite_x, sprite_y)
hex_group = pg.sprite.Group()
hex_group.add(hex)
side_length = 15
def generate(rows, columns):
    for col  in range(columns):
        for row in range(rows):
            if col %2 == 0:
                hex = Hex(side_length + 1.5*col * side_length, math.sqrt(3)*side_length+ math.sqrt(3)*row*side_length)
                print(side_length + 1.5*col * side_length, math.sqrt(3)+ 2*math.sqrt(3)*row*side_length)
                hex_group.add(hex)
            else:
                hex = Hex(side_length + 1.5*col * side_length,math.sqrt(3)*(1+row)*side_length)
                print(side_length + 1.5*col * side_length, 2*math.sqrt(3)*(1+row)*side_length)
                hex_group.add(hex)

generate(5,5)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Convert the mouse position to the sprite's local coordinates
            relative_x = mouse_x - sprite_x
            relative_y = mouse_y - sprite_y

            # Check if the mouse position collides with the sprite's mask
            for sprite in hex_group:
                try:
                    if sprite.mask.collidepoint((mouse_x, mouse_y)):
                        print("Clicked")
                except:
                    pass

    screen.fill((235,255,255))

    hex_group.draw(screen)

    pygame.display.flip()
