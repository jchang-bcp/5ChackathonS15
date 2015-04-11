# Alex Ozdemir <aozdemir@hmc.edu>
# Configuration file

import math

NEAR_WIDTH = 11. # Arbitrary Units
FAR_WIDTH = 20. # Arbitrary Units
OFFSET_DISTANCE = 100. # Arbitrary units (Distance to bottom from stand)
FOV_Y = 30. # Who knows (degrees)
ALPHA =  30. # Pixel Units?
H = OFFSET_DISTANCE / math.tan(math.radians(ALPHA))

# Width and height of kinect image
KINECT_WIDTH = 640
KINECT_HEIGHT = 480

# Width and height of game
GAME_WIDTH  = 1600
GAME_HEIGHT =  int(1.8*1200)
