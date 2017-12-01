import sys
    
"""
display a message on standard error and exit the program
@param msg: the message to display
"""
def exitError(msg):
    print("Error:",msg,file=sys.stderr)
    sys.exit(1)
