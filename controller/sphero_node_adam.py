#!/usr/bin/env python2

import rospy
import std_msgs.msg
from sphero_driver import sphero_driver
import sys


def callback(data):
    global robot
    print data.data
    eval(data.data)

def main():
    global robot
    rospy.init_node('sphero_node_adam')

    robot = sphero_driver.Sphero()
    if not robot.connect():
        sys.exit(1)

    print 'calling start()'
    #robot.start() # not necessary?
    print 'done calling start()'
    robot.set_rgb_led(0,255,0, False, False)

    print 'Starting up!'
    sub = rospy.Subscriber('/sphero', std_msgs.msg.String, callback)

    rospy.spin()

    print 'Shutting down'


if __name__ == '__main__':
    main()
