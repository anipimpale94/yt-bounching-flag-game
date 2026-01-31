import time as t
from math import pi

# Game presets
start_time = t.time()
fps = 120
width, height = 800, 600

# Window position
x, y = 1360 - width, 40

# Colors
white        = (255, 255, 255)
whitest      = (204, 234, 234)
# grey       = (45 ,  45,  45)
grey         = ( 27,  27,  27)
black        = (  0,   0,   0)
blackcoral   = ( 39,  22,  16)
deepblue     = (  0,   4,  30)
red          = (225,  40,  40)
green        = ( 10, 200,  27)
yellowish    = (191, 202,  37)
orange       = (255,  72,   0)
velvet       = (232,  20,  20)
bluish_white = (179, 255, 251)
blue         = (17 , 200, 251)
tastyellow   = (255, 230,   0)
arrow_color  = (255, 255, 255)
golden       = (255, 166,  32) # note: overwritten in original by next line, but keeping for completeness if needed or removing
golden       = (245, 170,  10)
algeablue    = (7  , 197,  70)
magenta      = (255,  13, 130)
magenta2     = (214,   0, 100)
bg = deepblue

# 27 balls: (name, (r,g,b))
BALL_CONFIGS = [
    ("Golden", (245, 170, 10)), ("Red", (225, 40, 40)), ("Green", (10, 200, 27)), ("Blue", (17, 200, 251)),
    ("Orange", (255, 72, 0)), ("Yellow", (255, 230, 0)), ("Cyan", (0, 200, 200)), ("Magenta", (255, 13, 130)),
    ("Lime", (50, 255, 50)), ("Teal", (0, 128, 128)), ("Navy", (0, 0, 128)), ("Purple", (128, 0, 128)),
    ("Coral", (255, 127, 80)), ("Pink", (255, 192, 203)), ("Brown", (139, 69, 19)), ("Olive", (128, 128, 0)),
    ("Maroon", (128, 0, 0)), ("Turquoise", (64, 224, 208)), ("Violet", (238, 130, 238)), ("Crimson", (220, 20, 60)),
    ("Silver", (192, 192, 192)), ("Sky", (135, 206, 235)), ("Salmon", (250, 128, 114)), ("Plum", (221, 160, 221)),
    ("Mint", (152, 255, 152)), ("Cream", (255, 253, 208)), ("Lavender", (230, 230, 250)),
]

# g = -0.1
g = -9.81
RING_MARGIN = 50  # space between ring outer edge and screen edge
bigr = min(width, height)//2 - RING_MARGIN  # radius of ring
centx, centy = width//2, height//2  # center of circle
SPAWN_RADIUS = 25  # small circle around center where balls respawn
# frames = 0 # frames is a state variable, usually kept in main loop or game state
ring_angle = 0  # rotation of outer ring (degrees) # initial state
RING_SPIN_SPEED = 0.5  # degrees per frame (slower spin)
JERK_ANGLE_DEG = 6  # random direction change on ring bounce (degrees, ±this)
GAP_SEGMENT_DEG = 30  # angular width of the single escape hole (degrees)
