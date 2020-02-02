import power_algorithms.odss_network_management as nm
from power_algorithms.odss_power_flow import ODSSPowerFlow

def is_kth_bit_set(mask, k):
    if (mask & (1 << k)): 
        return True
    else:
        return False

def vvo_brute_force(df_test):
    network_manager = nm.ODSSNetworkManagement()
    power_flow = ODSSPowerFlow()
    
    for index, row in df_test.iterrows():
        row_list = row.values.tolist()

        loads_count = network_manager.get_load_count()
        consumption_percents = row_list[1:loads_count + 1]
        capacitor_statuses = row_list[loads_count + 1:]

        network_manager.set_load_scaling(consumption_percents)
        network_manager.set_capacitors_initial_status(capacitor_statuses)
        
        power_flow.calculate_power_flow()
        min_losses = power_flow.get_losses()
        print ('Starting losses: ', min_losses)
        
        capacitor_names = network_manager.get_all_capacitor_switch_names()
        n_capacitors = len(capacitor_names)
        optimal_statuses = [False for i in range(n_capacitors)]

        for combination_mask in range(2 ** n_capacitors):
            temp_statuses = []
            for cap_idx in range (n_capacitors):
                cap_status = is_kth_bit_set(combination_mask, cap_idx)
                network_manager.set_capacitor_status(capacitor_names[cap_idx], cap_status)
                temp_statuses.append(cap_status)
            power_flow.calculate_power_flow()
            current_losses = power_flow.get_losses()
            if (current_losses < min_losses):
                min_losses = current_losses
                optimal_statuses = temp_statuses

        print ('Minimal losses: ', min_losses)
        print('Minimal losses are achieved when the following capacitors are toogled:')
        for i in range(n_capacitors):
            if (optimal_statuses[i] != capacitor_statuses[i]):
                print("Capacitor ", capacitor_names[i], " changed its status from:", capacitor_statuses[i], "to", optimal_statuses[i])