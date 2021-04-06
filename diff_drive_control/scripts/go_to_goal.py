#!/usr/bin/env python2.7

import rospy
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sin, cos, sqrt

x = y = theta = 0.0

def callback(data):
    global x, y, theta
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    q = data.pose.pose.orientation
    (_, _, theta) = euler_from_quaternion([q.x, q.y, q.z, q.w])

def move_bot():
    global x, y, theta
    k_linear = 0.25
    k_angular = 1.0
    rospy.init_node('go_to_goal', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, callback)
    vel = Twist()
    goal = Point()
    rate = rospy.Rate(10)
    goal.x = float(input('Enter x - coordinate of goal: '))
    goal.y = float(input('Enter y - coordinate of goal: '))
    while not rospy.is_shutdown():
        e_y = goal.y - y
        e_x = goal.x - x
        e_linear = sqrt(e_x**2 + e_y**2)
        theta_desired = atan2(e_y,e_x)
        e_theta = theta_desired - theta
        e_theta = atan2(sin(e_theta),cos(e_theta))
        vel.angular.z = k_angular*e_theta
        vel.linear.x = k_linear*e_linear
        pub.publish(vel)
        rate.sleep()
    vel.linear.x = 0.0
    vel.angular.z  = 0.0
    pub.publish(vel)

if __name__=='__main__':
    try:
        move_bot()
    except rospy.ROSInterruptException:
        pass