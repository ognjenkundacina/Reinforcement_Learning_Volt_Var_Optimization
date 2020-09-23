import os
from environment.environment import Environment
import pandas as pd
from rl_algorithms.deep_q_learning import DeepQLearningAgent
from power_algorithms.vvo import VVO
from power_algorithms.vvo_brute_force import vvo_brute_force
import time
from power_algorithms.odss_network_management import ODSSNetworkManagement
from power_algorithms.odss_power_flow import ODSSPowerFlow
from power_algorithms.objective_functions import ObjectiveFunctions, ObjFuncType


def load_dataset():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './dataset/data.csv')
    df = pd.read_csv(file_path)

    return df

def split_dataset(df, split_index):
    df_train = df[df.index <= split_index]
    df_test = df[df.index > split_index]

    return df_train, df_test

def main():
    #dataset contains random power injection of nodes
    df = load_dataset()
    df_train, df_test = split_dataset(df, 998)

    objectives = [ObjFuncType.ACTIVE_POWER_LOSSES]
    network_manager = ODSSNetworkManagement()
    power_flow = ODSSPowerFlow()
    objective_functions = ObjectiveFunctions(objectives, power_flow)
    print('=====================vvo=====================')
    vvo = VVO(network_manager, power_flow, objective_functions) 
    vvo.test(df_test, resetCapacitorStatuses = True)
    
    print('=====================vvo_brute_force=====================')
    vvo_brute_force(df_test)

    #environment should'n have the entire dataset as an input parameter, but train and test methods
    network_manager = ODSSNetworkManagement()
    environment = Environment(network_manager)

    print('=====================agent=====================')
    agent = DeepQLearningAgent(environment)

    n_episodes = 1000
    print('agent training started')
    t1 = time.time()
    agent.train(df_train, n_episodes)
    t2 = time.time()
    print ('agent training finished in', t2-t1)

    agent.test(df_test)

def vvo_after_rl():
    #dataset contains random power injection of nodes
    df = load_dataset()
    df_train, df_test = split_dataset(df, 998)

    print('=====================vvo_brute_force=====================')
    vvo_brute_force(df_test)

    objectives = [ObjFuncType.ACTIVE_POWER_LOSSES]
    network_manager = ODSSNetworkManagement()
    power_flow = ODSSPowerFlow()
    
    #environment should'n have the entire dataset as an input parameter, but train and test methods
    environment = Environment(network_manager)

    print('=====================agent=====================')
    agent = DeepQLearningAgent(environment)

    n_episodes = 1000
    print('agent training started')
    t1 = time.time()
    #agent.train(df_train, n_episodes)
    t2 = time.time()
    print ('agent training finished in', t2-t1)

    agent.test(df_test)
    network_manager.print_all_capacitor_statuses()

    objective_functions = ObjectiveFunctions(objectives, power_flow)
    print('=====================vvo=====================')
    vvo = VVO(network_manager, power_flow, objective_functions) 
    vvo.test(df_test, resetCapacitorStatuses = False)
    network_manager.print_all_capacitor_statuses()


if __name__ == '__main__':
    #main()
    vvo_after_rl()
