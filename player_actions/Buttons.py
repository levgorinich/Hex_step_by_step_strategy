from typing import NoReturn
from abc import ABC, abstractmethod
import pygame, sys

from main_components.Map import Map


def empty_funciton():
    print("")

class Button:
    def __init__(self, text, x, y, width, height, action = empty_funciton, color=(0, 255, 0), font_size=24, font_name="Arial",):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        font = pygame.font.SysFont(font_name, font_size)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        # self.is_clickable = False

    # def reset_clickability(self):
    #     self.is_clickable = True

    def draw(self, display_surface: pygame.Surface) -> None:
        pygame.draw.rect(display_surface, self.color, self.rect)
        pygame.draw.rect(display_surface, "Black", self.rect, 2)
        display_surface.blit(self.text_surf, self.text_rect)

    @abstractmethod
    def check_click(self,) -> bool:
        pass


class MenuButton(Button):
    def __init__(self, text, x, y, width, height,action = empty_funciton,action_args= (), color=(0, 255, 0), font_size=24, font_name="Arial",  ):

        super().__init__(text, x, y, width, height, action, color, font_size, font_name)
        self.action = action
        self.action_args = action_args

    def check_click(self,) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]-offset_x,mouse_pos[1])
        # print(mouse_pos)
        # print(self.rect)
        if  self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # self.is_clickable = False
                self.action(*self.action_args)
                return True
        return False



class ButtonList():
    def __init__(self, offset_x, y_pos = 10):
        self.surf = pygame.Surface((200,300), pygame.SRCALPHA)
        self.surf.fill((255, 255,0))
        self.elements_count = 0
        self.x_pos =x_pos
        self.y_pos = y_pos
        self.button_width = 180
        self.button_height = 35
        self.elements = {}
        self.selected_element = None
        self.offset_x = offset_x





    def add_element(self,button_text,element_to_choose):
        self.y_pos += 40


        game_button = MenuButton(button_text, self.x_pos, self.y_pos, self.button_width, self.button_height)
        game_button.draw(self.surf)
        self.elements[game_button] = element_to_choose
        self.elements_count += 1

    def check_selection(self):

        for element in self.elements:


            if element.check_click(self.offset_x):
                self.selected_element = self.elements[element]





