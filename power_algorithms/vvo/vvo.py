import pandas
from power_algorithms.power_flow import PowerFlow

class VVO():

    def __init__(self, capacitors, objectiveFunctions):
        self.capacitors = capacitors
        self.objectiveFunctions = objectiveFunctions

    def execute(self):
        switchingSequence = []
        return switchingSequence

    #execute VVO for every example in the test set and calculate the total reward
    def test(self, df_test):
        pass