import pygame
from pygame.locals import *

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Drawing Polygons on a Sprite")
clock = pygame.time.Clock()

class PolygonSprite(pygame.sprite.Sprite):
    def __init__(self, color, vertices, initial_position):
        super().__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)  # Create a blank surface with transparency
        pygame.draw.polygon(self.image, color, vertices)
        self.rect = self.image.get_rect(topleft=initial_position)
        # self.image.fill((0, 0, 0, 0))
        # pygame.draw.polygon(self.image, color, self.vertices)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

        # Define the color and vertices for the polygon
polygon_color = (255, 0, 0)  # Red color (R=255, G=0, B=0)
polygon_vertices = [(0, 0), (50, 100), (100, 0)]  # Triangle vertices

# Define the initial position of the sprite
sprite_position = (200, 200)

# Create the polygon sprite object
polygon_sprite = PolygonSprite(polygon_color, polygon_vertices, sprite_position)

# Create a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(polygon_sprite)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for sprite in all_sprites:
                if sprite.rect.collidepoint(mouse_x, mouse_y):
                    local_x = mouse_x - sprite.rect.x
                    local_y = mouse_y - sprite.rect.y
                    if sprite.mask.get_at((local_x, local_y)):
                        print("Clicked")

    all_sprites.update()

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()