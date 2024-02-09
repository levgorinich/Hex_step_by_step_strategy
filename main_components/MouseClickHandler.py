import pygame


class MouseClickHandler:
    def __init__(self,game_map,  User_interface, tracker, mover):
        self.user_interface = User_interface
        self.game_map = game_map
        self.tracker = tracker
        self.mover = mover
        self.selected_sprite = None
        self.sprite_clicked = None
        self.unit_selected = None

        self.was_clicked = False
        self.hexes_available_move_selected_unit = []


    def handle_click(self, event):
        mouse_pos = event.dict["pos"]
        self.was_clicked =False
        self.check_UI_click(mouse_pos)

        # need to decide what ot do if I click with the right button on a ui, i can move unit behind ui
        if not self.was_clicked:
            self.check_hex_click(event)
    def check_UI_click(self, mouse_pos: tuple[int, int]):
        result = self.user_interface.check_click(mouse_pos)
        if result:
            self.was_clicked = True
            print("UI was clicked")

        else:
            self.was_clicked = False

    def check_hex_click(self, event):

        self.clear_selected_hexes()
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse -= self.tracker.get_dragging_offset()

        if event.button == 1:
            print("got ivent from mouse")

            if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
                print("Sprite was selected")
                self.selected_sprite = selected_sprite_clicked
                hex_selected = self.user_interface.button_list.selected_element
                self.game_map.change_hex(hex_selected, self.selected_sprite.grid_pos)

                print("this is printing object in hexes", self.game_map.hexes[self.selected_sprite.grid_pos])


        if event.button == 3:

            self.sprite_clicked = self.check_if_hex_is_clicked(event)
            if self.check_if_hex_is_clicked(event) and self.unit_selected :
                starting_sprite = self.selected_sprite.grid_pos
                ending_sprite = self.sprite_clicked.grid_pos

                available_pos= self.game_map.reachable_hexes(
                        self.selected_sprite.grid_pos, self.unit_selected.stamina)

                if ending_sprite in available_pos and self.player.moves > 0:
                    self.mover.move(starting_sprite, ending_sprite)
                    self.game_map.actions.append("<move"+str(starting_sprite)+ ","+str(ending_sprite)+">")
                    self.player.moves -= 1
                    self.unit_selected = None

        self.draw_selected_hexes()


    def clear_selected_hexes(self):

        for pos in self.hexes_available_move_selected_unit:
            cell_hex = self.game_map.get_hex_by_coord(pos)
            if cell_hex:
                cell_hex.draw()
        self.hexes_available_move_selected_unit = []
    def draw_selected_hexes(self):

        for pos in self.hexes_available_move_selected_unit:
            cell_hex = self.game_map.get_hex_by_coord(pos)
            if cell_hex:
                cell_hex.draw_in_unit_range()
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


                    return sprite
        return None
