import network_definition as grid
import pandapower as pp

class NetworkManagement:
    def __init__(self):
         self.power_grid = grid.create_network()

    def get_power_grid(self):
        return self.power_grid
    
    # For given capacitor switch name (CapSwitch1, CapSwitch2...) status is changed.
    def change_capacitor_status(self, capSwitchName, closed):
        switchIndex = pp.get_element_index(self.power_grid, "switch", capSwitchName)
        self.power_grid.switch.closed.loc[switchIndex] = closed
