import math

import pandas as pd
import re
import pywt

from scipy.signal import butter, filtfilt
from hampel import hampel
from ESP32_CSI_Visualiser.utilities.CSI import CSIDATA

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


def CSVparser(CSVFile):
    CSI_amplitudes = {}
    dataframe = pd.read_csv(CSVFile)
    macAddresses = list(set(dataframe["mac"]))
    mac_CSI = dataframe[["mac", "CSI_DATA", "local_timestamp", "real_timestamp"]]

    pattern = r'([0-9A-F]{2}:?){6}'
    macAddresses = [x for x in macAddresses if re.search(pattern, str(x))]

    for mac in macAddresses:
        filtered_df = mac_CSI.loc[mac_CSI["mac"] == mac]
        # 2D array of packets x subcarriers
        amplitudes = []
        phases = []
        timestamp = []
        for index, row in filtered_df.iterrows():
            amp, phase = process(row["CSI_DATA"])
            if len(amp) > 0:
                amplitudes.append(amp)
            if len(phase) > 0:
                phases.append(phase)
            if len(amp) and len(phase) > 0:
                timestamp.append(row["real_timestamp"])

        CSI_amplitudes[mac] = CSIDATA(amplitudes, phases, timestamp)
    return CSI_amplitudes, macAddresses


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


def hampel_filter(data, window_size):
    return hampel(pd.Series(data), window_size=window_size).filtered_data.tolist()


def dwt_filter(data, wavelet):
    return pywt.dwt(data, wavelet=f"db{wavelet}")
