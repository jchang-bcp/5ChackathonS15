#!/usr/bin/env python2
# Alex Ozdemir <aozdemir@hmc.edu>

import numpy as np
import cv2
import math
import Geometry
import Vector

a = np.loadtxt('f.txt')

# a = cv2.GaussianBlur(a, ksize=(7, 7), sigmaX=2)

class Calibration:
	pass
calibration = Calibration()
calibration.ul= (100, 100)
calibration.ll = (400, 160)
calibration.ur = (100, 500)
calibration.lr = (400, 440)

def kinect_to_cartesian(kinect_pos, calib):
	top_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)
	bot_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)
	left_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)
	right_dist = Geometry.distFromPointToLine(kinect_pos, calib.ul, calib.ur)

# a = a[100:-100, 100:-100]
# cv2.imwrite('f.jpg', a.astype(np.uint8))


# def xang(x):
# 	return math.radians(-23.5 + x*57./639)
# def yang(y):
# 	return math.radians(21.5 - y*43./480)

# x = []
# y = []
# z = []
# for xi in xrange(a.shape[1]):
# 	for yi in xrange(a.shape[0]):
# 		zi = a[yi,xi]
# 		x.append(xi)
# 		y.append(yi)
# 		z.append(zi)
# 		# x.append(math.sin(xang(xi))*math.cos(yang(yi))*zi)
# 		# y.append(math.cos(xang(xi))*math.sin(yang(yi))*zi)
# 		# z.append(math.cos(xang(xi))*math.cos(yang(yi))*zi)


# xa = np.array(x)
# ya = np.array(y)
# za = np.array(z)

# res = np.linalg.lstsq(np.vstack([xa, ya, np.ones(len(xa))]).T, za)
# xc, yc, cc = res[0]

# d = np.array(a)
# for xi in xrange(a.shape[1]):
# 	for yi in xrange(a.shape[0]):
# 		d[yi,xi] = 255 - abs(d[yi,xi] - (cc + yc * yi + xc * xi))*50


# d = d.astype(np.uint8)
# def f(y, x):
# 	print 'plane: %.2f, img: %.2f, res: %.2f' % (xc * x + yc * y + cc, a[y,x], d[y,x])



#function to get RGB image from kinect
# def get_video():
#     array,_ = freenect.sync_get_video()
#     array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
#     return array

# while 1:
#     #get a frame from RGB camera
#     frame = get_video()

#     #display RGB image
#     cv2.imshow('RGB image',frame)

#     # quit program when 'esc' key is pressed
#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:	
#         break
# cv2.destroyAllWindows()

def findSphero(img):
	''' Given a color img, finds the finds the sphero.
	Returns the center of the sphero as an x,y coordinate pair.
	Returns None if no sphero is found'''
	gray = cv2.cvtColor(co, cv2.COLOR_RGB2GRAY)

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
	uc, vc = np.linalg.solve(A, B)

	xc_1 = x_m + uc
	yc_1 = y_m + vc
	
	print (int(xc_1), int(yc_1))
	return (int(xc_1), int(yc_1))

co = cv2.imread('f.png',cv2.IMREAD_COLOR)

center = findSphero(co)

cv2.circle(co, center, 5, (255, 0, 0), 2)

cv2.imshow('im', co)

cv2.waitKey(10)

# print circles
