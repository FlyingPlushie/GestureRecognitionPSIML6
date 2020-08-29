from torch.utils.data import IterableDataset
import consts as c
import os
import re
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import Dataset, IterableDataset, DataLoader
from itertools import cycle, islice, chain
import random
from torch.utils.data import random_split
from sklearn.model_selection import StratifiedShuffleSplit

class FormatDataset():
    def __init__(self, root_dir, seed=None):
        self.root_dir = root_dir
        self.file_IDs,\
        self.paths = self.getSkeletonFileList(self.root_dir)

    def getSkeletonFileList(self, root_dir):
        """Returns a list containing all skeleton files in screen coords."""
        skeleton_IDs = []
        file_paths = {}
        for root, _, files in os.walk(root_dir, topdown=False):
            for file in files:
                searchObj = re.search('_screen.txt$', file)
                if searchObj:
                    skeleton_ID = re.search('^a[0-9][0-9]_s[0-9][0-9]_e[0-9][0-9]', file)
                    skeleton_ID = skeleton_ID.group(0)
                    skeleton_IDs.append(skeleton_ID)
                    if skeleton_ID not in file_paths:
                        file_paths[skeleton_ID] = os.path.join(root, file)
        return skeleton_IDs, file_paths
    
    def randomSplit(self, file_list, split, seed=None):
        """Accepts the 'split' list with [train, validation, test] vals and splits the datasets accordingly"""
        assert sum(split) == 1.0
        dataset_len = len(self.file_IDs)
        split_vals = []
        for elem in split:
            temp = int(dataset_len * elem)
            split_vals.append(temp)
        gen = torch.Generator()
        if seed == None:
            gen.seed()
            sets = random_split(file_list, split_vals, generator=gen)
        else:
            sets = random_split(file_list, split_vals, generator=torch.Generator().manual_seed(seed))
        return sets

    def stratifiedSplit(self, file_list, split_ratio):
        """Does a stratified split (train, val, test = 60 : 20 : 20) to a provided list of indices"""
        #split = StratifiedShuffleSplit(n_splits=1, test_size=0.4, random_state=42)
        pass

class OneHotEncoder():
    def __init__(self, length):
        self.labels = []
        self.encoder = {}
        for i, elem in enumerate(range(1, c.ACTIVITIES + 1)):
            if i < 9:
                label = '0' + str(elem)
                self.labels.append(label)
                self.encoder[label] = torch.zeros(1, c.ACTIVITIES, dtype=torch.long)
                self.encoder[label][0, i] = 1
            else:
                label = str(elem)
                self.labels.append(label)
                self.encoder[label] = torch.zeros(1, c.ACTIVITIES, dtype=torch.long)
                self.encoder[label][0, i] = 1
    def encode(self, label):
        return self.encoder[label]


class KardDataset(IterableDataset):
    def __init__(self, file_list, paths):

        #Store the filename in object's memory
        self.file_list = file_list
        self.paths = paths
        self.current_label = None
        self.ohe = OneHotEncoder(c.ACTIVITIES)
    
    def getActionLabel(self, index):
        # Gets the action label from the filename string
        file = self.file_list[index]
        label = file[1:3] # Hard-coded based on the filename structure throughout the dataset
        # Cross-entropy does not support one-hot encoding
        # We'll just pass the indice then
        label = int(label) - 1
        self.current_label = label
    
    def mapper(self, input):
        #oneHotLabel = self.ohe.encode(self.current_label)
        return self.current_label, input # Just prepare for mapping, put label and tensor together
        #return oneHotLabel, input
    
    def __iter__(self):

        # BASIC SKELETON
        #Create an iterator
        #file_itr = open(self.paths[self.file])
        #for i, line in enumerate(file_iter):
        for i, file in enumerate(self.file_list):
            # REPURPOSED
            # Get the data from the text file -> (15 points x N frames) x U x V x D (list with U, V and D as columns)
            data = np.loadtxt(self.paths[file])
            self.getActionLabel(i)
            # Find the maxIndex to properly split the data into tensors
            maxIndex = np.argmax(data.shape)
            # Continuous n x 3 data is now n/15 tensors of size 15x3
            data = data.reshape(int(data.shape[maxIndex]/c.JOINTS), c.JOINTS, c.COORDS)
            # Treat as torch data type
            data = torch.as_tensor(data, dtype=torch.float32)
            # Map the tensors to their proper label
            mapped_itr = map(self.mapper, data)
            # You must use 'yield from' to return an iterator.
            # 'yield' only returns a map, without reading it!
            yield from mapped_itr

if __name__ == '__main__':
    fd = FormatDataset(c.ROOT, 42) # 42
    sets = fd.randomSplit(fd.file_IDs, c.SPLIT, 42) # 42 - relict - used for replicable results
    trainSet = sets[0]
    valSet = sets[1]
    testSet = sets[2]
    #for val in trainSet:
    #    print(val)
    #dataset = KardDataset(trainSet[0], fd.paths)
    dataset = KardDataset(trainSet, fd.paths)
    dataloader = DataLoader(dataset, 
                            batch_size=c.BATCH_SIZE,
                            shuffle=False,
                            drop_last=True)

    # for i, data in enumerate(dataloader):
    #     print(data)
    #     print(data[1].shape)
    #     print(i)
    #     break # Get this off if you want the entire file...

    #ohe = OneHotEncoder(c.ACTIVITIES)
    #print(ohe.encode('10'))
    