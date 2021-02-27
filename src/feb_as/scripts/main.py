#!/usr/bin/env python
from DQLalgorithm import DQLalgotirhm

if __name__ == '__main__':
    dql = DQLalgotirhm()
    dql.trainModel(episodes=10000, skipFrames=2, trainingBatchSize=64, updateTargetModelFreq=5, saveModelFreq=25)
    #dql.testModel(modelFile='trial_25.h5', episodes=5, skipFrames=2)
    

