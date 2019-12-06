from power_algorithms.power_flow import PowerFlow
import power_algorithms.network_management as nm

def vvo_brute_force():
    network_manager = nm.NetworkManagement()
    power_flow = PowerFlow(network_manager)
        
    power_flow.calculate_power_flow()
    min_losses = power_flow.get_losses()
    print ('Starting losses: ', min_losses)
    optimal_statuses = [False, False, False, False, False, False]

    for a in False, True:
        for b in False, True:
            for c in False, True:
                for d in False, True:
                    for e in False, True:
                        for f in False, True:
                            network_manager.change_capacitor_status('CapSwitch1', a)
                            network_manager.change_capacitor_status('CapSwitch2', b)
                            network_manager.change_capacitor_status('CapSwitch3', c)
                            network_manager.change_capacitor_status('CapSwitch4', d)
                            network_manager.change_capacitor_status('CapSwitch5', e)
                            network_manager.change_capacitor_status('CapSwitch6', f)
                            power_flow.calculate_power_flow()
                            current_losses = power_flow.get_losses()
                            if (current_losses < min_losses):
                                min_losses = current_losses
                                optimal_statuses = [a, b, c, d, e, f]

    print ('Minimal losses: ', min_losses)
    print('Minimal losses are achieved when the following capacitors are ON:')
    for i in range(6):
        if (optimal_statuses[i]):
            print("CapSwitch", i+1)