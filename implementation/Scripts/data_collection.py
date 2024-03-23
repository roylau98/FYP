from tqdm import tqdm
import csv

# adapted from ESP32 CSI python utilities
# https://github.com/StevenMHernandez/ESP32-CSI-Tool/blob/master/python_utils/read_stdin.py
from read_stdin import readline, ignore_until_first_csi_line

with open('<file location>', 'r') as f:
    labels = f.readline()

# ensures that last key is taken, 0 key will be ignored
labels = labels.split(",") + ["0"]
ignore_until_first_csi_line()
data = []
f = open('<file location>', 'a')
writer = csv.writer(f)
i = 0

with tqdm(total=40) as pbar:
    while i != len(labels):

        line = readline()
        newLine = line.split(",")

        # only capture CSI from the receiver, ignore "corrupted" data
        if "CSI_DATA" in line and line[17:34] == "B0:CA:68:91:B2:F5" and len(newLine[-1].split(" ")) == 129:
            data.append(newLine)
            pbar.update(1)

        if pbar.n == 40:
            data.append([f"Start Collection {labels[i]}"])
            writer.writerows(data)
            data = []
            print(f"Start collection {labels[i]}")
            i += 1
            pbar.refresh()
            pbar.reset()