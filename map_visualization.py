import sys

import pygame
from pygame.locals import *
from math import *
from some_russian_gay_m.Groups import CameraGroup
from some_russian_gay_m.Map import Map

pygame.init()
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
# pygame.event.set_grab(True)
pygame.display.set_caption("Drawing Polygons on a Sprite")
clock = pygame.time.Clock()

# diagonal size of hexagon = 2a , where a is the radius of hexagon, or it's side length



game_map = Map(25,25)

hexes = CameraGroup(game_map.hexes)











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