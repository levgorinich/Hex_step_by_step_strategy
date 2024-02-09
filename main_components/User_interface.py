import pygame

from player_actions.Buttons import MenuButton


class UI:
    def __init__(self, window_size, game_map, spawner):
        self.UI_surface = pygame.Surface(window_size, pygame.SRCALPHA)
        self.game_map = game_map
        self.spawner = spawner
        print(self.spawner)
        self.buttons = self.add_buttons("Square")
        self.display_buttons(self.UI_surface)


    def draw_coins(self):
        pass
    def spawn_function(self, spawner,type,coords):
        pass
    def end_turn(self, ):
        pass
    def save_game(self):
        self.game_map.save_to_json("json_save")

    def add_buttons(self, text):
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

    def display_buttons(self, surface):
        for button in self.buttons:
            button.draw(self.UI_surface)


    def fill_UI_surface(self):
        self.display_buttons(self.UI_surface)

    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        for button in self.buttons:
            if button.check_click(mouse_pos):
                return True
        return False


