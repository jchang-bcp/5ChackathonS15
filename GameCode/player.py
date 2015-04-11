import pygame
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, initx, inity, radius = 80, numSides = 10):
        pygame.sprite.Sprite.__init__(self)
        self._xpos = initx
        self._ypos = inity
        self._color = "blue"
        self._colorIndex = 0
        self._colorList = ["blue", "green", "yellow", "purple", "orange"]
        self._radius = radius
        self._numSides = numSides
        self.updateVertices()

    def colorShift(self, N):
        self._color = self._colorList[(self._colorIndex + N) % len(self._colorList)]
        self._colorIndex = (self._colorIndex + 1) % len(self._colorList)

    def updatePos(self, newx, newy):
        self._xpos = newx
        self._ypos = newy
        self.updateVertices()

    def updateVertices(self):
        self._vertexList = [[self._xpos + self._radius*np.cos(i*2*np.pi/self._numSides),
                             self._ypos + self._radius*np.sin(i*2*np.pi/self._numSides)] for i in range(0, self._numSides)]

    def getVertices(self):
        return self._vertexList

    def getPosition(self):
        return (self._xpos, self._ypos)

    def getRadius(self):
        return self._radius

    def collide(self):
        print "Ow!"
