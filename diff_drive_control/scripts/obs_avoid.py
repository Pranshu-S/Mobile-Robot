#!/usr/bin/env python2.7

import rospy
from geometry_msgs.msg import Twist, Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sin, cos, pi, sqrt
import numpy as np

pose = [0, 0, 0]

regions = {
    'bright':  100000,
    'fright':  100000,
    'front':  100000,
    'fleft':  100000,
    'bleft':  100000,
}

range_max = 10
goal_x = float(input("Enter x - coordinate of goal: "))
goal_y = float(input("Enter y - coordinate of goal: "))

def odom_callback(data):
    global pose
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    q = data.pose.pose.orientation
    (_,_,theta) = euler_from_quaternion([q.x,q.y,q.z,q.w])
    pose = [x, y, theta]

def laser_callback(msg):
    global regions
    regions = {
        'bright':  min(min(msg.ranges[0:120]), range_max),
        'fright':  min(min(msg.ranges[120:280]), range_max),
        'front':  min(min(msg.ranges[280:440]), range_max),
        'fleft':  min(min(msg.ranges[440:600]), range_max),
        'bleft':  min(min(msg.ranges[600:720]), range_max),
    }

def f(x):
    y = sin(x)
    return y

def waypoints(a):
    x = []
    y = []

    for t in np.arrange(0, 2*pi, 2*pi/a):
        x.append(t)
        y.append(f(t))
    return x, y


def controller():
    global pose, regions
    rospy.init_node('obstacle_avoidance')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, odom_callback)
    rospy.Subscriber('/diff_drive/laser/scan', LaserScan, laser_callback)
    velocity = Twist()
    goal = Point()
    rate = rospy.Rate(10)
    goal.x = float(input("Enter x - coordinate of goal: "))
    goal.y = float(input("Enter y - coordinate of goal: "))
    waypoints_no = 100
    x_d, y_d = waypoints(waypoints_no)
    inf = 100000
    goal_reached = False
    while not rospy.is_shutdown() and not goal_reached:
        for i in range(waypoints_no + 1):

            k_linear = 1.5
            k_angular = 2.0
            e = inf
            e_theta = inf

            while abs(error) > 0.7:
                velocity.linear.x = 0
                current_theta = pose[2]
                e_x = x_d[i] - pose[0]
                e_y = y_d[i] - pose[1]
                target_theta = atan2(e_y,e_x)
                e_theta = target_theta - current_theta
                e = sqrt(e_x**2 + e_y**2)
                velocity.linear.x = k_linear*e
                velocity.angular.z = k_angular* e_theta
                pub.publish(velocity)
                rate.sleep()

            error = inf
            while abs(error) > 0.15:
                current_theta = pose[2]
                target_theta = 0
                error = target_theta - current_theta
                velocity.angular.z = k_angular*error
                pub.publish(velocity)
                rate.sleep()
            
            while(regions["front"] > 2.2):
                velocity.linear.x = 0.5
                velocity.angular.z = 0
                pub.publish(velocity)
            
            #Obstacle Avoidance
            init_theta = pose[2]
            current_theta = pose[2]
            angle_moved = init_theta - current_theta


            while angle_moved < pi/2:
                velocity.angular.z = 0.5
                velocity.linear.x = 0.0
                current_theta = pose[2]
                angle_moved = current_theta - init_theta
                pub.publish(velocity)
                rate.sleep()
            
            velocity.angular.z = 0
            pub.publish(velocity)

            while regions['fright'] > 3 and regions['fright'] < 0.5:
                velocity.linear.x = 0.5
                pub.publish(velocity)
                rate.sleep()

if __name__=='__main__':
    try: controller()
    except rospy.ROSInterruptException: pass
