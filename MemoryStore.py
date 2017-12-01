"""
The MemoryStore class represents an array of memory slots with a set number of frames
"""
class MemoryStore():
    """
    MemoryStore contructor: creates a new memory store with the desired number of frames
    @param numFrames: the fixed number of frames that can be stored here
    @param framesPerLine: optional arg specifying how many frames of memory to output per-line (has no effect on internal repr)
    """
    def __init__(self, numFrames, framesPerLine=32):
        self.numFrames = numFrames
        self.framesPerLine = framesPerLine
        self.memory = '-'*numFrames
        
    """
    return a string representing this store's memory, split into lines as specified by framesPerLine
    """
    def __str__(self):
        return '\n'.join([self.memory[i:i+self.framesPerLine] for i in range(0, self.numFrames, self.framesPerLine)])

print(MemoryStore(256))