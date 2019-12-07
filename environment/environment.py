import gym
from gym import spaces
import random
import numpy as np 
from power_algorithms.power_flow import PowerFlow
import power_algorithms.network_management as nm

#todo uvazi consumption u ovom fajlu gdje god se pominje
class Environment(gym.Env):
    
    def __init__(self):
        super(Environment, self).__init__()
        
        self.state = []
        self.state_space_dims = 101
        self.n_actions = 6 #n_capacitors
        self.i_step = 0

        self.network_manager = nm.NetworkManagement() #zamijeni kasnije sa linijom ispod
        #self.network_manager = nm.NetworkManagement(consumption)
        self.power_flow = PowerFlow(self.network_manager)

        self.current_losses = 0.0

        self.available_actions = [i for i in range(self.n_actions)] #todo ovo bi mogao biti dictionary, ako bismo tap changere koristili, ili diskretizovane setpointe generatora

    def _update_state(self):
        self.power_flow.calculate_power_flow()

        bus_voltages_dict = self.power_flow.get_bus_voltages()
        self.state = list(bus_voltages_dict.values())
        #line_rated_powers_dict = self.power_flow.get_line_rated_powers()
        #self.state = list(line_rated_powers_dict.values())

        if (len(self.state) != self.state_space_dims):
            print('Environment: len(self.state) != self.state_space_dims')

        return self.state

    #action: 0..n_actions
    def step(self, action):
        #todo promjeniti da ovo bude promjena statusa switcha, a ne sa false na true => bice potrebna metoda get capacitor status TOGGLE
        self.network_manager.change_capacitor_status('CapSwitch'+str(action + 1), True)
        self.available_actions.remove(action)
        
        next_state = self._update_state()

        reward = self.calculate_reward(action)

        self.i_step += 1

        done = (self.i_step == self.n_actions)

        if (reward < 0.0):
            done = True  #todo staviti odradjivanje vrijednosti za done u jednu liniju

        return next_state, reward, done
    
    #only for test set
    def revert_action(self, action):
        self.network_manager.change_capacitor_status('CapSwitch'+str(action + 1), False) #todo TOGGLE
        next_state = self._update_state()
        return self.power_flow.get_losses()


    def calculate_reward(self, action):
        new_losses = self.power_flow.get_losses()
        losses_decrease = self.current_losses - new_losses
        reward = losses_decrease * 1000
        print ('losses_decrease', losses_decrease)
        self.current_losses = new_losses
        #ObjectiveFunctions

        #neka nagrada/kazna za gubitke bude delta, a ne sami iznos gubitaka 
        #nek za pocetak bude samo optimizacija gubitaka, pa kasnije mozemo dodavati voltage deviation

        #mala kazna za svaki novi self.i_step

        #sprijeciti ponavljanje istih akcija vise puta u epizodi
        #1. Dati veliku kaznu ako je akcija vec odradjena - lose, imamo previse nagrada i kazni i zbunjujemo agenta
        #2. Izmjeniti metodu get_action tako da biramo samo najbolju akciju (ili random akciju) iz aktuelne liste akcija, koja se mijenja tokom jedne epizode
        #todo
        return reward

    def reset(self, consumption):
        #todo: bilo bi dobro da se NetworkManagement() poziva samo u konstruktoru environmenta, 
        #a da se ovdje poziva samo metoda koja updatuje consumption u okviru objekta network_manager
        self.network_manager = nm.NetworkManagement() #zamijeni kasnije sa linijom ispod
        #self.network_manager = nm.NetworkManagement(consumption)
        self.power_flow = PowerFlow(self.network_manager)
        
        self.power_flow.calculate_power_flow()
        bus_voltages_dict = self.power_flow.get_bus_voltages()
        self.state = list(bus_voltages_dict.values())
        #line_rated_powers_dict = self.power_flow.get_line_rated_powers()
        #self.state = list(line_rated_powers_dict.values())

        self.current_losses = self.power_flow.get_losses()

        self.i_step = 0
        self.available_actions = [i for i in range(self.n_actions)]

        return self.state