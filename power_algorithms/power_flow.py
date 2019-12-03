import pandapower as pp
import network_management as nm

class PowerFlow:
    def __init__(self, grid_creator):
        self.power_grid = grid_creator.get_power_grid()

    def calculate_power_flow(self):
        pp.runpp(self.power_grid, algorithm="bfsw", calculate_voltage_angles=False)

    def get_losses(self):
        grid_losses = 0
        for line_losses in self.power_grid.res_line.pl_mw:
            grid_losses += line_losses
        for transformer_losses in self.power_grid.res_trafo.pl_mw:
            grid_losses += transformer_losses
        
        return grid_losses

    def get_bus_voltages(self):
        switch_busses = set(self.power_grid.switch.element.values)
        mv_buses = self.power_grid.bus[(self.power_grid.bus.vn_kv == 20) & (~self.power_grid.bus.index.isin(switch_busses))].index
        name_with_voltage = {}
        for bus_index in mv_buses:
            name_with_voltage.update( {self.power_grid.bus.name.at[bus_index] : self.power_grid.res_bus.vm_pu.at[bus_index]} )

        return name_with_voltage

    def get_network_injected_p(self):
        return self.power_grid.res_ext_grid.p_mw

    def get_network_injected_q(self):
        return self.power_grid.res_ext_grid.q_mvar

# def main():
#     network_manager = nm.NetworkManagement()
#     power_flow = PowerFlow(network_manager)
#     power_flow.calculate_power_flow()
#     print(power_flow.get_losses())
#     print(power_flow.get_network_injected_p())
#     print(power_flow.get_network_injected_q())
#     network_manager.change_capacitor_status('CapSwitch6', True)
#     power_flow.calculate_power_flow()
#     print(power_flow.get_losses())

#     print(*network_manager.get_all_capacitor_switch_names())
#     print(power_flow.get_network_injected_p())
#     print(power_flow.get_network_injected_q())

#     print(power_flow.get_bus_voltages())

# main()