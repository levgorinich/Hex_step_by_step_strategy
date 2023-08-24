from math import cos, sin, pi, sqrt
import pygame

hex_side = 15 * sqrt(3)
hex_width = 2 * hex_side
hex_height = hex_side * sqrt(3)
class Hexagon(pygame.sprite.Sprite):
    def __init__(self, grid_pos_x, grid_pos_y, map_coord_x, map_coord_y, color = (70,70,120), width = hex_width, height =hex_height ):
        super().__init__()
        self.grid_pos_x = grid_pos_x
        self.grid_pos_y = grid_pos_y
        self.map_coord_x = map_coord_x
        self.map_coord_y = map_coord_y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(map_coord_x, map_coord_y))
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

    # def resize_mask(self, zoom=1):
    #     map_coord_x = int(self.map_coord_x * zoom)
    #     map_coord_y = int(self.map_coord_y * zoom)
    #     # self.imgage = pygame.transform.scale(self.image, (int(self.image.get_width() * zoom), int(self.image.get_height() * zoom)))
    #     self.rect= self.imgage.get_rect(center=(map_coord_x, map_coord_y))
    #     print(self.rect)



    def add_unit(self, unit):
        self.unit_on_hex = unit

    def remove_unit(self):
        self.unit_on_hex = False
    def kill_unit(self):
        if self.unit_on_hex:
            self.unit_on_hex.kill()
        self.remove_unit()

    def __str__(self):
        return f"Hexagon {self.grid_pos_x}, {self.grid_pos_y}"
    def update(self):
        pass

class MapObject(pygame.sprite.Sprite):
    def __init__(self, grid_pos_x, grid_pos_y, ):
        super().__init__()
        self.grid_pos_x = grid_pos_x
        self.grid_pos_y = grid_pos_y
        self.width = 20
        self.height = 20
        self.name = "map object"
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.surf.fill((125,125,125))
        self.image = self.surf

        map_coords = self.calculate_coordinate_by_hex_position((self.grid_pos_x, self.grid_pos_y))
        self.map_coord_x = map_coords[0]
        self.map_coord_y = map_coords[1]
        self.rect = self.image.get_rect(center=(self.map_coord_y, self.map_coord_x))

    def __str__(self):
        return f"{self.name} {self.grid_pos_x}, {self.grid_pos_y}"

    def calculate_coordinate_by_hex_position(self, hex_position,):
        map_coord_x = hex_side + hex_side * hex_position[0]
        if hex_position[1] % 2 == 0:
            map_coord_y = hex_height/2 + hex_height * hex_position[1]
        else:
            map_coord_y = hex_height + hex_side * hex_position[1]

        return (map_coord_x, map_coord_y)

class Unit(MapObject):
    def __init__(self, grid_pos_x, grid_pos_y):
        super().__init__(grid_pos_x, grid_pos_y)
        self.name = "unit"

    def move(self, move_on_hex_grid):
        self.grid_pos_x += move_on_hex_grid[0]
        self.grid_pos_y += move_on_hex_grid[1]
        self.map_coord_x, self.map_coord_y = self.calculate_coordinate_by_hex_position((self.grid_pos_x, self.grid_pos_y))

class TriangularUnit(Unit):
    def __init__(self, grid_pos_x, grid_pos_y):
        super().__init__(grid_pos_x, grid_pos_y)
        print("I am here")
        self.name = "triangular unit"
        self.race = 1
        pygame.draw.polygon(self.surf, (255,0,0), [(0, 0), (self.width/2,self.height), (self.width-1, 0)])


class SquareUnit(Unit):
    def __init__(self, grid_pos_x, grid_pos_y):
        super().__init__(grid_pos_x, grid_pos_y)
        self.name = "square unit"
        self.race = 2
        pygame.draw.rect(self.surf, (255,0,0), (0, 0, self.width, self.height))


class CircleUnit(Unit):
    def __init__(self, grid_pos_x, grid_pos_y):
        super().__init__(grid_pos_x, grid_pos_y)
        self.name = "circle unit"
        self.race = 3
        pygame.draw.circle(self.surf, (255,0,0), (self.width/2, self.height/2), 10)
        self.image= self.surf



