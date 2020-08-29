# CONSTANTS

# KARD DATA LOADER CONSTANTS
# Different file types per repetition
ROOT = 'D:/datasets/KARD'
SPLIT = [0.6, 0.2, 0.2]
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
# Total number of joints per frame
JOINTS = 15
# Number of coordinates within a single row in a skeleton file - u, v, d (screen)
COORDS = 3

# NETWORK CONSTS
# Learning rate
LEARNING_RATE = 0.00005
# Batch size - number of skeletons
BATCH_SIZE = 30
# Number of recurrent cells
N_STEPS = 64 # original: 28
# Number of inputs - in our case - number of input points (15 per skeleton)
N_INPUTS = 15
# Number of neurons, duh!
N_NEURONS = 32
# Number of outputs - we have 18 gestures - 18 categories on output
N_OUTPUTS = 18
# Number of full passes through the data
N_EPOCHS = 100