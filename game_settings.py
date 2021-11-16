import pygame as pg

# basic game settings

# core settings
fps = 60
screen_width = 1200
screen_height = 600

# BarAndPuck object properties
puck_radius = 30
puck_speed = 14
bar_length = 100
bar_width = 18
bar_speed = 10

# colors
color_background = (13, 28, 59)
color_puck = (255, 231, 90)
yellow = (255, 252, 144)

# fonts
pg.font.init()
stats_font = pg.font.SysFont("Arial", 20)
