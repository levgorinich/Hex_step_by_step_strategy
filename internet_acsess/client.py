import pygame
from network import Network


win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("client")

clientNumber = 0

class Player():
    def __init__(self, x,y,width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.speed = 0.5
    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        self.rect = (self.x, self.y, self.width, self.height)

def read_pos(string):
    stritng = string.split(",")
    return int(stritng[0]), int(stritng[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def redraw(win, player):
    win.fill ((255, 255, 255))
    player.draw()
    pygame.display.update()



def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())

    p = Player(startPos[0],startPos[1],100,100,(255,0,0))
    p2 = Player(0,0,100,100,(0,0,255))
    while run:

        p2Pos = read_pos(n.send(make_pos((p.x,p.y))))
        p2.x = p2Pos[0]
        p2.y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
        p.move()
        redraw(win, p)

main()