from typing import NoReturn
from abc import ABC, abstractmethod
import pygame, sys

from main_components.Map import Map


def empty_funciton():
    print("")

class Button:
    def __init__(self, text, x, y, width, height,x_offset = 0, y_offset = 0, action = empty_funciton, color=(0, 255, 0), font_size=24, font_name="Arial",):
        self.rect = pygame.Rect(x, y, width, height)
        print(x, x_offset)
        self.abs_x = x + x_offset
        self.abs_y = y + y_offset
        self.absolute_rect = pygame.Rect(self.abs_x, self.abs_y, width, height)
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
    def __init__(self, text, x, y, width, height,x_offset =0, y_offset = 0, action = empty_funciton,action_args= (), color=(0, 255, 0), font_size=24, font_name="Arial",  ):
        print(x_offset)
        super().__init__(text, x, y, width, height,x_offset=x_offset, y_offset= y_offset, action= action, color=color, font_size = font_size, font_name = font_name)
        self.action = action
        self.action_args = action_args

    def check_click(self,) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        # mouse_pos = (mouse_pos[0],mouse_pos[1])
        # print(mouse_pos)
        # print(self.rect)
        if  self.absolute_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # self.is_clickable = False
                self.action(*self.action_args)
                return True
        return False



class ButtonList():
    def __init__(self,x_offset = 0, y_offset = 0):
        self.surf = pygame.Surface((200,300), pygame.SRCALPHA)
        self.surf.fill((255, 255,0))
        self.elements_count = 0
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.x_pos = 10
        self.y_pos = 10
        self.button_width = 180
        self.button_height = 35
        self.elements = {}
        self.selected_element = None
        # self.offset_x = offset_x





    def add_element(self,button_text,element_to_choose):

        self.y_pos += 40
        game_button = MenuButton(button_text, self.x_pos, self.y_pos, self.button_width, self.button_height, x_offset=self.x_offset, y_offset=self.y_offset,)
        game_button.draw(self.surf)
        self.elements[game_button] = element_to_choose
        self.elements_count += 1

    def check_selection(self):

        for element in self.elements:
            if element.check_click():
                self.selected_element = self.elements[element]





