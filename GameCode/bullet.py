import pygame
import random
import numpy as np

class Bullet(pygame.sprite.Sprite):
    def __init__(self, Width, Height, Radius = 30, numSides = 10):
        pygame.sprite.Sprite.__init__(self)
        self._screenWidth = Width
        self._screenHeight = Height
        self._xpos = random.randint(0, Width)
        self._ypos = random.randint(0, Height)

        angle = random.random()*2*np.pi
        speed = random.randint(40, 80)
        self._xvel = int(speed * np.cos(angle))
        self._yvel =  int(speed * np.sin(angle))

        self._color = random.choice(["blue", "green", "yellow", "purple", "orange"])
        self._radius = Radius
        self._numSides = numSides
        self.updateVertices()

    def updatePos(self, deltaT, time):
        self._xpos = (self._xpos + self._xvel * deltaT / 1000.0 * self.speedFrac(time) ) % self._screenWidth
        self._ypos = (self._ypos + self._yvel * deltaT / 1000.0 * self.speedFrac(time) ) % self._screenHeight
        self.updateVertices()

    def updateVertices(self):
        self._vertexList = [[self._xpos + self._radius*np.cos(i*2*np.pi/self._numSides),
                             self._ypos + self._radius*np.sin(i*2*np.pi/self._numSides)] for i in range(0, self._numSides)]

    def getVertices(self):
        return self._vertexList

    def speedFrac(self, time):
        return (time/10000.0)**(1.0/2) + 1

    def checkForHit(self, target):
        xdiff = target.getPosition()[0] - self._xpos
        ydiff = target.getPosition()[1] - self._ypos
        return (np.sqrt(xdiff**2 + ydiff**2) <= self._radius + target.getRadius())
