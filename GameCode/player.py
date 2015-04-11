import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, initx, inity):
        pygame.sprite.Sprite.__init__(self)
        self._xpos = initx
        self._ypos = inity
        self._rect = pygame.Rect(self._xpos, self._ypos, 10, 10)
        self.color = "red"

    def updatePos(self, newx, newy):
        self._xpos = newx
        self._ypos = newy
        self._rect.x = newx
        self._rect.y = newy

    def getRect(self):
        return self._rect

    def collide(self):
        print "Ow!"
