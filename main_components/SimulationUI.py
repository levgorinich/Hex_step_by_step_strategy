import pygame

from player_actions.UI_Elements import MenuButton


class SimUI:
    def __init__(self, window_size, game_map, spawner):
        self.window_size = window_size
        self.UI_surface = None
        self.game_map = game_map
        self.spawner = spawner
        self.lvl_1_elements = []
        self.lvl_2_elements = []
        self.button_lists = {}
        self.init_elements()
        self.draw_elements()

    def start_simulation(self):
        print("Start Simulation")
    def init_elements(self):
        self.add_buttons()

    def draw_elements(self):
        self.UI_surface = pygame.Surface(self.window_size, pygame.SRCALPHA)
        for element in self.lvl_1_elements:
            if element.visible:
                element.draw(self.UI_surface)
        for element in self.lvl_2_elements:
            if element.visible:
                element.draw(self.UI_surface)


    def add_buttons(self,):

        display_size = pygame.display.get_surface().get_size()
        button_size = (100, 100)

        start_simlation= MenuButton("Start Simulation", display_size[0]-100, display_size[1]-100-100*4,
                                  button_dimensions=button_size, action=self.start_simulation(),color=(255, 0, 0),
                                  font_size=24, font_name="Arial")

        self.lvl_1_elements.append(start_simlation)
