__author__ = 'abykov'

def getCurrentDateforFileName():
    #other format %Y%m%d-%H%M%S
    import time
    return (time.strftime("%y%m%d"))

#print getCurrentDateforFileName()