import pandapower as pp
import network_definition as grid

class PowerFlow:
    def __init__(self):
        self.power_grid = grid.create_network()

    def calculate_power_flow(self):
        pp.runpp(self.power_grid, algorithm="bfsw", calculate_voltage_angles=False)


# def main():
#     power_flow = PowerFlow()
#     power_flow.calculate_power_flow()

# main()