import sys
sys.path.insert(1, '..')

import math

from scipy.signal import butter, filtfilt

def process(csi_data):
    # Parser
    try:
        csi_data = csi_data.replace("[", "").replace(" ]", "").split(" ")
        csi_data = [int(c) for c in csi_data if c]

        # corrupted data
        if len(csi_data) != 128:
            return [], []

        amplitudes = []
        phases = []
        for i in range(0, len(csi_data), 2):
            # (imaginary, real)
            amplitudes.append(math.sqrt(csi_data[i] ** 2 + csi_data[i+1] ** 2))
            phases.append(math.atan2(csi_data[i], csi_data[i+1]))

        return amplitudes, phases
    except:
        return [], []


def butter_lowpass(cutoffFrequency, samplingFrequency, order=2):
    try:
        nyquist = 0.5 * samplingFrequency
        normal_cutoff = cutoffFrequency / nyquist
        b, a = butter(order, normal_cutoff, btype='lowpass', analog=False)
        return b, a
    except Exception as e:
        raise e


def butter_lowpass_filter(data, cutoffFrequency, samplingFrequency, order=2):
    b, a = butter_lowpass(cutoffFrequency, samplingFrequency, order=order)
    y = filtfilt(b, a, data)
    return y
