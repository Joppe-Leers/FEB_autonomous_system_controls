#!/usr/bin/env python2
# license removed for brevity
import rospy
from fs_msgs.msg import ControlCommand

def talker():
    pub = rospy.Publisher('/fsds/control_command', ControlCommand, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        print("while")
        pub.publish(throttle=0.5, steering=-1.0, brake=0.0)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
