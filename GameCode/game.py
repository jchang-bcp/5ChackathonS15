import pygame, player, bullet, keystone, random
from pygame.locals import *



def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    #Initialize Everything
    WIDTH = 500
    HEIGHT = 500

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('HARVEY MUDD HACKATHON')
    pygame.mouse.set_visible(1)

    ks = keystone.Keystone(WIDTH, HEIGHT)

    calibrationIndex = 0
    calibrationPoints = [(0, 0), (0, 0)]

    #Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    playerObj = player.Player(250, 250)
    bulletList = [bullet.Bullet(WIDTH,HEIGHT) for x in range (3)]

    while 1:
        deltaT = clock.tick(60)

        if calibrationIndex < 2:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    calibrationPoints[calibrationIndex] = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    calibrationIndex += 1
                    if calibrationIndex >= 2:
                        ks.setHomography(calibrationPoints[0], calibrationPoints[1])
                        pygame.mouse.set_visible(0)

            if pygame.font:
                font = pygame.font.Font(None, 36)
                text = font.render("Calibration", 1, (10, 10, 10))
                textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/8*7)
                background.blit(text, textpos)
                text = font.render("Please click on the upper corners of the game field", 1, (10, 10, 10))
                textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/16*15)
                background.blit(text, textpos)

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            playerObj.updatePos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if random.random() < .03/len(bulletList) :
                bulletList += [bullet.Bullet(WIDTH,HEIGHT)]

            for bulletObj in bulletList:
                bulletObj.updatePos(deltaT, pygame.time.get_ticks())
                if bulletObj.checkForHit(playerObj):
                    playerObj.collide()
                    if pygame.font:
                        font = pygame.font.Font(None, 36)
                        text = font.render("Game Over", 1, (10, 10, 10))
                        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/8*7)
                        background.blit(text, textpos)
                        text = font.render("self.getRect()", 1, (10, 10, 10))
                        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/16*15)
                        background.blit(text, textpos)
                        screen.blit(background, (0, 0))
                        pygame.display.flip()
                    print "GAME OVER BRAH"
                    pygame.time.delay(3000)
                    return

            background.fill((250, 250, 250))
            ks.polygon(background, getRGB(playerObj._color), playerObj.getVertices())

            for bulletObj in bulletList:
                ks.polygon(background, getRGB(bulletObj._color), bulletObj.getVertices())
        screen.blit(background, (0, 0))
        pygame.display.flip()

def getRGB(color):
    if color == "blue":
        return (0,191,255)
    if color == "green":
        return (34,139,34)
    if color == "red":
        return (178,34,34)
    if color == "purple":
        return (106,90,205)
    if color == "orange":
        return (250,128,114)

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
