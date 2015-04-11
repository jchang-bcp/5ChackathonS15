import pygame
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, Width, Height, Size=20):
        pygame.sprite.Sprite.__init__(self)
        self._screenWidth = Width
        self._screenHeight = Height
        self._xpos = random.randint(0, Width)
        self._ypos = random.randint(0, Height)
        self._xvel = random.randint(60,100)*random.choice([-1,1])
        self._yvel =  random.randint(60,100)*random.choice([-1,1])
        self._size = Size
        self.updateVertices()

    def updatePos(self, deltaT, time):
        self._xpos = (self._xpos + self._xvel * deltaT / 1000.0 * self.speedFrac(time) ) % self._screenWidth
        self._ypos = (self._ypos + self._yvel * deltaT / 1000.0 * self.speedFrac(time) ) % self._screenHeight
        self.updateVertices()

    def updateVertices(self):
        self._vertexList = [[self._xpos - self._size, self._ypos - self._size],
                            [self._xpos + self._size, self._ypos - self._size],
                            [self._xpos + self._size, self._ypos + self._size],
                            [self._xpos - self._size, self._ypos + self._size]]

    def getVertices(self):
        return self._vertexList

    def speedFrac(self, time):
        return (time/10000.0)**(1.0/2) + 1

    def checkForHit(self, target):
        collisionRect = pygame.Rect(self._xpos - self._size, self._ypos - self._size, 2*self._size, 2*self._size)
        return collisionRect.colliderect(target.getCollider())
