#!/usr/bin/env python
from DQLalgorithm import DQLalgotirhm
from simWrap import SimWrap

if __name__ == '__main__':
    dql = DQLalgotirhm()
    dql.trainModel(episodes=5000, skipFrames=2, trainingBatchSize=64, updateTargetModelFreq=5, saveModelFreq=25)
    #dql.testModel(modelFile='trial_25.h5', episodes=5, skipFrames=2)
    
# if __name__ == '__main__':
    # simulationWrapper = SimWrap(manualControl=True)
    # simulationWrapper.init()
    # while True:
        # nextState, r, done = simulationWrapper.step([0,0,0])
        # print("state: " + str(len(nextState)) + " r: " + str(r) + " done: " + str(done))
