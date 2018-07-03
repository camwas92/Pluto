import random
from collections import deque

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam


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
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.random_value = 0

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        self.random_value = np.random.rand()
        if self.random_value < self.epsilon:
            act_values = np.random.uniform(low=-1, high=1, size=(self.action_size,))
        else:
            act_values = self.model.predict(state)[0]
        return scale_range(act_values, -1, 1)  # returns action

    def replay(self, batch_size):
        if batch_size > len(self.memory):
            batch_size = len(self.memory)
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            # todo figure out a better reward
            target = reward
            if not done:
                target = reward + self.gamma * \
                         (self.model.predict(next_state))

            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
