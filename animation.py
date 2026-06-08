import pygame
import utils


class Animation:
    def __init__(self, path, scale, countimg, period, repeat):
        self.images = utils.loadimages(path, scale, countimg)
        self.index = 0
        self.period = period
        self.startperiod = period
        self.repeat = repeat

    def render(self, screen, x, y, dir, scale=1):
        image = self.images[self.index]
        image = utils.transform_image(image, scale, dir != 'r')
        self.hitbox = screen.blit(image, [round(x), round(y)])
        return self.hitbox

    def update(self):
        self.period -= 1
        if self.period == 0:
            self.index += 1
            self.period = self.startperiod
        if self.index == len(self.images):
            if self.repeat == True:
                self.index = 0 
            else:
                self.index = len(self.images) - 1
    def reset(self):
        self.index = 0
        self.period = self.startperiod
    def what_size_of_img(self):
        return self.images[self.index].get_size()
        
        
