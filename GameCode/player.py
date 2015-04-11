import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, initx, inity):
        pygame.sprite.Sprite.__init__(self)
        self._xpos = initx
        self._ypos = inity
        self.updateVertices()

    def updatePos(self, newx, newy):
        self._xpos = newx
        self._ypos = newy
        self.updateVertices()

    def updateVertices(self):
        self._vertexList = [[self._xpos - 5, self._ypos - 5],
                            [self._xpos + 5, self._ypos - 5],
                            [self._xpos + 5, self._ypos + 5],
                            [self._xpos - 5, self._ypos + 5]]

    def getVertices(self):
        return self._vertexList

    def getCollider(self):
        return pygame.Rect(self._xpos - 5, self._ypos - 5, 10, 10)

    def collide(self):
        print "Ow!"
