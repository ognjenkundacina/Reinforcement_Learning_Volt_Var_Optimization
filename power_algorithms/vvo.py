import pandas
import network_management as nm
from objective_functions import ObjectiveFunctions, ObjFuncType, ObjectivesStatus
from power_flow import PowerFlow

class VVO():

    def __init__(self, network_manager, power_flow, objective_functions):
        self.network_manager = network_manager
        self.power_flow = power_flow
        self.objective_functions = objective_functions

    def execute(self):
        switchingSequence = []
        self.power_flow.calculate_power_flow()
        self.objective_functions.SetInitialObjectivesResults()

        capacitors = self.network_manager.get_all_capacitor_switch_names()
        close = True
        for capacitor in capacitors:
            self.network_manager.change_capacitor_status(capacitor, close)
            self.power_flow.calculate_power_flow()
            improves_objectives = self.doesCapacitorImprovesObjectives()
            if improves_objectives == True:
                switchingSequence.append(capacitor)

        return switchingSequence

    def doesCapacitorImprovesObjectives(self):
        status = self.objective_functions.CalculateObjFunction()
        if status.value == ObjectivesStatus.IMPROVED_CONSTRAINT.value \
         | status.value == ObjectivesStatus.IMPROVED_OBECTIVE_FUNCTION.value:
            return True
        else:
            return False


    #execute VVO for every example in the test set and calculate the total reward
    def test(self, df_test):
        pass

#def main():
  #  objectiveFunction = ObjFuncType.ACTIVE_POWER_LOSSES
  #  constraint = ObjFuncType.MV_VOLTAGE_DEVIATION
  #  objectives = (objectiveFunction, constraint)
  #  network_manager = nm.NetworkManagement()
  #  power_flow = PowerFlow(network_manager)
  #  objective_functions = ObjectiveFunctions(objectives, power_flow)

  #  vvo = VVO(network_manager, power_flow, objective_functions)
  #  vvo.execute()

#main()