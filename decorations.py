import utils
import pytmx
import pygame
import animation
import bar

imgtrees = utils.loadimages('images/Terrain/Resources/Wood/Trees/Tree3.png', 1, 8)
imgstump = utils.loadimg('images/Terrain/Resources/Wood/Trees/Stump 3.png', 1)
trees = []

def loadtrees():
    map = pytmx.load_pygame('Tiled/World.tmx')
    for x, y, gid in map.get_layer_by_name('Tree3'):
        if gid != 0:
            tree = Tree(x * 64, (y - 2) * 64,)
            trees.append(tree)
            
class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.bar = bar.Bar(100)
        self.anim = animation.Animation('images/Terrain/Resources/Wood/Trees/Tree3.png', 1, 8, 12, True)
    def render(self, screen, xcamera, ycamera, scale):
        #screen.blit(imgtrees[0], ((self.x - xcamera) * scale, (self.y - ycamera) * scale))
        self.bar.val = self.hp
        if self.hp > 0:
            self.anim.render(screen, self.x - xcamera, self.y - ycamera, 'r', 1)
            self.anim.update()
            if self.hp != self.bar.maxval:
                self.bar.render(screen, self.x, self.y, xcamera, ycamera)
        else:
            screen.blit(imgstump, [self.x - xcamera, self.y - ycamera])
    def get_hitbox(self):
        return pygame.rect.Rect([self.x, self.y], imgtrees[0].get_size())
    