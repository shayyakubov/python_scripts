

def splitCoordForSig(lenSig,width):

    subCoord = list(range(0,lenSig,width))
    if subCoord[-1] < lenSig-1:# in case it not devide exactly
        subCoord.append(lenSig-1)
    intervals = [[subCoord[i], subCoord[i+1]-1] for i in range(len(subCoord)-1)]
    intervals[-1][1] = intervals[-1][1] +1 # correct the last interval
    return intervals

