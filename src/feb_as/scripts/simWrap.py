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
    """Help of the simulationWrapper class

    This class provides an easy to use interface to test deep reinforcement algorithms on the
    Formula student driverless simulater. It folows the same structure as openAI gym uses
    https://gym.openai.com/
    
    The class contains three main functions that must be used in the RL algorithm:
    init()
    state, score, done = step(action)
    reset()
    
    See documentation in the methods itself for more information
    
    State:
    The state is a list with length 3*maxConesInState + 6. Every cone in the vision of the car
    is put in the list with its x, y value and the color. the six aditional features are for odometry data
    
    Score:
    score is calculated in the get_reward method and...
    
    TODO: Alec geeft gij hier wat meer uitleg bij?
    """
    
    def __init__(self, lidarRange=20, maxConesInState = 20):
        self.cones = []
        self.lidarRange = lidarRange
        self.pub = 0
        self.receivedTrack = False 
        self.next_cone = 0
        self.maxConesInState = maxConesInState
        self.stateLenght = maxConesInState * 3 + 6
        self.episode_length = 0
        
        # postition is used for the reward scores and
        self.posX = 0.0 ; self.posY = 0.0 ; self.posZ = 0.0
         
        # orientation (or), linear_acceleration (la) and angular_velocity (av) is used for the state of the car
        self.orX = 0.0 ; self.orY = 0.0 ; self.orZ = 0.0 ; self.orW = 0.0      
        self.laX = 0.0 ; self.laY = 0.0 ; self.laZ = 0.0
        self.avX = 0.0 ; self.avY = 0.0 ; self.avZ = 0.0
        
        self.right_list = []
        self.left_list = []
        self.passed_cone_list = [] # boolean list: True = car has passed this cone
        self.amount_of_cones = 0
        
    def init(self):
        """Initialises the ROS node that receives the sensor information and sends control commands and subscribe on the right topics."""

        rospy.init_node('FEB_autonomous_system', anonymous=True, disable_signals=True)

        rospy.Subscriber("/fsds/testing_only/track", Track, self.__conesCallback)
        # wait until simulation wrapper recieved the full track information
        while not self.receivedTrack:
            pass
        
        rospy.Subscriber("/fsds/testing_only/odom", Odometry, self.__odomCallback)
        rospy.Subscriber("/fsds/imu", Imu, self.__imuCallback)
        self.pub = rospy.Publisher('/fsds/control_command', ControlCommand, queue_size=3)

    def step(self, action):
        """Takes a step, according to the input action.

        Action must be in the format (steering, throttle, brake)  in ranges: steering -1 to 1, throttle 0 to 1, brake 0 to 1.
        Returns a tuple (state, score, done), indicating the new state of the car in its environment,
        the score received for the step and whether or not the episode is finished. 
        """

        self.pub.publish(steering=action[0], throttle=action[1],brake=action[2])
        score, done = self.__check_reward()
        state = []
        vision = self.__getVision()
        for count in range(0,self.maxConesInState):
            if count <= len(vision)-1:
                state += [vision[count].location.x, vision[count].location.y, vision[count].color]
            else:
                state += [0,0,0]            
        state += [self.laX, self.laY, self.laZ ,self.avX, self.avY, self.avZ]        
            
        return state, score, done

    def reset(self):
        """Resets the environment. The simulator will be reset and some parameters will be reinitialised."""
        
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

        self.next_cone = 0
        for i in range(self.amount_of_cones):
            self.passed_cone_list[i] = False

        self.episode_length = 0
            

    def __getVision(self):
        """Returns a list of cones that are inside the lidar range (a class parameter). It calculates this based on the cone list en position of the car."""
        
        conesInRange = []
        for cone in self.cones:
            if distance([cone.location.x, cone.location.y], [self.posX, self.posY]) <= self.lidarRange:
                # calculate position (x,y,z) of cone and rotate relative to the car
                vec = rotateVector([cone.location.x - self.posX,
                                    cone.location.y - self.posY,
                                    cone.location.z - self.posZ],
                                   [self.orW, self.orX, self.orY, -self.orZ])
                # back wing of feb's car blocks the vision behind the car for the lidar
                # -> only the cones within an angle of 180 degree in front of the car is seen
                if vec[0] >= 0:
                    tempcone = Cone()
                    tempcone.location.x = vec[0]
                    tempcone.location.y = vec[1]
                    tempcone.location.z = vec[2]
                    tempcone.color = cone.color
                    conesInRange.append(tempcone)
        return conesInRange    

    def __check_reward(self):
        """Calculates the reward the car got based on the track map and the position of the car
        Returns True if the car is close to a reward line it hasn't passed yet.                             
        Returns False otherwise."""
        
        clear = False
        min_distance = 1000
        cone = 0
        self.episode_length += 1
        if self.episode_length > 450:
            return -10, True
        if(self.passed_cone_list[self.amount_of_cones - 1] == True):
            clear = True
        if(self.__check_on_track()):
            for i in range(self.amount_of_cones):
                if clear == True:
                    self.passed_cone_list[i] = False
                    if(i == self.amount_of_cones -1):
                        self.next_cone = 0
            (m,q) = self.__get_function_of_reward_line(self.next_cone)
            distance = self.__get_distance_to_line(m, q)
            if abs(distance) < 3:    # if car is close to the line
                if self.passed_cone_list[self.next_cone] == False:
                    # give reward
                    self.passed_cone_list[self.next_cone] = True
                    self.next_cone +=1
                    print("Have a cookie!")
                    return 5 , False
            
            return -0.3 , False
        else:
            return -10 , True

    def __get_distance_to_line(self, m, q):
        """Returns the perpendicular distance between the position of the car (self.posX, self.posY) and the line mx+q."""
        
        root = math.sqrt(m**2 + 1)
        return abs(m*self.posX - self.posY + q)/root

    def __get_function_of_reward_line(self, line_index):
        """Return the rico (m) and offset (q) of the reward line corresponding to the line between the line_index'th
        cones on the left and right side of the track."""
        
        x1 = self.right_list[line_index][0]
        x2 = self.left_list[line_index][0]
        y1 = self.right_list[line_index][1]
        y2 = self.left_list[line_index][1]
        m = (y2-y1)/(x2-x1)
        q = y2 - m*x2
        return (m, q)

    def __check_on_track(self):
        """Checks whether the car is on or off the track. If car's position (x, y) is closer than 0.5m from the
        position of a cone (x_list, y_list), the car is outside the track, as the car is 0.5m wide on both sides."""
        
        distance_list = []
        in_square_list = []
        min_distance = 100.0
        for i in range(self.amount_of_cones):
            distance_right = distance([self.right_list[i][0], self.right_list[i][1]], [self.posX, self.posY])
            if distance_right < min_distance:
                min_distance = distance_right
                closest_cone = i
            if distance_right <= 0.7: # 0.5 is half the car width
                return False
            distance_left = distance([self.left_list[i][0], self.left_list[i][1]], [self.posX, self.posY])
            if distance_left < min_distance:
                min_distance = distance_left
                closest_cone = i
            if distance_left <= 0.7:  # 0.5 is half the car width
                return False


        # get all coordinates
        cone1 = self.right_list[closest_cone]
        if closest_cone == self.amount_of_cones-1:
            cone2 = self.right_list[0]
            cone3 = self.left_list[0]
        else:
            cone2 = self.right_list[closest_cone + 1]
            cone3 = self.left_list[closest_cone + 1]
        cone4 = self.left_list[closest_cone]
        if closest_cone == 0:
            cone5 = self.right_list[self.amount_of_cones-1]
            cone6 = self.left_list[self.amount_of_cones-1]
        else:
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
                return True
        return False

    def __conesCallback(self, msg):
        """setup right/left cone list, passed cone list and other class variables."""
        self.cones = msg.track
        for cone in self.cones:
            location = [cone.location.x, cone.location.y]
            if cone.color == 1:
                self.right_list.append(location)
            elif cone.color == 0:
                self.left_list.append(location)
        for _ in range(2):
            for i in range(0, len(self.right_list), 2):
                avg_loc_right = [(self.right_list[i][0] + self.right_list[i+1][0])/2,
                           (self.right_list[i][1] + self.right_list[i+1][1])/2]
                avg_loc_left = [(self.left_list[i][0] + self.left_list[i+1][0])/2,
                           (self.left_list[i][1] + self.left_list[i+1][1])/2]
                self.right_list.insert(i+1, avg_loc_right)
                self.left_list.insert(i+1, avg_loc_left)
        
        for _ in self.right_list:
            self.passed_cone_list.append(False)
        self.amount_of_cones = len(self.right_list)
        self.receivedTrack = True

    def __odomCallback(self, msg):
        """update car position"""
        
        self.posX = msg.pose.pose.position.x + 1.98257 # Simulator bug: offset of 1.98257 on the X-axis
        self.posY = msg.pose.pose.position.y
        self.posZ = msg.pose.pose.position.z

    def __imuCallback(self, msg):
        """update car orientation (or), linear_acceleration (la) and angular_velocity (av)"""
        
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

    def plot(self):
        """Plots the boundaries of the track. Left in blue, right in yellow.
        This function is not used during training, merely for documentation purposes."""
        
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
        plt.savefig('cones.jpg')


#################### EXTRA FUNCTIONS ####################

def rotateVector(vec, q):
    """Rotates a 3D (vec) with the quaternion rotation vector (q)."""
    
    r = [0]+vec
    q_conj = [q[0],-1*q[1],-1*q[2],-1*q[3]]
    return hamiltonProduct(hamiltonProduct(q,r),q_conj)[1:]

def hamiltonProduct(q,r):
    """Returns the Hamilton product, calculating the product between two quaternions."""

    return [r[0]*q[0]-r[1]*q[1]-r[2]*q[2]-r[3]*q[3],
            r[0]*q[1]+r[1]*q[0]-r[2]*q[3]+r[3]*q[2],
            r[0]*q[2]+r[1]*q[3]+r[2]*q[0]-r[3]*q[1],
            r[0]*q[3]-r[1]*q[2]+r[2]*q[1]+r[3]*q[0]]


def distance(p1,p2):
    """calculate distance between [x1,y1] and [x2, y2]"""
    
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

