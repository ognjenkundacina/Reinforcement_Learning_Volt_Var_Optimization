import power_algorithms.network_definition as grid
import pandapower as pp
import pandas as pd

class NetworkManagement:
    def __init__(self):
         self.power_grid = grid.create_network()

    def get_power_grid(self):
        return self.power_grid
    
    # For given capacitor switch name (CapSwitch1, CapSwitch2...) status is changed.
    def change_capacitor_status(self, capSwitchName, closed):
        switchIndex = pp.get_element_index(self.power_grid, "switch", capSwitchName)
        self.power_grid.switch.closed.loc[switchIndex] = closed
    
    def toogle_capacitor_status(self, capSwitchName):
        switchIndex = pp.get_element_index(self.power_grid, "switch", capSwitchName)
        currentState = self.power_grid.switch.closed.loc[switchIndex]
        self.power_grid.switch.closed.loc[switchIndex] = not currentState

    def get_all_capacitor_switch_names(self):
        return self.power_grid.switch['name'].tolist()

    def get_all_capacitors(self):
        return pd.Series(self.power_grid.switch.closed.values, index=self.power_grid.switch.name).to_dict()

