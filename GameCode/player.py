import pygame

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._xpos = 0
        self._ypos = 0
        self._rect = pygame.Rect(self._xpos, self._ypos, 10, 10)

    def updatePos(self, newx, newy):
        self._xpos = newx
        self._ypos = newy
        self._rect.x = newx
        self._rect.y = newy

    def collide(self):
        print "Ow!"
