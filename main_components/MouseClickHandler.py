import pygame


class MouseClickHandler:
    def __init__(self,game_map,  User_interface, tracker, mover):
        self.user_interface = User_interface
        self.game_map = game_map
        self.selected_sprite = None
        self.sprite_clicked = None
        self.unit_selected = None
        self.tracker = tracker
        self.was_clicked = False
        self.mover = mover
        self.pos = []
        self.clear = None
        self.check_on_activate = 0
        # self.mover = Mover(self.game_map)
        self.actions  = set()
        self.player = User_interface.player
        pass


    def handle_click(self, event):

        self.was_clicked =False
        self.check_UI_click()

        # need to decide what ot do if I click with the right button on a ui, i can move unit behind ui
        if not self.was_clicked:
            self.check_hex_click(event)
    def check_UI_click(self):
        result = self.user_interface.check_click(self.game_map)
        if result:
            self.was_clicked = True

        else:
            self.was_clicked = False

    def check_hex_click(self, event):

        mouse = pygame.math.Vector2(pygame.mouse.get_pos())

        mouse -= self.tracker.get_dragging_offset()
        if event.button == 1:
            self.pos = []
            if selected_sprite_clicked := self.check_if_hex_is_clicked(event):
                self.selected_sprite = selected_sprite_clicked

                if self.selected_sprite.unit_on_hex:


                    print("check", self.selected_sprite.unit_on_hex.player_id == self.game_map.player_id)
                    if self.selected_sprite.unit_on_hex and self.selected_sprite.unit_on_hex.player_id == self.game_map.player_id:
                        self.unit_selected = self.selected_sprite.unit_on_hex
                        print("got inside ")
                        if self.selected_sprite.grid_pos[0]%2 == 0:
                            offset = 1
                        else:
                            offset = -1

                        # set the mobility
                        # col,row = self.unit_selected.range_of_2(self.selected_sprite.grid_pos,offset)
                        available_pos = self.unit_selected.hex_reachable(self.selected_sprite.grid_pos,self.game_map.empty_hexes,
                                                                         self.game_map.rows,self.game_map.columns)
                        for i in range(len(available_pos)):
                                self.pos.append(available_pos[i])
                        self.clear = True
                        self.check_on_activate+=1

        if event.button == 3:
            self.check_on_activate = 0


            self.sprite_clicked = self.check_if_hex_is_clicked(event)
            if self.check_if_hex_is_clicked(event) and self.unit_selected :
                self.clear = None
                # self.pos = []
                starting_sprite = self.selected_sprite.grid_pos
                ending_sprite = self.sprite_clicked.grid_pos

                diff = (ending_sprite[0]-starting_sprite[0],ending_sprite[1]-starting_sprite[1])

                # #check on even or odd
                if starting_sprite[0]%2 == 0:
                    offset = 1
                else:
                    offset = -1
                
                # # set the mobility
                available_pos= self.unit_selected.hex_reachable(self.selected_sprite.grid_pos,self.game_map.empty_hexes,
                                                                         self.game_map.rows,self.game_map.columns)
                # if self.unit_selected.range_of_movement(diff,offset):
                if ending_sprite in available_pos and self.player.moves > 0:
                    self.mover.move(starting_sprite, ending_sprite)
                    self.player.moves -= 1
                    if self.player.moves == 0:
                        print("end turn")


                    self.game_map.actions.add("<move"+str(starting_sprite)+ ","+str(ending_sprite)+">")

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
