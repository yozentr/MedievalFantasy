import pygame
import utils
import bar

gridsize = 64
buildings = []
houseimg = utils.loadimg('images/Buildings/Blue Buildings/House2.png', 1)

class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 500
        self.bar = bar.Bar(500)
    def render(self, screen, xcamera, ycamera):
        self.bar.val = self.hp
        screen.blit(houseimg, (self.x - xcamera, self.y - ycamera))
        if self.hp < self.bar.maxval:
            self.bar.render(screen, self.x, self.y, xcamera, ycamera, 1)