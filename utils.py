import math
import pandas as pd
import re

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
    mac_CSI = dataframe[["mac", "CSI_DATA"]]

    pattern = r'([0-9A-F]{2}:?){6}'
    macAddresses = [x for x in macAddresses if re.search(pattern, str(x))]
    print(macAddresses)
    for mac in macAddresses:
        filtered_df = mac_CSI.loc[mac_CSI["mac"] == mac]
        amplitudes = []
        for index, row in filtered_df.iterrows():
            amp = process(row["CSI_DATA"])
            if len(amp) > 0:
                amplitudes.append(amp)

        CSI_amplitudes[mac] = amplitudes
    return CSI_amplitudes, macAddresses
