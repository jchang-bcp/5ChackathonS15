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

sys.path.append('..')
import config

class Data:
    pass

D = Data()

pictureCorners = []

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

    dstPts = np.array([(                0,                  0),
                       (                0, config.GAME_HEIGHT),
                       (config.GAME_WIDTH,                  0),
                       (config.GAME_WIDTH, config.GAME_HEIGHT)], dtype=np.float32)

    #print srcPts, '->', dstPts

    H, _ = cv2.findHomography(srcPts, dstPts)

    print H

def findSphero(img):
	''' Given a color img, finds the finds the sphero.
	Returns the center of the sphero as an x,y coordinate pair.
	Returns None if no sphero is found'''
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key = cv2.contourArea)
	bestContour = contours[-1] if len(contours) > 0 else None

	return centerContour(bestContour) if bestContour.all() else None


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

def kinect_callback(data):
    color_image = D.bridge.imgmsg_to_cv2(data, "bgr8")

    center = findSphero(color_image)

    if not center:
        print 'None'

    D.pub.publish(str(center))

    cv2.circle(color_image, center, 5, (255, 0, 0), 2)

    
    try:
        color_image = cv2.warpPerspective(color_image, H, (config.GAME_WIDTH,config.GAME_HEIGHT))
    except NameError:
        pass

    cv2.imshow('im', color_image)

    key_press = cv2.waitKey(5) & 0xff
    if key_press == 27 or key_press == ord('q'):
        rospy.signal_shutdown(0)

def onMouse(event,x,y,flags,param):
    """ the method called when the mouse is clicked """
    # if the left button was clicked
    if event==cv2.EVENT_LBUTTONDOWN: 
        print "x, y are", x, y
        pictureCorners.append( (x,y) )
        if len(pictureCorners) == 4:
            updateCalibration()

def main():
    rospy.init_node('sphero_finder')

    cv2.namedWindow('im')
    cv2.setMouseCallback('im', onMouse, None)

    D.bridge = cv_bridge.CvBridge()

    D.pub = rospy.Publisher('/sphero_coordinates', std_msgs.msg.String, queue_size=1)
    D.kinectSub = rospy.Subscriber('/camera/rgb/image_color', sensor_msgs.msg.Image, kinect_callback)

    rospy.spin()

if __name__ == '__main__':
    main()

