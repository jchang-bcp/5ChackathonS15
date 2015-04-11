import pygame
import cv2
import numpy as np

class Keystone:
    def __init__(self, w, h, sw, sh, H=np.eye(3)):
        self._screenWidth = w
        self._screenHeight = h
        self._transformation = H

    def setHomography(self, pt1, pt2):
        srcPts = np.array([ (0,self._screenHeight), (self._screenWidth,self._screenHeight),
                            (0,0), (self._screenWidth,0)], dtype=np.float32)
        dstPts = np.array([ (0,self._screenHeight/1.5), (self._screenWidth,self._screenHeight/1.5),
                            min(pt1,pt2), max(pt1,pt2)], dtype=np.float32)

    #    self._transformation, _ = cv2.findHomography(srcPts, dstPts)

    def transformPoint(self, pt):
        t = self._transformation.dot(np.array(pt+[1]))
        return [ t[0]/t[2], t[1]/t[2] ]

    def polygon(self, surface, color, pointlist):
        transformedPtList = [self.transformPoint(pt) for pt in pointlist]

        pygame.draw.polygon(surface, color, transformedPtList)
