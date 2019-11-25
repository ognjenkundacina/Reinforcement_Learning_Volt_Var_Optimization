from enum import Enum

class SwitchStatus(Enum):
    STATUS_ON: 1
    STATUS_OFF: 2

class Capacitor:
    def __init__(self, capacity, switchStatus, iNode):
        self.capacity = capacity
        self.switchStatus = switchStatus
        self.iNode = iNode