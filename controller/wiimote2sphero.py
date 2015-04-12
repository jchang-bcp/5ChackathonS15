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
    tilt2spdfactor = 28 #34
    buttonSpd = 120


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
        if rospy.get_time() - D.last_sent_time > 1 or D.lastVel != (speed, angle):
            D.last_sent_time = rospy.get_time()
            #if speed >= 250:
            #    D.robotPub.publish('robot.boost(10, '\
            #                       +str(int(angle))+', False)')
            #else:
            D.robotPub.publish('robot.roll('\
                               +str(int(speed))+', '\
                               +str(int(angle))+', 1, False)')
    except AttributeError:
        D.last_sent_time = rospy.get_time()

    D.lastVel = (speed, angle)

    if data.buttons[2]:
        if not D.just_changed_color:

            col = getRGB(D.colorList[D.colorIndex])
            D.colorIndex += 1
            D.colorIndex %= 5

            D.robotPub.publish('robot.set_rgb_led(' \
                    +str(int(col[0]))+', ' \
                    +str(int(col[1]))+', ' \
                    +str(int(col[2]))+', ' \
                    +'False, False)')
            D.colorPub.publish(True)
        D.just_changed_color = True
    else:
        D.just_changed_color = False


    if data.buttons[4] or data.buttons[5]:
        if not D.just_changed_heading:
            if data.buttons[4]:
                D.heading += 5
            elif data.buttons[5]:
                D.heading -= 5
            D.heading += 360
            D.heading %= 360
            #D.robotPub.publish('robot.set_heading('+str(D.heading)+', False)')
            D.robotPub.publish('robot.set_heading(10, False)')
            D.robotPub.publish('robot.set_back_led(255, False)')
        D.just_changed_heading = True
    else:
        if D.just_changed_heading:
            D.robotPub.publish('robot.set_back_led(0, False)')
        D.just_changed_heading = False

def getRGB(color):
    if color == "blue":
        return (0,191,255)
    if color == "green":
        return (50,205,50)
    if color == "yellow":
        return (210,210,0)
    if color == "purple":
        return (160,32,240)
    if color == "orange":
        return (234,94,29)

def main():
    rospy.init_node('wiimote2sphero')
    D.heading = 0
    D.just_changed_color = False
    D.just_changed_heading = False
    D.colorIndex = 0
    D.colorList = ["blue", "green", "yellow", "purple", "orange"]

    D.robotPub = rospy.Publisher('/sphero', std_msgs.msg.String, queue_size=4)
    D.colorPub = rospy.Publisher('/sphero_change_color', std_msgs.msg.Bool, queue_size=10)
    D.robotPub.publish('robot.set_back_led(255, False)')
    print 'Ready'
    D.wiimoteSub = rospy.Subscriber('/joy', sensor_msgs.msg.Joy, wiimote_callback)

    #while True:
    #    input()
    rospy.spin()

    print 'Shutting down'


if __name__ == '__main__':
    main()
