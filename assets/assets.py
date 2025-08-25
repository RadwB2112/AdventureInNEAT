import pygame
from PIL import Image, ImageFilter
from constants import *

# BACKGROUND
backgroundd = pygame.image.load('images/background.png')
backgroundd = pygame.transform.scale(backgroundd, (SCREEN_WIDTH, SCREEN_HEIGHT))

# title logo
title = pygame.image.load('images/game_title.png')
title = pygame.transform.scale(title, (MAIN_LOGO_WIDTH, MAIN_LOGO_HEIGHT))

# play button
play = pygame.image.load('images/play_button.png')
play = pygame.transform.scale(play, (PLAY_BUTTON_WIDTH, PLAT_BUTTON_HEIGHT))

# pause button
pause_button = pygame.image.load('images/pause_button.png')

# LOGO
logo = pygame.image.load('images/logo.jpg')
pygame.display.set_icon(logo)

# Landing platform
platform = pygame.image.load('images/platform.png')
platform = pygame.transform.scale(platform, (PLATFORM_WIDTH, PLATFORM_HEIGHT))


# Rects
play_button_rect = pygame.Rect(PLAY_BUTTON_CORNER_X, PLAY_BUTTON_CORNER_Y,\
                               PLAY_BUTTON_WIDTH, PLAT_BUTTON_HEIGHT)

"""
# logo - leave them like this, cause i will changed this shit sometimes
title_2 = pygame.image.load('images/nava_tit_1.png')
title_2 = pygame.transform.scale(title_2, (350, 350))

bt_start = pygame.image.load('images/start.png')
bt_start = pygame.transform.scale(bt_start, (300, 100))
bt_start_rect = pygame.Rect(300, 350, 300, 100)

high = pygame.image.load('images/high_score.png')
high = pygame.transform.scale(high, (400, 50))"""



# OBSTACLES
# I. black hole = bh
black_hole = pygame.image.load('images/black_hole_obs2.png')
black_hole = pygame.transform.scale(black_hole, (70, 70))


# Confirmation button for black holes
# confirmation_button = pygame.image.load('<image>')


"""
bh = pygame.image.load('images/black_hole_obs2.png')
bh = pygame.transform.scale(bh, (70, 70)).convert_alpha()
str_bh = bh.tostring(image, "RGBA")
pil_bh = Image.frombytes("RGBA", bh.get_size(), str_bh)
blurred_pil_bh = pil_bh.filter(ImageFilter.GaussianBlur(radius=5))
blurred_str_bh = blurred_pil_bh.tobytes()
blurred_bh = pygame.image.fromstring(blurred_str_bh, bh.get_size(), "RGBA")
"""
