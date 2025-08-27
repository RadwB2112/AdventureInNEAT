import math
import pickle

import pygame.mouse

from objects import *
from assets.background import *

from core.utils import *
from .shared_stuff import make_watchers
from . import game, utils

import objects
from assets import assets
import constants
from assets.background import platforms, bhs


start_ticks = 0
journey_start = False
should_recreate_ship = False
first_time_here = True
debugging = True  # IF YOU WANT TO SEE THE AREAS OF BLACKHOLES AND THE SHIP RECTANGLE -> True, if not False

watch_and_reload = make_watchers(game, objects, assets, constants, always_reload=(game,))


def pause(screen):
    global should_recreate_ship
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bt_start_rect.collidepoint(event.pos):
                return "journey"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "journey"
            if event.key == pygame.K_r:
                watch_and_reload()

    zeus(screen)

    screen.blit(pause_button, (540, 190))

    filter_pause = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    filter_pause.fill((0, 0, 0, 128))
    screen.blit(filter_pause, (0, 0))

    return None


x_ship_start = BORDER + PLATFORM_WIDTH / 2 - NORMAL_SHIP_X / 2
y_ship_start = platforms[0].platform_corner_y - NORMAL_SHIP_Y  # - 20 # remove the -20 when you solve the bug
ship = nava(x_ship_start, y_ship_start, 3.5, 0, 'r')


def journey(screen):
    global journey_start, start_ticks, ship, should_recreate_ship, platforms, x_ship_start, y_ship_start, \
        first_time_here, mouse_positions

    if not journey_start:
        start_ticks = pygame.time.get_ticks()
        journey_start = True

    if ship is None or should_recreate_ship or ship.dead:  # cause at reload i want to start from 0
        ship = nava(x_ship_start, y_ship_start, 3.5, 0, 'r')
        should_recreate_ship = False

    filter = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    filter.fill((0, 0, 0, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_4:
                should_recreate_ship = False
                return "pause"
            elif event.key == pygame.K_5:
                return "menu"
            if event.key == pygame.K_r:
                should_recreate_ship = True
                # watch_and_reload()

    # ------------- for black holes + background -------------- START
    zeus(screen, "not")

    for bh, (x, y) in zip(bhs, mouse_positions):  # keeping the obstacles (already set) on screen
        bh.rect_draw(screen, x, y)
        if debugging:
            pygame.draw.circle(screen, RED, bh.bh_rect.center, int(bh.radius), 1)

    afis_stele_caz(screen)  # i want the falling stars to go over the bhs

    # --------------------- for countdown --------------------- END / START
    if first_time_here:
        countdown(screen, start_ticks)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > 3:
            first_time_here = False
        else:
            screen.blit(filter, (0, 0))
    else:
        ship.left_right(screen, platforms, bhs)
        # print("ship pos after move:", ship.x, ship.y)

        for plat in platforms:       # draw the platforms
            plat.draw_platform(screen)
            if debugging:
                plat.draw_rect(screen)   # for the debugging  <-> delete them
        if debugging:
            ship.draw_rect_ship(screen)  # for the debugging

    return None


pygame.font.init()
black_hole_instructions_text = "Deploy the 3 Black Holes and then press SPACE"
black_hole_instructions_text2 = "press 'r' to reset the positions"
font = pygame.font.Font("images/orbitron-mediem.otf", 40)
font2 = pygame.font.Font("images/orbitron-mediem.otf", 28)
text_surface = font.render(black_hole_instructions_text, True, TEXT_COLOR)
text_surface2 = font2.render(black_hole_instructions_text2, True, TEXT_COLOR)

counter = 0  # number of black holes already placed


# function to choose the positions of the blackholes
def set_obstacles(screen):
    global counter, mouse_positions  # , black_hole  # ca sa se roteasca <- adauga ca global

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN and counter < 3:  # at most 3 black holes
            if BLACK_BARS_HEIGHT < pygame.mouse.get_pos()[0] < SCREEN_WIDTH - BLACK_BARS_HEIGHT:
                mouse_positions.append(pygame.mouse.get_pos())
                counter += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and counter == 3:
                return "journey"
            elif event.key == pygame.K_t:
                return "train"
            elif event.key == pygame.K_b:
                return "best_genome"
            elif event.key == pygame.K_r:
                if mouse_positions:
                    mouse_positions.pop()
                    counter -= 1

    zeus(screen)

    for bh, (x, y) in zip(bhs, mouse_positions):
        bh.rect_draw(screen, x, y)

    afis_stele_caz(screen)  # i want the falling stars to go over the bhs

    # INSTRUCTIONS FOR THE BH'S INSTRUCTIONS
    xtext = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
    ytext = BORDER + BORDER  # SCREEN_HEIGHT // 2 - text_surface.get_height() // 2
    draw_text(screen, black_hole_instructions_text, font, xtext, ytext, (112, 31, 212, 0.741), WHITE)

    xtext2 = SCREEN_WIDTH // 2 - text_surface2.get_width() // 2
    ytext2 = BORDER + ytext + 1.5 * BORDER
    draw_text(screen, black_hole_instructions_text2, font2, xtext2, ytext2, (112, 31, 212, 0.741), WHITE)

    # black lines to mark the place where you cant put the bh's
    filter = pygame.Surface((BLACK_BARS_HEIGHT, SCREEN_HEIGHT - (ytext + font.get_height() + ytext)), pygame.SRCALPHA)
    filter.fill((0, 0, 0, 64))
    screen.blit(filter, (SCREEN_WIDTH - BLACK_BARS_HEIGHT, ytext + font.get_height() + ytext))
    screen.blit(filter, (0, ytext + font.get_height() + ytext))

    return None


# function to run the best genome after the training finished
def best_genome(screen):
    global bhs, mouse_positions

    with open("best_genome.pkl", "rb") as f:
        winner = pickle.load(f)

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        'config_neat.txt'
    )

    net = neat.nn.FeedForwardNetwork.create(winner, config)

    ship = nava(x_ship_start, y_ship_start, 3.5, 0, 'r')  # + idx * 3 - 15

    run = True
    clock_sim = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_5:
                    return "menu"
        # draw the background ---------------------------------------------------
        screen.fill(BLACK)
        zeus(screen)
        for plat in platforms:
            plat.draw_platform(screen)
        for bh, (x, y) in zip(bhs, mouse_positions):
            if debugging:
                pygame.draw.circle(screen, RED, bh.bh_rect.center, int(bh.radius), 1)
            bh.rect_draw(screen, x, y)
        afis_stele_caz(screen)
        # -----------------------------------------------------------------------

        landing_x = platforms[1].platform_rect.centerx
        landing_y = platforms[1].platform_rect.centery
        state = ship.get_state(landing_x, landing_y, bhs)

        outputs = net.activate(state)

        ship.update_ai(outputs[0], outputs[1], outputs[2], screen, platforms, bhs)

        if ship.land_end or ship.crashed(bhs) \
                or ship.x < 0 or ship.x > SCREEN_WIDTH or ship.y < 0 or ship.y > SCREEN_HEIGHT:
            run = False

        pygame.display.flip()
        clock_sim.tick(30)

    return "set_obstacles"


def main_menu(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                return "set_obstacles"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "set_obstacles"
            if event.key == pygame.K_r:
                watch_and_reload()

    zeus(screen, "lol")

    screen.blit(title, (MAIN_LOGO_CORNER_X, MAIN_LOGO_CORNER_Y))
    screen.blit(play, (PLAY_BUTTON_CORNER_X, PLAY_BUTTON_CORNER_Y))

    afis_stele_caz(screen)

    return None


# NEAT functions :
import sys
import neat
from constants import screen


# this function rewards for surviving, getting closer to target, setting vertically for landing, landing
# angle of the ship near platform, and even decreased for going inside a blackhole, out of screen, away from target
def eval_generation2(genomes, config):
    ships = []
    nets = []
    genomes_fitness = []
    ships_positions = []
    for idx, (genome_id, genome) in enumerate(genomes):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        pos = BORDER + idx * 5 - SHIP_FIRE_X / 2
        ship = nava(pos, y_ship_start, 3.5, 0, 'r')  # x_ship_start + idx * 3 - 25

        # we start with ships from the platform left max, and we add 5px distance between ships, 20 * 5 = PLATFORM_WIDTH
        genome.fitness = 0
        ships.append(ship)
        nets.append(net)
        genomes_fitness.append(genome)
        ships_positions.append(pos + SHIP_FIRE_X / 2)

    alive = True
    steps = 0
    max_steps = 3600  # divide by fps to get seconds
    clock_sim = pygame.time.Clock()
    n = len(ships)

    # ---- we calculate all the distances from all ships to landing platform ----
    landing_x = platforms[1].platform_rect.centerx
    landing_y = platforms[1].platform_rect.centery
    last_dist = [0.0] * n

    for i, ship in enumerate(ships):
        last_dist[i] = math.hypot(ship.x - landing_x, ship.y - landing_y)
    # --------------------------------------------------------------------------

    DIST_REWARD_SCALE = 0.2   # 0.08
    ANGLE_REWARD_SCALE = 0.1  # 0.04
    # DIST_PENALTY = False  # set to False to give small negative reward when moving away from target

    # so we dont have huge rewards we cap it each frame
    MAX_DIST_REWARD_FRAME = 4.0    # 1.0
    MAX_ANGLE_REWARD_FRAME = 2.0   # 1.0

    while alive and steps < max_steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4:
                    return "pause"

        # ------------------------- we are drawing the background ----------------
        screen.fill(BLACK)
        zeus(screen, "olo")
        for plat in platforms:
            plat.draw_platform(screen)
            # plat.draw_rect(screen)  # for the debugging  <-> delete them

        for bh, (x, y) in zip(bhs, mouse_positions):
            if debugging:
                pygame.draw.circle(screen, RED, bh.bh_rect.center, int(bh.radius), 1)
            bh.rect_draw(screen, x, y)
        # ------------------------------------------------------------------------
        alive = False

        for i, ship in enumerate(ships):
            genome = genomes_fitness[i]
            net = nets[i]

            if ship.dead:  # if the ship died we add a little penalty and skip it
                genome.fitness -= DEAD_SHIP
                continue

            alive = True
            # ship.draw_rect_ship(screen) # debugging

            state = ship.get_state(landing_x, landing_y, bhs)
            outputs = net.activate(state)
            ship.update_ai(outputs[0], outputs[1], outputs[2], screen, platforms, bhs)

            if steps >= 210 and abs(ship.x - ships_positions[i]) < 2:  # if they just go up, i kill them
                # print(f"ship.x_corner: {ship.x}, ships_pos[i]: {ships_positions[i]}")
                ship.dead = True
                genome.fitness -= ONLY_UP_SHIP

            # reward for surviving
            # 60 fps with 1 minute max -> 60 * 60 = 3600 seconds * SURVIVE_SHIP = N points
            genome.fitness += SURVIVE_SHIP

            # -------------------- REWARDING IF WE GET CLOSER TO THE TARGET -------------------
            current_dist = math.hypot(ship.x - landing_x, ship.y - landing_y)
            delta = last_dist[i] - current_dist
            last_dist[i] = current_dist

            if delta > 0:  # reward for getting closer, and penalty for getting further away
                dist_reward = min(MAX_DIST_REWARD_FRAME, DIST_REWARD_SCALE * delta)
            else:
                dist_reward = max(-MAX_DIST_REWARD_FRAME, DIST_REWARD_SCALE * delta * 0.5)

            genome.fitness += dist_reward * 3

            # reward for being over the platform (for landing), we try forcing the ship to land more in center by -/+20
            if platforms[1].platform_rect.left + 10 <= ship.x <= platforms[1].platform_rect.right - 10:
                if ship.y < platforms[1].platform_rect.top:             # and only over
                    genome.fitness += OVER_PLATFORM_SHIP

                    #  +++ reward for low vertical speed when over the platform
                    if abs(ship.y - platforms[1].platform_rect.top) < 50:                      # if i am very close
                        if abs(ship.vel_y) < 1.0:                                              # and i have small speed
                            genome.fitness += LOW_VERT_SPEED_SHIP
            # ---------------------------------------------------------------------------------

            # ------------------- REWARDING IF WE THE ANGLE AT LANDING IS 0.0 -----------------
            if current_dist < 300:  # we reward 0.0 angle only near the landing platform
                angle = ship.angle % 360  # we normalize to -180 180 because we need the shortest angular difference
                if angle > 180:           # 355 degrees == -5 degrees, and we cant pass 355 as error
                    angle -= 360

                target_angle = 0.0
                angle_err = abs(angle - target_angle)
                angle_reward = (1.0 - angle_err / 180.0) * ANGLE_REWARD_SCALE  # we map error to [0,1] & reward prop.
                angle_reward = max(0.0, min(MAX_ANGLE_REWARD_FRAME, angle_reward))
                genome.fitness += angle_reward * 10
            # ---------------------------------------------------------------------------------

            # if we enter blackholes radius we apply a small penalty
            for bh in bhs:
                dist = distance(ship.x, bh.x, ship.y, bh.y)
                if dist < bh.radius:  # if i am in the black hole
                    genome.fitness -= INSIDE_BHS_SHIP

            # if the ship don't move from the start platform we kill it
            if abs(ship.vel_x) < 0.02 and abs(ship.vel_y) < 0.02:
                ship.dead = True
                genome.fitness -= DONT_MOVE_SHIP  # 100

            # if we safely land + 1000
            if ship.land_end:
                ship.dead = True
                genome.fitness += LAND_SHIP

                ship.draw_rect_ship(screen)
                pygame.display.flip()
                pygame.time.delay(1500)
            # if we die in a blackhole -200
            elif ship.crashed(bhs):
                ship.dead = True
                genome.fitness -= BLACKHOLE_DIE_SHIP
            # if we get out of the screen -300
            elif ship.x < 0 or ship.x > SCREEN_WIDTH or ship.y < 0 or ship.y > SCREEN_HEIGHT:
                ship.dead = True
                genome.fitness -= OUT_OF_SCREEN_SHIP

            """
            if debugging:  # this shows the axes to black holes for each ship
                for bh in bhs:
                    dx = bh.bh_rect.centerx - ship.x
                    dy = bh.bh_rect.centery - ship.y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        vx = dx / dist * 10  # scale for visualization
                        vy = dy / dist * 10
                        pygame.draw.line(screen, RED, (ship.x, ship.y), (ship.x + vx * 4, ship.y + vy * 4), 1)
            """

        pygame.display.flip()
        clock_sim.tick(FPS)
        steps += 1


"""
    any stars?? please dont just copy this code ))))
"""
