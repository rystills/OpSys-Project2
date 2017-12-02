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
        
        #store a list of tuples containing the position and size of each process
        self.processes = []
        
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

#test MemoryStore __str__ if we run this class file directly
if __name__ == "__main__":
    #print("MemoryStore Sample Output: \n" + str(MemoryStore()))
    testMS = MemoryStore()
    print(testMS.getFreeMemoryLocations())
    print(testMS.getFreeMemory())
    testMS.memory = testMS.memory[:4] + 'a' + testMS.memory[5:]
    print(testMS.getFreeMemoryLocations())
    print(testMS.getFreeMemory())