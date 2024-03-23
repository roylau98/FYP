import sys
sys.path.insert(1, '..')

from implementation.ESP32_CSI_Visualiser.utilities.utils import CSVparser, butter_lowpass_filter
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import argparse


def main(input_file, MAC, output_file):
    CSI_DATA, _ = CSVparser(input_file)
    timestamp = CSI_DATA[MAC].getTimeStamp()
    amp_csi_data = np.asarray(CSI_DATA[MAC].getAmplitude(), dtype="float32")
    amp_csi_data = StandardScaler().fit_transform(amp_csi_data)

    pca = PCA(n_components=4)
    # take the fourth principal component
    amp_csi_pca = pca.fit_transform(amp_csi_data).transpose()[3]

    fig, ax = plt.subplots(1, 2, figsize=(10, 5), tight_layout=True)
    ax = ax.ravel()
    ax[0].scatter(timestamp, butter_lowpass_filter(amp_csi_pca, 0.2513, 25), s=3)
    ax[1].plot(butter_lowpass_filter(amp_csi_pca, 0.2513, 25))
    ax[0].set_xlabel("Time (seconds)")
    ax[0].set_ylabel("PCA 4")
    ax[1].set_xlabel("Packets")
    ax[1].set_ylabel("PCA 4")
    ax[0].set_title(f"(a)")
    ax[1].set_title(f"(b)")
    plt.suptitle('PCA of CSI Amplitude')
    fig.tight_layout()

    plt.savefig(f"{output_file}.png", bbox_inches='tight')
    plt.show()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='PCA Analysis script.')
    parser.add_argument('input_file', help='CSV file to process')
    parser.add_argument('MAC', help='MAC of receiver')
    parser.add_argument('output_file', help='Saved plot name')
    args = parser.parse_args()
    main(args.input_file, args.MAC, args.output_file)
