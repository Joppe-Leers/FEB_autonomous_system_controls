#!/usr/bin/env python

from simWrap import SimWrap
import random
import numpy as np
from collections import deque
from DeepQnetwork import DeepQnetwork
from common_functions import plotLearning


class DQLalgotirhm:
    def __init__(self,
                 action_space=[(-1, 1, 0)     , (0, 1, 0)     , (1, 1, 0),
                                (-1, 0, 1)     , (0, 0, 1)     , (1, 0, 1),
                                (-1, 0, 0)     , (0, 0, 0)     , (1, 0, 0)],
                 stateLenght=66,
                 memory_size=5000,
                 gamma=0.95,  # discount rate
                 epsilon=1.0,  # exploration rate
                 epsilon_min=0.1,
                 epsilon_decay=0.9999,
                 learning_rate=0.001
                 ):
        print("DQLA constructor")
        self.action_space = action_space
        self.stateLenght = stateLenght
        self.memory = deque(maxlen=memory_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.model = DeepQnetwork(len(self.action_space), self.learning_rate, self.stateLenght)
        self.target_model = DeepQnetwork(len(self.action_space), self.learning_rate, self.stateLenght)

        self.episodeOffset = 0

    def update_target_model(self):
        self.target_model.updateModelFromModel(self.model)

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, self.action_space.index(action), reward, next_state, done))

    def act(self, state):
        if np.random.rand() > self.epsilon:
            act_values = self.model.forward(state)
            action_index = np.argmax(act_values[0])
        else:
            action_index = random.randrange(len(self.action_space))
        return self.action_space[action_index]

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        train_state = []
        train_target = []
        for state, action_index, reward, next_state, done in minibatch:
            target = self.model.forward(state)[0]
            if done:
                target[action_index] = reward
            else:
                t = self.target_model.forward(next_state)[0]
                target[action_index] = reward + self.gamma * np.amax(t)
            train_state.append(state)
            train_target.append(target)
        self.model.train(train_state, train_target)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    #################### start training from another loaded model ####################
    def continueTraining(self, fileName, episodeOffset, episodes, skipFrames, trainingBatchSize,
                         updateTargetModelFreq, saveModelFreq, epsilon):
        self.episodeOffset = episodeOffset
        self.epsilon = epsilon

        self.model.loadModel(fileName)
        self.target_model.loadModel(fileName)

        self.trainModel(episodes, skipFrames, trainingBatchSize, updateTargetModelFreq, saveModelFreq)

    #################### start training from the currently loaded model ####################
    def trainModel(self, episodes, skipFrames, trainingBatchSize, updateTargetModelFreq, saveModelFreq):
        simulationWrapper = SimWrap()
        simulationWrapper.init()
        print("init done")
        scores, eps_history = [], []
        for e in range(self.episodeOffset + 1, self.episodeOffset + episodes + 1):
            simulationWrapper.reset()
            currentState, _, _ = simulationWrapper.step([0,0,0])
            
            total_reward = 0
            negative_reward_counter = 0
            time_frame_counter = 1
            done = False

            while True:
                action = self.act(currentState)
                reward = 0
                for _ in range(skipFrames + 1):
                    nextState, r, done = simulationWrapper.step(action)
                    print("state: " + str(len(nextState)) + " r: " + str(r) + " done: " + str(done))
                    reward += r
                    if done:
                        break

                total_reward += reward

                if reward < 0:
                    negative_reward_counter += 1
                    if negative_reward_counter >= 100:
                        reward = -100
                        done = True
                else:
                    negative_reward_counter = 0

                self.memorize(currentState, action, reward, nextState, done)
                
                if done:
                    print(
                        'Episode: {}/{}, Scores(Time Frames): {}, Total Rewards(adjusted): {:.2}, Epsilon: {:.2}'.format(
                            e, self.episodeOffset + episodes, time_frame_counter, float(total_reward),
                            float(self.epsilon)))
                    break
                if len(self.memory) > trainingBatchSize:
                    self.replay(trainingBatchSize)
                time_frame_counter += 1

            scores.append(total_reward)
            eps_history.append(self.epsilon)

            if e % updateTargetModelFreq == 0:
                self.update_target_model()

            if e % saveModelFreq == 0:
                self.target_model.saveModel('saves/trial_{}.h5'.format(e))
            simulationWrapper.reset()

        x = [i + 1 for i in range(self.episodeOffset, self.episodeOffset + episodes)]
        filename = 'trainingPlot.png'
        plotLearning(x, scores, eps_history, filename)
        simulationWrapper.reset()
        
    #################### Test model ####################
    def testModel(self, modelFile, episodes, skipFrames):
        simulationWrapper = SimWrap()
        simulationWrapper.init()
        self.model.loadModel(modelFile)
        for e in range(1, episodes+1):
            print("episode: " + str(e))
            simulationWrapper.reset()
            total_reward = 0
            negative_reward_counter = 0
            time_frame_counter = 1
            done = False
            currentState, _, _ = simulationWrapper.step([0,0,0])
            while True:
                reward = 0
                act_values = self.model.forward(currentState)
                action_index = np.argmax(act_values[0])
                
                print(action_index)
                print(self.action_space[action_index])
              
                for _ in range(skipFrames + 1):
                    nextState, r, done = simulationWrapper.step(self.action_space[action_index])
                    reward += r
                    if done:
                        break
                total_reward += reward
                if done:
                    print('Episode: {}/{}, Scores(Time Frames): {}, Total Rewards(adjusted): {:.2}'.format(
                            e, episodes, time_frame_counter, float(total_reward)))
                    break
                time_frame_counter += 1
        simulationWrapper.reset()
                    
               
                    
                    
            
            
            
            
            
            
            
            
            
