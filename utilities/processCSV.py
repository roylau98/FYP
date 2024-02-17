from utils import process
import pandas as pd
import numpy as np


def main():
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


if __name__=='__main__':
    main()
