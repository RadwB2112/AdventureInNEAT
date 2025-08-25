from assets.background import *
import pygame
import neat
from core import game
from constants import screen
import pickle

pygame.init()
pygame.display.set_caption("ADVENTURE IN SPACE") # ADVENTURE IN NEAT
clock = pygame.time.Clock()

gen_stele_caz()
gen_stele_caz()
gen_list_stele()

state = "menu"
while True:
    next_state = None

    if state == "menu":
        next_state = game.main_menu(screen)
    elif state == "set_obstacles":
        next_state = game.set_obstacles(screen)
    elif state == "pause":
        next_state = game.pause(screen)
    elif state == "journey":
        next_state = game.journey(screen)
        if next_state is not None:
            game.journey_start = False
    elif state == "train":
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            'config_neat.txt'
        )
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(game.eval_generation2, 50)

        with open("best_genome.pkl", "wb") as f:
            pickle.dump(winner, f)  # we save the best model

        print("best genome:", winner)
        next_state = "set_obstacles"

        # we output the coordinates so that we know the params. we trained on
        from core.game import mouse_positions, platforms, bhs_size
        print(platforms[0].platform_corner_x, platforms[0].platform_corner_y)
        print(platforms[1].platform_corner_x, platforms[1].platform_corner_y)
        print(mouse_positions)  # for blackholes pos
        print(bhs_size)         # and their sizes

    elif state == "best_genome":
        next_state = game.best_genome(screen)
    elif state == "quit":
        pygame.quit()
        exit()

    if next_state is not None and next_state != state:
        state = next_state
        print(next_state)

    pygame.display.flip()
    clock.tick(FPS)

    """
            for gen in range(40):
                if gen < 20:
                    # we try this shit now, for better randomness and exploring: 
                    p.config.genome_config.mutation_rate = 0.5
                    p.config.genome_config.conn_add_prob = 0.4
                    p.config.genome_config.conn_delete_prob = 0.2
                    p.config.genome_config.node_add_prob = 0.2
                    p.config.genome_config.node_delete_prob = 0.1
                    p.config.genome_config.enabled_mutate_rate = 0.1
                    
                else:
                    # this were the basic values
                    # but using this, ships will form clusters and will not 'explore'
                    
                    p.config.genome_config.mutation_rate = 0.25
                    p.config.genome_config.conn_add_prob = 0.2
                    p.config.genome_config.conn_delete_prob = 0.1
                    p.config.genome_config.node_add_prob = 0.1
                    p.config.genome_config.node_delete_prob = 0.02
                    p.config.genome_config.enabled_mutate_rate = 0.01
                    
                    # before this like a week ago : node_add_prob 0.05
    """

# ~1250 lines of code, counting only the things I really used
