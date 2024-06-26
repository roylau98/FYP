from utils import process, butter_lowpass_filter
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def process_data():
    extension = ".csv"
    dict = {}
    from sklearn.decomposition import PCA

    for i in range(10):
        dict[str(i)] = []

    for file in os.listdir("../../data/keystroke_inference_raw/"):
        if file.endswith(extension):
            df = pd.read_csv("../../data/keystroke_inference_raw/" + file)

            # 64 x 40
            for i in range(40, len(df)-41, 41):
                pca = PCA(n_components=4)

                subset = df.iloc[i:i+41]
                key = subset.iloc[0]["type"].split(" ")[-1]

                temp = []
                for j in range(1, len(subset)):
                    amp, _ = process(subset.iloc[j]['CSI_DATA'])
                    temp.append(amp)

                # 64 x 40
                new_nparray = np.asarray(temp, dtype='float32')
                new_nparray = new_nparray.transpose()
                # apply butterworth low pass filter on all subcarriers
                denoised = []
                for subcarrier in new_nparray:
                    denoised.append(butter_lowpass_filter(subcarrier, 10, 25))

                # 40 x 64 for PCA, reduce to 4 components
                denoised = np.asarray(denoised, dtype='float32')
                denoised = denoised.transpose()
                # scale the values
                denoised = StandardScaler().fit_transform(denoised)
                pca_newnparray = pca.fit_transform(denoised)

                # 4 x 40, take the first principal component
                pca_newnparray = pca_newnparray.transpose()[0]
                # 2nd round of denoising
                denoised = butter_lowpass_filter(pca_newnparray, 5, 25)
                dict[key].append([denoised])

    for key, value in dict.items():
        final_array = np.asarray(dict[key], dtype='float32')
        # shuffle the dataset, and split it
        # 70:20:10
        np.random.shuffle(final_array)
        test_array, val_array, train_array = final_array[:50], final_array[50:150], final_array[150:]
        print(train_array.shape, val_array.shape, test_array.shape)
        np.save(f'../../data/processed_data/{key}_table_test.npy', test_array)
        np.save(f'../../data/processed_data/{key}_table_val.npy', val_array)
        np.save(f'../../data/processed_data/{key}_table_train.npy', train_array)

def main():
    process_data()

if __name__=='__main__':
    main()
