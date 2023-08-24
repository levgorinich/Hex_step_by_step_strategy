import pygame

class MouseClickHandler:
    def __init__(self, game_map, User_interface, tracker):
        self.user_interface = User_interface
        self.game_map = game_map
        self.selected_sprite = None
        self.unit_selected = None
        self.tracker = tracker
        self.was_clicked = False
        pass



    def handle_click(self, event):


        self.was_clicked =False
        self.check_UI_click()

        # need to decide what ot do if I click with the right button on a ui, i can move unit behind ui
        if not self.was_clicked:
            self.check_hex_click(event)
    def check_UI_click(self):
        self.was_clicked = self.user_interface.check_click(self.game_map)

    def check_hex_click(self, event):

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
                if sprite_clicked.unit_on_hex:


                    atacking_unit = self.unit_selected.race
                    defending_unit = sprite_clicked.unit_on_hex.race

                    match(defending_unit - atacking_unit):
                        case 1|-2:
                            sprite_clicked.kill_unit()
                            self.unit_selected.grid_pos_x = sprite_clicked.grid_pos_x
                            self.unit_selected.grid_pos_y = sprite_clicked.grid_pos_y

                            sprite_clicked.add_unit(self.unit_selected)
                            self.unit_selected = None
                            print(self.game_map.units)
                        case _:
                            pass
                else:
                    print("no unit")
                    self.selected_sprite.remove_unit()

                    self.unit_selected.grid_pos_x = sprite_clicked.grid_pos_x
                    self.unit_selected.grid_pos_y = sprite_clicked.grid_pos_y

                    sprite_clicked.add_unit(self.unit_selected)
                    self.unit_selected = None



    def check_if_hex_is_clicked(self, event):
        mouse = pygame.math.Vector2(event.pos)

        zoom=self.tracker.get_zoom()
        mouse *= 1 / zoom


        mouse += self.tracker.get_internal_offset()
        mouse = pygame.math.Vector2(int(mouse.x), int(mouse.y))
        print(mouse, "real  mouse pos")

        for sprite in self.game_map.hexes:
            offset = self.tracker.get_total_offset()
            new_rec = pygame.Rect(offset.x + sprite.rect.x, offset.y + sprite.rect.y, sprite.rect.width, sprite.rect.height)
            if new_rec.collidepoint(mouse.x, mouse.y):
                local_x = int(mouse.x) - new_rec.x
                local_y = int(mouse.y) - new_rec.y

                if sprite.mask.get_at((local_x, local_y)):
                    print(sprite)

                    return sprite
        return None



