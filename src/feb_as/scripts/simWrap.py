#!/usr/bin/env python
import rospy
import math
from fs_msgs.msg import Track
from fs_msgs.msg import ControlCommand
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from fs_msgs.msg import Cone
from fs_msgs.srv import Reset

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import time

class SimWrap:
    
    def __init__(self, lidarRange=10, lidarAngle = 180):
        self.cones = []
        self.lidarRange = lidarRange
        self.lidarAngle = lidarAngle
        self.pub = 0
        # postition is used or the reward scores
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        # orientation (or), linear_acceleration (la) and angular_velocity (av) is used for the state of the car
        self.orX = 0.0
        self.orY = 0.0
        self.orZ = 0.0
        self.orW = 0.0
        self.laX = 0.0
        self.laY = 0.0
        self.laZ = 0.0
        self.avX = 0.0
        self.avY = 0.0
        self.avZ = 0.0
        
    # initialize the ros node that receives the sensor information and sends control commands
    def init(self):
        rospy.init_node('FEB_autonomous_system', anonymous=True, disable_signals=True)
        rospy.Subscriber("/fsds/testing_only/track", Track, self.conesCallback)        
        rospy.Subscriber("/fsds/testing_only/odom", Odometry, self.odomCallback)
        rospy.Subscriber("/fsds/imu", Imu, self.imuCallback)
        self.pub = rospy.Publisher('/fsds/control_command', ControlCommand, queue_size=3)

        # action must be in the format (steering, throttle, brake) : steering -1 to 1, throttle 0 to 1, brake 0 to 1
    def step(self, action):
        self.pub.publish(steering=action[0], throttle=action[1],brake=action[2])
        score, done = self.reward()
        # prepare next state
        state = [self.orX, self.orY, self.orZ, self.orW, self.laX, self.laY, self.laZ ,self.avX, self.avY, self.avZ]
        for cone in self.getVision():
            state.append(cone.location.x)
            state.append(cone.location.y)
            state.append(cone.color)

        return state, score, done

    # reset the environment
    def reset(self):
        # reset the simulator using service /fsds/reset
        rospy.wait_for_service('/fsds/reset')
        try:
            reset = rospy.ServiceProxy('/fsds/reset', Reset)
            reset(True)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

        # reinitialize class parameters
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        self.orX = 0.0
        self.orY = 0.0
        self.orZ = 0.0
        self.orW = 0.0
        self.laX = 0.0
        self.laY = 0.0
        self.laZ = 0.0
        self.avX = 0.0
        self.avY = 0.0
        self.avZ = 0.0
        
    # calculate the reward the car got based on the track map en the position of the car
    def reward(self):
        #print("reward")
        return 100, False

    # returns a list of cones that are close enough to the car. Based on the cone list en position of the car.
    def getVision(self):
        # TODO: enkel de kegels die binnen een bepaalde hoek zijn voor de auto terug geven
        conesInRange = []
        for cone in self.cones:
            if math.sqrt((cone.location.x - self.posX)**2 + (cone.location.y - self.posY)**2) <= self.lidarRange:
                # calculate position (x,y,z) from the cone relative to the car
                tempcone = Cone()
                tempcone.location.x = cone.location.x - self.posX
                tempcone.location.y = cone.location.y - self.posY
                tempcone.location.z = cone.location.z - self.posZ
                tempcone.color = cone.color
                conesInRange.append(tempcone)
        return conesInRange

    
    def conesCallback(self, msg):
        self.cones = msg.track

        
    def odomCallback(self, msg):
        self.posX = msg.pose.pose.position.x
        self.posY = msg.pose.pose.position.y
        self.posZ = msg.pose.pose.position.z

    def imuCallback(self, msg):
        self.orX = msg.orientation.x
        self.orY = msg.orientation.y
        self.orZ = msg.orientation.z
        self.orW = msg.orientation.w
        self.laX = msg.linear_acceleration.x
        self.laY = msg.linear_acceleration.y
        self.laZ = msg.linear_acceleration.z
        self.avX = msg.angular_velocity.x
        self.avY = msg.angular_velocity.y
        self.avZ = msg.angular_velocity.z
        
if __name__ == '__main__':
    simulationWrapper = SimWrap()
    simulationWrapper.init()
    count = 0
    while count <=200:
        count+=1
        simulationWrapper.step([-1,0.5,0])
        time.sleep(0.1)
    simulationWrapper.reset()
    rospy.spin() # deze zal er uitijndelijk uit moeten
