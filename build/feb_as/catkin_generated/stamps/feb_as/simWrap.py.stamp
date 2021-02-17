#!/usr/bin/env python
import rospy
from fs_msgs.msg import Track
from fs_msgs.msg import ControlCommand

class SimWrap:
    def __init__(self):
        ###### het is ook mogelijk om deze stappen in een andere functie te doen zodat het opbject op voorhand al aangemaakt kan worden. Ik weet niet wat het beste zou zijn. ######
        print("simulator wrapper object created. call init to initialize")

    def init(self):
        print("#### start initialization process ####")
        # Get all the cones in the track by subscribing to topic /fsds/testing_only/track
        print("subscribe to: /fsds/testing_only/track")
        rospy.init_node('trackListener', anonymous=True, disable_signals=True)
        rospy.Subscriber("/fsds/testing_only/track", Track, self.conesCallback)
        rospy.spin() # wait here untill the node recieved all the cones
        
        # vorm de positie van de kegels om naar het formaat die gebruikt kan worden in de reward functie (twee lijnen -> blokken) Alec is met deze functie bezig

        # subscribe op topic odom om de positie en de orientatie van de auto te weten te komen

        # subscribe op topic extra info om in de reward score te weten te komen hoeveel kegels er geraakt zijn.
    
    # action must be in the format (steering, throttle, brake) : steering -1 to 1, throttle 0 to 1, brake 0 to 1
    def step(self, action):
        print("step")
        # publish action op topic control_command
        # bereken de bekomen state met getVision methode
        # 
        # bereken de reward

    # reset the environment
    def reset(self):
        print("reset")
        # herinitialiseer alle variabelen
        # ros service reset om de auto terug op de startpositie te krijgen en de simulator te resetten

    # calculate the reward the car got based on the track map en the position of the car
    def __reward(self):
        print("reward")
        # alec is met deze functie bezig
        return 100

    # returns a list of cones that are close enough to the car. Based on the cone list en position of the car.
    def __getVision(self):
        print("getVision")
        # overloop elke kegel en check of deze binnen een bepaalde straal is van de auto.
        # als da is voeg die toe in een lijst
        # return conesInRange

    def conesCallback(self, msg):
        print("ROS message recieved")
        self.cones = msg.track
##        for cone in msg.track:
##            print("########")
##            print(cone.location.x)
##            print(cone.location.y)
##            print(cone.location.z)
        print(len(self.cones), "cones saved in list")
        rospy.signal_shutdown("don't need this node anymore")
        
if __name__ == '__main__':
    simulationWrapper = SimWrap()
    simulationWrapper.init()
    
        
