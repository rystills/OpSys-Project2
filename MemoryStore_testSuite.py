from MemoryStore import *

func = ""

"""
test printing a new Memory Store instance
"""
def testStoreOutput():
    expectedOutput = """MemoryStore Sample Output: 
================================
................................
................................
................................
................................
................................
................................
................................
................................
================================"""
    realOutput = "MemoryStore Sample Output: \n{0}".format(MemoryStore())
    return compareOutput(expectedOutput, realOutput)
    
"""
test finding all free memory locations
"""
def testFreeMemoryLocations():
    expectedOutput = """free memory locations for initial Store: [[0, 256]]
free memory size: 256
free memory locations after inserting 'a' at position 4: [[0, 4], [5, 251]]
free memory size after inserting 'a' at position 4: 255
""" 
    realOutput = ""
    
    testMS = MemoryStore()
    realOutput += "free memory locations for initial Store: {0}\n".format(testMS.getFreeMemoryLocations())
    realOutput += "free memory size: {0}\n".format(testMS.getFreeMemory())
    testMS.memory = testMS.memory[:4] + 'a' + testMS.memory[5:]
    realOutput += "free memory locations after inserting 'a' at position 4: {0}\n".format(testMS.getFreeMemoryLocations())
    realOutput += "free memory size after inserting 'a' at position 4: {0}\n".format(testMS.getFreeMemory())
    return compareOutput(realOutput, expectedOutput)

"""
test adding a process to a new Memory Store
"""
def testAddProcessNext():
    expectedOutput = """initial processes: []
initial memory locations: [[0, 256]]
new processes: [PID A: size=6 arrivalRunPairs=[(0, 1)] memLoc=0 memEnterTime=0]
new memory locations: [[6, 250]]
"""
    realOutput = ""
    testMS = MemoryStore()
    realOutput += "initial processes: {0}\n".format(testMS.processes)
    realOutput += "initial memory locations: {0}\n".format(testMS.getFreeMemoryLocations())
    testMS.addProcessNext(Process('A',"6",["0/1"]))
    realOutput += "new processes: {0}\n".format(testMS.processes)
    realOutput += "new memory locations: {0}\n".format(testMS.getFreeMemoryLocations()) 
    return compareOutput(realOutput, expectedOutput)
    
"""
test adding a process to a new Memory Store
"""
def testAddProcessFirst():
    expectedOutput = """initial processes: []
initial memory locations: [[0, 256]]
new processes: [PID A: size=6 arrivalRunPairs=[(0, 1)] memLoc=0 memEnterTime=0]
new memory locations: [[6, 250]]
"""
    realOutput = ""
    testMS = MemoryStore()
    realOutput += "initial processes: {0}\n".format(testMS.processes)
    realOutput += "initial memory locations: {0}\n".format(testMS.getFreeMemoryLocations())
    testMS.addProcessFirst(Process('A',"6",["0/1"]))
    realOutput += "new processes: {0}\n".format(testMS.processes)
    realOutput += "new memory locations: {0}\n".format(testMS.getFreeMemoryLocations())
    return compareOutput(realOutput, expectedOutput)
    
"""
test adding a process to a new Memory Store
"""
def testAddProcessBest():
    expectedOutput = """initial processes: []
initial memory locations: [[0, 256]]
new processes: [PID A: size=6 arrivalRunPairs=[(0, 1)] memLoc=0 memEnterTime=0]
new memory locations: [[6, 250]]
"""
    
    realOutput = ""
    testMS = MemoryStore()
    realOutput += "initial processes: {0}\n".format(testMS.processes)
    realOutput += "initial memory locations: {0}\n".format(testMS.getFreeMemoryLocations())
    testMS.addProcessBest(Process('A',"6",["0/1"]))
    realOutput += "new processes: {0}\n".format(testMS.processes)
    realOutput += "new memory locations: {0}\n".format(testMS.getFreeMemoryLocations())
    return compareOutput(expectedOutput, realOutput)

"""
compare expected output to received output, displaying an error if test output does not match expected output
@param real: the output that was received when running the test
@param expected: the ouput that should have been received if the test passed
@returns whether real output matched expected output (true) or not (false)
"""
def compareOutput(real,expected):
    if (real != expected):
        print("TEST '{0}' FAILED! \nexpected: {1}\nreceived: {2}\n".format(str(func).split(' ')[1],expected,real))
        return False
    return True
    

if __name__ == "__main__":  
    testList = [testStoreOutput,testFreeMemoryLocations,testAddProcessNext,testAddProcessFirst,testAddProcessBest]
    testsPassed = 0
    testsRan = 0
    for func in testList:
        testsPassed += (1 if func() == True else 0)
        testsRan += 1
    print("Summary: {0} out of {1} tests passed".format(testsPassed,testsRan))