import pygame


class TextInputHandler:
    def __init__(self, user_interface):
        self.active_element = None
        self.user_interface = user_interface

    def update(self, element):
        self.active_element = element

    def remove_active_element(self):
        self.active_element = None

    def handle_input(self, event):
        if self.active_element:
            if event.type == pygame.TEXTINPUT:
                self.active_element.text += event.text
                print(self.active_element.text, "new text")
                self.user_interface.draw_elements()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.active_element.text = self.active_element.text[:-1]
                    self.user_interface.draw_elements()