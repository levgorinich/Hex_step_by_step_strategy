import pygame, sys
from some_russian_gay_m.Sprites import *

class Button:
    def __init__(self, text, x,y , width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0,255,0)
        font = pygame.font.SysFont('Arial', 24)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

    def draw(self, display_surface):
        pygame.draw.rect(display_surface, self.color, self.rect)
        display_surface.blit(self.text_surf, self.text_rect)

    def check_click(self, game_map):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                spawn_point =(1,1)
                unit = TriangularUnit(spawn_point[0], spawn_point[1])
                hex = game_map.hexes_grid[spawn_point[0], spawn_point[1]]
                if not hex.unit_on_hex:
                    hex.add_unit(unit)
                    game_map.units.addmy(unit)

                print("clicked")
                return True
        return False



