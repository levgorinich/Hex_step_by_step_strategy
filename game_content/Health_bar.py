import pygame

class Health_bar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.max_hp = max_hp
    
    def draw(self, surface, hp):
        ratio = hp/self.max_hp
        pygame.draw.rect(surface, "red", (self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface,"green",(self.x,self.y,self.w*ratio,self.h))
    