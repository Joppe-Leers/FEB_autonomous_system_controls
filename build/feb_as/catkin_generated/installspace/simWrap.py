#!/usr/bin/env python2
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
        self.right_list = []
        self.left_list = []
        self.passed_cone_list = []
        self.lidarRange = lidarRange
        self.lidarAngle = lidarAngle
        self.pub = 0
        self.amount_of_cones = 0
        # postition is used for the reward scores and
        self.posX = 0.0 ; self.posY = 0.0 ; self.posZ = 0.0
         
        # orientation (or), linear_acceleration (la) and angular_velocity (av) is used for the state of the car
        self.orX = 0.0 ; self.orY = 0.0 ; self.orZ = 0.0 ; self.orW = 0.0      
        self.laX = 0.0 ; self.laY = 0.0 ; self.laZ = 0.0
        self.avX = 0.0 ; self.avY = 0.0 ; self.avZ = 0.0
        
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
        #score, done = self.check_reward()
        score = 100
        done = False
        # prepare next state
        # TODO: orientation hoort niet in de state te staan
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
        self.posX = 0.0 ; self.posY = 0.0 ; self.posZ = 0.0
        self.orX = 0.0 ; self.orY = 0.0 ; self.orZ = 0.0 ; self.orW = 0.0      
        self.laX = 0.0 ; self.laY = 0.0 ; self.laZ = 0.0
        self.avX = 0.0 ; self.avY = 0.0 ; self.avZ = 0.0

    # returns a list of cones that are close enough to the car. Based on the cone list en position of the car.
    def getVision(self):
        # TODO: enkel de kegels die binnen een bepaalde hoek zijn voor de auto terug geven
        # TODO: orientation is eigenlijk alleen maar nodig 
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

    # calculate the reward the car got based on the track map en the position of the car
    #####################################
    # Returns True if the car is close  #
    #  to a reward line it hasn't passed#
    #  yet.                             #
    # Returns False otherwise.          #
    #####################################
    def check_reward(self):
        print("")
        print("calculating reward for position: " + str((self.posX,self.posY)))
        clear = False
        if(self.passed_cone_list[self.amount_of_cones - 1] == True):
            clear = True
        if(self.check_on_track()):
            for i in range(self.amount_of_cones):
                if clear == True:
                    self.passed_cone_list[i] = False
                (m, q) = self.get_function_of_reward_line(i)
                distance = self.get_distance_to_line(m, q)
                if abs(distance) < 0.1:    # if car is close to the line
                    if self.passed_cone_list[i] == False:
                        # give reward
                        print("reward incoming")
                        self.passed_cone_list[i] = True
                        return 100 , False
            
            print("I'm sad to report that you haven't earned a reward")
            return -1 , False
        else:
            print("Stay on the track!")
            # call reset
            return -100 , True

    #####################################
    # Returns the vertical distance of  #
    #  point (x,y) to the line mx+q.    #
    #####################################
    def get_distance_to_line(self, m, q):
        return self.posY - ((m*self.posX) + q)

    #####################################
    # Return the rico (m) and offset (q)#
    #  of the reward line corresponding #
    #  to the line_index'th cone on the #
    #  track (only counting one side).  #
    # mx+q                              #
    #####################################
    def get_function_of_reward_line(self, line_index):
        x1 = self.right_list[line_index][0]
        x2 = self.left_list[line_index][0]
        y1 = self.right_list[line_index][1]
        y2 = self.left_list[line_index][1]
        m = (y2-y1)/(x2-x1)
        q = y2 - m*x2
        return (m, q)

    def get_distance_to_cone(self, loc):
        conex = loc[0]
        coney = loc[1]
        return math.sqrt( (conex-self.posX)**2 + (coney-self.posY)**2 )

    #####################################
    # Check whether the car is on or off#
    #  the track.                       #
    # If car's position (x, y) are      #
    #  closer than 0.5 from position of #
    #  a cone (x_list, y_list), the car #
    #  is outside the track.            #
    #####################################
    def check_on_track(self):
        distance_list = []
        in_square_list = []
        min_distance = 100.0
        for i in range(self.amount_of_cones):
            distance_right = self.get_distance_to_cone(self.right_list[i])
            if distance_right < min_distance:
                min_distance = distance_right
                closest_cone = i
            if distance_right <= 0.5: # 0.5 is half the car width
                print("off track")
                return False
            distance_left = self.get_distance_to_cone(self.left_list[i])
            if distance_left < min_distance:
                min_distance = distance_left
                closest_cone = i
            if distance_left <= 0.5:  # 0.5 is half the car width
                print("off track")
                return False


        # get all coordinates
        cone1 = self.right_list[closest_cone]
        cone2 = self.right_list[closest_cone + 1]
        cone3 = self.left_list[closest_cone + 1]
        cone4 = self.left_list[closest_cone]
        cone5 = self.right_list[closest_cone - 1]
        cone6 = self.left_list[closest_cone - 1]
        x1 = cone1[0] ; y1 = cone1[1]
        x2 = cone2[0] ; y2 = cone2[1]
        x3 = cone3[0] ; y3 = cone3[1]
        x4 = cone4[0] ; y4 = cone4[1]
        x5 = cone5[0] ; y5 = cone5[1]
        x6 = cone6[0] ; y6 = cone6[1]

        # indicates whether (x,y) is to the left or to the right
        # credit: https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-40.php
        # first square: 1,2,3,4
        c1 = (x2-x1)*(self.posY-y1)-(y2-y1)*(self.posX-x1) 
        c2 = (x3-x2)*(self.posY-y2)-(y3-y2)*(self.posX-x2)
        c3 = (x4-x3)*(self.posY-y3)-(y4-y3)*(self.posX-x3)
        c4 = (x1-x4)*(self.posY-y4)-(y1-y4)*(self.posX-x4)
        if (c1<=0 and c2<=0 and c3<=0 and c4<=0) or (c1>=0 and c2>=0 and c3>=0 and c4>=0): # TODO check if we kan drop the second condition
            in_square_list.append(True)
        else:
            in_square_list.append(False)

        # second square: 1,4,5,6
        c1 = (x4-x1)*(self.posY-y1)-(y4-y1)*(self.posX-x1) 
        c2 = (x6-x4)*(self.posY-y4)-(y6-y4)*(self.posX-x4)
        c3 = (x5-x6)*(self.posY-y6)-(y5-y6)*(self.posX-x6)
        c4 = (x1-x5)*(self.posY-y5)-(y1-y5)*(self.posX-x5)
        if (c1<=0 and c2<=0 and c3<=0 and c4<=0) or (c1>=0 and c2>=0 and c3>=0 and c4>=0): # TODO check if we kan drop the second condition
            in_square_list.append(True)
        else:
            in_square_list.append(False)

        for i in range(2):
            if in_square_list[i] == True:
                print("on track")
                return True
        print("off track")
        return False
    
    def conesCallback(self, msg):
        self.cones = msg.track
        for cone in self.cones:
            location = [cone.location.x, cone.location.y]
            if cone.color == 1:
                self.right_list.append(location)
            elif cone.color == 0:
                self.left_list.append(location)
        for _ in self.right_list:
            self.passed_cone_list.append(False)
        self.amount_of_cones = len(self.right_list)
        print(self.amount_of_cones)
        
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

    #####################################
    # Plot the boundaries of the track. #
    #   Left in blue, right in yellow.  #
    #####################################
    # This function is not used during training
    def plot(self):
        right_x_list = []
        left_x_list = []
        right_y_list = []
        left_y_list = []
        # Preprocess data
        for loc in self.right_list:
            right_x_list.append(loc[0])
            right_y_list.append(loc[1])
        for loc in self.left_list:
            left_x_list.append(loc[0])
            left_y_list.append(loc[1])
            
        # Add first cone again to complete the "circle"
        right_x_list.append(right_x_list[0])
        left_x_list.append(left_x_list[0])
        right_y_list.append(right_y_list[0])
        left_y_list.append(left_y_list[0])

        # Plot lines
        plt.plot(left_x_list, left_y_list, 'b-') # b- means blue line
        plt.plot(right_x_list, right_y_list, 'y-') # y- means yellow line

        for i in range(len(right_x_list)):
            x = [left_x_list[i], right_x_list[i]]
            y = [left_y_list[i], right_y_list[i]]
            plt.plot(x, y, 'g-')

        #plt.savefig('/mnt/c/FEB_autonomous_system_controls/cones.jpg')
        plt.savefig('cones.jpg')
        
if __name__ == '__main__':
    simulationWrapper = SimWrap()
    simulationWrapper.init()
    time.sleep(5)
    count = 0
    while count <=200:
        count += 1
        state, score, done = simulationWrapper.step([-1.0,0.5,0.0])
        print("step count: ", state , score, done)
        time.sleep(0.1)
        
    rospy.spin() # deze zal er uitijndelijk uit moeten
