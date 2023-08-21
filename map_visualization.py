import sys

import pygame
from pygame.locals import *
from math import *
# from some_russian_gay_m.Groups import CameraGroup
from some_russian_gay_m.Map import Map
from some_russian_gay_m.Render import Render
from mapMovement import MapMovementTracker
pygame.init()
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
# pygame.event.set_grab(True)
pygame.display.set_caption("Drawing Polygons on a Sprite")
clock = pygame.time.Clock()
internal_surface = pygame.Surface((2500, 2500),pygame.SRCALPHA)

# diagonal size of hexagon = 2a , where a is the radius of hexagon, or it's side length

game_map = Map(25,25)
tracker = MapMovementTracker(internal_surface.get_size(), pygame.display.get_surface().get_size())
renderer = Render(map_movement_tracker=tracker, internal_surface=internal_surface)


running = True
while running:

    events_list = pygame.event.get()

    game_map.hexes.update()
    # screen.fill('#71deee')
    renderer.pre_display(events_list)
    renderer.display_objects(game_map.hexes)
    renderer.display_units(game_map.units)
    renderer.display()

    # renderer.display_objects(game_map.hexes)
    pygame.display.flip()

    for event in events_list:
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Get the mouse position
            mouse = pygame.math.Vector2(pygame.mouse.get_pos())

            mouse -= tracker.get_dragging_offset()
            for sprite in game_map.hexes:

                if sprite.rect.collidepoint(mouse.x, mouse.y):
                    local_x = mouse.x - sprite.rect.x
                    local_y = mouse.y - sprite.rect.y
                    if sprite.mask.get_at((local_x, local_y)):
                        print("sprite", sprite.grid_pos_x, sprite.grid_pos_y)
                        break

    clock.tick(60)

pygame.quit()