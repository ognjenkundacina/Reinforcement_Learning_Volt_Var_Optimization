import power_algorithms.odss_network_management as nm
from power_algorithms.odss_power_flow import ODSSPowerFlow

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
        optimal_statuses = [False, False, False, False]
        
        capacitor_names = network_manager.get_all_capacitor_switch_names()
        c0 = capacitor_names[0]
        c1 = capacitor_names[1]
        c2 = capacitor_names[2]
        c3 = capacitor_names[3]
        
        for a in False, True:
            for b in False, True:
                for c in False, True:
                    for d in False, True:
                        network_manager.set_capacitor_status(c0, a)
                        network_manager.set_capacitor_status(c1, b)
                        network_manager.set_capacitor_status(c2, c)
                        network_manager.set_capacitor_status(c3, d)
                        power_flow.calculate_power_flow()
                        current_losses = power_flow.get_losses()
                        if (current_losses < min_losses):
                            min_losses = current_losses
                            optimal_statuses = [a, b, c, d]

        print ('Minimal losses: ', min_losses)
        print('Minimal losses are achieved when the following capacitors are toogled:')
        for i in range(4):
            if (optimal_statuses[i] != capacitor_statuses[i]):
                print("CapSwitch", i+1, " changed its status from:", capacitor_statuses[i], "to", optimal_statuses[i])