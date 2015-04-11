#!/usr/bin/env python2
# Alex Ozdemir <aozdemir@hmc.edu>

import rospy
import std_msgs.msg
import sensor_msgs.msg
import numpy as np
import cv2
import math
import Geometry
import Vector
import cv_bridge
import sys
import freenect

sys.path.append('..')
import config

class Data:
    pass

D = Data()

pictureCorners = []

D.processingScaleFactor = 5

def kinect_to_cartesian(kinect_pos, calib):
    top_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)
    bot_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)
    left_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)
    right_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)

    h = []
    #cv2.findHomography(

def updateCalibration():
    global pictureCorners
    global H

    largeXs = set(sorted(pictureCorners, key=lambda x: -x[0])[0:2])
    smallXs = set(sorted(pictureCorners, key=lambda x:  x[0])[0:2])
    largeYs = set(sorted(pictureCorners, key=lambda x: -x[1])[0:2])
    smallYs = set(sorted(pictureCorners, key=lambda x:  x[1])[0:2])

    srcPts = np.array([(smallXs & smallYs).pop(),
                       (smallXs & largeYs).pop(),
                       (largeXs & smallYs).pop(),
                       (largeXs & largeYs).pop()], dtype=np.float32)

    dstPts = np.array([(                0/D.processingScaleFactor,                  0/D.processingScaleFactor),
                       (                0/D.processingScaleFactor, config.GAME_HEIGHT/D.processingScaleFactor),
                       (config.GAME_WIDTH/D.processingScaleFactor,                  0/D.processingScaleFactor),
                       (config.GAME_WIDTH/D.processingScaleFactor, config.GAME_HEIGHT/D.processingScaleFactor)], dtype=np.float32)

    #print srcPts, '->', dstPts

    H, _ = cv2.findHomography(srcPts, dstPts)

    print H

def findSphero(img):
    ''' Given a color img, finds the finds the sphero.
    Returns the center of the sphero as an x,y coordinate pair.
    Returns None if no sphero is found'''
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

    try:
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea)
        bestContour = contours[-1] if len(contours) > 0 else None
        return centerContour(bestContour)
    except:
        return None

def xang(x):
    return math.radians(-23.5 + x*57./639)
def yang(y):
    return math.radians(21.5 - y*43./480)

def findPlane(img):
    x = []
    y = []
    z = []
    for xi in xrange(img.shape[1]):
        for yi in xrange(img.shape[0]):
            zi = img[yi,xi]
            #x.append(xi)
            #y.append(yi)
            z.append(zi)
            x.append(math.sin(xang(xi))*math.cos(yang(yi))*zi)
            y.append(math.cos(xang(xi))*math.sin(yang(yi))*zi)
            #z.append(math.cos(xang(xi))*math.cos(yang(yi))*zi)


    xa = np.array(x)
    ya = np.array(y)
    za = np.array(z)

    #print xa, ya, za, 'shapes:', xa.shape, ya.shape, za.shape, len(xa), np.ones(len(xa)).shape

    #res = np.linalg.lstsq(np.hstack([xa, ya, np.ones(len(xa))]), za)
    res = np.linalg.lstsq(np.vstack([xa, ya, np.ones(len(xa))]).T, za)
    xc, yc, cc = res[0]
    print 'Coefficients: ', res[0]

    D.plane_depths = np.array(img)
    for xi in xrange(img.shape[1]):
        for yi in xrange(img.shape[0]):
            D.plane_depths[yi,xi] = (cc + yc * yi + xc * xi)/8


def findSphero_depth(img):


    if not hasattr(D, 'plane_depths'):
        findPlane(img)


    D.diffs = img/8 - D.plane_depths
    #print D.diffs
    #disp = diffs*20 

    #img = D.diffs.astype(np.uint8)
    img = D.diffs.astype(np.uint8)
    #print img[70,30], img.shape
    cv2.imshow('im', img)

    return (0,0)

def f(y, x):
    print 'plane: %.2f, img: %.2f, res: %.2f' % (xc * x + yc * y + cc, D.plane_depths[y,x], D.plane_depths[y,x])

def onMouse(event,x,y,flags,param):
    """ the method called when the mouse is clicked """
    # if the left button was clicked
    if event==cv2.EVENT_LBUTTONDOWN:
        #print "x, y are", x, y, D.plane_depths[y,x], D.diffs[y,x]
        print "x, y are", x, y
        pictureCorners.append( (x,y) )
        if len(pictureCorners) == 4:
            updateCalibration()


def mean(x):
    return sum(x)/len(x)

def centerContour(contour):

    x = contour[:,0,0]
    y = contour[:,0,1]

    x_m = mean(x)
    y_m = mean(y)

    # calculation of the reduced coordinates
    u = x - x_m
    v = y - y_m

    # linear system defining the center (uc, vc) in reduced coordinates:
    #    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
    #    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
    Suv  = sum(u*v)
    Suu  = sum(u**2)
    Svv  = sum(v**2)
    Suuv = sum(u**2 * v)
    Suvv = sum(u * v**2)
    Suuu = sum(u**3)
    Svvv = sum(v**3)

    # Solving the linear system
    A = np.array([ [ Suu, Suv ], [Suv, Svv]])
    B = np.array([ Suuu + Suvv, Svvv + Suuv ])/2.0
    try:
        uc, vc = np.linalg.solve(A, B)
    except np.LinAlgError:
        return (0,0)

    xc_1 = x_m + uc
    yc_1 = y_m + vc

    #print (int(xc_1), int(yc_1))
    return (int(xc_1), int(yc_1))

# a = a[100:-100, 100:-100]

def kinect_rgb_callback(data):
    color_image = D.bridge.imgmsg_to_cv2(data, "bgr8")

    try:
        color_image = cv2.warpPerspective(color_image, H, (config.GAME_WIDTH/D.processingScaleFactor,config.GAME_HEIGHT/D.processingScaleFactor))
    except NameError:
        cv2.imshow('im', color_image)

    center = findSphero(color_image)
    pubcenter = (center[0]*D.processingScaleFactor, center[1]*D.processingScaleFactor)
    pubcenter = (pubcenter[0], pubcenter[1] + 80 + (1 - pubcenter[1])/config.GAME_HEIGHT)

    if center:
        D.pub.publish(str(pubcenter))
    else:
        print 'None'

    #cv2.circle(color_image, center, 5, (255, 0, 0), 2)


    key_press = cv2.waitKey(5) & 0xff
    if key_press == 27 or key_press == ord('q'):
        rospy.signal_shutdown(0)

def process_depth(depth):
    #depth_image = D.bridge.imgmsg_to_cv2(data, "32FC1").astype(np.uint8)
    #cv2.imshow('im', depth)

    #try:
    #    depth_image = cv2.warpPerspective(depth_image, H, (config.GAME_WIDTH,config.GAME_HEIGHT))
    #except NameError:
    #    pass

    center = findSphero_depth(depth)

    if not center:
        print 'None'

    D.pub.publish(str(center))

    #depth_image = depth.astype(np.uint8)

    #cv2.circle(depth_image, center, 5, (255, 0, 0), 2)

    #cv2.imshow('im', depth_image)

    key_press = cv2.waitKey(5) & 0xff
    if key_press == 27 or key_press == ord('q'):
        rospy.signal_shutdown(0)

def main():
    rospy.init_node('sphero_finder')

    cv2.namedWindow('im')
    cv2.setMouseCallback('im', onMouse, None)

    D.bridge = cv_bridge.CvBridge()

    D.pub = rospy.Publisher('/sphero_coordinates', std_msgs.msg.String, queue_size=1)
    D.kinectRGBSub = rospy.Subscriber('/camera/rgb/image_color', sensor_msgs.msg.Image, kinect_rgb_callback)
    rospy.spin()
    #D.kinectDepthSub = rospy.Subscriber('/camera/depth/image', sensor_msgs.msg.Image, kinect_depth_callback)

    #while not rospy.is_shutdown():
    #    depth = freenect.sync_get_depth()[0]
    #    process_depth(depth)

if __name__ == '__main__':
    main()
