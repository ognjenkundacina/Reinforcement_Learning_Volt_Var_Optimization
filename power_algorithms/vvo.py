import pandas
import network_management as nm
from objective_functions import ObjectiveFunctions, ObjFuncType
from power_flow import PowerFlow

class VVO():

    def __init__(self):
        objectiveFunction = ObjFuncType.ACTIVE_POWER_LOSSES
        constraint = ObjFuncType.MV_VOLTAGE_DEVIATION
        objectives = (objectiveFunction, constraint)
        power_flow = PowerFlow(nm.NetworkManagement())

        self.power_flow = power_flow
        self.objectives = ObjectiveFunctions(objectives, power_flow.power_grid)

    def execute(self):
        switchingSequence = []

        self.objectives.CalculateObjFunction()
        self.power_flow.calculate_power_flow()
        return switchingSequence

    #execute VVO for every example in the test set and calculate the total reward
    def test(self, df_test):
        pass

#def main():
    #vvo = VVO()
    #vvo.execute()

#main()