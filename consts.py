# CONSTANTS

# KARD DATA LOADER CONSTANTS
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