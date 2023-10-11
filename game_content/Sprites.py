from math import cos, sin, pi, sqrt
import pygame
import random
from game_content.Health_bar import Health_bar

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
        self.image = self.surf
        self.map_coords = self.calculate_coordinate_by_hex_position(self.grid_pos)
        self.rect = self.image.get_rect(center=self.map_coords)

    def __str__(self):
        return f"{self.name} {self.grid_pos[0]}, {self.grid_pos[1]}"

    def offset_to_cube_coords(self, grid_pos):
        q = grid_pos[0]
        r = grid_pos[1] - (grid_pos[0] - (grid_pos[0] & 1)) / 2
        return q, r, -q - r
    ## correct version. [col,row] in this order
    def offset_to_cube_coords_for_moving(self, grid_pos,offset):
    
        q = grid_pos[0]
        r = grid_pos[1] - (grid_pos[0] - offset*(grid_pos[0] & 1)) / 2
        return q, r, -q - r


    def calculate_coordinate_by_hex_position(self, hex_position, ):
        map_coord_x = hex_width * (0.5 + 0.75 * hex_position[0])

        if hex_position[0] % 2 == 0:
            map_coord_y = hex_height * (0.5 + hex_position[1])
        else:
            map_coord_y = hex_height * (1 + hex_position[1])

        return map_coord_x, map_coord_y


class Hexagon(MapObject):
    def __init__(self, grid_pos, color=(30, 70, 50), color_not_viewed = (0,0,0), width=hex_width, height=hex_height):
        super().__init__(grid_pos)
        self.grid_pos = grid_pos
        self.color = color
        self.color_not_viewed = color_not_viewed
        self.width = width
        self.height = height
        self.type = "hexagon"
        self.points = self.calculate_points_for_hexagon()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(self.map_coords[0], self.map_coords[1]))
        pygame.draw.polygon(self.image, self.color, self.points)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_discovered = False
        self.is_viewed = 0

        self.unit_on_hex = None
        self.building_on_hex = None

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

    def add_building(self, building):
        self.building_on_hex = building

    def remove_unit(self):
        self.unit_on_hex = False

    def kill_unit(self):
        if self.unit_on_hex:
            print("kill unit")
            self.unit_on_hex.hide_hexes()
            self.unit_on_hex.kill()
        self.remove_unit()

    def __str__(self):
        return f"{self.type}, {self.grid_pos[0]}, {self.grid_pos[1]}"

    def update(self):
        pass
    def draw(self):
        if self.is_discovered and self.is_viewed:
            pygame.draw.polygon(self.image, self.color, self.points)
        elif self.is_discovered and not self.is_viewed:
            pygame.draw.polygon(self.image, self.color_not_viewed, self.points)
        else:
            pygame.draw.polygon(self.image, (0, 0, 0), self.points)

    def draw_in_unit_range(self):
        print("Do nothing")
        pass

    def reveal_hex(self):
        self.is_discovered = True
        self.draw()

    def view_hex(self):
        self.is_viewed+=1
        self.draw()

    def hide_hex(self):
        self.is_viewed-=1
        self.draw()

class Hexagon_land(Hexagon):
    def __init__(self, grid_pos, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, color, width=hex_width, height=hex_height)
        self.color = color
        self.color_not_viewed = (20,50,40)
        self.type = "land Hexagon"
        self.draw()

    # def draw(self):
    #     pygame.draw.polygon(self.image, self.color, self.points)

    def draw_in_unit_range(self):

        color_selected = (30,20,50)
        pygame.draw.polygon(self.image, color_selected, self.points)
class Hexagon_mountain(Hexagon):
    def __init__(self, grid_pos, color=(255,255, 255), width=hex_width, height=hex_height):
        super().__init__(grid_pos, color, width=hex_width, height=hex_height)
        self.color = color
        self.color_not_viewed = (240,230,240)
        self.type = "mountain Hexagon"
        self.draw()

    # def draw(self):
    #     pygame.draw.polygon(self.image, self.color, self.points)

    def draw_in_unit_range(self):
        color_selected = (225,225, 225)
        pygame.draw.polygon(self.image, color_selected, self.points)

class Hexagon_sea(Hexagon):
    def __init__(self, grid_pos, color=(83,236, 236), width=hex_width, height=hex_height):

        super().__init__(grid_pos, color, width=hex_width, height=hex_height)
        self.color = color
        self.color_not_viewed = (70,210,220)

        self.type = "sea Hexagon"

        self.draw()

    # def draw(self):
    #     pygame.draw.polygon(self.image, self.color, self.points)
    def draw_in_unit_range(self):
        color_selected = (53,186, 186)
        pygame.draw.polygon(self.image, color_selected, self.points)


class Building(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.image = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)

class Mine(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        coin_image=  pygame.image.load("Resources/goldcoin1.png")
        self.image.blit(coin_image,(-17,-20))


class Unit(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "unit"
        self.max_stamina = None
        self.stamina = None
        self.price=None
        self.view_range =4
        self.hexes_viewed = []


    def move(self, grid_pos, distance):
        self.grid_pos = grid_pos
        self.stamina -= distance
        # self.map_coord = self.calculate_coordinate_by_hex_position(self.grid_pos)

    def restore_stamina(self):
        self.stamina = self.max_stamina

    def hide_hexes(self):
        [hex.hide_hex() for hex in self.hexes_viewed]
        self.hexes_viewed = []
    def view_hexes(self):
        [hex.view_hex() for hex in self.hexes_viewed]





class MilitaryUnit(Unit):
    def __init__(self, grid_pos, player_id, ):
        super().__init__(grid_pos)
        self.player_id = player_id
        self.attack = None
        self.hp = 10
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw()
        self.discovery_range = 2

    def draw_shape(self):
        pass
    def draw(self):
        self.draw_shape()
        self.health_bar = Health_bar(0, 0, self.width, self.height / 4, self.hp)
        self.health_bar.draw(self.image, self.hp)

    def strike(self):
        self.stamina =0
        return self.attack *(random.random()/2 +0.75)

    def defend(self):
        return self.attack * (random.random()/2 +0.25)

    def update_hp(self, ):
        if self.hp > 0:
            self.health_bar.draw(self.image, self.hp)


class TriangularUnit(MilitaryUnit):

    def __init__(self, grid_pos, player_id, color= (255, 0, 0)):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.price = 30
        self.hp = 3
        self.name = "triangular unit"
        self.attack = 3
        self.max_stamina =1
        self.stamina = 1
        self.draw()

    def draw_shape(self):
        pygame.draw.polygon(self.image, self.color, [(0, self.height / 4 + 2), (self.width / 2, self.height),
                                                (self.width - 1, self.height / 4 + 2)])

    def __repr__(self):
        return f" unit {self.name} on hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


class SquareUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id, color):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.name = "square unit"
        self.price = 30
        self.attack = 2
        self.hp =3
        self.max_stamina= 2
        self.stamina = 2
        self.draw()

    def draw_shape(self):
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))

    def __repr__(self):
        return f"{self.name} on hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


class WarBase(MilitaryUnit):
    def __init__(self, grid_pos, player_id, color):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.name = "war base"
        self.max_stamina= 0
        self.stamina = 0

        self.attack = 0
        self.hp = 10
        self.draw()

    def draw_shape(self):
        pygame.draw.rect(self.image, (0,0,0), (0, self.height / 4 + 2, self.width,
                                               self.height - self.height / 4 + 2))

    def __repr__(self):
        return f"{self.name} on hex {self.grid_pos[0]}, {self.grid_pos[1]}, player {self.player_id}"


class CircleUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id,color):
        self.color = color
        super().__init__(grid_pos, player_id,)
        self.name = "circle unit"
        self.price = 30
        self.attack = 1
        self.hp = 3
        self.max_stamina= 3
        self.stamina = 3
        self.draw()

    def draw_shape(self):
        pygame.draw.circle(self.image, self.color, (self.width / 2, self.height / 2), 10)

    def __repr__(self):
        return f"CircleUnit o hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


