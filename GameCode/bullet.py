import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._xpos = 0
        self._ypos = 0
        self._xvel = 20
        self._yvel = 20
        self._rect = pygame.Rect(self._xpos, self._ypos, 10, 10)

    def updatePos(self, deltaT):
        self._xpos += self._xvel * deltaT / 1000.0
        self._ypos += self._yvel * deltaT / 1000.0
        self._rect.x = self._xpos
        self._rect.y = self._ypos

    def getRect(self):
        return self._rect

    def collide(self):
        print "Ow!"

    def deltaT():
        return 1