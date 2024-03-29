from Process import Process
from enum import Enum
from Event import Event, EventType
import bisect
import Simulator

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
        
        #store a list of processes currently in the memory store (sorted in order of smallest to greatest memLocation)
        self.processes = []
        
        self.lastPlacedLoc = 0
        
        self.t_memmove = 1
        
        #dict of pid:[(pageNum,frameNum)]
        self.pageTable = {}
        
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
    print the current state of the page table
    """
    def displayPageTable(self):
        print("PAGE TABLE [page,frame]:")
        #print out the page table ordered by pid
        keys = list(self.pageTable.keys())
        keys.sort()
        for key in keys:
            print("{0}: ".format(key),end='')
            #print out all entries corresponding to this key, with a newline after every 10th entry
            vals = self.pageTable[key]
            for i in range(len(vals)):
                print((' ' if i%10 != 0 else '') + str(vals[i]).replace('(','[').replace(')',']').replace(' ',''),end=('\n' if (i+1)%10 == 0 else ''))
            #print a newline before moving on to the next value unless we just finished a row
            if (len(vals) % 10 != 0):
                print()
                      
    """
    check whether or not a defragmentation will free up enough space to place the desired process
    @param memNeeded: the amount of memory we need to have after defragmenting
    """
    def defragmentWillWork(self, memNeeded):
        return memNeeded <= self.getFreeMemory()

    """
    defragment our memory, moving processes up to fill all free gaps, and increasing simTime accordingly
    """
    def defragment(self):
        #keep track of how far we move time forward so we can push back events accordingly
        prevSimTime = Simulator.simTime
        affectedProcesses = []
        
        self.lastPlacedLoc = 0
        for proc in self.processes:
            earliestFree = self.memory.find('.')
            if (earliestFree < proc.memLocation):
                #there is free space in our memory before this location's starting value; move it up and increment time accordingly
                removedMem = self.memory[:proc.memLocation] + self.memory[proc.memLocation+proc.memSize:]
                reinsertedMem = removedMem[:earliestFree] + proc.pid * proc.memSize + removedMem[earliestFree:]
                self.memory = reinsertedMem
                #add t_memmove for each frame of memory in the process
                Simulator.simTime += self.t_memmove * proc.memSize
                affectedProcesses.append(proc)
                proc.memLocation = earliestFree
        
        timeDiff = Simulator.simTime - prevSimTime
        
        #update all events to compensate for elapsed time during defragmentation
        for ev in Simulator.events.queue:
                ev.time += timeDiff
        
        print("time {0}ms: Defragmentation complete (moved {1} frames: {2})".format(Simulator.simTime,timeDiff,
                                                                                    str([p.pid for p in affectedProcesses]).strip('[').strip(']').replace("'","")))
        print(self)

    """
    insert the specified process into our processes list sorted by memLocation
    """
    def insertProcess(self,process):
        bisect.insort(self.processes,process)
        
    """
    remove the specified process from the memory store
    """
    def removeProcess(self,process):
        if (process.pid in self.pageTable):
            self.pageTable.pop(process.pid)
            #iterate over memory, removing all references to the process
            for i in range(len(self.memory)):
                if (self.memory[i] == process.pid):
                    self.memory = self.memory[:i] + '.' + self.memory[i+1:]
        else:
            #remove the process from memory
            self.memory = self.memory[:process.memLocation] + '.'*process.memSize + self.memory[process.memLocation+process.memSize:]
                
        #remove the process from our processes list
        self.processes.remove(process)
    
    """
    add the desired process at the specified location in memory
    @param process: the process to add into memory
    @param loc: the location in memory at which to add the process
    @returns true
    """
    def addProcessAtLocation(self,proc,loc):
        proc.memLocation = loc
        self.memory = self.memory[:loc] + proc.pid*proc.memSize + self.memory[loc+proc.memSize:]
        proc.memEnterTime = Simulator.simTime
        self.insertProcess(proc)
        self.lastPlacedLoc = loc + proc.memSize
        return True
    
    """
    check if we are on the first pass of attempting to add a process. if so, defrag if it will generate enough space
    @param firstRun: whether this is the first time we have attempted to add the process during this event (true) or not (false)
    @param func: the add function to call again after defragmenting
    @param proc: the process we wish to add
    @returns a call to the specified function after defragmenting if this is the first run and defragmenting will help; otherwise false
    """
    def checkFirstRun(self,firstRun, func, proc):
        if (firstRun):
            if (self.defragmentWillWork(proc.memSize)):
                print("time {0}ms: Cannot place process {1} -- starting defragmentation".format(Simulator.simTime,proc.pid))
                self.defragment()
                return func(proc,False)
        #we already defragmented and still didn't find a location, so nothing we can do
        return False
    
    """
    add a process to memory utilizing our page table
    @param process: the process to add to memory
    @returns whether the process was added successfully (true) or not (false)
    """
    def addProcessPageTable(self, process):
        #first make sure there is enough space in memory
        if (not self.defragmentWillWork(process.memSize)):
            return False
        
        #begin building up a list of pid memory locations, to be added to our pageTable at the end
        newPages = []
        pagesAdded = 0
        for i in range(len(self.memory)):
            if (self.memory[i] == '.'):
                #this memory slot is free; add the process here
                self.memory = self.memory[:i] + process.pid + self.memory[i+1:]
                newPages.append((pagesAdded,i))
                pagesAdded += 1
                
                #stop once we've allocated enough pages
                if (pagesAdded == process.memSize):
                    break
        
        #apply the new pageList to the pageTable and return success  
        self.pageTable[process.pid] = newPages
        self.processes.append(process)
        return True
    
    """
    add a process to the store using the next-fit algorithm
    @param process: the process to be added
    @param firstRun: whether we are running the process for the first time (true) or immediately after a defragmentation (false)
    """
    def addProcessNext(self,process, firstRun = True):
        #iterate from lastPlacedLoc to the end of memory, looking for a large enough slot
        pos = self.lastPlacedLoc
        while (pos+process.memSize <= len(self.memory)):
            if (self.memory[pos] == '.'):
                #this is a valid space and our process will fit; now check that all required slots are free
                slotsFree = True
                for i in range(process.memSize):
                    if (self.memory[pos+i] != '.'):
                        slotsFree = False
                        break
                if (slotsFree):
                    return self.addProcessAtLocation(process,pos)
            pos += 1
        
        #we didn't find a valid memory location after lastPlacedLoc, so now let's search again from the beginning up to lastPlacedLoc
        pos = 0
        while (pos < self.lastPlacedLoc and pos+process.memSize <= len(self.memory)):
            if (self.memory[pos] == '.'):
                #this is a valid space and our process will fit; now check that all required slots are free
                slotsFree = True
                for i in range(process.memSize):
                    if (self.memory[pos+i] != '.'):
                        slotsFree = False
                        break
                if (slotsFree):
                    return self.addProcessAtLocation(process,pos)
            pos += 1
        
        #we didn't find a location at which to place the process, so defragment and try again
        return self.checkFirstRun(firstRun,self.addProcessNext,process)         

    """
    add a process to the store using the first-fit algorithm
    @param process: the process to be added
    @param firstRun: whether we are running the process for the first time (true) or immediately after a defragmentation (false)
    """
    def addProcessFirst(self,process, firstRun = True):
        freeLocs = self.getFreeMemoryLocations()
        #check all free memory locations for the first location big enough to contain the new process
        for loc in freeLocs:
            if (loc[1] >= process.memSize):
                #we found a location for the process! add it to the processes list
                return self.addProcessAtLocation(process,loc[0])
            
        #we didn't find a location at which to place the process, so defragment and try again
        return self.checkFirstRun(firstRun,self.addProcessFirst,process)
                
    """
    add a process to the store using the best-fit algorithm
    @param process: the process to be added
    @param firstRun: whether we are running the process for the first time (true) or immediately after a defragmentation (false)
    """
    def addProcessBest(self,process, firstRun = True):
        freeLocs = self.getFreeMemoryLocations()
        #check all free memory locations for the smallest location big enough to contain the new process
        smallestValidLocSize = None
        smallestValidLoc = None
        for loc in freeLocs:
            if (loc[1] >= process.memSize):
                if (smallestValidLocSize == None or loc[1] < smallestValidLocSize):
                    smallestValidLocSize = loc[1]
                    smallestValidLoc = loc[0]
                    
        if (smallestValidLoc != None):
            #we found a location for the process! add it to the processes list
            return self.addProcessAtLocation(process,smallestValidLoc)
            
        #we didn't find a location at which to place the process, so defragment and try again
        return self.checkFirstRun(firstRun,self.addProcessBest,process)