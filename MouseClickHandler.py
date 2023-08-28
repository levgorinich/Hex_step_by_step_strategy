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
            if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
                self.selected_sprite = selected_sprite_clicked
                if self.selected_sprite.unit_on_hex:
                    self.unit_selected = self.selected_sprite.unit_on_hex

        if event.button == 3:
            print("am i here")
            sprite_clicked = self.check_if_hex_is_clicked(event)
            if self.check_if_hex_is_clicked(event) and self.unit_selected :

                if defending_unit := sprite_clicked.unit_on_hex:
                    atacking_unit = self.unit_selected

                    if atacking_unit.grid_pos != defending_unit.grid_pos:
                        print("or here")
                        if (defending_unit.health_bar.hp - atacking_unit.attack <= 0
                            and atacking_unit.health_bar.hp - defending_unit.attack <= 0):
                            self.selected_sprite.kill_unit()
                            sprite_clicked.kill_unit()
                            print("double death")
                        elif (defending_unit.health_bar.hp - atacking_unit.attack <= 0
                            and atacking_unit.health_bar.hp - defending_unit.attack > 0):
                            sprite_clicked.kill_unit()
                            print("kill enemy")
                            self.unit_selected.update(defending_unit.attack)

                        if (defending_unit.health_bar.hp - atacking_unit.attack <= 0
                            and atacking_unit.health_bar.hp - defending_unit.attack <= 0):
                            self.selected_sprite.kill_unit()
                            sprite_clicked.kill_unit()
                            print("another kill")
                        elif (defending_unit.health_bar.hp - atacking_unit.attack <= 0
                            and atacking_unit.health_bar.hp - defending_unit.attack > 0):
                            sprite_clicked.kill_unit()
                            self.unit_selected.update(defending_unit.attack)

                            self.unit_selected.grid_pos = sprite_clicked.grid_pos

                            sprite_clicked.add_unit(self.unit_selected)
                            self.unit_selected = None
                            print(self.game_map.units)
                            print("what is this")


                        elif (defending_unit.health_bar.hp - atacking_unit.attack > 0
                            and atacking_unit.health_bar.hp - defending_unit.attack <= 0):
                            defending_unit.update(atacking_unit.attack)
                            self.selected_sprite.kill_unit()
                            print("waw anoter wariant")
                        
                        else:
                            defending_unit.update(atacking_unit.attack)
                            self.unit_selected.update(defending_unit.attack)
                            print("last case")


                    else:
                            pass

                else:
                    # print("no unit")
                    self.selected_sprite.remove_unit()
                    self.unit_selected.grid_pos = sprite_clicked.grid_pos
                    sprite_clicked.add_unit(self.unit_selected)
                    self.unit_selected = None



    def check_if_hex_is_clicked(self, event):
        mouse = pygame.math.Vector2(event.pos)

        zoom=self.tracker.get_zoom()
        mouse *= 1 / zoom


        mouse += self.tracker.get_internal_offset()
        mouse = pygame.math.Vector2(int(mouse.x), int(mouse.y))
        # print(mouse, "real  mouse pos")

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



