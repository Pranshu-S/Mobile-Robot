#include<iostream>
#include<ros/ros.h>
#include<geometry_msgs/Twist.h>
#include<geometry_msgs/Point.h>
#include<nav_msgs/Odometry.h>
#include<tf/tf.h>
#include<math.h>

double x, y, theta;

void callback(const nav_msgs::Odometry::ConstPtr& msg)
{
    double roll, pitch;
    tf::Quaternion q(msg->pose.pose.orientation.x, msg->pose.pose.orientation.y, msg->pose.pose.orientation.z, msg->pose.pose.orientation.w);
    tf::Matrix3x3 matrix(q);
    matrix.getRPY(roll, pitch, theta);
    x = msg->pose.pose.position.x;
    y = msg->pose.pose.position.y;
}

int main(int argc, char **argv)
{
    double k_angular = 1.0, k_linear = 0.25, e_x, e_y, e_theta, e_linear, theta_d;
    ros::init(argc, argv, "go_to_goal");
    ros::NodeHandle n;
    ros::Publisher pub = n.advertise<geometry_msgs::Twist>("/cmd_vel",1000);
    ros::Subscriber sub = n.subscribe("/odom", 1000, callback); 
    ros::Rate rate(10);
    geometry_msgs::Twist vel;
    geometry_msgs::Point goal;
    std::cout<<"Enter x - coordinate of goal: ";
    std::cin>>goal.x;
    std::cout<<"Enter y - coordinate of goal: ";
    std::cin>>goal.y;
    while(ros::ok())
    {
        e_x = goal.x - x;
        e_y = goal.y - y;
        e_linear = sqrt(pow(e_x,2) + pow(e_y,2));
        theta_d = atan2(e_y,e_x);
        e_theta = theta_d - theta;
        e_theta = atan2(sin(e_theta),cos(e_theta));
        vel.linear.x = k_linear*e_linear;
        vel.angular.z = k_angular*e_theta;
        pub.publish(vel);
        rate.sleep();
        ros::spinOnce();
    }
    vel.linear.x = 0.0;
    vel.angular.z = 0.0;
    pub.publish(vel);
    return 0;
}