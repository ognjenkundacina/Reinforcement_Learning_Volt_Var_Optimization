from collections import namedtuple
from itertools import count
import random

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 50)
        self.fc2 = nn.Linear(50, 50)
        self.fc3 = nn.Linear(50, 50)
        self.fc3_bn = nn.BatchNorm1d(50)
        self.fc4 = nn.Linear(50, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3_bn(self.fc3(x)))
        return self.fc4(x)


class DeepQLearningAgent:

    def __init__(self, environment):
        self.environment = environment
        self.epsilon = 0.1
        self.batch_size = 32
        self.gamma = 0.9
        self.target_update = 5
        self.memory = ReplayMemory(1000000)

        #self.state_space_dims = environment.state_space_dims
        #self.n_actions = environment.n_actions

        #self.policy_net = DQN(self.state_space_dims, self.n_actions)
        #self.target_net = DQN(self.state_space_dims, self.n_actions)
        #self.target_net.load_state_dict(self.policy_net.state_dict())

        #self.policy_net.train() #train mode (train vs eval mode)

        #self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.00001) 

    def reset_environment_training(self, state_variables):
        pass
        #return self.environment.reset(state_variables)

    def get_action(self, state):
        pass

    def train(self, df_train, n_episodes):
        pass

    def test(self, df_test):
        pass

    def optimize_model(self):
        pass