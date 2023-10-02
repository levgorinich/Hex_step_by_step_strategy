from math import cos, sin, pi, sqrt
import pygame

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
    ## correct version. [col,row] in this order
    def offset_to_cube_coords_for_moving(self, grid_pos,offset):
    
        q = grid_pos[0]
        r = grid_pos[1] - (grid_pos[0] - offset*(grid_pos[0] & 1)) / 2
        return q, r, -q - r

    

    def qoffset_from_cube(self,q,r,s,offset):
        col = q
        if offset == -1:
            row = -col - s + (col - (col & 1)) / 2 + 1
        else:
            row = -col - s + (col - (col & 1)) / 2 
        return (col, row)

    def calculate_coordinate_by_hex_position(self, hex_position, ):
        map_coord_x = hex_width * (0.5 + 0.75 * hex_position[0])

        if hex_position[0] % 2 == 0:
            map_coord_y = hex_height * (0.5 + hex_position[1])
        else:
            map_coord_y = hex_height * (1 + hex_position[1])

        return map_coord_x, map_coord_y
    


    def oddq_offset_neighbor(self,hex,direction):
        oddq_direction_differences = [
        # even cols 
        [[+1,  0], [+1, -1], [ 0, -1], 
        [-1, -1], [-1,  0], [ 0, +1]],
        # odd cols 
        [[+1, +1], [+1,  0], [ 0, -1], 
        [-1,  0], [-1, +1], [ 0, +1]],
        ]
        
        
        parity = hex[0] & 1
        diff = oddq_direction_differences[parity][direction]
        return (hex[0] + diff[0], hex[1]+ diff[1])





class Hexagon(MapObject):
    def __init__(self, grid_pos, color=(30, 70, 50), width=hex_width, height=hex_height):
        super().__init__(grid_pos)
        self.grid_pos = grid_pos
        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency

        self.rect = self.image.get_rect(center=(self.map_coords[0], self.map_coords[1]))

        # calculating points for hexagon

        pygame.draw.polygon(self.image, self.color, self.calculate_points_for_hexagon())
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

class Hexagon_mountain(Hexagon):
    def __init__(self, grid_pos, color=(255,255, 255), width=hex_width, height=hex_height):
        super().__init__(grid_pos, color, width=hex_width, height=hex_height)

class Hexagon_sea(Hexagon):
    def __init__(self, grid_pos, color=(83,236, 236), width=hex_width, height=hex_height):
        super().__init__(grid_pos, color, width=hex_width, height=hex_height)


class Unit(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "unit"
        self.mobility = None

    def move(self, move_on_hex_grid):
        self.grid_pos += move_on_hex_grid

        self.map_coord = self.calculate_coordinate_by_hex_position(self.grid_pos)


    def hex_reachable(self,start,blocked,x,y):
        visited = set() # set of hexes
        visited.add(start)
        l1,l2 = [],[]
        fringes = [] # array of arrays of hexes
        fringes.append([start])

        for mov in range(1,self.mobility+1):
            
            for hex in fringes[mov-1]:
                fringes.append([])
                for dir in range(0,6):
                    
                    neighbor  = self.oddq_offset_neighbor(hex,dir)
                    
                    if neighbor not in visited and neighbor not in blocked and neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < x and neighbor[1] < y:
                        visited.add(neighbor)
                        fringes[mov].append(neighbor)
                        
        return tuple(visited)
                

    

    def range_of_movement(self,grid_pos, offset):
        q,r,s = self.offset_to_cube_coords_for_moving(grid_pos,offset)
        if -self.mobility <= q and q <= self.mobility:
            if - self.mobility <= r and r <= self.mobility:
                if - self.mobility <= s and s <= self.mobility:
                    if q + r + s == 0: 
                        print(q," ",r," ",s)
                        return 1
                    
    def range_of_drawing(self, start_pos ,offset):
        q_s,r_s,s_s = self.offset_to_cube_coords_for_moving(start_pos,offset)
        q = [i for i in range(-10,11,1)]
        r = [i for i in range(-10,11,1)]
        s = [i for i in range(-10,11,1)]
        col = []
        row = []
        for i in q:
            if -self.mobility <= i and i <= self.mobility:
                for j in r:
                    if - self.mobility <= j and j <= self.mobility:
                        for h in s:
                            if - self.mobility <= h and h <= self.mobility:
                                if i + j + h == 0 and (i != 0 or j != 0 or h != 0): 
                                    co, ro=self.qoffset_from_cube(i+q_s,j+r_s,h+s_s,offset)
                                    if co >= 0 and ro >= 0:
                                        print(co," ",ro," ")
                                        col.append(co)
                                        row.append(int(ro))
                                        print(col,row)
                                    
        return col,row


class MilitaryUnit(Unit):
    def __init__(self, grid_pos, player_id):
        super().__init__(grid_pos)
        self.player_id = player_id

        self.hp = 10
        self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.mobility = 
        self.health_bar = Health_bar(0, 0, self.width, self.height / 4, 3)
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

    def __init__(self, grid_pos, player_id):

        super().__init__(grid_pos, player_id)

        self.name = "triangular unit"
        self.attack = 1
        self.mobility = 1
        # pygame.draw.polygon(self.surf, (255, 0, 0), [(0, 0), (self.width / 2, self.height), (self.width - 1, 0)])
        # self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.health_bar.draw(self.pict)
        pygame.draw.polygon(self.pict, (255, 0, 0), [(0, self.height / 4 + 2), (self.width / 2, self.height),
                                                     (self.width - 1, self.height / 4 + 2)])
        self.surf.blit(self.pict, (0, 0))


    def __repr__(self):
        return f"{self.name} {self.grid_pos[0]}, {self.grid_pos[1]}, {self.player_id}"
    def update(self, hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.polygon(self.pict, (255, 0, 0), [(0, self.height / 4 + 2), (self.width / 2, self.height),
                                                         (self.width - 1, self.height / 4 + 2)])
            self.surf.blit(self.pict, (0, 0))
        return self.health_bar.hp


class SquareUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id):

        super().__init__(grid_pos, player_id)
        self.name = "square unit"
        self.attack = 2
        self.mobility = 2
        pygame.draw.rect(self.surf, (255, 0, 0), (0, 0, self.width, self.height))
        # self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.health_bar = Health_bar.Health_bar(0, 0, self.width, self.height / 4, 3)
        # self.health_bar.draw(self.pict)
        pygame.draw.rect(self.pict, (255, 0, 0), (0, self.height / 4 + 2, self.width,
                                                  self.height - self.height / 4 + 2))
        self.surf.blit(self.pict, (0, 0))

    def __repr__(self):
        return f"{self.name} {self.grid_pos[0]}, {self.grid_pos[1]}, {self.player_id}"
    def update(self, hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.rect(self.pict, (255, 0, 0), (0, self.height / 4 + 2, self.width,
                                                      self.height - self.height / 4 + 2))
            self.surf.blit(self.pict, (0, 0))
        return self.health_bar.hp


class CircleUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id):
        super().__init__(grid_pos, player_id)
        self.name = "circle unit"
        self.attack = 3
        self.mobility = 3
        pygame.draw.circle(self.surf, (255, 0, 0), (self.width / 2, self.height / 2), 10)
        self.image = self.surf
        # self.pict = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.health_bar = Health_bar.Health_bar(0, 0, self.width, self.height / 4, 3)
        # self.health_bar.draw(self.pict)
        pygame.draw.circle(self.surf, (255, 0, 0), (self.width / 2, self.height / 2), 10)
        self.surf.blit(self.pict, (0, 0))

    def __repr__(self):
        return f"CircleUnit {self.grid_pos[0]}, {self.grid_pos[1]}, {self.player_id}"
    def update(self, hp):
        self.health_bar.hp -= hp
        if self.health_bar.hp > 0:
            self.health_bar.draw(self.pict)
            pygame.draw.circle(self.surf, (255, 0, 0), (self.width / 2, self.height / 2), 10)
            self.surf.blit(self.pict, (0, 0))
        return self.health_bar.hp
