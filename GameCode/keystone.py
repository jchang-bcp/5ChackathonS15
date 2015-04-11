import pygame
import numpy as np

class Keystone:
    def __init__(self, w, h, H=np.eye(3)):
        #self._far = 100
        #self._near = 120
        self._screenWidth = w
        self._screenHeight = h
        self._transformation = H


    #def xtransform(self, x, y):
    #    mathx = x - self._screenWidth/2
    #    mathy = self._screenHeight - y
    #    return self._screenWidth/2 + (x - (x*(1-near/far)/self._screenHeight)*mathy)

    #def ytransform(self, x, y):
    #    mathy = self._screenHeight - y

    #def makeShape(self, src):
    #    """
    #    Converts rectangle src to keystone-corrected polygon.
    #    Polygon is returned as a list of vertices
    #    """
    #    tl = src.topleft
    #    tr = src.topright
    #    bl = src.bottomleft
    #    br = src.bottomright

    #    newtl = [xtransform(tl[0], tl[1]), ytransform(tl[0], tl[1])]
    #    newtr = [xtransform(tr[0], tr[1]), ytransform(tr[0], tr[1])]
    #    newbl = [xtransform(bl[0], bl[1]), ytransform(bl[0], bl[1])]
    #    newbr = [xtransform(br[0], br[1]), ytransform(br[0], br[1])]

    #    return [newtl, newtr, newbl, newbr]

    def setHomography(self, pt1, pt2):
        srcPts = np.array([ (0,self._screenHeight), (self._screenWidth,self._screenHeight),
                            (0,0), (self._screenWidth,0)], dtype=np.float32)
        dstPts = np.array([ (0,self._screenHeight), (self._screenWidth,self._screenHeight),
                            min(pt1,pt2), max(pt1,pt2)], dtype=np.float32)

    #    self._transformation, _ = cv2.findHomography(srcPts, dstPts)

    def transformPoint(self, pt):
        t = self._transformation.dot(np.array(pt+[1]))
        return [ t[0]/t[2], t[1]/t[2] ]

    def polygon(self, surface, color, pointlist):
        transformedPtList = [self.transformPoint(pt) for pt in pointlist]

        pygame.draw.polygon(surface, color, transformedPtList)