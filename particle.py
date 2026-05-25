import pygame
import utils
import animation

particles = []

class Dust:
    def __init__(self, x, y, xcamera, ycamera):
        self.x = x - xcamera + 64
        self.y = y - ycamera + 64
        self.anim = animation.Animation("images/Particle FX/Dust_01.png", 2, 8, 12, False)
    def render(self, screen):
        self.anim.render(screen, self.x, self.y, 'r', 1)
        self.anim.update()