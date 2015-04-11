#!/usr/bin/env python2
# Alex Ozdemir <aozdemir@hmc.edu>

import numpy as np
import cv2
import math

# a = np.loadtxt('f.txt')

# # a = cv2.GaussianBlur(a, ksize=(7, 7), sigmaX=2)

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



# cv2.imwrite('residual.jpg', d)

# c = cv2.Sobel(d, -1, 2, 2, ksize=3, scale=20)
# # c = cv2.Laplacian(d, ddepth=-1, ksize=3, scale=20)

# cv2.imwrite('c.jpg', c)

# def s(x, y, w):
# 	print a[y-w:y+w, x-w:x+w]

# small_r = 1
# big_r = 30
# circles = cv2.HoughCircles(d,
#                            cv2.cv.CV_HOUGH_GRADIENT,
#                            1,
#                            4 * small_r,
#                            1,
#                            1,
#                            minRadius = small_r,
#                            maxRadius = big_r)


def draw_circles(output, circles):
	if circles:
	    for (x, y, r) in circles[0]:
	        cv2.circle(output, (x, y), r, (0, 0, 255), 2)

# print circles
small_r = 1
big_r = 20

co = cv2.imread('f.png',cv2.IMREAD_COLOR)
gray = cv2.cvtColor(co, cv2.COLOR_RGB2GRAY)

thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

print 'contours...'
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key = cv2.contourArea)
print 'done'

drawing = np.zeros(thresh.shape, np.uint8)
cv2.drawContours(drawing, contours[-1:], -1, (255, 0, 0), -1)


cv2.imshow('im', drawing)
# cv2.imshow('im', thresh[1])

cv2.waitKey(10)

# print circles
