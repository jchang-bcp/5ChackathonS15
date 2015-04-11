import pygame
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, Width, Height):
        pygame.sprite.Sprite.__init__(self)
        self._screenWidth = Width
        self._screenHeight = Height
        self._xpos = random.randint(0, Width)
        self._ypos = random.randint(0, Height)
        self._xvel = random.randint(-50,50)
        self._yvel = random.randint(-50,50)
        self._rect = pygame.Rect(self._xpos, self._ypos, 10, 10)

    def updatePos(self, deltaT):
        self._xpos = (self._xpos + self._xvel * deltaT / 1000.0) % self._screenWidth
        self._ypos = (self._ypos + self._yvel * deltaT / 1000.0) % self._screenHeight
        self._rect.x = self._xpos
        self._rect.y = self._ypos

    def getRect(self):
        return self._rect

    def checkForHit(self, target):
        return self._rect.colliderect(target.getRect())