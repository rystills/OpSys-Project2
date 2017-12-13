import copy
import queue
from Event import Event, EventType
from MemoryStore import MemoryAlgorithm
import sys

#set 'this' to point to this module, so we can maintain module-wide globals
this = sys.modules[__name__]

#The Simulator class is a static class responsible for emulating our CPU, Running through the input processes using the selected algorithm
this.algo = MemoryAlgorithm.bestFit
this.simTime = 0
this.processes = []
this.events = []
this.contiguous = True

"""
Reset the simulator, clearing all processes, and setting time back to 0
"""
def reset():
    this.simTime = 0
    this.processes = []
    this.events = []
    
"""
show a message indicating that the Simulator is starting up
"""
def showStartMessage():
    print("time 0ms: Simulator started ({0} -- {1})".format("Contiguous" if this.contiguous else "Non-contiguous", this.algo.name))

"""
run the simulation
"""
def run():
    this.showStartMessage()
    '''#populate the event queue with the arrival event for all processes
    for p in self.processes:
        self.addEvent(EventType.Arrive,p.arrivalTime, p)
        
    #jump from event to event
    while(not self.events.empty()):
        #get the current event and update time
        currEvent = self.events.get()
        self.t = currEvent.time
        
        #process the current event
        self.processEvent(currEvent)
            
        #check the ready queue once all same-time events have finished, pulling in a new process if nothing is running now
        if (len(self.events.queue) == 0 or self.events.queue[0].time != self.t):
            self.updateReadyQueue()
        
    #once we're done running, aggregate our average stats
    self.avgWaitTime /= self.totalBursts
    self.avgTurnaroundTime /= self.totalBursts
            
    self.showStopMessage()'''