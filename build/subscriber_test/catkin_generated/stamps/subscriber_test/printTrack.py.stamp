#!/usr/bin/env python
import rospy
from fs_msgs.msg import Track

def callback(msg):
    for cone in msg.track:
        print("########")
        print(cone.location.x)
        print(cone.location.y)
        print(cone.location.z)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/fsds/testing_only/track", Track, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
