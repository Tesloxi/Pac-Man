from pygame.image import load
from pygame.font import init, SysFont

# Setup display

NB_SPRITES_WIDTH = 28
NB_SPRITES_HEIGHT = 31
SPRITE_SIZE = 20
WIDTH = NB_SPRITES_WIDTH * SPRITE_SIZE
HEIGHT = NB_SPRITES_HEIGHT * SPRITE_SIZE

# Colors

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Fonts

init()
MENU_FONT = SysFont("comicsans", 60)
READY_FONT = SysFont("comicsans", 80)
SCORE_FONT = SysFont("comicsans", 30)

# Images

# Character images

UP_IMAGE = load("./pacman/assets/character/up.png")
RIGHT_IMAGE = load("./pacman/assets/character/right.png")
DOWN_IMAGE = load("./pacman/assets/character/down.png")
LEFT_IMAGE = load("./pacman/assets/character/left.png")

# Phantom images

PHANTOM_IMAGES = [
    load("./pacman/assets/phantom/blue.png"),
    load("./pacman/assets/phantom/green.png"),
    load("./pacman/assets/phantom/orange.png"),
    load("./pacman/assets/phantom/red.png")
]

# Heart image
HEART_IMAGE = load("./pacman/assets/character/heart.png")

# Game settings

SPEED = 2
MAX_NUMBER_OF_LIVES = 3
MAX_SCORE = 0