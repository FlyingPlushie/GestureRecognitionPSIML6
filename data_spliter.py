# TODO
# Get the dataset
# Split the dataset
# Get random training example

from kard_data_loader import KardDataLoader
import consts as c
import numpy as np

kdl = KardDataLoader(c.PATH)
# Load the data
kdl.getActivityData(c.FILETYPES['screen'])

shuffleFlag = True
# Shuffle data
for activity in kdl.data:
    if shuffleFlag == True:
        np.random.shuffle(activity)
    print(len(activity))

# Split within activity
train = 0.6
val = 0.2
test = 0.2
