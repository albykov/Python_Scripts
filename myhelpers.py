__author__ = 'abykov'

def getCurrentDateforFileName():
    #other format %Y%m%d-%H%M%S
    import time
    return (time.strftime("%y%m%d"))

def getCurrentDateTimeforFileName():
    #other format %Y%m%d-%H%M%S
    import time
    return (time.strftime("%y%m%d%H%M"))

#print getCurrentDateforFileName()

def getNewFilePathWithDateNoSpaces(ffn):
    import os

    fn_noExt = os.path.splitext(os.path.basename(ffn))[0]
    fn_noExt_NoSpaces = fn_noExt.replace(' ', '')
    fExt = os.path.splitext(ffn)[1]
    fDir = os.path.dirname(ffn)

    return fDir + '\\' +fn_noExt_NoSpaces + '_' +getCurrentDateTimeforFileName() + fExt

print getNewFilePathWithDateNoSpaces(r'D:\abykov\BigProjectFiles\151003 Lethbridge Ecological Inventory\titles_160411\RVMP titles222.xlsx')