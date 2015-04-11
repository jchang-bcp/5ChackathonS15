import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._xpos = 500
        self._ypos = 0
        self._xvel = -50
        self._yvel = 50
        self._rect = pygame.Rect(self._xpos, self._ypos, 10, 10)

    def updatePos(self, deltaT):
        self._xpos += self._xvel * deltaT / 1000.0
        self._ypos += self._yvel * deltaT / 1000.0
        self._rect.x = self._xpos
        self._rect.y = self._ypos

    def getRect(self):
        return self._rect

    def checkForHit(self, target):
        return self._rect.colliderect(target.getRect())

    def deltaT():
        return 1
