import gym
from gym import spaces
import random
import numpy as np 
from power_algorithms.load_flow import load_flow

class Environment(gym.Env):
    
    def __init__(self):
        super(Environment, self).__init__()
        
        self.state = None
        #self.state_space_dims = #e.g. n_nodes * n_steps 
        self.action_space_dims = 1 # capacitor case
        #self.n_actions = n_capacitors

    def step(self, action):
        #update state

        #reward = self.calculate_reward(action)

        #done =

        return next_state, reward, done

    def calculate_reward(self, action, obs):
        reward = 0.0
        #todo
        return reward

    def reset(self, state_variables):
        self.state = state_variables
        return self.state