import pygame
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, initx, inity, radius = 10, numSides = 10):
        pygame.sprite.Sprite.__init__(self)
        self._xpos = initx
        self._ypos = inity
        self._color = "red"
        self._radius = radius
        self._numSides = numSides
        self.updateVertices()

    def updatePos(self, newx, newy):
        self._xpos = newx
        self._ypos = newy
        self.updateVertices()

    def updateVertices(self):
        self._vertexList = [[self._xpos + 10*np.cos(i*2*np.pi/self._numSides),
                             self._ypos + 10*np.sin(i*2*np.pi/self._numSides)] for i in range(0, self._numSides)]

    def getVertices(self):
        return self._vertexList

    def getPosition(self):
        return (self._xpos, self._ypos)

    def getRadius(self):
        return self._radius

    def collide(self):
        print "Ow!"
