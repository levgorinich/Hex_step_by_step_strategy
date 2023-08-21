
import pygame
from some_russian_gay_m.mapMovement import MapMovementTracker
class Render:
    def __init__(self,map_movement_tracker, internal_surface):
        self.map_movement_tracker = map_movement_tracker
        self.internal_surface = pygame.Surface((2500, 2500),pygame.SRCALPHA)
        self.display_surface = pygame.display.get_surface()
        self.internal_surface_rect = self.internal_surface.get_rect(center = (self.display_surface.get_size()[0]//2, self.display_surface.get_size()[1]//2))


    def display_objects(self,sprite_group):
        offset = self.map_movement_tracker.get_total_offset()
        for sprite in sprite_group.sprites():
            self.internal_surface.blit(sprite.image, offset + sprite.rect.topleft)
    def display_units(self,sprite_group, hexes):
        offset = self.map_movement_tracker.get_total_offset()

        for sprite in sprite_group.sprites():
            unit_hex = hexes[sprite.grid_pos_x, sprite.grid_pos_y]
            unit_center=  (unit_hex.map_coord_x-sprite.width//2, unit_hex.map_coord_y-sprite.height//2)
            self.internal_surface.blit(sprite.image, offset + unit_center)
    def pre_display(self, events_list):

        self.internal_surface.fill((0, 0, 0, 0))

        self.map_movement_tracker.screen_movement_with_mouse_dragging(events_list)

        offset = self.map_movement_tracker.get_total_offset()
        self.display_surface.fill('#71deee')
    def display(self):

        scaled_surface = pygame.transform.scale(self.internal_surface, self.map_movement_tracker.get_internal_surface_scale())
        scaled_rect = scaled_surface.get_rect(center = self.internal_surface_rect.center)
        self.display_surface.blit(scaled_surface,scaled_rect)


