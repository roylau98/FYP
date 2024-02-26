from utils import process
import os
import pandas as pd
import numpy as np


def process_training_data():
    for i in range(10):
        output = []
        print(f"Processing file {i}")
        df = pd.read_csv(f"../data/raw_data/{i}_table.csv")

        temp = []
        for index, row in df.iterrows():
            curr_row = row['type']
            if 'End Collection' in curr_row:
                new_nparray = np.asarray(temp, dtype='float32')
                new_nparray = new_nparray.transpose()
                output.append(new_nparray.tolist())
                temp = []
            else:
                amp = process(row['CSI_DATA'])
                temp.append(amp)

        final_array = np.asarray(output, dtype='float32')
        print(final_array.shape)

        # shuffle the dataset, and split it
        np.random.shuffle(final_array)
        test_array, val_array, train_array = final_array[:30], final_array[30:90], final_array[90:]
        print(train_array.shape, val_array.shape, test_array.shape)

        np.save(f'../data/processed_data/{i}_table_test.npy', test_array)
        np.save(f'../data/processed_data/{i}_table_val.npy', val_array)
        np.save(f'../data/processed_data/{i}_table_train.npy', train_array)


def process_env_data():
    extension = ".csv"
    for file in os.listdir("../data/real_env"):
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
                    output.append(new_nparray.tolist())
                    temp = []
                else:
                    amp = process(row['CSI_DATA'])
                    temp.append(amp)

            final_array = np.asarray(output, dtype='float32')
            np.save(f'../data/real_env/{file.split(".")[0]}.npy', final_array)


def main():
    # process_training_data()
    process_env_data()


if __name__=='__main__':
    main()
