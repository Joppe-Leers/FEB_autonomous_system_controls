#!/usr/bin/env python

import gym
import random
import numpy as np
from collections import deque
from DeepQnetwork import DeepQnetwork
from common_functions import process_state_image, generate_state_frame_stack_from_queue, plotLearning


class DQLalgotirhm:
    def __init__(self,
                 action_space=[
                     (-1, 1, 0.2), (0, 1, 0.2), (1, 1, 0.2),
                     (-1, 1, 0), (0, 1, 0), (1, 1, 0),
                     (-1, 0, 0.2), (0, 0, 0.2), (1, 0, 0.2),
                     (-1, 0, 0), (0, 0, 0), (1, 0, 0)
                 ],
                 frame_stack_num=3,
                 memory_size=5000,
                 gamma=0.95,  # discount rate
                 epsilon=1.0,  # exploration rate
                 epsilon_min=0.1,
                 epsilon_decay=0.9999,
                 learning_rate=0.001
                 ):
        self.action_space = action_space
        self.frame_stack_num = frame_stack_num
        self.memory = deque(maxlen=memory_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.model = DeepQnetwork(len(self.action_space), self.learning_rate, self.frame_stack_num)
        self.target_model = DeepQnetwork(len(self.action_space), self.learning_rate, self.frame_stack_num)

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

    #################### start training from the currently loaded model ####################
    def continueTraining(self, fileName, episodeOffset, episodes, render, skipFrames, trainingBatchSize,
                         updateTargetModelFreq, saveModelFreq, epsilon):
        self.episodeOffset = episodeOffset
        self.epsilon = epsilon

        self.model.loadModel(fileName)
        self.target_model.loadModel(fileName)

        self.trainModel(episodes, render, skipFrames, trainingBatchSize, updateTargetModelFreq, saveModelFreq)

    #################### start training from the currently loaded model ####################
    def trainModel(self, episodes, render, skipFrames, trainingBatchSize, updateTargetModelFreq, saveModelFreq):
        env = gym.make('CarRacing-v0')

        scores, eps_history = [], []
        for e in range(self.episodeOffset + 1, self.episodeOffset + episodes + 1):
            init_state = env.reset()
            init_state = process_state_image(init_state)
            state_frame_stack_queue = deque([init_state] * self.frame_stack_num, maxlen=self.frame_stack_num)

            total_reward = 0
            negative_reward_counter = 0
            time_frame_counter = 1
            done = False

            while True:
                if render:
                    env.render()

                current_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)
                action = self.act(current_state_frame_stack)

                reward = 0
                for _ in range(skipFrames + 1):
                    next_state, r, done, info = env.step(action)
                    reward += r
                    if done:
                        break

                # If continually getting negative reward 10 times after the tolerance steps, terminate this episode
                negative_reward_counter = negative_reward_counter + 1 if time_frame_counter > 100 and reward < 0 else 0

                # Extra bonus for the model if it uses full gas
                if action[1] == 1 and action[2] == 0:
                    reward *= 1.5

                total_reward += reward

                next_state = process_state_image(next_state)
                state_frame_stack_queue.append(next_state)
                next_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)

                self.memorize(current_state_frame_stack, action, reward, next_state_frame_stack, done)

                if done or negative_reward_counter >= 25 or total_reward < 0:
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
                self.target_model.saveModel('./save/trial_{}.h5'.format(e))
            env.close()

        x = [i + 1 for i in range(self.episodeOffset, self.episodeOffset + episodes)]
        filename = 'CarRacing.png'
        plotLearning(x, scores, eps_history, filename)
        env.close()
