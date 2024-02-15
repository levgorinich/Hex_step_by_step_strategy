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
    def __init__(self, grid_pos, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos)
        self.grid_pos = grid_pos
        self.color = color

        self.width = width
        self.height = height
        self.type = "hexagon"
        self.points = self.calculate_points_for_hexagon()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(self.map_coords[0], self.map_coords[1]))
        pygame.draw.polygon(self.image, self.color, self.points)
        self.image.set_at(list(map(int,self.points[0])), (225,0,0))
        self.mask = pygame.mask.from_surface(self.image)

        self.rivers = [False,False,False,False,False,False]

        self.unit_on_hex = None
        self.building_on_hex = None

    def save_to_json(self):
        print("Call buildings save to json ", self.building_on_hex)
        hex_dict = {"type":str(self.__class__.__name__)}

        if self.building_on_hex:
            print("in building on hex ")
            hex_dict["building_on_hex"] = self.building_on_hex.save_to_json()
        else:
            hex_dict["building_on_hex"] = None

        return str(self.grid_pos) , hex_dict

    def __repr__(self):
        return f"{self.__class__.__name__}, {self.unit_on_hex}, {self.building_on_hex}"
    def calculate_points_for_hexagon(self):
        points = []
        v = 0
        for i in range(6):
            points.append((round(cos(v) * ((self.width // 2) ) + self.width / 2, 2),
                           round(sin(v) * ((self.width // 2) ) + self.width / 2 - (self.width - self.height) / 2, 2)))
            v += (pi * 2) / 6
        print(points, self.grid_pos)
        return points

    def add_unit(self, unit):
        self.unit_on_hex = unit

    def add_building(self, building):
        self.building_on_hex = building

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

        # pygame.draw.circle(self.image, (0, 255, 255), self.points[1], 5)

    def draw_a_river(self, triangle):
        try:
            self.rivers[triangle] = False
        except IndexError as e:
            print("Invalid triangle number")

        pygame.draw.polygon(self.image, (0, 255, 255), self.draw_river(triangle))


    def draw_river(self,triangle_number: int, river_thickness: int = 3, ):

        river_thickness = river_thickness
        another_side = math.sqrt(3)
        point_0_left = (self.points[0][0] - another_side, self.points[0][1] + river_thickness)
        point_0_right = (self.points[0][0] - another_side, self.points[0][1] - river_thickness)
        point_1_left = (self.points[1][0] - river_thickness, self.points[1][1] )
        point_1_right = (self.points[1][0] + another_side, self.points[1][1] - river_thickness)
        point_2_left = (self.points[2][0] - another_side, self.points[2][1] - river_thickness)
        point_2_right= (self.points[2][0] + river_thickness, self.points[2][1] )
        point_3_left = (self.points[3][0] + another_side, self.points[3][1] - river_thickness)
        point_3_right = (self.points[3][0] + another_side, self.points[3][1] + river_thickness)
        point_4_left = (self.points[4][0] + river_thickness, self.points[4][1] )
        point_4_right = (self.points[4][0] - another_side, self.points[4][1] + river_thickness)
        point_5_left = (self.points[5][0] + another_side, self.points[5][1] + river_thickness)
        point_5_right = (self.points[5][0] - river_thickness, self.points[5][1])

        points_for_triangle = {0:[self.points[0], point_0_right, point_1_left, self.points[1]],
                               1:[self.points[1], point_1_right, point_2_left, self.points[2]],
                               2:[self.points[2], point_2_right, point_3_left, self.points[3]],
                               3:[self.points[3], point_3_right, point_4_left, self.points[4]],
                               4:[self.points[4], point_4_right, point_5_left, self.points[5]],
                               5:[self.points[5], point_5_right, point_0_left, self.points[0]]}


        return points_for_triangle[triangle_number]

    def compse_another(self ):
        draw_river = self.draw_river()
        vect1 = (draw_river[1][0] - draw_river[0][0], draw_river[1][1] - draw_river[0][1])
        vect2 = (draw_river[2][0] - draw_river[3][0], draw_river[2][1] - draw_river[3][1])
        vect1_rot = self.rotate_vector_by_an_ange(pi/6, vect1)
        vect2_rot = self.rotate_vector_by_an_ange(pi/6, vect2)
        return [self.points[1], np.array(self.points[1])+np.array(vect1_rot), np.array(self.points[0])+np.array(vect2_rot), self.points[0]]

    def rotate_vector_by_an_ange(self, angle, vector):
        rotation_matrix = numpy.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
        return numpy.dot(rotation_matrix, vector)


    def draw_in_unit_range(self):
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
        self.type = "sea Hexagon"

        self.draw()
class Hexagon_empty(Hexagon):
    def __init__(self, grid_pos, color=(0,0, 0), width=hex_width, height=hex_height):
        super().__init__(grid_pos, color, width=hex_width, height=hex_height)
        self.color = color
        self.type = "empty Hexagon"

        self.draw()



class Building(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.image = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)

    def save_to_json(self):
        print("in buildings save to json")
        return {"name":str(self.__class__.__name__), "data" : {}}

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

    def __repr__(self):
        return f"{self.__class__}, {self.player_id}, {self.hp}"

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
        return f" unit {self.__class__} on hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


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
    #
    # def __repr__(self):
    #     return f"CircleUnit o hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"




class Town(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        type = "town"
        town_image = pygame.image.load("Resources/town.png")
        self.image.blit(town_image, (0,0))

class Village(Building):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        type = "village"
        village_image = pygame.image.load("Resources/village.png")
        self.image.blit(village_image, (0,0))
