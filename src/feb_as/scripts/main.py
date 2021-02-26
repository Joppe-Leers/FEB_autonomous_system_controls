#!/usr/bin/env python
# from DQLalgorithm import DQLalgotirhm

# if __name__ == '__main__':
    # dql = DQLalgotirhm()
    # #dql.trainModel(episodes=2000, skipFrames=2, trainingBatchSize=64, updateTargetModelFreq=5, saveModelFreq=25)
    # dql.testModel(modelFile='trial_25.h5', episodes=5, skipFrames=2)
    
from simWrapManualControl import SimWrapManualControl
import time

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    simulationWrapper = SimWrapManualControl()
    simulationWrapper.init()
    while True:
        state, score, done = simulationWrapper.step()
        print("score: " + str(score) + " done: " + str(done) + " stateLenght: " + str(len(state)))
        cones = state[:len(state)-6]
        x = []
        y = []
        for i in range(0,len(cones),3):
            x.append(cones[i])
            y.append(cones[i+1])
        plt.scatter(x, y)
        plt.scatter(0, 0)
        plt.savefig('vision.jpg')
        plt.close()
        time.sleep(5)
