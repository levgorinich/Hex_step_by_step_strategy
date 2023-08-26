from math import cos, sin, pi, sqrt
import pygame
import Health_bar

hex_side = 15 * sqrt(3)
hex_width = 2 * hex_side
hex_height = hex_side * sqrt(3)
class Hexagon(pygame.sprite.Sprite):
    def __init__(self, grid_pos, map_coord, color = (70,70,120), width = hex_width, height =hex_height ):
        super().__init__()
        self.grid_pos = grid_pos
        self.map_coord = map_coord
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        print(self.map_coord)
        self.rect = self.image.get_rect(center=(self.map_coord[0], self.map_coord[1]))
        self.points = []


        # calculating points for hexagon
        v = 0
        for i in range(6):
            self.points.append((cos(v)*((width//2)-1)+ width/2,
                                sin(v)*((width//2)-1)+ width/2-(width-height)/2))
            v += (pi*2)/6

        pygame.draw.polygon( self.image, (30,70,50),self.points )
        self.mask = pygame.mask.from_surface(self.image)

        self.unit_on_hex = False

    def offset_to_cube_coords(self, grid_pos):
        q = grid_pos[1]
        r = grid_pos[0] - (grid_pos[1] - (grid_pos[1]&1)) / 2
        return(q, r, -q-r)

    def add_unit(self, unit):
        self.unit_on_hex = unit

    def remove_unit(self):
        self.unit_on_hex = False
    def kill_unit(self):
        if self.unit_on_hex:
            self.unit_on_hex.kill()
        self.remove_unit()

    def __str__(self):
        return f"Hexagon {self.grid_pos[0]}, {self.grid_pos[1]}"
    def update(self):
        pass

class MapObject(pygame.sprite.Sprite):
    def __init__(self, grid_pos ):
        super().__init__()
        self.grid_pos = grid_pos
        self.width = 25
        self.height = 25
        self.name = "map object"
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.surf.fill((125,125,125))
        self.image = self.surf

        map_coords = self.calculate_coordinate_by_hex_position(self.grid_pos)
        self.map_coord = map_coords

        self.rect = self.image.get_rect(center=map_coords)

    def __str__(self):
        return f"{self.name} {self.grid_pos[0]}, {self.grid_pos[1]}"

    def offset_to_cube_coords(self, x, y):
        q = y
        r = x - (y - (y&1)) / 2
        return(q, r, -q-r)

    def calculate_coordinate_by_hex_position(self, hex_position,):
        map_coord_x = hex_side + hex_side * hex_position[0]
        if hex_position[1] % 2 == 0:
            map_coord_y = hex_height/2 + hex_height * hex_position[1]
        else:
            map_coord_y = hex_height + hex_side * hex_position[1]

        return (map_coord_x, map_coord_y)

class Unit(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "unit"

    def move(self, move_on_hex_grid):
        self.grid_pos += move_on_hex_grid

        self.map_coord = self.calculate_coordinate_by_hex_position(self.grid_pos)

class TriangularUnit(Unit):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        print("I am here")
        self.name = "triangular unit"
        self.race = 1
        self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.health_bar = Health_bar.Health_bar(0,0,self.width,self.height/4,3)
        self.health_bar.draw(self.pict)
        pygame.draw.polygon(self.pict, (255,0,0), [(0, self.height/4 + 2), (self.width/2,self.height), 
                                                   (self.width-1, self.height/4+ 2)])
        self.surf.blit(self.pict,(0,0))
    def update(self,hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.polygon(self.pict, (255,0,0), [(0, self.height/4 + 2), (self.width/2,self.height), 
                                                    (self.width-1, self.height/4+ 2)])
            self.surf.blit(self.pict,(0,0))
        return self.health_bar.hp

        



class SquareUnit(Unit):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "square unit"
        self.race = 2
        self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.health_bar = Health_bar.Health_bar(0,0,self.width,self.height/4,3)
        self.health_bar.draw(self.pict)
        pygame.draw.rect(self.pict, (255,0,0), (0, self.height/4 + 2, self.width, 
                                                self.height - self.height/4 + 2))
        self.surf.blit(self.pict,(0,0))
    def update(self,hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.rect(self.pict, (255,0,0), (0, self.height/4 + 2, self.width, 
                                                self.height -self.height/4 + 2))
            self.surf.blit(self.pict,(0,0))
        return self.health_bar.hp


class CircleUnit(Unit):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "circle unit"
        self.race = 3
        self.image= self.surf
        self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.health_bar = Health_bar.Health_bar(0,0,self.width,self.height/4,3)
        self.health_bar.draw(self.pict)
        pygame.draw.circle(self.surf, (255,0,0), (self.width/2, self.height/2), 10)
        self.surf.blit(self.pict,(0,0))
    def update(self,hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.circle(self.surf, (255,0,0), (self.width/2, self.height/2), 10)
            self.surf.blit(self.pict,(0,0))
        return self.health_bar.hp




