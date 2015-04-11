#!/usr/bin/env python2

import rospy
import sensor_msgs.msg
import geometry_msgs.msg
import std_msgs.msg
import random
from sphero_driver import sphero_driver
import sys
import math

class Data:
    pass

D = Data()


def wiimote_callback(data):
    #print '%+2.2f %+2.2f %+2.2f' % data.axes
    #print data
    #return

    deadband = 2
    tilt2spdfactor = 17 #34
    buttonSpd = 90


    if data.buttons[3]:
        xax = data.axes[0]
        yax = data.axes[1]

        if -deadband < xax and xax < deadband:
            xspd = 0
        elif xax > 0:
            xspd = (xax-deadband)*tilt2spdfactor
        else:
            xspd = (xax+deadband)*tilt2spdfactor

        if -deadband < yax and yax < deadband:
            yspd = 0
        elif yax > 0:
            yspd = (yax-deadband)*tilt2spdfactor
        else:
            yspd = (yax+deadband)*tilt2spdfactor
    else:
        xspd = 0
        yspd = 0

        if data.buttons[6]:
            xspd += -buttonSpd
        if data.buttons[7]:
            xspd += buttonSpd

        if data.buttons[8]:
            yspd += buttonSpd
        if data.buttons[9]:
            yspd += -buttonSpd

    angle = math.atan2(xspd, yspd) * 180/math.pi
    angle = (angle + 360) % 360 # normalize so it's positive

    speed = math.sqrt(xspd*xspd + yspd*yspd)
    try:
        if D.lastVel != (speed, angle):
            #if speed >= 250:
            #    D.robotPub.publish('robot.boost(10, '\
            #                       +str(int(angle))+', False)')
            #else:
            D.robotPub.publish('robot.roll('\
                               +str(int(speed))+', '\
                               +str(int(angle))+', 1, False)')
    except AttributeError:
        pass
    D.lastVel = (speed, angle)

    if data.buttons[2]:
        if not D.just_changed_color:
            D.robotPub.publish('robot.set_rgb_led(' \
                    +str(int(random.uniform(0,256)))+', ' \
                    +str(int(random.uniform(0,256)))+', ' \
                    +str(int(random.uniform(0,256)))+', ' \
                    +'False, False)')
        D.just_changed_color = True
    else:
        D.just_changed_color = False

def main():
    rospy.init_node('wiimote2sphero')

    D.robotPub = rospy.Publisher('/sphero', std_msgs.msg.String, queue_size=1)
    D.robotPub.publish('robot.set_back_led(255, False)')
    print 'Ready'
    D.wiimoteSub = rospy.Subscriber('/joy', sensor_msgs.msg.Joy, wiimote_callback)

    while True:
        input()
    #rospy.spin()

    print 'Shutting down'


if __name__ == '__main__':
    main()
