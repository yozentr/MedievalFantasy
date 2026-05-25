import utils
import pytmx
import pygame
import animation
import bar
import random
import inventory

imgtrees = utils.loadimages('images/Terrain/Resources/Wood/Trees/Tree3.png', 1, 8)
imgstump = utils.loadimg('images/Terrain/Resources/Wood/Trees/Stump 3.png', 1)
wood_resource = utils.loadimg('images/Terrain/Resources/Wood/Wood Resource/Wood Resource.png', 2)
stone_resource = utils.loadimg('images/Terrain/Decorations/Rocks/Rock2.png', 2)
trees = []
stumps = []
stones = []

def loadtrees():
    map = pytmx.load_pygame('Tiled/World.tmx')
    for x, y, gid in map.get_layer_by_name('Tree3'):
        if gid != 0:
            tree = Tree(x * 64, (y - 2) * 64,)
            trees.append(tree)
    for x, y, gid in map.get_layer_by_name('Stone'):
        if gid != 0:
            stone = Stone(x * 64, (y) * 64, map.get_tile_image_by_gid(gid))
            stones.append(stone)

            
class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.bar = bar.Bar(100)
        self.dead = False
        self.anim = animation.Animation('images/Terrain/Resources/Wood/Trees/Tree3.png', 1, 8, 12, True)
    def render(self, screen, xcamera, ycamera, scale):
        self.bar.val = self.hp
        screen_x, screen_y = utils.world_to_screen(self.x, self.y, xcamera, ycamera, scale)
        if self.hp > 0:
            self.anim.render(screen, screen_x, screen_y, 'r', scale)
            self.anim.update()
            if self.hp != self.bar.maxval:
                self.bar.render(screen, self.x, self.y, xcamera, ycamera, scale)
            
        else:
            screen.blit(utils.scale_image(imgstump, scale), [round(screen_x), round(screen_y - 60 * scale)])
            if self.dead == False:
                for i in range(random.randint(1, 3)):
                    stumps.append(Stump(screen_x, screen_y))
                self.dead = True
            
    def get_hitbox(self):
        return pygame.rect.Rect([self.x, self.y], imgtrees[0].get_size())
    
class Stump:
    def __init__(self, x, y):
        self.x = x + random.randint(-80, 80) + 100
        self.y = y + random.randint(-60, 60)
        self.starttimer = 60
        inventory.add('Wood Resource', 1)
    def render(self, screen, xcamera, ycamera, scale):
        self.starttimer -= 1
        screen.blit(wood_resource, [self.x, self.y])
        if self.starttimer == -500:
            stumps.remove(self)
        if self.starttimer < 1:
            self.x += (0 - self.x) / 10 * (-self.starttimer / 100)
            self.y += (screen.get_height() - self.y) / 10 * (-self.starttimer / 100)
class Stone:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.hp = 100
        self.bar = bar.Bar(100)
    def render(self, screen, xcamera, ycamera, scale=1):
        self.bar.val = self.hp
        screen_x, screen_y = utils.world_to_screen(self.x, self.y, xcamera, ycamera, scale)
        screen.blit(utils.scale_image(self.img, scale), (round(screen_x), round(screen_y)))
        pygame.draw.rect(screen, 'red', utils.world_rect_to_screen(self.get_hitbox(), xcamera, ycamera, scale), 2)
        if self.hp != self.bar.maxval:
            self.bar.render(screen, self.x, self.y, xcamera, ycamera, scale)
            if self.hp < 1:
                stones.remove(self)
                for i in range(1):
                    stumps.append(StoneResource(screen_x, screen_y))
    def get_hitbox(self):
        return pygame.rect.Rect([self.x, self.y], self.img.get_size())
class StoneResource:
    def __init__(self, x, y):
        self.x = x + random.randint(-80, 80)
        self.y = y + random.randint(-60, 60)
        self.starttimer = 60
        inventory.add('Stone Resource', 1)
    def render(self, screen, xcamera, ycamera, scale):
        self.starttimer -= 1
        screen.blit(stone_resource, [self.x, self.y])
        if self.starttimer == -500:
            stumps.remove(self)
        if self.starttimer < 1:
            self.x += (0 - self.x) / 10 * (-self.starttimer / 100)
            self.y += (screen.get_height() - self.y) / 10 * (-self.starttimer / 100)
