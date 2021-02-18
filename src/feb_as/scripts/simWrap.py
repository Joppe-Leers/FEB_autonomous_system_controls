#!/usr/bin/env python
import rospy
import math
from fs_msgs.msg import Track
from fs_msgs.msg import ControlCommand
from nav_msgs.msg import Odometry

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
        self.orX = 0.0
        self.orY = 0.0
        self.orZ = 0.0
        self.orW = 0.0
        self.cones = []
        self.lidarRange = lidarRange
        

    def init(self):
        rospy.init_node('listener', anonymous=True, disable_signals=True)
        rospy.Subscriber("/fsds/testing_only/track", Track, self.conesCallback)        
        rospy.Subscriber("/fsds/testing_only/odom", Odometry, self.odomCallback)
    
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
    def getVision(self): # TODO deze zal uitijndelijk private moeten worden maar heb hem public gemaakt om te testen
        print("get vision")
        conesInRange = []
        #count = 0
        for cone in self.cones:
            #count += 1
            if math.sqrt((cone.location.x - self.posX)**2 + (cone.location.y - self.posY)**2) <= self.lidarRange:
                print(math.sqrt((cone.location.x - self.posX)**2 + (cone.location.y - self.posY)**2))
                conesInRange.append(cone)
            #print("cheking distance cone " + str(count) + ": " + str(math.sqrt((cone.location.x - self.posX)**2 + (cone.location.y - self.posZ)**2)))
        return conesInRange

    def conesCallback(self, msg):
        self.cones = msg.track
        # TODO vorm de positie van de kegels om naar het formaat die gebruikt kan worden in de reward functie (twee lijnen -> blokken) Alec is met deze functie bezig
        
##        x = []
##        y = []
##        for cone in self.cones:
##            print(cone.location.x , cone.location.y)
##            x.append(cone.location.x)
##            y.append(cone.location.y)
##        print("###########################################")
##        for i in range(0, len(x)):
##            print(x[i], y[i])
##        plt.scatter(x, y)
##        plt.savefig('cones.jpg')
            
    
    def odomCallback(self, msg):
        # update the variables
        #print(msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z)
        self.posX = msg.pose.pose.position.x
        self.posY = msg.pose.pose.position.y
        self.posZ = msg.pose.pose.position.z
        self.orX = msg.pose.pose.orientation.x
        self.orY = msg.pose.pose.orientation.y
        self.orZ = msg.pose.pose.orientation.z
        self.orW = msg.pose.pose.orientation.w
        
if __name__ == '__main__':
    simulationWrapper = SimWrap()
    simulationWrapper.init()
    while True:
        conesClose = simulationWrapper.getVision()
        print(len(conesClose))
        x = []
        y = []
        for cone in conesClose:
            x.append(cone.location.x)
            y.append(cone.location.y)
        plt.scatter(x, y)
        plt.scatter(simulationWrapper.posX, simulationWrapper.posY)
        plt.savefig('vision.jpg')
        plt.close()
        time.sleep(5)
        
        #simulationWrapper.getVision()
    #rospy.spin() # deze zal er uitijndelijk uit moeten
