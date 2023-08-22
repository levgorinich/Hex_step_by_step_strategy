import pygame

class MouseClickHandler:
    def __init__(self, game_map, tracker):
        self.game_map = game_map
        self.selected_sprite = None
        self.unit_selected = None
        self.tracker = tracker
        pass

    def handle_click(self, event):

        mouse = pygame.math.Vector2(pygame.mouse.get_pos())

        mouse -= self.tracker.get_dragging_offset()
        if event.button == 1:
            sprite_clicked = self.check_if_hex_is_clicked(event)
            if sprite_clicked:
                self.selected_sprite = sprite_clicked
                if self.selected_sprite.unit_on_hex:
                    self.unit_selected = self.selected_sprite.unit_on_hex

        if event.button == 3:
            sprite_clicked = self.check_if_hex_is_clicked(event)
            if sprite_clicked and self.unit_selected :
                self.selected_sprite.remove_unit()
                self.unit_selected = None
                sprite_clicked.add_unit(self.unit_selected)


    def check_if_hex_is_clicked(self, event):
        mouse = pygame.math.Vector2(event.pos)

        mouse -= self.tracker.get_dragging_offset()
        for sprite in self.game_map.hexes:

                if sprite.rect.collidepoint(mouse.x, mouse.y):
                    local_x = mouse.x - sprite.rect.x
                    local_y = mouse.y - sprite.rect.y
                    if sprite.mask.get_at((local_x, local_y)):
                        print(sprite)

                        return sprite
        return None


