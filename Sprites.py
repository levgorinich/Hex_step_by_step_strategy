from math import cos, sin, pi, sqrt

import pygame

hex_width = 30* sqrt(3)
hex_height = hex_width*sqrt(3)/2
class Hexagon(pygame.sprite.Sprite):
    def __init__(self, grid_pos_x, grid_pos_y, map_coord_x, map_coord_y, color = (70,70,120), width = hex_width, height =hex_height ):
        super().__init__()
        self.grid_pos_x = grid_pos_x
        self.grid_pos_y = grid_pos_y
        self.map_coord_x = map_coord_x
        self.map_coord_y = map_coord_y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(grid_pos_x, grid_pos_y))
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
