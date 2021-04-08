#!/usr/bin/env python2.7

import rospy
from geometry_msgs.msg import Twist, Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sin, cos, pi, sqrt

pose = [0, 0, 0]

regions = {
    'bright':  100000,
    'fright':  100000,
    'front':  100000,
    'fleft':  100000,
    'bleft':  100000,
}

def odom_callback(data):
    global pose
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    q = data.pose.pose.orientation
    (_,_,theta) = euler_from_quaternion([q.x,q.y,q.z,q.w])
    pose = [x, y, theta]

def laser_callback(data):
    regions = {
            'right':  min(min(data.ranges[0:143]), 10),
            'fright': min(min(data.ranges[144:287]), 10),
            'front':  min(min(data.ranges[288:431]), 10),
            'fleft':  min(min(data.ranges[432:575]), 10),
            'left':   min(min(data.ranges[576:713]), 10),
        }

def controller():
    rospy.init_node('obstacle_avoidance')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, odom_callback)
    rospy.Subscriber('/diff_drive/laser/scan', LaserScan, laser_callback)
    velocity = Twist()
    goal = Point()
    goal.x = float(input("Enter x - coordinate of goal: "))
    goal.y = float(input("Enter y - coordinate of goal: "))
    velocity.linear.x = 0
    velocity.angular.z = 0
    pub.publish(velocity)


if __name__=='__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass