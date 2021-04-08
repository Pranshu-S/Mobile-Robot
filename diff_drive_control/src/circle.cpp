#include<ros/ros.h>
#include<geometry_msgs/Twist.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "circle_node");
    ros::NodeHandle n;
    ros::Publisher pub = n.advertise<geometry_msgs::Twist>("/cmd_vel",1000);
    ros::Rate rate(10);
    ROS_INFO("Moving the bot.");
    int radius = 1;
    while(ros::ok())
    {
        geometry_msgs::Twist vel;
        vel.linear.x = 0.4;
        vel.angular.z = 0.4/radius;
        pub.publish(vel);
        ros::spinOnce();
        rate.sleep();
    }
    ROS_INFO("Stopping the bot."); 
    return 0;
}