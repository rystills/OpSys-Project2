import sys
from Process import Process
from MemoryStore import MemoryStore
    
"""
display a message on standard error and exit the program
@param msg: the message to display
"""
def exitError(msg):
    print("Error:",msg,file=sys.stderr)
    sys.exit(1)
    
"""
read the process info from the specified input file
@param fileName: the name of the file containing our process info
@returns a list of processes corresponding to the data in the input file
"""
def readInput(fileName):
    processes = []
    try:
        #read the file line by line, ignoring lines that start with a # or lines that are entirely whitespace
        for line in (l for l in open(fileName) if l[0] != '#' and l.strip() != ""):
            #make sure the input line contains at least 3 elements (type-checking and validity will be handled in Process constructor) 
            splitLine = line.strip().split(' ')
            if (len(splitLine) < 3):
                raise TypeError()
            processes.append(Process(splitLine[0],splitLine[1],splitLine[2:]))
    except (IOError, TypeError):
        exitError("Invalid input file format")
    return processes
  
"""
main method: parse the input file while checking for errors, then start our simulator instance
"""      
def main():
    #make sure the user specifies the correct number of arguments
    if (len(sys.argv) < 2):
        exitError("ERROR: Invalid arguments\nUSAGE: /usr/bin/python3.5 project1.py p1-input01.txt simout01.txt")

    #extract our processes from the input file, then begin the simulation
    processes = readInput(sys.argv[1])
    sim = MemoryStore()
    
if __name__ == "__main__":
    main()