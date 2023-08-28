from typing import NoReturn

import pygame, sys

from Map import Map
from Sprites import *

class Button:
    def __init__(self, text, x,y , width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (0,255,0)
        font = pygame.font.SysFont('Arial', 24)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

    def draw(self, display_surface: pygame.Surface)-> None:
        pygame.draw.rect(display_surface, self.color, self.rect)
        pygame.draw.rect(display_surface, "Black", self.rect,2)
        display_surface.blit(self.text_surf, self.text_rect)

    def check_click(self,game_map:Map)->bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                spawn_point =(1,1)
                if self.text == "Triangular":
                    unit = TriangularUnit(spawn_point)
                elif self.text == "Square":
                    unit = SquareUnit(spawn_point)
                elif self.text == "Circle":
                    unit = CircleUnit(spawn_point)
                hexagon = game_map.hexes.hexes_dict[spawn_point]
                print(hexagon)
                if not hexagon.unit_on_hex:
                    hexagon.add_unit(unit)
                    game_map.units.add(unit)

                print("clicked")
                return True
        return False



