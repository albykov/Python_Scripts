__author__ = 'abykov'
def getShortTitleNameNoSpaces(tn):
    return tn.split('+')[0].replace(' ', '') + tn.split('+')[1].zfill(3)

print getShortTitleNameNoSpaces('941 299 535 +3')