import pygame
from constants import *

class Circle:
    def __init__(self, win, color, row, col):
        self.win = win
        self.color = color
        self.row = row
        self.col = col
        self.pos = (self.row, self.col)
        self.selected = False
        # self.draw()

    def draw(self):
        pygame.draw.circle(self.win, self.color, (self.col * SQUARE_SIZE + RADIUS, self.row * SQUARE_SIZE + RADIUS), RADIUS)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.pos = (self.row, self.col)
        self.draw()