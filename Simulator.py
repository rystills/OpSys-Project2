import copy
import queue
from Event import Event, EventType
from MemoryStore import MemoryStore, MemoryAlgorithm
import sys

#set 'this' to point to this module, so we can maintain module-wide globals
this = sys.modules[__name__]

#The Simulator class is a static class responsible for emulating our CPU, Running through the input processes using the selected algorithm
this.algo = MemoryAlgorithm.bestFit
this.simTime = 0
this.processes = []
this.events = queue.PriorityQueue()
this.contiguous = True
this.memStore = MemoryStore()

"""
Reset the simulator, clearing all processes, and setting time back to 0
"""
def reset():
    this.simTime = 0
    this.processes = []
    this.events = []
    this.memStore = MemoryStore()
    
"""
add an event with the specified time and type for the specified process to the event queue
@param eventType: the type of event to add
@param time: the time at which the event will occur
@param process: the process to which the event corresponds
"""
def addEvent(eventType, time, process):
    this.events.put(Event(eventType,time,process))

"""
show a message indicating that the Simulator is starting up
"""
def showStartMessage():
    print("time 0ms: Simulator started ({0} -- {1})".format("Contiguous" if this.contiguous else "Non-contiguous", this.algo.name))
    
"""
show a message indicating that the Simulator has ended
"""
def showStopMessage():
    print("time {0}ms: Simulator ended ({1} -- {2})".format(this.simTime, "Contiguous" if this.contiguous else "Non-contiguous", this.algo.name))
    
"""
process the specified event, calling the corresponding helper method
@param event: the event to process
"""
def processEvent(event):
    #process switch in event type
    if (event.eType == EventType.SwitchIn):
        handleSwitchIn(event)
    #process switch out event type
    elif (event.eType == EventType.SwitchOut):
        handleSwitchOut(event)
        
"""
when a process switches in, display that information and add it to the Memory Store
@param event: the event containing information about the process that just arrived
"""
def handleSwitchIn(event):
    p = event.process
    print("time {0}ms: Process {1} arrived (requires {2} frames)".format(this.simTime, p.pid, p.arrivalRunPairs[p.pairsCompleted][1]))
    
    if (this.algo == MemoryAlgorithm.nextFit):
        this.memStore.addProcessNext(p)
    elif (this.algo == MemoryAlgorithm.firstFit):
        this.memStore.addProcessFirst(p)
    elif (this.algo == MemoryAlgorithm.bestFit):
        this.memStore.addProcessBest(p)

"""
when a process switches out, display that information and remove it from the Memory Store
@param event: the event containing information about the process that just left
"""
def handleSwitchOut(event):
    p = event.process
    print("time {0}ms: Process {1} removed:".format(this.simTime, p.pid))
    this.memStore.removeProcess(p)
    print(this.memStore)
    p.pairsCompleted += 1

"""
run the simulation
"""
def run():
    this.showStartMessage()
    #populate the event queue with the arrival event for all processes
    for p in this.processes:
        addEvent(EventType.SwitchIn,p.arrivalRunPairs[0], p)
        
    #jump from event to event
    while(not this.events.empty()):
        #get the current event and update time
        currEvent = this.events.get()
        this.simTime = currEvent.time
        
        #process the current event
        this.processEvent(currEvent)
    
    this.showStopMessage()