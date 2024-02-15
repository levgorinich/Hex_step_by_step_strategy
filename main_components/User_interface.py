import pygame

from player_actions.Buttons import MenuButton, ButtonList


class UI:
    def __init__(self, window_size, game_map, spawner):
        self.UI_surface = pygame.Surface(window_size, pygame.SRCALPHA)
        self.game_map = game_map
        self.spawner = spawner
        print(self.spawner)
        self.buttons = self.add_buttons()
        self.button_list = self.add_button_list()
        self.editor_mods_list =  self.add_editor_mods_list()
        self.UI_surface.blit(self.editor_mods_list.upper_surf, (0, 0))
        self.UI_surface.blit(self.button_list.upper_surf, (200, 200))
        self.display_buttons()


    def draw_coins(self):
        pass
    def spawn_function(self, spawner,type,coords):
        pass
    def end_turn(self, ):
        pass
    def save_game(self):
        self.game_map.save_to_json("json_save")

    def add_button_list(self):
        button_list = ButtonList(offset=(200,200))
        hexes_types = ["Hexagon_land", "Hexagon_mountain", "Hexagon_sea", "Hexagon_empty"]
        [button_list.add_element(hex_type, hex_type) for hex_type in hexes_types]
        return button_list

    def add_editor_mods_list(self):
        button_list = ButtonList(offset=(0,0))
        modes = ["Hexes", "Rivers", "Roads"]
        [button_list.add_element(mode, mode) for mode in modes]
        return button_list

    def add_buttons(self,):
        buttons = []
        titles = ["Triangular","Square","Circle"]
        display_size = pygame.display.get_surface().get_size()
        button_size = (100, 100)
        for i in range(len(titles)):
            button = MenuButton(titles[i], display_size[0]-100, display_size[1]-100-100*i, button_size,
                                           action=self.spawn_function, action_args =(self.spawner, titles[i],self.game_map.spawn_point))
            buttons.append(button)
        finish_move = MenuButton("Finish Move", display_size[0]-100, display_size[1]-100-100*len(titles),
                                 button_dimensions=button_size, action=self.end_turn,color=(255, 0, 0),
                                 font_size=24, font_name="Arial")

        load_to_json = MenuButton("Save Game", display_size[0]-100, display_size[1]-100-100*4,
                                 button_dimensions=button_size, action=self.save_game,color=(255, 0, 0),
                                 font_size=24, font_name="Arial")
        buttons.append(finish_move)
        buttons.append(load_to_json)
        return buttons

    def display_buttons(self,):
        for button in self.buttons:
            button.draw(self.UI_surface)




    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        for button in self.buttons:
            if button.check_click(mouse_pos):
                return True
            if self.button_list.check_click(mouse_pos):
                return True
            if self.editor_mods_list.check_click(mouse_pos):
                return True
        return False


