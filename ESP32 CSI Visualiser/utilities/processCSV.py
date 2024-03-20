from utils import process, butter_lowpass_filter, dwt_filter
import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


def process_training_data():
    for i in range(10):
        output = []
        print(f"Processing file {i}")
        df = pd.read_csv(f"../data/raw_data/{i}_table.csv")

        temp = []
        for index, row in df.iterrows():
            curr_row = row['type']
            if 'End Collection' in curr_row:

                # 40 x 64, transposed to apply butterworth filter on all subcarriers
                new_nparray = np.asarray(temp, dtype='float32')
                new_nparray = new_nparray.transpose()

                denoised = []
                for subcarrier in new_nparray:
                    denoised.append(butter_lowpass_filter(subcarrier, 4.712, 40))

                # 64 x 40
                output.append(denoised)
                temp = []
            else:
                amp, _ = process(row['CSI_DATA'])
                temp.append(amp)

        final_array = np.asarray(output, dtype='float32')
        print(final_array.shape)

        # shuffle the dataset, and split it
        np.random.shuffle(final_array)
        test_array, val_array, train_array = final_array[:30], final_array[30:90], final_array[90:]
        print(train_array.shape, val_array.shape, test_array.shape)

        np.save(f'../data/processed_data_denoised_butter/{i}_table_test.npy', test_array)
        np.save(f'../data/processed_data_denoised_butter/{i}_table_val.npy', val_array)
        np.save(f'../data/processed_data_denoised_butter/{i}_table_train.npy', train_array)


def process_env_data():
    extension = ".csv"
    for file in os.listdir("../../data/real_env"):
        if file.endswith(extension):
            print(file)
            df = pd.read_csv("../data/real_env/" + file)

            output = []
            temp = []
            for index, row in df.iterrows():
                curr_row = row['type']
                if 'End Collection' in curr_row:
                    new_nparray = np.asarray(temp, dtype='float32')
                    new_nparray = new_nparray.transpose()

                    denoised = []
                    for subcarrier in new_nparray:
                        denoised.append(butter_lowpass_filter(subcarrier, 4.712, 40))

                    output.append(denoised)
                    temp = []
                else:
                    amp, _ = process(row['CSI_DATA'])
                    temp.append(amp)

            final_array = np.asarray(output, dtype='float32')
            print(final_array.shape)
            np.save(f'../data/real_env_denoised_butter/{file.split(".")[0]}.npy', final_array)


def process_movement_data():
    # ignore the first sample
    extension = ".csv"
    dict = {}

    for i in range(10):
        dict[str(i)] = []

    for file in os.listdir("../../data/movement_new"):
        if file.endswith(extension):
            df = pd.read_csv("../data/movement_new/" + file)

            # 64 x 40
            for i in range(40, len(df)-41, 41):
                subset = df.iloc[i:i+41]
                key = subset.iloc[0]["type"].split(" ")[-1]

                temp = []
                for j in range(1, len(subset)):
                    amp, _ = process(subset.iloc[j]['CSI_DATA'])
                    temp.append(amp)

                new_nparray = np.asarray(temp, dtype='float32')
                new_nparray = new_nparray.transpose()
                denoised = []
                for subcarrier in new_nparray:
                    denoised.append(butter_lowpass_filter(subcarrier, 7.5398, 25))

                dict[key].append(denoised)

    for key, value in dict.items():
        final_array = np.asarray(dict[key], dtype='float32')
        # shuffle the dataset, and split it
        # 70:20:10
        np.random.shuffle(final_array)

        test_array, val_array, train_array = final_array[:50], final_array[50:150], final_array[150:]
        print(train_array.shape, val_array.shape, test_array.shape)

        np.save(f'../data/movement_processed_data/{key}_table_test.npy', test_array)
        np.save(f'../data/movement_processed_data/{key}_table_val.npy', val_array)
        np.save(f'../data/movement_processed_data/{key}_table_train.npy', train_array)

def process_movement_data_pca():
    extension = ".csv"
    dict = {}
    from sklearn.decomposition import PCA

    for i in range(10):
        dict[str(i)] = []

    for file in os.listdir("../../data/movement_new"):
        if file.endswith(extension):
            df = pd.read_csv("../data/movement_new/" + file)

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
                    denoised.append(butter_lowpass_filter(subcarrier, 7.5398, 25))

                # 40 x 64 for PCA, reduce to 4 components
                denoised = np.asarray(denoised, dtype='float32')
                denoised = denoised.transpose()
                pca_newnparray = pca.fit_transform(denoised)

                # 4 x 40, take the first principal component
                pca_newnparray = pca_newnparray.transpose()[0]
                # 2nd round of denoising
                denoised = butter_lowpass_filter(pca_newnparray, 2.5132, 25)
                # print(pca_newnparray)
                # print(pca_newnparray.shape)
                # exit()
                # # second round of denoising
                # denoised = []
                # for subcarrier in pca_newnparray:
                #     denoised.append(butter_lowpass_filter(subcarrier, 2.5132, 25))
                dict[key].append([denoised])

    for key, value in dict.items():
        final_array = np.asarray(dict[key], dtype='float32')
        # shuffle the dataset, and split it
        # 70:20:10
        np.random.shuffle(final_array)
        test_array, val_array, train_array = final_array[:50], final_array[50:150], final_array[150:]
        print(train_array.shape, val_array.shape, test_array.shape)
        np.save(f'../data/windtalker_steps/{key}_table_test.npy', test_array)
        np.save(f'../data/windtalker_steps/{key}_table_val.npy', val_array)
        np.save(f'../data/windtalker_steps/{key}_table_train.npy', train_array)


def main():
    # process_training_data()
    # process_env_data()
    # process_movement_data()
    process_movement_data_pca()


if __name__=='__main__':
    main()
