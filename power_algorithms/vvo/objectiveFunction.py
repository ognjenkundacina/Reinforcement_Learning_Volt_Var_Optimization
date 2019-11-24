from enum import Enum

class ObjFuncType(Enum):
    ACTIVE_POWER_LOSSES = 1
    POWER_FACTOR = 2
    MV_VOLTAGE_DEVIATION = 3

class ObjectiveFunction:
    def __init__(self, type, limits):
        self.type = type
        self.limits = limits

    def CalculateObjFunction(self):
        result = 0
        if self.type == ObjFuncType.ACTIVE_POWER_LOSSES: 
            result = result + self.CalculatePowerLosses
        return result

    def CalculatePowerLosses(self):
        result = 0
        return result

    def CalculatePowerFactor(self):
        pass

    def CalculateVoltageDeviation(self):
        pass
