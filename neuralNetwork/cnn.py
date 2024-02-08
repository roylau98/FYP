import random
import os
import torch

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from tqdm import trange

# Define the 1D CNN model
class CNN1D(nn.Module):
    def __init__(self, number_of_categories):
        super(CNN1D, self).__init__()
        # convolution layer
        self.conv1d = nn.Conv1d(in_channels=64, out_channels=50, kernel_size=3, stride=1)
        self.maxpool = nn.MaxPool1d(kernel_size=2)
        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(64 * 24, 128)
        self.fc2 = nn.Linear(128, number_of_categories)

    def forward(self, x):
        # input tensor size [batch_size, 64, 50]
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(-1, 64 * 24)  # Adjust the input size based on the output size after convolutions and pooling
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        # log softmax
        x = F.log_softmax(x, dim=1)
        return x

def dataLoader():
    pass

def data_iterator(arrays, labels, total_size, batch_size, shuffle=False):
    order = list(range(total_size))
    if shuffle:
        random.seed(200)
        random.shuffle(order)

    for i in range((total_size+1)//batch_size):
        batch_arrays = np.array(arrays[idx] for idx in order[i*batch_size:(i+1)*batch_size])
        batch_labels = np.array(labels[idx] for idx in order[i*batch_size:(i+1)*batch_size])

        yield batch_arrays, batch_labels

class RunningAverage:
    def __init__(self):
        self.steps = 0
        self.total = 0

    def update(self, val):
        self.total += val
        self.steps += 1

    def __call__(self):
        return self.total / float(self.steps)

def accuracy(outputs, labels):
    outputs = np.argmax(outputs.cpu().detach().numpy(), axis=1)
    labels = labels.squeeze()
    # compare outputs with labels
    return np.sum([1 if first == second else 0 for first, second in zip(labels, outputs)]) / float(len(labels))

def train(model, optimizer, loss_fn, data_iterator, num_steps):
    model.train()
    train_loss_avg = RunningAverage()
    t = trange(num_steps)
    for i in range(num_steps):
        train_batch, labels_batch = next(data_iterator)
        output_batch = model(train_batch)
        loss = loss_fn(output_batch, labels_batch)

        optimizer.zero_grad()
        loss.backward()

        optimizer.step()
        train_loss_avg.update(loss.item())
        t.set_postfix(loss='{:05.3f}'.format(train_loss_avg()))

def evaluate(model, loss_fn, data_iterator, num_steps):
    model.eval()
    validation_loss_avg = RunningAverage()
    validation_accuracy_avg = RunningAverage()

    for i in range(num_steps):
        eval_batch, labels_batch = next(data_iterator)
        output_batch = model(eval_batch)
        loss = loss_fn(output_batch, labels_batch)

        validation_loss_avg.update(loss.item())
        validation_accuracy_avg.update(accuracy(output_batch, labels_batch))

    print(f"{validation_loss_avg()=}")
    print(f"{validation_accuracy_avg()=}")

def loss_fn(outputs, labels):
    loss = F.cross_entropy(outputs, labels)
    return loss

def train_and_eval(model, train_array, train_labels, val_array, val_labels, num_epochs, batch_size, optimizer, loss_fn):
    for epoch in range(num_epochs):
        # Run one epoch
        print("Epoch {}/{}".format(epoch + 1, num_epochs))

        # compute number of batches in one epoch (one full pass over the training set)
        num_steps = (len(train_array) + 1) // batch_size
        train_data_iterator = data_iterator(train_array, train_labels, len(train_array), batch_size, shuffle=True)
        train(model, optimizer, loss_fn, train_data_iterator, num_steps)

        # Evaluate for one epoch on validation set
        num_steps = (len(val_array) + 1) // batch_size
        val_data_iterator = data_iterator(val_array, val_labels, len(val_array), batch_size, shuffle=False)
        evaluate(model, loss_fn, val_data_iterator, num_steps)

def main():
    number_of_categories = 10
    model = CNN1D(number_of_categories)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    if (os.path.isfile("model.pth")):
        model.load_state_dict(torch.load('model.pth'))
    else:
        train_and_eval(model, X_train, y_train, X_val, y_val, 100, 32, optimizer, loss_fn)

    # Simple check with test dataset
    model.eval()
    test_data_iterator = data_iterator(X_test, y_test, len(X_test), len(y_test), shuffle=False)
    test_batch, labels_batch = next(test_data_iterator)

    output_batch = model(test_batch)
    final_test_accuracy = accuracy(output_batch, labels_batch)
    print(f"{final_test_accuracy=}")


if __name__=='__main__':
    main()
