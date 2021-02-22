#!/usr/bin/env python

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
import numpy as np


class DeepQnetwork:
    def __init__(self, outputSize, learning_rate=0.001, frame_stack_num=3, ):
        # Neural Net for Deep-Q learning Model
        self.model = Sequential()
        self.model.add(
            Conv2D(filters=6, kernel_size=(7, 7), strides=3, activation='relu', input_shape=(96, 96, frame_stack_num)))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(filters=12, kernel_size=(4, 4), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())
        self.model.add(Dense(216, activation='relu'))
        self.model.add(Dense(outputSize, activation=None))
        self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate, epsilon=1e-7))

    def forward(self, state):
        return self.model.predict(np.expand_dims(state, axis=0))

    def train(self, train_state, train_target):
        self.model.fit(np.array(train_state), np.array(train_target), epochs=1, verbose=0)

    def updateModelFromModel(self, deepQnetwork):
        self.model.set_weights(deepQnetwork.getWeights())

    def getWeights(self):
        return self.model.get_weights()

    def saveModel(self, filename):
        self.model.save_weights(filename)

    def loadModel(self, filename):
        self.model.load_weights(filename)

    def summary(self):
        self.model.summary()
