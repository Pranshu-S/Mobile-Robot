#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def spiral():
    rospy.init_node('spiral_node',anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    velocity = Twist()
    rate = rospy.Rate(10)
    rospy.loginfo('Moving Bot in Spiral')
    radius = 0.1

    while not rospy.is_shutdown():
        velocity.linear.x = 0.4
        velocity.angular.z = 0.4/radius
        pub.publish(velocity)
        rate.sleep()
        radius += 0.01
    
    velocity.linear.x = 0
    velocity.angular.z = 0
    pub.publish(velocity)

if __name__=='__main__':
    try:
        spiral()
    except rospy.ROSInterruptException:
        pass