#!/usr/bin/env python
from DQLalgorithm import DQLalgotirhm

if __name__ == '__main__':
    dql = DQLalgotirhm()
    dql.trainModel(episodes=2000, skipFrames=2, trainingBatchSize=64, updateTargetModelFreq=5, saveModelFreq=25)
