from enum import Enum
"""
EventType is a simple enum containing each of the potential EventTypes that may occur in our simulation
""" 
class EventType(Enum):
    SwitchOut = 1
    SwitchIn = 2
    
"""
the event class is responsible for holding information about events that will occur at calculated points in time
"""
class Event():
    """
    event constructor: create a new event with the specified time, type, and process
    @param type: the EventType for this event
    @param time: the time (in milliseconds) at which this event will occur
    @param proc: the process to which this event corresponds
    """
    def __init__(self,eType,time,proc):
        self.eType = eType
        self.time = time
        self.process = proc
    
    """
    override the less-than operator for priority queue sorting based on event time
    @param other: the Event we are comparing ourselves to
    """
    def __lt__(self, other):
        #first we compare times
        if (self.time != other.time):
            return self.time < other.time
        #when time is the same, we compare event priority
        if (self.eType != other.eType):
            return self.eType.value < other.eType.value
        #when events are the same, we compare PID
        return self.process.pid < other.process.pid