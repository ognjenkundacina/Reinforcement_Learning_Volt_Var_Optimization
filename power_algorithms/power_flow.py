import pandapower as pp
import network_definition as grid

class PowerFlow:
    def __init__(self):
        self.power_grid = grid.create_network()

    def calculate_power_flow(self):
        pp.runpp(self.power_grid, algorithm="bfsw", calculate_voltage_angles=False)

    def get_losses(self):
        grid_losses = 0
        for line_losses in self.power_grid.res_line.pl_mw:
            grid_losses += line_losses
        for transformer_losses in self.power_grid.res_trafo.pl_mw:
            grid_losses += transformer_losses
        
        return grid_losses

# def main():
#     power_flow = PowerFlow()
#     power_flow.calculate_power_flow()
#     print(power_flow.get_losses())

# main()