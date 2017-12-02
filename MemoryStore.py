from Process import Process
from enum import Enum
"""
State is a simple enum containing each of the potential process states
"""
class MemoryAlgorithm(Enum):
    nextFit = 1
    firstFit = 2
    bestFit = 3

"""
The MemoryStore class represents an array of memory slots with a set number of frames
"""
class MemoryStore():
    """
    MemoryStore contructor: creates a new memory store with the desired number of frames
    @param numFrames: the fixed number of frames that can be stored here
    @param framesPerLine: optional arg specifying how many frames of memory to output per-line (has no effect on internal repr)
    """
    def __init__(self, numFrames=256, framesPerLine=32):
        self.numFrames = numFrames
        self.framesPerLine = framesPerLine
        self.memory = '.'*numFrames
        
        #store a list of processes currently in the memory store
        self.processes = []
        
        #keep track of the current simulation time
        self.simTime = 0
        
    """
    get the amount of free memory currently available in the store
    """
    def getFreeMemory(self):
        return self.memory.count('.')
    
    """
    get a list containing the location and size of each free block of memory
    """
    def getFreeMemoryLocations(self):
        memLocs = []
        inMemBlock = False
        memStartPos = -1
        #iterate over the memory store to find the beginning of each block of memory
        for i in range(len(self.memory)):
            if (self.memory[i] == '.'):
                if (not inMemBlock):
                    inMemBlock = True
                    memStartPos = i
            else:
                if (inMemBlock):
                    inMemBlock = False
                    memLocs.append([memStartPos,(i-memStartPos)])
        #if we were still reading free memory when we reached the end of the store, add the remaining memory to the list of locations
        if (inMemBlock):
            memLocs.append([memStartPos,(i+1-memStartPos)])
        return memLocs
        
    """
    return a string representing this store's memory, split into lines as specified by framesPerLine
    """
    def __str__(self):
        border = '='*self.framesPerLine
        return border + '\n' + '\n'.join([self.memory[i:i+self.framesPerLine] for i in range(0, self.numFrames, self.framesPerLine)]) + '\n' + border

    """
    add a process to the store
    @param process: the process to be added
    """
    def addProcess(self,process):
        freeLocs = self.getFreeMemoryLocations()
        #check all free memory locations for the first location big enough to contain the new process
        for loc in freeLocs:
            if (loc[1] >= process.memSize):
                #we found a location for the process! add it to the processes list
                self.processes.append(process)
                process.memLocation = loc[0]
                self.memory = self.memory[:loc[0]] + process.pid*process.memSize + self.memory[loc[0]+process.memSize:]
                process.memEnterTime = self.simTime

"""
test printing a new Memory Store instance
"""
def testStoreOutput():
    print("MemoryStore Sample Output: \n" + str(MemoryStore()))
    
"""
test finding all free memory locations
"""
def testFreeMemoryLocations():
    testMS = MemoryStore()
    print("free memory locations for initial Store:", testMS.getFreeMemoryLocations())
    print("free memory size:", testMS.getFreeMemory())
    testMS.memory = testMS.memory[:4] + 'a' + testMS.memory[5:]
    print("free memory locations after inserting 'a' at position 4:", testMS.getFreeMemoryLocations())
    print("free memory size after inserting 'a' at position 4:", testMS.getFreeMemory())
    
"""
test adding a process to a new Memory Store
"""
def testAddProcess():
    testMS = MemoryStore()
    print("initial processes:",testMS.processes)
    print("initial memory locations:",testMS.getFreeMemoryLocations())
    testMS.addProcess(Process('A',"6",["0/1"]))
    print("new processes:",testMS.processes)
    print("new memory locations:",testMS.getFreeMemoryLocations())
    
#test MemoryStore __str__ if we run this class file directly
if __name__ == "__main__":
    testAddProcess()