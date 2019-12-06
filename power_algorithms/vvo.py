import pandas
import power_algorithms.network_management as nm
from power_algorithms.objective_functions import ObjectiveFunctions, ObjFuncType, ObjectivesStatus
from power_algorithms.power_flow import PowerFlow

class VVO():

    def __init__(self, network_manager, power_flow, objective_functions):
        self.network_manager = network_manager
        self.power_flow = power_flow
        self.objective_functions = objective_functions

    def execute(self):
        switchingSequence = []
        n_power_flow_execution = 0
        self.power_flow.calculate_power_flow()
        n_power_flow_execution = n_power_flow_execution + 1
        self.objective_functions.SetCurrentObjectivesResults()

        should_use_capacitor = {}
        capacitors = self.network_manager.get_all_capacitor_switch_names()
        for capacitor in capacitors:
            should_use_capacitor.update({capacitor : True})
        there_is_capacitors_for_use = True

        while there_is_capacitors_for_use:
            previous_benefit = 0
            for capacitor in capacitors:
                if should_use_capacitor[capacitor] == False:
                    continue
                self.network_manager.toogle_capacitor_status(capacitor)
                self.power_flow.calculate_power_flow()
                n_power_flow_execution = n_power_flow_execution + 1
                benefit = self.objective_functions.CalculateObjFunction()
                if benefit > previous_benefit:
                    candidateCapacitor = capacitor
                    previous_benefit = benefit
                self.network_manager.toogle_capacitor_status(capacitor)

            if previous_benefit != 0:
                switchingSequence.append(candidateCapacitor)
                self.network_manager.toogle_capacitor_status(candidateCapacitor)
                self.power_flow.calculate_power_flow()
                n_power_flow_execution = n_power_flow_execution + 1
                self.objective_functions.SetCurrentObjectivesResults()
                should_use_capacitor.update({candidateCapacitor : False})
                there_is_capacitors_for_use = self.isThereCapacitorsForUse(should_use_capacitor)
            else:
                there_is_capacitors_for_use = False

        print('VVO results:')
        print('Number of power flow executions: ', n_power_flow_execution)
        print('Final losses: ', self.objective_functions.current_objectives_result[ObjFuncType.ACTIVE_POWER_LOSSES.name])
        for capacitor in switchingSequence:
            print(capacitor)

        return switchingSequence

    def isThereCapacitorsForUse(self, should_use_capacitor):
        for capacitor in should_use_capacitor:
            if should_use_capacitor[capacitor]:
                return True
        return False

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