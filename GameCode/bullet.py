import pygame
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, Width, Height):
        pygame.sprite.Sprite.__init__(self)
        self._screenWidth = Width
        self._screenHeight = Height
        self._xpos = random.randint(0, Width)
        self._ypos = random.randint(0, Height)
        self._xvel = random.randint(40,50)*random.choice([-1,1])
        self._yvel =  random.randint(40,50)*random.choice([-1,1])
        self.updateVertices()

    def updatePos(self, deltaT, time):
        self._xpos = (self._xpos + self._xvel * deltaT / 1000.0 * self.speedFrac(time) ) % self._screenWidth
        self._ypos = (self._ypos + self._yvel * deltaT / 1000.0 * self.speedFrac(time) ) % self._screenHeight
        self.updateVertices()

    def updateVertices(self):
        self._vertexList = [[self._xpos - 5, self._ypos - 5],
                            [self._xpos + 5, self._ypos - 5],
                            [self._xpos + 5, self._ypos + 5],
                            [self._xpos - 5, self._ypos + 5]]

    def getVertices(self):
        return self._vertexList

    def speedFrac(self, time):
        return (time/10000.0)**(1.0/2) + 1

    def checkForHit(self, target):
        collisionRect = pygame.Rect(self._xpos - 5, self._ypos - 5, 10, 10)
        return collisionRect.colliderect(target.getCollider())
