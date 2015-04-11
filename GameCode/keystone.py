import pygame

class Keystone:
    def __init__(self, w, h):
        self._far = 100
        self._near = 120
        self._screenWidth = w
        self._screenHeight = h

    def xtransform(x, y):
        mathx = x - self._screenWidth/2
        mathy = self._screenHeight - y
        return self._screenWidth/2 + (x - (x*(1-near/far)/self._screenHeight)*mathy)

    def ytransform(x, y):
        mathy = self._screenHeight - y

    def makeShape(src):
        """
        Converts rectangle src to keystone-corrected polygon.
        Polygon is returned as a list of vertices
        """
        tl = src.topleft
        tr = src.topright
        bl = src.bottomleft
        br = src.bottomright

        newtl = [xtransform(tl[0], tl[1]), ytransform(tl[0], tl[1])]
        newtr = [xtransform(tr[0], tr[1]), ytransform(tr[0], tr[1])]
        newbl = [xtransform(bl[0], bl[1]), ytransform(bl[0], bl[1])]
        newbr = [xtransform(br[0], br[1]), ytransform(br[0], br[1])]

        return [newtl, newtr, newbl, newbr]

    def polygon(surface, color, pointlist):
        pygame.draw.polygon(surface, color, pointlist)
