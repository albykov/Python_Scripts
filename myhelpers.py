__author__ = 'abykov'

def getCurrentDateforFileName():
    import time
    return (time.strftime("%y%m%d"))

def getCurrentDateTimeforFileName():
    import time
    return (time.strftime("%y%m%d%H%M"))

def getNewFilePathWithDateNoSpaces(ffn):
    import os

    fn_noExt = os.path.splitext(os.path.basename(ffn))[0]
    fn_noExt_NoSpaces = fn_noExt.replace(' ', '')
    fExt = os.path.splitext(ffn)[1]
    fDir = os.path.dirname(ffn)

    return fDir + '\\' +fn_noExt_NoSpaces + '_' +getCurrentDateTimeforFileName() + fExt