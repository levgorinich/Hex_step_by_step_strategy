from math import cos, sin, pi, sqrt
import pygame
import Health_bar

hex_side = 15 * sqrt(3)
hex_width = 30 * sqrt(3)
hex_height = hex_width / 2 * sqrt(3)


class MapObject(pygame.sprite.Sprite):
    def __init__(self, grid_pos):
        super().__init__()
        self.grid_pos = grid_pos
        self.width = 25
        self.height = 25
        self.name = "map object"
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.surf.fill((125,125,125))
        self.image = self.surf

        self.map_coords = self.calculate_coordinate_by_hex_position(self.grid_pos)
        self.rect = self.image.get_rect(center=self.map_coords)

    def __str__(self):
        return f"{self.name} {self.grid_pos[0]}, {self.grid_pos[1]}"

    def offset_to_cube_coords(self, grid_pos):
        q = grid_pos[1]
        r = grid_pos[0] - (grid_pos[1] - (grid_pos[1] & 1)) / 2
        return q, r, -q - r

    def calculate_coordinate_by_hex_position(self, hex_position, ):
        map_coord_x = hex_width * (0.5 + 0.75 * hex_position[0])

        if hex_position[0] % 2 == 0:
            map_coord_y = hex_height * (0.5 + hex_position[1])
        else:
            map_coord_y = hex_height * (1 + hex_position[1])

        return map_coord_x, map_coord_y


class Hexagon(MapObject):
    def __init__(self, grid_pos, color=(70, 70, 120), width=hex_width, height=hex_height):
        super().__init__(grid_pos)
        self.grid_pos = grid_pos

        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency

        self.rect = self.image.get_rect(center=(self.map_coords[0], self.map_coords[1]))

        # calculating points for hexagon

        pygame.draw.polygon(self.image, (30, 70, 50), self.calculate_points_for_hexagon())
        self.mask = pygame.mask.from_surface(self.image)

        self.unit_on_hex = False

    def calculate_points_for_hexagon(self):
        points = []
        v = 0
        for i in range(6):
            points.append((cos(v) * ((self.width // 2) - 1) + self.width / 2,
                           sin(v) * ((self.width // 2) - 1) + self.width / 2 - (self.width - self.height) / 2))
            v += (pi * 2) / 6
        return points

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


class Unit(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "unit"

    def move(self, move_on_hex_grid):
        self.grid_pos += move_on_hex_grid

        self.map_coord = self.calculate_coordinate_by_hex_position(self.grid_pos)


class MilitaryUnit(Unit):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.hp = 10
        self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.health_bar = Health_bar.Health_bar(0, 0, self.width, self.height / 4, 3)
        self.health_bar.draw(self.pict)

    def update_hp(self, hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.rect(self.pict, (255, 0, 0), (0, self.height / 4 + 2, self.width,
                                                      self.height - self.height / 4 + 2))
            self.surf.blit(self.pict, (0, 0))
        return self.health_bar.hp


class TriangularUnit(MilitaryUnit):

    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        print("I am here")
        self.name = "triangular unit"
        self.attack = 1
        # pygame.draw.polygon(self.surf, (255, 0, 0), [(0, 0), (self.width / 2, self.height), (self.width - 1, 0)])
        # self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.health_bar.draw(self.pict)
        pygame.draw.polygon(self.pict, (255, 0, 0), [(0, self.height / 4 + 2), (self.width / 2, self.height),
                                                     (self.width - 1, self.height / 4 + 2)])
        self.surf.blit(self.pict, (0, 0))


    def update(self, hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.polygon(self.pict, (255, 0, 0), [(0, self.height / 4 + 2), (self.width / 2, self.height),
                                                         (self.width - 1, self.height / 4 + 2)])
            self.surf.blit(self.pict, (0, 0))
        return self.health_bar.hp


class SquareUnit(MilitaryUnit):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "square unit"
        self.attack = 2
        pygame.draw.rect(self.surf, (255, 0, 0), (0, 0, self.width, self.height))
        # self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.health_bar = Health_bar.Health_bar(0, 0, self.width, self.height / 4, 3)
        # self.health_bar.draw(self.pict)
        pygame.draw.rect(self.pict, (255, 0, 0), (0, self.height / 4 + 2, self.width,
                                                  self.height - self.height / 4 + 2))
        self.surf.blit(self.pict, (0, 0))

    def update(self, hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.rect(self.pict, (255, 0, 0), (0, self.height / 4 + 2, self.width,
                                                      self.height - self.height / 4 + 2))
            self.surf.blit(self.pict, (0, 0))
        return self.health_bar.hp


class CircleUnit(MilitaryUnit):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "circle unit"
        self.attack = 3
        pygame.draw.circle(self.surf, (255, 0, 0), (self.width / 2, self.height / 2), 10)
        self.image = self.surf
        # self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.health_bar = Health_bar.Health_bar(0, 0, self.width, self.height / 4, 3)
        # self.health_bar.draw(self.pict)
        pygame.draw.circle(self.surf, (255, 0, 0), (self.width / 2, self.height / 2), 10)
        self.surf.blit(self.pict, (0, 0))

    def update(self, hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.circle(self.surf, (255, 0, 0), (self.width / 2, self.height / 2), 10)
            self.surf.blit(self.pict, (0, 0))
        return self.health_bar.hp
