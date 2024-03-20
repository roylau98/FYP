from utilities.utils import CSVparser
from utilities.utils import butter_lowpass_filter, dwt_filter
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
from scipy.signal import find_peaks


def main(input_file):
    CSI_DATA, _ = CSVparser(input_file)
    timestamp = pd.read_csv(input_file)[["mac", "real_timestamp"]]
    timestamp = timestamp.loc[timestamp['mac'] == "B0:CA:68:91:B2:F5"]["real_timestamp"].tolist()
    amp_csi_data = np.asarray(CSI_DATA["B0:CA:68:91:B2:F5"].getAmplitude(), dtype="float32")

    # denoised = []
    # for i in amp_csi_data.transpose():
    #     denoised.append(butter_lowpass_filter(i, 0.251, 25))
    #
    # amp_csi_data = np.asarray(denoised, dtype="float32").transpose()
    pca = PCA(n_components=4)
    amp_csi_pca = pca.fit_transform(amp_csi_data).transpose()
    fig, ax = plt.subplots(2, 2, figsize=(10, 6))

    # ax = ax.ravel()
    #
    # for i in range(4):
    #     # plot = butter_lowpass_filter(amp_csi_pca[i], 0.3141, 40)
    #     # peaks, _ = find_peaks(plot, height=0)
    #     # ax[i].plot(amp_csi_pca[i])
    #     # one_pass = butter_lowpass_filter(amp_csi_pca[i], 0.251, 25)
    #     ax[i].scatter(timestamp, butter_lowpass_filter(amp_csi_pca[i], 0.251, 25), s=3)
    #     # ax[i].scatter(timestamp, amp_csi_pca[i], s=3)
    #     # ax[i].plot(peaks, plot[peaks], "x")
    #     # ax[i].plot(amp_csi_pca[i])
    #     ax[i].set_xlabel("Time (seconds)")
    #     ax[i].set_ylabel("CSI Amplitude")
    #     ax[i].set_title(f"({chr(97+i)})")

    plt.suptitle('PCA of CSI Amplitude')
    fig.tight_layout()
    # plt.savefig(f"{input_file.split('.')[0]}_PCA.png", bbox_inches='tight')
    plt.show()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='PCA Analysis script.')
    parser.add_argument('input_file', help='CSV file to process')
    # parser.add_argument('MAC', help='MAC of receiver')
    # args = parser.parse_args()
    # main(args.input_file, args.MAC)
    args = parser.parse_args()
    main(args.input_file)
