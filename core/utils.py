
import numpy as np
import math
import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BORDER, RED


def rotate_img(image, angle, pos):
    rotated_img = pygame.transform.rotate(image, angle)
    old_rect = image.get_rect(center=pos)
    new_rect = rotated_img.get_rect(center=old_rect.center)
    return rotated_img, new_rect


def countdown(screen, start_ticks):
    seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)
    if seconds < 4:
        text = str(3 - seconds)
        timer_font = pygame.font.Font(None, 300)
        text_width, text_height = timer_font.size(text)
        countdown_1 = timer_font.render(text, True, (255, 255, 255))
        screen.blit(countdown_1, (SCREEN_WIDTH / 2 - text_width / 2, SCREEN_HEIGHT / 2 - text_height / 2 - BORDER)) # 402x250


def get_distance(rect1, rect2):
    x1, y1 = rect1.center
    x2, y2 = rect2.center

    return ((x2-x1)**2 + (y2-y1)**2) ** 0.5


def draw_rect(x1, y1, width, height, screen):
    pygame.draw.rect(screen, RED, (x1, y1, width, height), 2)


# this function only handle collisions with rectangles (like a platform)
def handle_collision_with_platform(rect, vel_x, vel_y, platforms, prev_land_start, prev_land_end):
    next_rect = rect.move(vel_x, vel_y)
    landed_start = prev_land_start
    landed_end = prev_land_end
    bounce = -0.2

    for (i, plat) in enumerate(platforms):
        p_rect = plat.platform_rect

        if next_rect.colliderect(p_rect):
            dx = abs(next_rect.centerx - p_rect.centerx)
            dy = abs(next_rect.centery - p_rect.centery)

            overlap_x = (rect.width + p_rect.width) / 2 - dx
            overlap_y = (rect.height + p_rect.height) / 2 - dy

            if overlap_x < overlap_y:
                # Horizontal collision
                if next_rect.centerx > p_rect.centerx:
                    next_rect.left = p_rect.right
                else:
                    next_rect.right = p_rect.left
                vel_x *= bounce
            else:
                # Vertical collision
                if next_rect.centery > p_rect.centery:
                    next_rect.top = p_rect.bottom
                    vel_y *= bounce
                else:
                    next_rect.bottom = p_rect.top
                    vel_y = 0
                    if i == 0:
                        landed_start = True
                    elif i == 1:  # only land on the second platform
                        landed_end = True

    return next_rect, vel_x, vel_y, landed_start, landed_end


def draw_text(surface, text, font, x, y, glow_color, text_color):
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            if dx != 0 or dy != 0:
                glow = font.render(text, True, glow_color)
                surface.blit(glow, (x + 1 * dx, y + 1 * dy))

    main_text = font.render(text, True, text_color)
    surface.blit(main_text, (x, y))


def distance(a, b, c, d):
    return ((a - b) ** 2 + (c - d) ** 2) ** 0.5


