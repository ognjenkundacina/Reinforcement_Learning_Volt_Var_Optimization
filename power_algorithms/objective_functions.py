from enum import Enum

class ObjFuncType(Enum):
    ACTIVE_POWER_LOSSES = 1
    POWER_FACTOR = 2
    MV_VOLTAGE_DEVIATION = 3

class ObjectiveFunctions:
    def __init__(self, objectives, grid):
        self.objectives = objectives
        self.grid = grid

    def CalculateObjFunction(self):
        result = 0
        for iObjective in reversed(self.objectives):
            if iObjective.name == ObjFuncType.ACTIVE_POWER_LOSSES.name: 
                result = self.CalculatePowerLosses()
            elif iObjective.name == ObjFuncType.POWER_FACTOR.name:
                result = self.CalculatePowerFactor()
            elif iObjective.name == ObjFuncType.MV_VOLTAGE_DEVIATION.name:
                result == self.CalculateVoltageDeviation()
                
        return result

    def CalculatePowerLosses(self):
        result = 0
        #result = self.grid.get_losses()
        return result

    def CalculatePowerFactor(self):
        result = 0
        return result

    def CalculateVoltageDeviation(self):
        result = 0
        return result
