# Reinforcement Learning Volt-Var Optimization (VVO)

In this work, we apply Deep Q Learning to the discrete version of the Volt-Var Optimization (VVO) problem in distribution power networks, which generates the VVO sequence containing capacitor statuses to minimize the active power losses in the network. We train and test the proposed algorithm on the IEEE123 scheme using the Python interface to the DSS software package. Our code can be easily extended to use more complex loss functions and constraint penalties.

The action space is initialized to the set of all capacitor switches in the distribution network. In environment/environment.py we use an interface to the ODSS model of the network (network_manager) to get the number of all of the capacitor switches, as well as their names in the ODSS model:

self.n_actions = len(self.network_manager.get_all_capacitors())

self.capacitor_names = self.network_manager.get_all_capacitor_switch_names().

The switch names are predefined in the .DSS files (which can be found in the power_algorithms folder) and are created using the node number in the distribution network, as well as its phase.

At the beginning of each episode, these two are zipped into a dictionary:

self.available_actions = dict(zip(self.action_indices, self.capacitor_names)). 

Action on the switch corresponds to toggling its state. During each step in the episode, we exclude the selected switch from the action space, since the optimal VVO sequence shouldn't activate the same switch multiple times. Although the RL algorithm should figure this out during the training phase, this incorporation of prior knowledge by changing the action space dynamically resulted in a significant acceleration of the RL algorithm's training!

We've recently published a paper containing some of the tricks that could be helpful in using RL for various power systems problems, like changing the action space dynamically, efficient way of incorporating switching operation constraints in some problems or selecting the right set of state variables for switches which leads to lower observability requirements. They are demonstrated on a more complex example of dynamic distribution network reconfiguration, so if you consider it useful for your research, please consider citing it: 

https://www.researchgate.net/publication/355392682_Solving_dynamic_distribution_network_reconfiguration_using_deep_reinforcement_learning.

To simulate various scenarios, we reset them at the beginning of each episode, along with the initial capacitor statuses, in the environment.py using the interface to ODSS:

self.network_manager.set_load_scaling(consumption_percents).

Here we basically just scale the nominal consumption of each consumer in the distribution network using the array of relative values of the consumption for each consumer (although the variable is wrongly called consumption_percents). We read the consumption_percents array from the dataset (dataset/data.csv) which was populated uniformly randomly, but if you switch to using some real-world dataset in which consumptions vary less, it will probably lead to even better RL training convergence properties.

