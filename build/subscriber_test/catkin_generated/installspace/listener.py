#!/usr/bin/env python2
import rospy
from fs_msgs.msg import Track
from nav_msgs.msg import Odometry

def callback(msg):
    print(msg.pose.pose)
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg.data)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/fsds/testing_only/odom", Odometry, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print("before istener")
    listener()
    print("after istener")
