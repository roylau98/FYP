import math
import pandas as pd
import re
from scipy.signal import butter, lfilter
from datetime import datetime

def process(csi_data):
    # Parser
    try:
        csi_data = csi_data.split(" ")
        csi_data[0] = csi_data[0].replace("[", "")
        csi_data[-1] = csi_data[-1].replace("]", "")

        csi_data.pop()
        csi_data = [int(c) for c in csi_data if c]
        imaginary = []
        real = []
        for i, val in enumerate(csi_data):
            if i % 2 == 0:
                imaginary.append(val)
            else:
                real.append(val)

        csi_size = len(csi_data)
        amplitudes = []
        if len(imaginary) > 0 and len(real) > 0:
            for j in range(int(csi_size / 2)):
                amplitude_calc = math.sqrt(imaginary[j] ** 2 + real[j] ** 2)
                amplitudes.append(amplitude_calc)

        return amplitudes
    except:
        return []

def CSVparser(CSVFile):
    CSI_amplitudes = {}
    dataframe = pd.read_csv(CSVFile)
    macAddresses = list(set(dataframe["mac"]))
    mac_CSI = dataframe[["mac", "CSI_DATA", "local_timestamp"]]

    pattern = r'([0-9A-F]{2}:?){6}'
    macAddresses = [x for x in macAddresses if re.search(pattern, str(x))]

    for mac in macAddresses:
        filtered_df = mac_CSI.loc[mac_CSI["mac"] == mac]
        print(filtered_df)
        amplitudes = []
        for index, row in filtered_df.iterrows():
            amp = process(row["CSI_DATA"])
            if len(amp) > 0:
                amplitudes.append(amp)

        startTime = filtered_df["local_timestamp"].iloc[0]
        startTime = datetime.strptime(startTime, "%d/%m/%Y_%H:%M:%S")
        endTime = filtered_df["local_timestamp"].iloc[-1]
        endTime = datetime.strptime(endTime, "%d/%m/%Y_%H:%M:%S")
        difference = (endTime - startTime).total_seconds()
        frequency = len(amplitudes) / difference
        print(frequency)

        CSI_amplitudes[mac] = {"amplitudes": amplitudes, "frequency": frequency}
    return CSI_amplitudes, macAddresses


def butter_lowpass(cutoffFrequency, samplingFrequency, order=2):
    try:
        nyquist = 1/(2*samplingFrequency)
        #normal_cutoff = cutoffFrequency / (samplingFrequency / 2)
        normal_cutoff = cutoffFrequency / nyquist
        print(nyquist, normal_cutoff)
        b, a = butter(order, normal_cutoff, btype='lowpass', analog=False)
        return b, a
    except Exception as e:
        raise e


def butter_lowpass_filter(data, cutoffFrequency, samplingFrequency, order=2):
    b, a = butter_lowpass(cutoffFrequency, samplingFrequency, order=order)
    y = lfilter(b, a, data)
    return y