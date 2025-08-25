from core.shared_stuff import transform
import pygame, math

# --------------------------------- BASE CONSTANTS  ---------------------------------
FPS = 60  # idk 30 i guess
SCREEN_WIDTH = 1400  # 910
SCREEN_HEIGHT = 700
BORDER = 20

# SCREEN
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


# SOME COLORS
BLUE = (25, 11, 133)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GLOW_COLOR = (180, 130, 255)
TEXT_COLOR = (255, 255, 255)

# ----------------------------------- MAIN (first window) ----------------------------
# ADVENTURE IN SPACE LOGO coord.
MAIN_LOGO_WIDTH = 600
MAIN_LOGO_HEIGHT = 400

MAIN_LOGO_CORNER_X = SCREEN_WIDTH / 2 - MAIN_LOGO_WIDTH / 2
MAIN_LOGO_CORNER_Y = BORDER


# PLAY BUTTON
PLAY_BUTTON_WIDTH = 280
PLAT_BUTTON_HEIGHT = 120

PLAY_BUTTON_CORNER_X = (SCREEN_WIDTH - PLAY_BUTTON_WIDTH) / 2
PLAY_BUTTON_CORNER_Y = MAIN_LOGO_HEIGHT + MAIN_LOGO_CORNER_Y + 70

# ----------------------------------- MENU / PAUSE (second window) ----------------------------

# ----------------------------------- GAME / ACTION (third window) ----------------------------


# ------------------------------ SHIP CONSTANTS ------------------------------------

# ship with fire
SHIP_FIRE_X = 60
SHIP_FIRE_Y = transform(SHIP_FIRE_X, 'nava_fc.png')

# normal ship
NORMAL_SHIP_X = 58
NORMAL_SHIP_Y = transform(NORMAL_SHIP_X, 'nava_fr.png')


# --------------------- PLATFORMS --------------------
PLATFORM_WIDTH = 100  # half at 50 -> 30 fire / 29 normal ship
PLATFORM_HEIGHT = 20

MIN_PLATFORM_X = BORDER
MAX_PLATFORM_X = SCREEN_WIDTH - PLATFORM_WIDTH - BORDER

MIN_PLATFORM_Y = BORDER + math.ceil(SHIP_FIRE_Y)
MAX_PLATFORM_Y = SCREEN_HEIGHT - BORDER - PLATFORM_HEIGHT

FIRST_COLUMN_X = BORDER + PLATFORM_WIDTH
LAST_COLUMN_X = SCREEN_WIDTH - BORDER - PLATFORM_WIDTH


# ------------------------------- STARS --------------------------------------------
STARS_NUM = 80  # number of normal stars
SPAWN_TIME_FALL = 2500  # 2.5 seconds before each falling star
ADD_REMOVE_TIME = 2750

# ---------------------------- BLACK BARS  -----------------------------------------

BLACK_BARS_HEIGHT = BORDER + PLATFORM_WIDTH + BORDER
BLACK_BARS_WIDTH = 0  # nothing here, i just wrote in inside the code




# GENOME FITNESS VALUES
DEAD_SHIP = 10              # 100
ONLY_UP_SHIP = 20           # 150
SURVIVE_SHIP = 0.1          # 0.15
OVER_PLATFORM_SHIP = 5      # 7.5
LOW_VERT_SPEED_SHIP = 20    # 25
DONT_MOVE_SHIP = 15         # 150
LAND_SHIP = 500             # 5000
BLACKHOLE_DIE_SHIP = 20     # 200
OUT_OF_SCREEN_SHIP = 30     # 300
INSIDE_BHS_SHIP = 0.2
