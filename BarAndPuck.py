import pygame as pg
from game_settings import *
import random as rd
import math


class BarAndPuck:

    def __init__(self):

        self.puck = pg.Rect((screen_width*0.5 - puck_radius*0.5, screen_height * 0.35 - puck_radius*0.5), (puck_radius, puck_radius))
        self.puck_x_speed, self.puck_y_speed = BarAndPuck.set_intial_puck_speed()
        self.bar = pg.Rect((screen_width*0.5 - bar_length/2, screen_height-bar_width), (bar_length, bar_width))
        self.bar_speed = bar_speed
        self.color = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))


    # chooses a random direction among the 4 quadrants, and sets the x and y velocity components accordingly
    def set_intial_puck_speed():

        # making sure that neither x nor y component has too much weight over the other
        # as it might lead to either too much bouncing between the side walls OR the top wall and bar
        q1 = rd.randint(35, 55)
        q2 = rd.randint(125, 145)
        q3 = rd.randint(215, 235)
        q4 = rd.randint(305, 325)
        angle = rd.choice([q1, q2, q3, q4])
        to_rad = math.pi / 180
        x_speed, y_speed = puck_speed*math.cos(angle*to_rad), puck_speed*math.sin(angle*to_rad)

        return x_speed, y_speed
