import sys

import pygame
from pygame.locals import *
from math import *
from some_russian_gay_m.Groups import CameraGroup

pygame.init()
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
# pygame.event.set_grab(True)
pygame.display.set_caption("Drawing Polygons on a Sprite")
clock = pygame.time.Clock()

# diagonal size of hexagon = 2a , where a is the radius of hexagon, or it's side length
hex_width = 30* sqrt(3)
hex_height = hex_width*sqrt(3)/2


class Hexagon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, coord_x, coord_y, color = (70,70,120), width = hex_width, height =hex_height ):
        super().__init__()
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.points = []


        # calculating points for hexagon
        v = 0
        for i in range(6):
            self.points.append((cos(v)*((width//2)-1)+ width/2,
                                sin(v)*((width//2)-1)+ width/2-(width-height)/2))
            v += (pi*2)/6

        pygame.draw.polygon( self.image, (30,70,50),self.points )
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


def generate_map(cols, rows):
    """generating hexagon grid with given number of columns and rows"""

    hexes = CameraGroup()

    current_x = hex_width/2
    current_y = hex_height/2

    for col in range(cols):
        # each uneven column is moved down by hex_width/2
        if col %2 ==1:
            current_y+= hex_height/2
        for row in range(rows):
            coord_x = row+col//2+col%2
            coord_y = col

            hex = Hexagon(current_x,current_y, coord_x,coord_y)
            current_y += hex_height
            hexes.add(hex)
        current_x += hex_width*3/4
        current_y= hex_height/2
    return hexes

# Create the polygon sprite object
hexes = generate_map(25,25)








running = True
while running:

    events_list = pygame.event.get()

    hexes.update()
    screen.fill((255, 255, 255))
    hexes.custom_draw(events_list)
    pygame.display.flip()

    for event in events_list:
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Get the mouse position
            mouse = pygame.math.Vector2(pygame.mouse.get_pos())

            mouse -= hexes.offset

            for sprite in hexes:
                # if it is a collision with a rectangle we will check if we have a collision with a mask
                if sprite.rect.collidepoint(mouse.x, mouse.y):
                    local_x = mouse.x - sprite.rect.x
                    local_y = mouse.y - sprite.rect.y
                    if sprite.mask.get_at((local_x, local_y)):
                        print("sprite", sprite.coord_x, sprite.coord_y)
                        break

    clock.tick(60)

pygame.quit()