import copy
import queue
from Event import Event, EventType
from MemoryStore import MemoryAlgorithm
from pip.cmdoptions import process_dependency_links

"""
The Simulator class is a static class responsible for emulating our CPU, Running through the input processes using the selected algorithm
"""
class Simulator():
    algo = MemoryAlgorithm.bestFit
    simTime = 0
    processes = []
    events = []
    
    """
    Reset the simulator, clearing all processes, and setting time back to 0
    """
    @staticmethod
    def reset():
        __class__.simTime = 0
        __class__.processes = []
        __class__.events = []