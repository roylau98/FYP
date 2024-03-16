from utilities.utils import CSVparser
from utilities.utils import butter_lowpass_filter
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import argparse
from scipy.signal import find_peaks


def main(input_file):
    CSI_DATA, _ = CSVparser(input_file)
    amp_csi_data = np.asarray(CSI_DATA["B0:CA:68:91:B2:F5"].getAmplitude(), dtype="float32")

    pca = PCA(n_components=4)
    amp_csi_pca = pca.fit_transform(amp_csi_data).transpose()

    fig, ax = plt.subplots(2, 2, figsize=(10, 6))
    ax = ax.ravel()

    for i in range(4):
        plot = butter_lowpass_filter(amp_csi_pca[i], 0.3141, 40)
        #peaks, _ = find_peaks(plot, height=0)
        ax[i].plot(amp_csi_pca[i])
        ax[i].plot(butter_lowpass_filter(amp_csi_pca[i], 0.3141, 40))
        #ax[i].plot(peaks, plot[peaks], "x")
        # ax[i].plot(amp_csi_pca[i])
        ax[i].set_xlabel("Packets")
        ax[i].set_ylabel("CSI Amplitude")
        ax[i].set_title(f"({chr(97+i)})")

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
