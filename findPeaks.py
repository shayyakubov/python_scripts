
import numpy as np
import sigPro as sp
import matplotlib.pyplot as plt

def findPeaks(sig):
    """"
    This function find peaks for align signal of duration time of 4 seconds
    """
    #parameters
    lenSig = len(sig)
    # (getBufParams.bufParams['maxBPM']/60) is maximum peaks per second
    maxNumSampleForOnePeak = int(np.floor(sp.globals.bufParams['sampleRate'] / (sp.globals.bufParams['maxBPM'] / 60)))
    localMaximaTol = int(maxNumSampleForOnePeak)
    peaksCloseToPeaksToRemove =[]
    peaksNonLocalMaximaToRemove =[]

    #alignSig = sp.alignRawSignal(sig)# remove linear trend
    alignSig = sig

    intervals = sp.splitCoordForSig(lenSig,maxNumSampleForOnePeak)
    peaksLocal = [np.argmax(alignSig[intervals[i][0]:intervals[i][1] + 1]) for i in range(len(intervals))]
    startInterval = [intervals[i][0] for i in range(len(intervals))]
    peaks = [startInterval[i]+peaksLocal[i] for i in range(len(intervals))]

    #plot all peaks
    if 0:
        plt.plot(alignSig)
        plt.plot(peaks, [alignSig[p] for p in peaks], 'go')
        plt.title('peaks for each interval')
        plt.show()

    # remove peaks in fringes
    for i in range(2):
        if peaks[0]<= maxNumSampleForOnePeak:
            del peaks[0]

    for i in range(2):
        if peaks[-1]>= lenSig - maxNumSampleForOnePeak:
            del peaks[-1]

    if 0:
        plt.plot(alignSig)
        plt.plot(peaks, [alignSig[p] for p in peaks], 'go')
        plt.title('peaks after remove fringes')
        plt.show()


    #remove peaks that are not local maxima
    for p in peaks:
        currentMax = alignSig[p]
        for i in range(1,localMaximaTol+1):
            if alignSig[p + i]>currentMax or alignSig[p - i]>currentMax:
                peaksNonLocalMaximaToRemove.append(p)
                break
    peaks = [p for p in peaks if p not in peaksNonLocalMaximaToRemove]

    if 0:
        plt.plot(alignSig)
        plt.plot(peaks, [alignSig[p] for p in peaks], 'go')
        plt.title('number peaks removed from non local maxima criterion: ' + str(len(peaksNonLocalMaximaToRemove)))
        plt.show()

    if 0:
        plt.subplot(2, 1, 1)
        plt.plot(alignSig)
        plt.plot(peaks, [alignSig[p] for p in peaks], 'ro')
        plt.title('Detected Peaks (align)')
        plt.subplot(2, 1, 2)
        plt.plot(sig)
        plt.plot(peaks, [sig[p] for p in peaks], 'ro')
        plt.title('Detected Peaks (raw)')
        plt.show()
    return peaks
