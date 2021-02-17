#!/usr/bin/env python2
import rospy
import math
from fs_msgs.msg import Track
from fs_msgs.msg import ControlCommand
from nav_msgs.msg import Odometry

class SimWrap:
    
    def __init__(self, lidarRange=10):
        print("simulator wrapper object created. call init to initialize")
        self.posX = self.posY = self.posZ = 0.0
        self.orX = self.orY = self.orZ = self.orW = 0.0
        self.cones = []
        self.lidarRange = lidarRange
        

    def init(self):
        print("#### start initialization process ####")
        
        # Get all the cones in the track by subscribing to topic /fsds/testing_only/track
        print("subscribe to: /fsds/testing_only/track")
        rospy.init_node('listener', anonymous=True, disable_signals=True)
        rospy.Subscriber("/fsds/testing_only/track", Track, self.conesCallback)
        #rospy.spin() # wait here untill the node recieved all the cones
        
        # subscribe to topic /fsds/testing_only/odom to recieve the position and orientation from the car
        rospy.Subscriber("/fsds/testing_only/odom", Odometry, self.odomCallback)

        # subscribe op topic extra info om in de reward score te weten te komen hoeveel kegels er geraakt zijn.
        # rospy.init_node('extraInfoListener', anonymous=True, disable_signals=True)
        # rospy.Subscriber("/fsds/testing_only/track", Track, self.extraInfoCallback)
    
    # action must be in the format (steering, throttle, brake) : steering -1 to 1, throttle 0 to 1, brake 0 to 1
    def step(self, action):
        print("step")
        # TODO publish action op topic control_command
        # TODO bereken de bekomen state met getVision methode
        # 
        # TODO bereken de reward

    # reset the environment
    def reset(self):
        print("reset")
        # TODO herinitialiseer alle variabelen
        # TODO ros service reset om de auto terug op de startpositie te krijgen en de simulator te resetten

    # calculate the reward the car got based on the track map en the position of the car
    def __reward(self):
        print("reward")
        # TODO alec is met deze functie bezig
        return 100

    # returns a list of cones that are close enough to the car. Based on the cone list en position of the car.
    def getVision(self): # TODO deze zal uitijndelijk private moeten worden maar heb hem public gemaakt om te testen
        conesInRange = []
        for cone in self.cones:
            if math.sqrt((cone.location.x - self.posX)**2 + (cone.location.y - self.posZ)**2) <= self.lidarRange:
                conesInRange.append(cone)
        return conesInRange

    def conesCallback(self, msg):
        print("ROS message recieved")
        self.cones = msg.track
        print(len(self.cones), "cones saved in list")
        
        # TODO vorm de positie van de kegels om naar het formaat die gebruikt kan worden in de reward functie (twee lijnen -> blokken) Alec is met deze functie bezig
        
        #rospy.signal_shutdown("don't need this node anymore")

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
        print(len(simulationWrapper.getVision()))
        #simulationWrapper.getVision()
    #rospy.spin() # deze zal er uitijndelijk uit moeten
