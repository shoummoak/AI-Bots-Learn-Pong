# library imports
import pygame as pg
# import visualize
import neat
import os
import sys

# custom class imports
from game_settings import *
from BarAndPuck import BarAndPuck

# award fitness for simply surviving this long
def award_fitness(genomes_local):
    for genome in genomes_local:
        genome.fitness += 0.02


def stop_running(baps):
    if len(baps) == 0:
        return True


def draw_objects(baps, score, top_fitness):

    for bap in baps:
        pg.draw.ellipse(screen, bap.color, bap.puck)
        pg.draw.rect(screen, bap.color, bap.bar)

    score_text = stats_font.render("Score: {}".format(int(score)), True, yellow)
    high_score_text = stats_font.render("High Score: {}".format(int(high_score)), True, yellow)
    generation_text = stats_font.render("Generation: {}".format(generation), True, yellow)
    screen.blit(score_text, (0, 0))
    screen.blit(high_score_text, (0, 20))
    screen.blit(generation_text, (0, 40))
    if top_fitness is not None:
        top_fitness_text = stats_font.render("Best Fitness: {}".format(top_fitness), True, yellow)
        screen.blit(top_fitness_text, (0, 60))


def puck_animation(baps, genomes_local, nets):

    for index, bap in enumerate(baps):
        bap.puck.x += bap.puck_x_speed
        bap.puck.y += bap.puck_y_speed

        if bap.puck.top <= 0:
            bap.puck.top = 0
            bap.puck_y_speed *= -1

        if bap.puck.left <= 0:
            bap.puck.left = 0
            bap.puck_x_speed *= -1

        if bap.puck.right >= screen_width:
            bap.puck.right = screen_width
            bap.puck_x_speed *= -1

        # if puck hits bar, increase fitness by 4
        if bap.puck.colliderect(bap.bar):
            genomes_local[index].fitness += 4
            bap.puck_y_speed *= -1

        if bap.puck.bottom >= screen_height:
            baps.remove(bap)
            del(genomes_local[index])
            del(nets[index])


# NN controlling its respective bar
def player_bar_movement(baps, genomes_local, nets):

    for index, bap in enumerate(baps):

        input_data = (bap.bar.x, bap.puck.x, bap.puck.y)
        # get the ouput form the NN]
        output_data = nets[index].activate(input_data)
        # the output is a list of output_node numbr of values; in this case 2
        # we are looking for the index of the most activated/largest value in that list
        activated_index = output_data.index(max(output_data))

        # if 0, then move left by bar_speed
        if activated_index == 0:
            bap.bar.x -= bap.bar_speed
        # if 1, then move right by bar_speed
        else:
            bap.bar.x += bap.bar_speed

        # some checks to make sure bar does not extend awat from the window on the x-axis
        if bap.bar.left <= 0:
            bap.bar.left = 0
            genomes_local[index].fitness -= 0.08
        if bap.bar.right >= screen_width:
            bap.bar.right = screen_width
            genomes_local[index].fitness -= 0.08


def eval_genome(genomes, config):

    global high_score
    global generation
    generation += 1

    genomes_local = []
    nets = []
    baps = []
    for g_id, genome in genomes:
        genome.fitness = 0
        genomes_local.append(genome)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        baps.append(BarAndPuck())

    running = True
    score = 0
    while running:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

        # statistical attributes
        score += 1.0/60
        if score > high_score:
            high_score = score

        screen.fill(color_background)
        award_fitness(genomes_local)
        if stop_running(baps):
            running = False

        # the lambda fcuntion evaluates the LIVING BOT with the HIGHEST FITNESS in the CURRENT GENERATION
        draw_objects(baps, score, (lambda genomes_local: max([genome.fitness for genome in genomes_local]) if genomes_local != [] else None)(genomes_local))
        player_bar_movement(baps, genomes_local, nets)
        puck_animation(baps, genomes_local, nets)

        pg.display.flip()   # display the display surface
        clock.tick(fps)      # code refresh rate


def run(config_file):

    # create the config object with the config-feedforward.txt template
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    # create population object
    p = neat.Population(config)

    # statistical information stdout
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # repeat till the i'th generation if the ideal fitness has not been achieved by then
    winner = p.run(eval_genome, 50)

    # draw neural network of the best genome
    # visualize.draw_net(config, winner, True)


# intialize pygame
pg.init()
clock = pg.time.Clock()

# set up simulation window
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Pong")

high_score = 0
generation = -1

# prepare the path to the [NEAT] config file
if __name__ == "__main__":
    main_file_dir = os.path.dirname(__file__)
    config_file = os.path.join(main_file_dir, "config-feedforward.txt")
    run(config_file)


# KeyBoard control of bars.
# KeyBoard Input for controlling Bar
# if event.type == pg.KEYDOWN:
#     if event.key == pg.K_a:
#         for bap in baps:
#             bap.bar_speed -= 10
#     if event.key == pg.K_d:
#         for bap in baps:
#             bap.bar_speed += 10

# if event.type == pg.KEYUP:
#     if event.key == pg.K_a:
#         for bap in baps:
#             bap.bar_speed += 10
#     if event.key == pg.K_d:
#         for bap in baps:
#             bap.bar_speed -= 10