#!/usr/bin/env python2
import rospy
import math
from fs_msgs.msg import Track
from fs_msgs.msg import ControlCommand
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import time

class SimWrap:
    
    def __init__(self, lidarRange=10):
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        self.cones = []
        self.lidarRange = lidarRange
        

    def init(self):
        rospy.init_node('FEB_autonomous_system', anonymous=True, disable_signals=True)
        rospy.Subscriber("/fsds/testing_only/track", Track, self.conesCallback)        
        rospy.Subscriber("/fsds/testing_only/odom", Odometry, self.odomCallback)
        rospy.Subscriber("/fsds/imu", Imu, self.imuCallback)
    
    # action must be in the format (steering, throttle, brake) : steering -1 to 1, throttle 0 to 1, brake 0 to 1
    def step(self, action):
        print("step")
        # TODO publish action op topic control_command
        # TODO bereken de bekomen state met getVision methode
        # TODO bereken de reward

    # reset the environment
    def reset(self):
        print("reset")
        # TODO herinitialiseer alle variabelen
        # TODO ros service reset om de auto terug op de startpositie te krijgen en de simulator te resetten

    # calculate the reward the car got based on the track map en the position of the car
    def __reward(self):
        print("reward")
        return 100

    # returns a list of cones that are close enough to the car. Based on the cone list en position of the car.
    def __getVision(self):
        conesInRange = []
        for cone in self.cones:
            if math.sqrt((cone.location.x - self.posX)**2 + (cone.location.y - self.posY)**2) <= self.lidarRange:
                conesInRange.append(cone)
        return conesInRange
    
    def conesCallback(self, msg):
        self.cones = msg.track            
    
    def odomCallback(self, msg):
        # update the variables
        self.posX = msg.pose.pose.position.x
        self.posY = msg.pose.pose.position.y
        self.posZ = msg.pose.pose.position.z

    def imuCallback(self, msg):
        print("orientation" , msg.orientation.x, msg.orientation.y,msg.orientation.z, msg.orientation.w)
        print("angular vel" , msg.angular_velocity.x, msg.angular_velocity.y,msg.angular_velocity.z)
        print("linear acc" , msg.linear_acceleration.x, msg.linear_acceleration.y,msg.linear_acceleration.z)
        
if __name__ == '__main__':
    simulationWrapper = SimWrap()
    simulationWrapper.init()
    rospy.spin() # deze zal er uitijndelijk uit moeten
