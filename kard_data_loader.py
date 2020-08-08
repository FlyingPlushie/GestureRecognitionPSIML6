# Description of the KARD data
# KARD contains 18 Activities.
# Each activity is performed 3 times by 10 different subjects.

# 1 Horizontal arm wave
# 2 High arm wave
# 3 Two hand wave
# 4 Catch Cap
# 5 High throw
# 6 Draw X
# 7 Draw Tick
# 8 Toss Paper
# 9 Forward Kick
# 10 Side Kick
# 11 Take Umbrella
# 12 Bend
# 13 Hand Clap
# 14 Walk
# 15 Phone Call
# 16 Drink
# 17 Sit down
# 18 Stand up

# In total, you have:
# 4 (files) x 18 (activities) x 3 (repetitions) x 10 (subjects), that is 2160 files.
# Each filename is in the form aA_sS_eN_string
# A is a two-digit actionID and S is a two-digit subjectID for the N-th repetition.

# The string parameter depends on the the type of provided information:

#     depthmaps.txt: depth map,
#     .mp4: 640x480 RGB video,
#     realworld.txt: joints position in real world coordinates,
#     screen.txt: joints position in screen coordinates and depth value.

# For example, the file a04_s03_e02_realworld.txt contains the skeleton joints position
# in real world coordinates for the second repetition of the action #4 performed by the subject #3.
# The files containing the skeleton coordinates (realworld.txt and screen.txt) list the 15 joints
# in consecutive blocks, one for each frame.

# line 1 Head
# line 2 Neck
# line 3 Right Shoulder
# line 4 Right Elbow
# line 5 Right Hand
# line 6 Left Shoulder
# line 7 Left Elbow
# line 8 Left Hand
# line 9 Torso
# line 10 Right Hip
# line 11 Right Knee
# line 12 Right Foot
# line 13 Left Hip
# line 14 Left Knee
# line 15 Left Foot

# Each file contains 15xF lines, where F is the number of frames for that sequence,
# and each line reports three numbers: real world coordinates (x, y, z) for realworld.txt,
# or screen coordinates and depth value (u, v, depth) for screen.txt.

from pathlib import Path
import os
import numpy as np

# DATA CONSTS
# Path to dataset on the system
DATASET_PATH = Path('D:/datasets/KARD/')
# Different file types per repetition
FILETYPES = {'video': 'mp4',
             'depthmap': 'depthmaps.txt',
             'realworld': 'realworld.txt',
             'screen': 'screen.txt'}
# Activity labels from the set
ACTIVITY_LABELS = ['hor_arm_wave',
                   'high_arm_wave',
                   'two_hand_wave',
                   'catch_cap',
                   'high_throw',
                   'draw_x',
                   'draw_tick',
                   'toss_paper',
                   'fwd_kick',
                   'side_kick',
                   'take_umbrella',
                   'bend',
                   'hand_clap',
                   'walk',
                   'phone_call',
                   'drink',
                   'sit_down',
                   'stand_up']
# Number of recorded activities
ACTIVITIES = len(ACTIVITY_LABELS) # 'a' in filename
# Total number of repetitions per subject
EPISODES = 3 # 'e' in filename
# Total number of subjects
SUBJECTS = 10 # 's' in filename

def generateNameDigits(input_range):
    """Generate strings from 01 to input_range, including input_range.
    Returns an iterator in case of a long list."""
    return ['0' + str(i + 1) if i < 9 else str(i + 1) for i in range(input_range)]



def getActivityDataTree(path, filetype):
    """Reads the complete data tree:
    activities(18 total)
    |_subjects(10 per activity)
      |_episodes(3 per subject)"""
    files = os.listdir(path)
    filenames = []
    activities = generateNameDigits(ACTIVITIES)
    subjects = generateNameDigits(SUBJECTS)
    episodes = generateNameDigits(EPISODES)

    episode_data = []
    subject_data = []
    activity_data = []
    
    for activity in activities:
        for subject in subjects:
            for episode in episodes:
                filename = 'a' + activity + '_' + \
                           's' + subject + '_' + \
                           'e' + episode + '_' + \
                            filetype
                if filename in files:
                    file_path = Path(DATASET_PATH / filename)
                    filenames.append(filename)
                    #data_frame = pd.read_csv(file_path, header=None)
                    data = np.loadtxt(file_path)
                    episode_data.append(data)
            subject_data.append(episode_data)
            episode_data = []
        activity_data.append(subject_data)
        subject_data = []
    
    return activity_data

def getADTTest():
    adt = getActivityDataTree(DATASET_PATH, FILETYPES['screen'])
    print(len(adt))
    print(len(adt[0]))
    print(len(adt[0][0]))
    print(adt[0][0][0])
    print(adt[0][0][0][0][2])

def getActivityData(path, filetype):
    """Reads the complete data tree, but drops the subjects for easier access:
    activities(18 total)
      |_episodes(30 per activity)"""
    files = os.listdir(path)
    filenames = []
    activities = generateNameDigits(ACTIVITIES)
    subjects = generateNameDigits(SUBJECTS)
    episodes = generateNameDigits(EPISODES)

    episode_data = []
    activity_data = []
    
    for activity in activities:
        for subject in subjects:
            for episode in episodes:
                filename = 'a' + activity + '_' + \
                           's' + subject + '_' + \
                           'e' + episode + '_' + \
                            filetype
                if filename in files:
                    file_path = Path(DATASET_PATH / filename)
                    #filenames.append(filename)
                    data = np.loadtxt(file_path)
                    episode_data.append(data)
        activity_data.append(episode_data)
        episode_data = []
    
    return activity_data

def getADTest():
    ad = getActivityData(DATASET_PATH, FILETYPES['screen'])
    print(len(ad)) # 18 activities
    print(len(ad[0])) # 30 episodes (no subjects)
    print(len(ad[0][0])) # 1290/15 frames with (u, v, depth)

#getADTest()