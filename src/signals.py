import sys
# import numpy
# import math as m

def signal_metrics(relative_distance): #  , range_rate): #this function calculates the metric data of a signal like latency and doppler shift
    # todo: add doppler shift to this when the ui is made so the user can set the center frequency for the doppler metics
    c = 299792458 # speed of light in a vacuum

    sig_latency = (relative_distance * 1000) / c # calculates the signals latency

    # sig_doppler = frequency * range_rate # calculates the doppler shift a signal

    return sig_latency
