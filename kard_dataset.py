from pathlib import Path
import os
import numpy as np
import consts as c
from torch.utils.data import Dataset

class KardDataset(Dataset):
    def __init__(self, path):
        self.path = Path(path)
        self.data = []
    
    def __len__(self):
        return(len(self.data))

    def __getitem__(self, idx):
        return self.data[idx]
    
    def generateNameDigits(self, input_range):
        """Generate strings from 01 to input_range, including input_range.
        Returns an iterator in case of a long list."""
        return ['0' + str(i + 1) if i < 9 else str(i + 1) for i in range(input_range)]

    def getActivityDataTree(self, filetype):
        """Reads the complete data tree:
        activities(18 total)
        |_subjects(10 per activity)
        |_episodes(3 per subject)"""
        files = os.listdir(self.path)
        #filenames = []
        activities = self.generateNameDigits(c.ACTIVITIES)
        subjects = self.generateNameDigits(c.SUBJECTS)
        episodes = self.generateNameDigits(c.EPISODES)

        episode_data = []
        subject_data = []
 
        for activity in activities:
            for subject in subjects:
                for episode in episodes:
                    filename = 'a' + activity + '_' + \
                            's' + subject + '_' + \
                            'e' + episode + '_' + \
                                filetype
                    if filename in files:
                        file_path = Path(self.path / filename)
                        #filenames.append(filename)
                        #data_frame = pd.read_csv(file_path, header=None)
                        data = np.loadtxt(file_path)
                        self.data.append((c.ACTIVITY_LABELS[int(activity)-1], subject, episode, data))

if __name__ == '__main__':
    
    # Dataset instantiation and usage with pytorch's DataLoader
    dataset = KardDataset(c.PATH)
    dataset.getActivityDataTree(c.FILETYPES['screen'])
    
    #print(len(dataset))
    #print(dataset[0])
    #print(dataset[1:3])

    from torch.utils.data import DataLoader
    dataloader = DataLoader(dataset,
                            batch_size=1,
                            shuffle=True,
                            num_workers=1)
    for i, batch in enumerate(dataloader):
        print(i, batch)
