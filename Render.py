
import pygame
from some_russian_gay_m.mapMovement import MapMovementTracker
class Render:
    def __init__(self,map_movement_tracker, internal_surface):
        self.map_movement_tracker = MapMovementTracker
        self.internal_surface = internal_surface
        self.internal_surface_rect = internal_surface.get_rect()
        self.display_surface = pygame.display.get_surface()

    def display_objects(self,sprite_group):
        offset = self.map_movement_tracker.get_offset(self)
        for sprite in sprite_group.sprites():
            self.internal_surface.blit(sprite.image, offset + sprite.rect.topleft)

    def display(self, events_list):
        self.map_movement_tracker.screen_movement_with_mouse_dragging(events_list)

        scaled_surface = pygame.transform.scale(self.internal_surface, self.map_movement_tracker.get_internal_surface_scale())

        scaled_rect = scaled_surface.get_rect(center = self.internal_surface_rect.center)


        self.display_surface.blit(scaled_surface,scaled_rect)

