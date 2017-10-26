import pygame
from pygame.font import SysFont

pygame.font.init()

# Common

win_size = (950, 950)

ZERO = (0, 0)

TIMERATE = 0.001
PROPORTION = TIMERATE * 80

G = 80

# Colors

BLACK = (0, 0, 0)
DEFAULT_TEXT_COLOR = (100, 100, 200)

# Fonts

DEFAULT_TEXT_SIZE = 15
DEFAULT_FONT = SysFont("monospace", DEFAULT_TEXT_SIZE)
