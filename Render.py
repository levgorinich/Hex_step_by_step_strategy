
import pygame
from Buttons import Button
class Render:
    def __init__(self,internal_surface_size, map_movement_tracker, user_interface):
        self.map_movement_tracker = map_movement_tracker
        self.user_interface = user_interface
        self.internal_surface = pygame.Surface(internal_surface_size,pygame.SRCALPHA)
        self.display_surface = pygame.display.get_surface()
        self.internal_surface_rect = self.internal_surface.get_rect(center = (self.display_surface.get_size()[0]//2, self.display_surface.get_size()[1]//2))



    def display_objects(self,sprite_group: pygame.sprite.Group)->None:
        offset = self.map_movement_tracker.get_total_offset()

        for sprite in sprite_group.sprites():
            self.internal_surface.blit(sprite.image, offset + sprite.rect.topleft)
    def display_units(self,sprite_group: pygame.sprite.Group, hexes):
        offset = self.map_movement_tracker.get_total_offset()

        for sprite in sprite_group.sprites():
            unit_hex = hexes[sprite.grid_pos]
            # print(unit_hex, unit_hex.map_coord)
            unit_center=  (unit_hex.map_coord[0]-sprite.width//2, unit_hex.map_coord[1]-sprite.height//2)
            # print(unit_center)
            self.internal_surface.blit(sprite.image, offset + unit_center)
    def pre_display(self, events_list):

        self.internal_surface.fill((0, 0, 0, 0))

        self.map_movement_tracker.screen_movement_with_mouse_dragging(events_list)
        self.display_surface.fill('#71deee')


    def display(self, events_list, game_map):

        self.pre_display(events_list)
        self.display_objects(game_map.hexes)
        self.display_units(game_map.units, game_map.hexes.hexes_dict)

        scaled_surface = pygame.transform.scale(self.internal_surface, self.map_movement_tracker.get_internal_surface_scale())
        scaled_rect = scaled_surface.get_rect(center = self.internal_surface_rect.center)
        # print(scaled_rect, "size")
        self.display_surface.blit(scaled_surface,(scaled_rect[0],scaled_rect[1]))
        self.display_surface.blit(self.user_interface.UI_surface, (0,0))


