import torch
import torch.nn as nn
import consts as c
from torch.utils.data import Dataset, DataLoader

class ImageRNN(nn.Module):
    def __init__(self, batch_size, n_steps, n_inputs, n_neurons, n_outputs):
        super(ImageRNN, self).__init__()
        
        self.n_neurons = n_neurons
        self.batch_size = batch_size
        self.n_steps = n_steps
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.hidden = self.init_hidden()
        
        self.basic_rnn = nn.RNN(self.n_inputs, self.n_neurons) 
        
        self.FC = nn.Linear(self.n_neurons, self.n_outputs)
        
    def init_hidden(self):
        # (num_layers, batch_size, n_neurons)
        return (torch.zeros(1, self.batch_size, self.n_neurons))
        
    def forward(self, X):
        # transforms X to dimensions: n_steps X batch_size X n_inputs
        X = X.permute(2, 0, 1) 

        # Don't re-initialize hidden within the model!
        # It won't work when transferred to GPU!
        #self.batch_size = X.size(2)
        #self.hidden = self.init_hidden()

        _, self.hidden = self.basic_rnn(X, self.hidden)
        out = self.FC(self.hidden)
        
        return out.view(-1, self.n_outputs) # batch_size X n_output

if __name__ == '__main__':
    from kard import FormatDataset, KardDataset
    fd = FormatDataset(c.ROOT, 42)
    sets = fd.randomSplit(fd.file_IDs, c.SPLIT, 42)
    # Get the datasets based on c.SPLIT
    trainSet = sets[0]

    trainingDataset = KardDataset(trainSet, fd.paths)
    dataLoader = DataLoader(trainingDataset, 
                            batch_size=c.BATCH_SIZE,
                            shuffle=False,
                            drop_last=True)
    dataIter = iter(dataLoader)
    labels, skeletons = dataIter.next()
    model = ImageRNN(c.BATCH_SIZE, c.N_STEPS, c.N_INPUTS, c.N_NEURONS, c.N_OUTPUTS)
    # Permute the input tensor with *.view. Why? I have no idea!
    # Original skeleton input (batch_size x #points x point_coords) = 5 x 15 x 3
    # For this to work - 3 x 5 x15
    # Use permutation from torch instead of 'logits = model(skeletons.view(3, 5, 15))'
    logits = model(skeletons.permute(2, 0, 1))
    
    # Seems like it works - outputs batch_size (5) vectors (within a tensor) of length
    # c.N_OUTPUTS (18 -> number of categories). So, output: batch_size x #outputs
    print(logits[0:18])