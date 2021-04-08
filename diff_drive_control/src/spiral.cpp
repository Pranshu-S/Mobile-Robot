#include<ros/ros.h>
#include<geometry_msgs/Twist.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "spiral_node");
    ros::NodeHandle n;
    ros::Publisher pub = n.advertise<geometry_msgs::Twist>("/cmd_vel",1000);
    ros::Rate rate(10);
    geometry_msgs::Twist vel;
    ROS_INFO("Moving the bot.");
    float r = 0.1;
    while(ros::ok())
    {
        vel.linear.x = 0.4;
        vel.angular.z = 0.4/r;
        pub.publish(vel);
        r += 0.01;
        ros::spinOnce();
        rate.sleep();
    }

    ROS_INFO("Stopping the bot."); 
    return 0;
}