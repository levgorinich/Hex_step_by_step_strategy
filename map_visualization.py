import sys

import pygame
from pygame.locals import *
from math import *

pygame.init()
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
# pygame.event.set_grab(True)
pygame.display.set_caption("Drawing Polygons on a Sprite")
clock = pygame.time.Clock()

# diagonal size of hexagon = 2a , where a is the radius of hexagon, or it's side length
hex_width = 30* sqrt(3)
hex_height = hex_width*sqrt(3)/2


class Hexagon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, coord_x, coord_y, color = (70,70,120), width = hex_width, height =hex_height ):
        super().__init__()
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
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

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()


        self.offset = pygame.math.Vector2(0,0)
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'left':10, 'right':10, 'top':10, 'bottom':10}
        l = self.camera_borders['left']
        r = self.camera_borders['top']
        w = self.display_surface.get_size()[0] -(self.camera_borders['right'] + self.camera_borders['left'])
        h = self.display_surface.get_size()[1] -(self.camera_borders['bottom'] + self.camera_borders['top'])
        self.camera_rect = pygame.Rect(l, r, w, h)

        self.mouse_speed= 0.4

        # camera control
        self.mouse_pos_down = pygame.math.Vector2(0,0)
        self.drag_flag = False

        # zoom
        self.zoom_scale = 1
        self.internal_surface_size= (2500, 2500)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_width, self.half_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2(0,0)
        self.internal_offset.x = self.internal_surface_size[0]//2 - self.half_width
        self.internal_offset.y = self.internal_surface_size[1]//2 - self.half_height



    def mouse_zoom(self):
        pass
    def drag_mouse_control(self, events_list):
        # mouse_pos_down = (0,0)
        for event in events_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos_down = pygame.math.Vector2(pygame.mouse.get_pos())
                self.drag_flag = True
                print("mouse pos down", self.mouse_pos_down)

            if self.drag_flag:
                mouse_pos_up = pygame.math.Vector2(pygame.mouse.get_pos())
                print("after up", mouse_pos_up, self.mouse_pos_down)
                distance_draged = mouse_pos_up.distance_to(self.mouse_pos_down)
                if mouse_pos_up.distance_to(self.mouse_pos_down) > 5:
                    print(mouse_pos_up - self.mouse_pos_down)
                    self.offset+= (mouse_pos_up - self.mouse_pos_down) * self.mouse_speed
                if event.type == pygame.MOUSEBUTTONUP:
                    self.drag_flag = False
                self.mouse_pos_down = mouse_pos_up

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2(0,0)

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border, mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x =  mouse.x - right_border
                pygame.mouse.set_pos((right_border, mouse.y))

        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
                print(mouse_offset_vector)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))


        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x, top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y =  mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x, bottom_border))

        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))
        self.offset -= mouse_offset_vector *self.mouse_speed
    def custom_draw(self, screen, events_list):
        # self.mouse_control()
        self.drag_mouse_control(events_list)

        self.internal_surface.fill('#71deee')
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft + self.offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_pos)

        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(center = self.internal_rect.center)
        pygame.draw.rect(self.display_surface, 'yellow', self.camera_rect, 5)

        self.display_surface.blit(scaled_surface,scaled_rect)





def generate_map(cols, rows):
    """generating hexagon grid with given number of columns and rows"""

    hexes = CameraGroup()
    coord_x = coord_y = 0
    current_x = hex_width/2
    current_y = hex_height/2

    for col in range(cols):
        # each uneven column is moved down by hex_width/2
        if col %2 ==1:
            current_y+= hex_height/2
        for row in range(rows):
            coord_x = row+col//2+col%2
            coord_y = col

            hex = Hexagon(current_x,current_y, coord_x,coord_y)
            current_y += hex_height
            hexes.add(hex)
        current_x += hex_width*3/4
        current_y= hex_height/2
    return hexes

# Create the polygon sprite object
hexes = generate_map(35,35)







running = True
while running:
    events_list = pygame.event.get()
    for event in events_list:
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x, mouse_y)
            for sprite in hexes:
                # if it is a collision with a rectangle we will check if we have a collision with a mask
                if sprite.rect.collidepoint(mouse_x, mouse_y):
                    print("rectangle clicked")
                    local_x = mouse_x - sprite.rect.x
                    local_y = mouse_y - sprite.rect.y
                    if sprite.mask.get_at((local_x, local_y)):
                        print("Position x ", sprite.coord_x, "position y ", sprite.coord_y)
                        break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEWHEEL:
            hexes.zoom_scale += event.y * 0.03


    hexes.update()

    screen.fill((255, 255, 255))
    hexes.custom_draw(screen, events_list)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()