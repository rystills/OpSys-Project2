"""
The Process class represents a single process on our CPU
"""
class Process():
    """
    Process contructor: creates a new process with the specified properties
    @param pid: the string ID given to the process by the input file; used for tie-breaking
    @param memSize: the number of memory frames required by this process
    @param arrivalRunPairs: a list of arrival time, run time pairs for the process, separated by '/'
    """
    def __init__(self, pid, memSize, arrivalRunPairs):
        self.pid = pid
        
        if (not memSize.isdigit()):
            raise TypeError()
        self.memSize = int(memSize)
        
        #read the arrival run pairs one by one, raising an exception if any of them is not a pair or contains non-ints
        self.arrivalRunPairs = []
        for i in arrivalRunPairs:
            ARPair = i.split('/')
            if (not (len(ARPair) == 2 and ARPair[0].isdigit() and ARPair[1].isdigit())):
                raise TypeError()
            self.arrivalRunPairs.append( (int(ARPair[0]), int(ARPair[1])) )
   
    """
    return a string displaying this process' pid, memsize, and arrival/run pairs
    """         
    def __repr__(self):
        return "PID {0}: size={1} arrivalRunPairs={2}".format(self.pid,self.memSize,self.arrivalRunPairs)
                
    """
    override the less-than operator for priority queue sorting based on PID
    @param other: the process we are comparing ourselves to
    """
    def __lt__(self, other):
        return self.pid < other.pid