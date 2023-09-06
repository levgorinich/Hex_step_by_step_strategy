from typing import NoReturn
from abc import ABC, abstractmethod
import pygame, sys

from Map import Map
from Sprites import *

def empty_funciton():
    print("")

class Button:
    def __init__(self, text, x, y, width, height, action = empty_funciton, color=(0, 255, 0), font_size=24, font_name="Arial",):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        font = pygame.font.SysFont(font_name, font_size)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, display_surface: pygame.Surface) -> None:
        pygame.draw.rect(display_surface, self.color, self.rect)
        pygame.draw.rect(display_surface, "Black", self.rect, 2)
        display_surface.blit(self.text_surf, self.text_rect)

    @abstractmethod
    def check_click(self,) -> bool:
        pass


class MenuButton(Button):
    def __init__(self, text, x, y, width, height,action = empty_funciton, color=(0, 255, 0), font_size=24, font_name="Arial",  ):

        super().__init__(text, x, y, width, height, action, color, font_size, font_name)

    def check_click(self, function_if_clicked) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print(self.action)
                self.action()
                return True

class ButtonForUnitSpawner(Button):
    def __init__(self, text, x, y, width, height,action = empty_funciton, color=(0, 255, 0), font_size=24, font_name="Arial"):
        super().__init__(text, x, y, width, height, action, color, font_size, font_name)

    def draw(self, display_surface: pygame.Surface) -> None:
        pygame.draw.rect(display_surface, self.color, self.rect)
        pygame.draw.rect(display_surface, "Black", self.rect, 2)
        display_surface.blit(self.text_surf, self.text_rect)

    def check_click(self, game_map: Map) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                spawn_point = (1, 1)
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
