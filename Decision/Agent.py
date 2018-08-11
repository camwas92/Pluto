import random
from collections import deque

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam

from Setup import Constants as Con


def scale_range(input, min, max):
    input += -(np.min(input))
    input /= np.max(input) / (max - min)
    input += min
    return input

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = Con.parameters_decision['gamma']  # discount rate
        self.epsilon = Con.parameters_decision['epsilon']  # exploration rate
        self.epsilon_min = Con.parameters_decision['epsilon_min']
        self.epsilon_decay = Con.parameters_decision['epsilon_decay']
        self.learning_rate = Con.parameters_decision['learning_rate']
        self.drop_out = Con.parameters_decision['drop_out']
        self.model = self._build_model()
        self.random_value = 0

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        # Layer 1
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        # Layer 2
        model.add(Dense(24, activation='relu'))
        # Output Layer
        model.add(Dense(self.action_size, activation='linear'))

        # Training and optimisaiton
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        self.random_value = np.random.rand()
        if self.random_value < self.epsilon and self.epsilon > 0:
            act_values = np.random.uniform(low=-1, high=1, size=(self.action_size,))
        else:
            act_values = self.model.predict(state)[0]
        return scale_range(act_values, -1, 1)  # returns action

    def replay(self, batch_size):
        if batch_size > len(self.memory):
            batch_size = len(self.memory)
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            scaled_predition = scale_range(self.model.predict(next_state), -1, 1)
            target = reward * (self.gamma * (scaled_predition))

            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
