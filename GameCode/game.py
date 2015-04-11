import pygame, player
from pygame.locals import *

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('HARVEY MUDD HACKATHON')
    pygame.mouse.set_visible(0)

    #Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    playerObj = player.Player()
    bullet = bullet.bullet()

    while 1:
        deltaT = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        playerObj.updatePos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        bullet.update(deltaT)

        background.fill((250, 250, 250))
        pygame.draw.rect(background, (0, 0, 0), playerObj.getRect())
        screen.blit(background, (0, 0))
        pygame.display.flip()

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
