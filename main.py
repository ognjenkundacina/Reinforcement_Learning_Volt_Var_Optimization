import os
from environment.environment import Environment
import pandas as pd
from rl_algorithms.deep_q_learning import DeepQLearningAgent
from power_algorithms.vvo import VVO
import time

def load_dataset():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, './dataset/data.csv')
    #df = pd.read_csv(file_path)

    #return df
    return None

def split_dataset(df, split_index):
    #df_train = df[df.index <= split_index]
    #df_test = df[df.index > split_index]

    #return df_train, df_test
    return None, None


def main():
    #dataset contains random power injection of nodes
    df = load_dataset()
    df_train, df_test = split_dataset(df, 0)

    #environment should'n have the entire dataset as an input parameter, but train and test methods
    environment = Environment()
    agent = DeepQLearningAgent(environment)

    n_episodes = 0
    print('agent training started')
    t1 = time.time()
    agent.train(df_train, n_episodes)
    t2 = time.time()
    print ('agent training finished in', t2-t1)

    agent.test(df_test)

    """
    1. Testirati VVO algoritam na df_test primjerima, da bismo ih evaluirali istom metrikom kojom smo evaluirali rl agente (sabrana dugorocna nagrada sve sve primjere iz test seta)
    VVO.test(df_test)
    2. Smisliti jedan kritican primjer za prezentaciju i testirati rl i vvo na njemu
    """

if __name__ == '__main__':
  main()
