import pygame
from Buttons import *

class UI:
    def __init__(self, window_size, game_map):
        self.UI_surface = pygame.Surface(window_size, pygame.SRCALPHA)
        self.game_map = game_map
        self.buttons = self.add_buttons("Square")
        self.display_buttons(self.UI_surface)


    def add_buttons(self, text):
        buttons = []
        titles = ["Triangular","Square","Circle"]
        display_size = pygame.display.get_surface().get_size()
        for i in range(len(titles)):
            button = ButtonForUnitSpawner(titles[i], display_size[0]-100, display_size[1]-100-100*i, 100, 100,)
            buttons.append(button)
        return buttons

    def display_buttons(self, surface):
        for button in self.buttons:
            button.draw(self.UI_surface)
            button.check_click(self.game_map)

    def fill_UI_surface(self):
        self.display_buttons(self.UI_surface)

    def check_click(self, game_map):
        for button in self.buttons:
            if button.check_click(game_map):
                return True
        return False


