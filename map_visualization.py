import pygame
from pygame.locals import *
from math import *

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Drawing Polygons on a Sprite")
clock = pygame.time.Clock()

class Hexagon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color = (70,70,120), width = 70, height = 70):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a blank surface with transparency
        # pygame.draw.polygon(self.image, color, vertices)

        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.rect.x = pos_x
        self.rect.y = pos_y
        # self.rect.center = (pos_x, pos_y)
        self.points = []
        self.image.fill((0, 0, 0, 0))
        v = 0
        for i in range(6):
            self.points.append((cos(v)*((self.rect.width//2)-2)+ self.rect.width/2,
                                sin(v)*((self.rect.height//2)-2)+ self.rect.height/2))
            v += (pi*2)/6
        pygame.draw.polygon( self.image, (30,70,50),self.points )

        print(self.points)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

        # Define the color and vertices for the polygon
polygon_color = (255, 0, 0)  # Red color (R=255, G=0, B=0)
polygon_vertices = [(0, 0), (50, 100), (100, 0)]  # Triangle vertices

# Define the initial position of the sprite
sprite_position = (200, 200)

# Create the polygon sprite object
hex = Hexagon(50,50,)

# Create a sprite group
hexes = pygame.sprite.Group()
hexes.add(hex)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x, mouse_y)

            for sprite in hexes:
                if sprite.rect.collidepoint(mouse_x, mouse_y):
                    local_x = mouse_x - sprite.rect.x
                    local_y = mouse_y - sprite.rect.y
                    if sprite.mask.get_at((local_x, local_y)):
                        print("Clicked")

    hexes.update()

    screen.fill((255, 255, 255))
    hexes.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()