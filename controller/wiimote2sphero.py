#!/usr/bin/env python2

import rospy
import sensor_msgs.msg
import geometry_msgs.msg
import std_msgs.msg
import random

class Data:
    pass

D = Data()


def wiimote_callback(data):
    #print '%+2.2f %+2.2f %+2.2f' % data.axes
    #print data
    #return

    if data.buttons[3]:
        xax = data.axes[0]
        yax = data.axes[1]

        deadband = 2
        tilt2spdfactor = 34

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
            xspd += -200
        if data.buttons[7]:
            xspd += 200

        if data.buttons[8]:
            yspd += 200
        if data.buttons[9]:
            yspd += -200


    spheroMsg = geometry_msgs.msg.Twist()
    spheroMsg.linear.x = xspd
    spheroMsg.linear.y = yspd
    try:
        if D.lastMsg.linear.x != spheroMsg.linear.x or D.lastMsg.linear.y != spheroMsg.linear.y:
            print xspd, yspd
            D.spheroMovPub.publish(spheroMsg)
            D.backLED.publish(255)
            D.disableStabilization.publish(False)
    except AttributeError:
        pass
    D.lastMsg = spheroMsg

    if data.buttons[2]:
        if not D.just_changed_color:
            D.just_changed_color = True
            #D.spheroColPub.publish(std_msgs.msg.ColorRGBA
            #D.spheroColPub.publish(r=random.random(0,256), g=random.random(0,256), b=random.random(0,256), a=255)
            colMsg = std_msgs.msg.ColorRGBA()
            print '--------------------------------------------------------------------------------'
            colMsg.r = random.uniform(0,1)
            colMsg.g = random.uniform(0,1)
            colMsg.b = random.uniform(0,1)
            print colMsg
            print '--------------------------------------------------------------------------------'
            D.spheroColPub.publish(colMsg)
    else:
        D.just_changed_color = False

def main():
    rospy.init_node('wiimote2sphero')

    rospy.set_param('/sphero/cmd_vel_timeout', 10)

    D.wiimoteSub = rospy.Subscriber('/joy', sensor_msgs.msg.Joy, wiimote_callback)

    D.spheroMovPub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)

    D.spheroColPub = rospy.Publisher('/set_color', std_msgs.msg.ColorRGBA, queue_size=1)

    D.backLED = rospy.Publisher('/set_back_led', std_msgs.msg.Float32, queue_size=1)
    #D.spheroBackPub
    #/set_back_led

    rospy.spin()


if __name__ == '__main__':
    main()
