from enum import Enum

class ObjFuncType(Enum):
    ACTIVE_POWER_LOSSES = 1
    POWER_FACTOR = 2
    MV_VOLTAGE_DEVIATION = 3

class ObjectivesStatus(Enum):
    UNKNOWN = 0
    VIOLATED_CONSTRAINT = 1
    IMPROVED_CONSTRAINT = 2
    IMPROVED_OBECTIVE_FUNCTION = 3
    DETERIORATED_OBJECTIVE_FUNCTION = 4

class ObjectiveFunctions:
    def __init__(self, objectives, power_flow):
        self.objectives = objectives
        self.power_flow = power_flow
        self.initial_objectives_result = []
    
    def SetInitialObjectivesResults(self):
        for iObjective in self.objectives:
            if iObjective.name == ObjFuncType.ACTIVE_POWER_LOSSES.name: 
                result = self.CalculatePowerLosses()
            elif iObjective.name == ObjFuncType.POWER_FACTOR.name:
                result = self.CalculatePowerFactor()
            elif iObjective.name == ObjFuncType.MV_VOLTAGE_DEVIATION.name:
                result == self.CalculateVoltageDeviation()
            self.initial_objectives_result.append(result)

    def CalculateObjFunction(self):
        status = ObjectivesStatus.UNKNOWN

        for iObjective in reversed(self.objectives):
            if iObjective.name == ObjFuncType.ACTIVE_POWER_LOSSES.name: 
                result = self.CalculatePowerLosses()
                if result < self.initial_objectives_result[iObjective.value-1]:
                    status = ObjectivesStatus.IMPROVED_OBECTIVE_FUNCTION
                else:
                    status = ObjectivesStatus.DETERIORATED_OBJECTIVE_FUNCTION

            elif iObjective.name == ObjFuncType.POWER_FACTOR.name:
                result = self.CalculatePowerFactor()

            elif iObjective.name == ObjFuncType.MV_VOLTAGE_DEVIATION.name:
                result = self.CalculateVoltageDeviation()
                if result != 0.0:
                    status = ObjectivesStatus.VIOLATED_CONSTRAINT
                    break
                
        return status

    def CalculatePowerLosses(self):
        result = self.power_flow.get_losses()
        return result

    def CalculatePowerFactor(self):
        result = 0
        p = self.power_flow.get_network_injected_p
        q = self.power_flow.get_network_injected_q
        
        return result

    def CalculateVoltageDeviation(self):
        result = 0
        return result
