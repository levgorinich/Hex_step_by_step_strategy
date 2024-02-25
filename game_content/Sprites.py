import math
from abc import ABC
from math import cos, sin, pi, sqrt
import numpy
import numpy as np
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
    def offset_to_cube_coords_for_moving(self, grid_pos, offset):

        q = grid_pos[0]
        r = grid_pos[1] - (grid_pos[0] - offset * (grid_pos[0] & 1)) / 2
        return q, r, -q - r

    def calculate_coordinate_by_hex_position(self, hex_position, ):
        map_coord_x = hex_width * (0.5 + 0.75 * hex_position[0])

        if hex_position[0] % 2 == 0:
            map_coord_y = hex_height * (0.5 + hex_position[1])
        else:
            map_coord_y = hex_height * (1 + hex_position[1])

        return map_coord_x, map_coord_y


class Hexagon(MapObject):
    def __init__(self, grid_pos,game_map,  color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos)
        self.grid_pos = grid_pos
        self.color = color
        self.game_map = game_map
        self.width = width
        self.height = height
        self.type = "hexagon"
        self.points = self.calculate_points_for_hexagon()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(self.map_coords[0], self.map_coords[1]))
        pygame.draw.polygon(self.image, self.color, self.points)
        self.image.set_at(list(map(int, self.points[0])), (225, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rivers = [False] * 6
        self.roads = [False] * 7
        self.directions = {0:pygame.Vector3(1,0,-1), 1:pygame.Vector3(0, 1, -1), 2:pygame.Vector3(-1, 1,0),
                           3:pygame.Vector3(-1, 0, 1), 4:pygame.Vector3(0, -1, 1), 5:pygame.Vector3(1, -1, -0)}

        self.unit_on_hex = None
        self.building_on_hex = None


    def save_to_json(self):
        print("Call buildings save to json ", self.building_on_hex)
        hex_dict = {"type": str(self.__class__.__name__)}

        if self.building_on_hex:
            print("in building on hex ")
            hex_dict["building_on_hex"] = self.building_on_hex.save_to_json()
        else:
            hex_dict["building_on_hex"] = None

        return str(self.grid_pos), hex_dict

    def __repr__(self):
        return f"{self.__class__.__name__}, {self.unit_on_hex}, {self.building_on_hex}"

    def calculate_points_for_hexagon(self):
        points = []
        v = 0
        for i in range(6):
            points.append((round(cos(v) * (self.width // 2) + self.width / 2, 2),
                           round(sin(v) * (self.width // 2) + self.width / 2 - (self.width - self.height) / 2, 2)))
            v += (pi * 2) / 6
        return points

    def add_unit(self, unit):
        self.unit_on_hex = unit


    def remove_unit(self):
        self.unit_on_hex = False

    def kill_unit(self):
        if self.unit_on_hex:
            self.unit_on_hex.hide_hexes()
            self.unit_on_hex.kill()
        self.remove_unit()

    def __str__(self):
        return f"{self.type}, {self.grid_pos[0]}, {self.grid_pos[1]}"

    def update(self):
        pass

    def draw(self):

        pygame.draw.polygon(self.image, self.color, self.points)
        for idx, river in enumerate(self.rivers):
            if river:
                self.draw_a_river(idx)

        for idx, road in enumerate(self.roads):
            if road:
                self.draw_a_road(idx)

        if self.building_on_hex:

            self.image.blit(self.building_on_hex.image, (11,4))

        # pygame.draw.circle(self.image, (0, 255, 255), self.points[1], 5)
    def discover_rivers_to_draw(self, triangle):
        self.add_a_river(triangle)

        coords = pygame.Vector3(self.offset_to_cube_coords(self.grid_pos))

        new = tuple(coords + self.directions[triangle])
        new_tirangle = (triangle + 3) % 6
        self.game_map.hexes[new].add_a_river(new_tirangle)

    def add_building(self, building):
        self.building_on_hex = building
        self.draw()

    def add_a_river(self, triangle):
        try:
            self.rivers[triangle] = True
        except IndexError as e:
            print("Invalid triangle number")
        self.draw()


    def draw_a_river(self, triangle):
        pygame.draw.polygon(self.image, (0, 255, 255), self.draw_river(triangle))

    def draw_river(self, triangle_number: int, river_thickness: int = 3, ):

        river_thickness = river_thickness
        another_side = math.sqrt(3)
        point_0_left = (self.points[0][0] - another_side, self.points[0][1] + river_thickness)
        point_0_right = (self.points[0][0] - another_side, self.points[0][1] - river_thickness)
        point_1_left = (self.points[1][0] - river_thickness, self.points[1][1])
        point_1_right = (self.points[1][0] + another_side, self.points[1][1] - river_thickness)
        point_2_left = (self.points[2][0] - another_side, self.points[2][1] - river_thickness)
        point_2_right = (self.points[2][0] + river_thickness, self.points[2][1])
        point_3_left = (self.points[3][0] + another_side, self.points[3][1] - river_thickness)
        point_3_right = (self.points[3][0] + another_side, self.points[3][1] + river_thickness)
        point_4_left = (self.points[4][0] + river_thickness, self.points[4][1])
        point_4_right = (self.points[4][0] - another_side, self.points[4][1] + river_thickness)
        point_5_left = (self.points[5][0] + another_side, self.points[5][1] + river_thickness)
        point_5_right = (self.points[5][0] - river_thickness, self.points[5][1])

        points_for_triangle = {0: [self.points[0], point_0_right, point_1_left, self.points[1]],
                               1: [self.points[1], point_1_right, point_2_left, self.points[2]],
                               2: [self.points[2], point_2_right, point_3_left, self.points[3]],
                               3: [self.points[3], point_3_right, point_4_left, self.points[4]],
                               4: [self.points[4], point_4_right, point_5_left, self.points[5]],
                               5: [self.points[5], point_5_right, point_0_left, self.points[0]]}

        return points_for_triangle[triangle_number]

    def discover_what_roads_to_draw(self,):
            coords = pygame.Vector3(self.offset_to_cube_coords(self.grid_pos))
            for triangle, direction in self.directions.items():
                new = tuple(coords + direction)
                hex = self.game_map.hexes[new]
                if hex and any(hex.roads):
                    hex.add_a_road((triangle + 3) % 6)
                    self.add_a_road(triangle)
            if not any(self.roads):
                self.add_a_road(6)


    def draw_a_road(self, triangle_number):

        if triangle_number == 6:
            pygame.draw.circle(self.image, (0, 30, 170),self.calculate_points_for_road(triangle_number), 5)
        else:
            self.roads[6] = False
            pygame.draw.polygon(self.image, (0, 30, 170), self.calculate_points_for_road(triangle_number))



    def add_a_road(self, triangle_number):
        try:
            self.roads[triangle_number] = True
            self.draw()
        except IndexError as e:
            print("Invalid triangle number")









    def calculate_points_for_road(self, triangle, line_thickness = 4):
        p = [pygame.Vector2(point) for point in self.points]
        side = hex_side / 2 - line_thickness /2
        big_side = side * math.sqrt(3)/2
        small_side = side *0.5
        road_1_p0 = p[2] + (side, 0)
        road_1_p3 = p[1] + (-side, 0)
        road_2_p0 = p[3] +(small_side, big_side)
        road_2_p3 = p[2]+ (-small_side, -big_side)
        road_3_p0 = p[4]+(-small_side, big_side)
        road_3_p3 = p[3] + (small_side, -big_side)
        road_4_p0 = p[5] + (-side, 0)
        road_4_p3 = p[4] + (side, 0)
        road_5_p0 = p[0] + (-small_side, -big_side)
        road_5_p3 = p[5] + (small_side, big_side)
        road_0_p0 = p[1] + (small_side, -big_side)
        road_0_p3 = p[0] + (-small_side, big_side)
        center = (p[2] +(math.floor(hex_side/2), -hex_side/2*math.sqrt(3)))
        small_center_side = line_thickness/2
        large_center_side=  small_center_side * math.sqrt(3)
        center_point_0 =  center + (large_center_side, 0)
        center_point_1 = center + (small_center_side, large_center_side)
        center_point_2 = center + (-small_center_side, large_center_side)
        center_point_3 = center + (-large_center_side, 0)
        center_point_4 = center + (-small_center_side, -large_center_side)
        center_point_5 = center + (small_center_side, -large_center_side)

        points_for_river = {0: [road_0_p0, center_point_3, center_point_4, road_0_p3],
                            1: [road_1_p0, center_point_4, center_point_5, road_1_p3],
                            2: [road_2_p0, center_point_5, center_point_0, road_2_p3],
                            3: [road_3_p0, center_point_0, center_point_1, road_3_p3],
                            4: [road_4_p0, center_point_1, center_point_2, road_4_p3],
                            5: [road_5_p0, center_point_2, center_point_3, road_5_p3],
                            6 : center}

        return points_for_river[triangle]
        # pygame.draw.polygon(self.image, (0, 30, 170), [road_1_p0, center_point_4,  center_point_5, road_1_p3])
        # pygame.draw.polygon(self.image, (0, 30, 170), [road_2_p0, center_point_5, center_point_0, road_2_p3])
        # pygame.draw.polygon(self.image, (0, 30, 170), [road_3_p0, center_point_0, center_point_1, road_3_p3])
        # pygame.draw.polygon(self.image, (0, 30, 170), [road_4_p0, center_point_1, center_point_2, road_4_p3])
        # pygame.draw.polygon(self.image, (0, 30, 170), [road_5_p0, center_point_2, center_point_3, road_5_p3])
        # pygame.draw.polygon(self.image, (0, 30, 170), [road_0_p0, center_point_3,  center_point_4, road_0_p3])







class Hexagon_land(Hexagon):
    def __init__(self, grid_pos, game_map, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "land Hexagon"

        self.draw()

    # def draw(self):
    #     pygame.draw.polygon(self.image, self.color, self.points)

    def draw_in_unit_range(self):
        color_selected = (30, 20, 50)
        pygame.draw.polygon(self.image, color_selected, self.points)


class Hexagon_mountain(Hexagon):
    def __init__(self, grid_pos, game_map,  color=(255, 255, 255), width=hex_width, height=hex_height):
        super().__init__(grid_pos,game_map,  color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "mountain Hexagon"
        self.draw()

    # def draw(self):
    #     pygame.draw.polygon(self.image, self.color, self.points)

    def draw_in_unit_range(self):
        color_selected = (225, 225, 225)
        pygame.draw.polygon(self.image, color_selected, self.points)


class Hexagon_sea(Hexagon):
    def __init__(self, grid_pos, game_map, color=(83, 236, 236), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "sea Hexagon"

        self.draw()


class Hexagon_empty(Hexagon):
    def __init__(self, grid_pos, game_map, color=(0, 0, 0), width=hex_width, height=hex_height):
        super().__init__(grid_pos, game_map, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "empty Hexagon"

        self.draw()


class Building(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.image = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)
        self.name = "building"
        self.population = 123
        self.cattle = 0

    def save_to_json(self):
        print("in buildings save to json")
        return {"name": str(self.__class__.__name__), "data": {}}


class Mine(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        coin_image = pygame.image.load("Resources/goldcoin1.png")
        self.image.blit(coin_image, (-17, -20))


class Unit(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "unit"
        self.max_stamina = None
        self.stamina = None
        self.price = None
        self.view_range = 4
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

    def __repr__(self):
        return f"{self.__class__}, {self.player_id}, {self.hp}"

    def draw_shape(self):
        pass

    def draw(self):
        self.draw_shape()
        self.health_bar = Health_bar(0, 0, self.width, self.height / 4, self.hp)
        self.health_bar.draw(self.image, self.hp)

    def strike(self):
        self.stamina = 0
        return self.attack * (random.random() / 2 + 0.75)

    def defend(self):
        return self.attack * (random.random() / 2 + 0.25)

    def update_hp(self, ):
        if self.hp > 0:
            self.health_bar.draw(self.image, self.hp)


class TriangularUnit(MilitaryUnit):

    def __init__(self, grid_pos, player_id, color=(255, 0, 0)):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.price = 30
        self.hp = 3
        self.name = "triangular unit"
        self.attack = 3
        self.max_stamina = 1
        self.stamina = 1
        self.draw()

    def draw_shape(self):
        pygame.draw.polygon(self.image, self.color, [(0, self.height / 4 + 2), (self.width / 2, self.height),
                                                     (self.width - 1, self.height / 4 + 2)])

    def __repr__(self):
        return f" unit {self.__class__} on hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


class SquareUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id, color):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.name = "square unit"
        self.price = 30
        self.attack = 2
        self.hp = 3
        self.max_stamina = 2
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
        self.max_stamina = 0
        self.stamina = 0

        self.attack = 0
        self.hp = 10
        self.draw()

    def draw_shape(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, self.height / 4 + 2, self.width,
                                                 self.height - self.height / 4 + 2))

    def __repr__(self):
        return f"{self.name} on hex {self.grid_pos[0]}, {self.grid_pos[1]}, player {self.player_id}"


class CircleUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id, color):
        self.color = color
        super().__init__(grid_pos, player_id, )
        self.name = "circle unit"
        self.price = 30
        self.attack = 1
        self.hp = 3
        self.max_stamina = 3
        self.stamina = 3
        self.draw()

    def draw_shape(self):
        pygame.draw.circle(self.image, self.color, (self.width / 2, self.height / 2), 10)
    #
    # def __repr__(self):
    #     return f"CircleUnit o hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


class Town(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        type = "town"
        town_image = pygame.image.load("Resources/town.png")
        self.image.blit(town_image, (0, 0))


class Village(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        type = "village"
        village_image = pygame.image.load("Resources/village.png")
        self.image.blit(village_image, (0, 0))
