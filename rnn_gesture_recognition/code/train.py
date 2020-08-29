import torch
import torch.optim as optim
import torch.nn as nn
import time
import math
from torch.utils.data import Dataset, DataLoader
from kard import FormatDataset, KardDataset, OneHotEncoder
import consts as c
from model import ImageRNN


# Gather the files and split into train, val, test
fd = FormatDataset(c.ROOT, 42) # Don't use seed if you want full random!
sets = fd.randomSplit(fd.file_IDs, c.SPLIT, 42) # Don't forget to exclude 42 and let it randomize
# Get the datasets based on c.SPLIT
trainSet = sets[0]
valSet = sets[1]
testSet = sets[2]

# Prepare the dataloader
trainingDataset = KardDataset(trainSet, fd.paths)
trainLoader = DataLoader(trainingDataset, 
                         batch_size=c.BATCH_SIZE,
                         shuffle=False,
                         drop_last=True)

validationDataset = KardDataset(valSet, fd.paths)
validationLoader = DataLoader(validationDataset,
                              batch_size=c.BATCH_SIZE,
                              shuffle=False,
                              drop_last=True)

# CUDA for PyTorch
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
torch.backends.cudnn.benchmark = True

# Model instance

model = ImageRNN(c.BATCH_SIZE,
                 c.N_STEPS,
                 c.N_INPUTS,
                 c.N_NEURONS,
                 c.N_OUTPUTS)
model.to(device)

# CROSS-ENTROPY LOSS DOES NOT EXPECT A ONE-HOT ENCODED VECTOR AS THE TARGET!
# IT EXPECTS CLASS INDICES!
criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(model.parameters(), lr=0.05, momentum=0.2)
optimizer = optim.Adam(model.parameters(), c.LEARNING_RATE)

def getAccuracy(output, target, batch_size):
    """Get accuracy for training round"""
    _, topIndicesOutput = output.topk(1)
    topIndicesOutput = topIndicesOutput.T
    corrects = torch.eq(topIndicesOutput, target)
    corrects = corrects.sum(1)
    accuracy = 100.0 * corrects/batch_size
    return accuracy.item()

def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

start = time.time()

for epoch in range(c.N_EPOCHS): # loop over the dataset N_EPOCHS times
    train_running_loss = 0.0
    train_acc = 0.0
    model.train()

    # Training round
    for i, data in enumerate(trainLoader):
        # Zero the parameter gradients
        optimizer.zero_grad()

        # Get the inputs
        labels, inputs = data

        # Transfer to GPU
        labels, inputs = labels.to(device), inputs.to(device)

        # Reset hidden states
        model.hidden = model.init_hidden()
        model.hidden = model.hidden.to(device)

        # Forward, backward + optimize
        outputs = model(inputs)

        # Take care - you DO NOT NEED one-hot encoding!
        #labels = labels.reshape(c.BATCH_SIZE, c.ACTIVITIES)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_running_loss += loss.detach().item()
        train_acc += getAccuracy(outputs, labels, c.BATCH_SIZE)
    
    model.eval()

    print('Epoch: %d | Loss: %.4f | Train Accuracy: %.2f | Time: %s'
          % (epoch, train_running_loss / i, train_acc/i, timeSince(start)))
    
val_acc = 0.0
for i, data in enumerate(validationLoader, 0):
    labels, inputs = data
    inputs, labels = inputs.to(device), labels.to(device)
    outputs = model(inputs)
    labels = labels.reshape(c.BATCH_SIZE, c.ACTIVITIES)

    val_acc += getAccuracy(outputs.T, labels[0], c.BATCH_SIZE)
    
print('Test Accuracy: %.2f'%( val_acc/i))