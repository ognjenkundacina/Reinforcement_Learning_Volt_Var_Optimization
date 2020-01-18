import opendssdirect as dss
from opendssdirect.utils import Iterator

class ODSSNetworkManagement:
    def __init__(self):
        dss.run_command('Redirect power_algorithms/Test_scheme.dss')

    def toogle_capacitor_status(self, capSwitchName):
        dss.Capacitors.Name(capSwitchName)
        currentState = dss.Capacitors.States()
        if (currentState == 0):
            dss.Capacitors.Close()
        else:
            dss.Capacitors.Open()

    def get_all_capacitor_switch_names(self):
        return dss.Capacitors.AllNames()

    def get_all_capacitors(self):
        capacitorStatuses = {}
        for capName in Iterator(dss.Capacitors, 'Name'):
            dss.Capacitors.Name(capName())
            currentState = dss.Capacitors.States()
            capacitorStatuses.update( {capName() : currentState[0]} )

        return capacitorStatuses

    def set_capacitors_initial_status(self, capacitors_statuses):
        if (len(capacitors_statuses) != dss.Capacitors.Count()):
            print("(ERROR) Input list of capacitor statuses {} is not the same length as number of capacitors {}".format(len(capacitors_statuses), dss.Capacitors.Count()))
            return
        
        index = 0
        for capName in Iterator(dss.Capacitors, 'Name'):
            dss.Capacitors.Name(capName())
            if (capacitors_statuses[index] == 0):
                dss.Capacitors.Open()
            else:
                dss.Capacitors.Close()
            index = index + 1

    def set_load_scaling(self, scaling_factors):
        if (len(scaling_factors) != dss.Loads.Count()):
            print("(ERROR) Input list of scaling factors {} is not the same length as number of loads {}".format(len(scaling_factors), dss.Loads.Count()))
            return

        pNom = 140 #these hardcoded values should be changed, ODSS does not have scaling factor, discuss other solutions
        qNom = 50
        index = 0
        for loadName in Iterator(dss.Loads, 'Name'):
            dss.Loads.Name(loadName())
            dss.Loads.kW = pNom * scaling_factors[index]
            index = index + 1

    
