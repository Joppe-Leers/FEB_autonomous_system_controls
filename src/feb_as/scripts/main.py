#!/usr/bin/env python
from DQLalgorithm import DQLalgorithm
from simWrap import SimWrap

import time
import rospy
from fs_msgs.msg import Cone

from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# if __name__ == '__main__':
    # fig = plt.figure(1, figsize=(5,5), dpi=90)
    # ring_mixed = Polygon([[0, 0], [0, 2], [1, 1], [2, 2], [2, 0], [1, 0.8], [0, 0]])
    # ax = fig.add_subplot(111)
    # ring_patch = PolygonPatch(ring_mixed)
    # ax.add_patch(ring_patch)

    # #ax.set_title('Filled Polygon')
    # xrange = [-1, 3]
    # yrange = [-1, 3]
    # ax.set_xlim(*xrange)
    # ax.set_xticks(range(*xrange) + [xrange[-1]])
    # ax.set_ylim(*yrange)
    # ax.set_yticks(range(*yrange) + [yrange[-1]])
    # ax.set_aspect(1)
    # plt.savefig('test.jpg')
    # print(type(fig))



if __name__ == '__main__':
    dql = DQLalgorithm()
    dql.trainModel(episodes=5000, trainingBatchSize=64, updateTargetModelFreq=5, saveModelFreq=25)
    #dql.testModel(modelFile='trial_25.h5', episodes=5, skipFrames=2)
    
# if __name__ == '__main__':
    # simulationWrapper = SimWrap(manualControl=True)
    # simulationWrapper.init()
    # time.sleep(2)
    # conesInRange = simulationWrapper.getVision()
    
    # fig = plt.figure(1, figsize=(5,5), dpi=90)
    # corners = []
    # for cone in conesInRange:
        # corners.append([cone.location.x, cone.location.y])
    # corners = [[0.6010912190317252, -1.78116357375305], [4.603902789900433, -2.1740807248478333], [8.696386558638842, -2.4562175542791644], [12.987956604845566, -2.2595657828219062], [17.369157630931024, -0.9455087625789156], [0.9483830962286406, 1.7015555367251491], [4.9214907470217, 1.3114879069802523], [8.81864076698169, 1.041653547387591], [12.489172866966046, 1.2047150205152473], [15.752697043903241, 2.1588476806766623], [18.45835881152536, 4.384421506961106]]
    # print(corners)
    # ax = fig.add_subplot(111)
    # ring_patch = PolygonPatch(Polygon(corners))
    # ax.add_patch(ring_patch)
    # #ax.set_title('Filled Polygon')
    # xrange = [0, 20]
    # yrange = [-20, 20]
    # ax.set_xlim(*xrange)
    # ax.set_xticks(range(*xrange) + [xrange[-1]])
    # ax.set_ylim(*yrange)
    # ax.set_yticks(range(*yrange) + [yrange[-1]])
    # ax.set_aspect(1)
    # plt.savefig('test.jpg')            
                
                
                
                
                
     
    # plt.scatter(x_right, y_right, color='yellow', label='right cone')
    # plt.scatter(x_left, y_left, color='blue', label='left cone')
    # plt.scatter(0, 0, color='red', label='car')
    # plt.xlim([0,simulationWrapper.lidarRange])
    # plt.ylim([-simulationWrapper.lidarRange, simulationWrapper.lidarRange])
    # #plt.legend(loc="upper left")
    # #plt.xlabel('distance (meter)')
    # #plt.ylabel('distance (meter)')
    # plt.savefig('vision.jpg')
    # plt.close()
    # print("start spinning")
    # rospy.spin()
    #while True:
        #nextState, r, done = simulationWrapper.step([0,0,0])
        #print("state: " + str(len(nextState)) + " r: " + str(r) + " done: " + str(done))
        
        # cones = nextState[:len(nextState)-6]
        # x = []
        # y = []
        # for i in range(0,len(cones),3):
            # x.append(cones[i])
            # y.append(cones[i+1])
        # plt.scatter(x,y)
        # plt.savefig('vision.jpg')
        # plt.close()
        
        # cones = nextState[:len(nextState)-6]
        # x_blue = []
        # y_blue = []
        # x_yellow = []
        # y_yellow = []
        # for i in range(0,len(cones),3):
            # if cones[i+2] == 1: # yellow
                # x_yellow.append(cones[i])
                # y_yellow.append(cones[i+1])
            # else: # blue
                # x_blue.append(cones[i])
                # y_blue.append(cones[i+1])
        # plt.scatter(x_yellow, y_yellow, color='yellow', label='right cone')
        # plt.scatter(x_blue, y_blue, color='blue', label='left cone')
        # plt.scatter(0, 0, color='red', label='car')
        # plt.legend(loc="upper left")
        # plt.xlabel('distance (meter)')
        # plt.ylabel('distance (meter)')
        # #plt.show()
        # plt.savefig('vision.jpg')
        # plt.close()