import utils
import pygame

smallbar = utils.loadimages('images/UI Elements/UI Elements/Bars/SmallBar_Base.png', 1, 5)


class Bar:
    def __init__(self, maxval):
        global smallbar
        self.maxval = maxval
        self.val = maxval
        self.image = pygame.Surface([3 * 64, 64], pygame.SRCALPHA)
        smallbar2 = []
        for i in smallbar:
            smallbar2.append(i.convert_alpha())
        smallbar = smallbar2
        self.image.blit(smallbar[0], [0, 0])
        self.image.blit(smallbar[2], [64, 0])
        self.image.blit(smallbar[4], [128, 0])
    def render(self, screen, x, y, xcamera, ycamera):
        screen.blit(self.image, [x - xcamera, y - ycamera])
        pygame.draw.rect(screen, [255, 0, 0], [x - xcamera + 55, y - ycamera + 27, self.val / self.maxval * 80, 10])