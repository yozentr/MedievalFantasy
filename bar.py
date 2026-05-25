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
    def render(self, screen, x, y, xcamera, ycamera, scale=1):
        screen_x, screen_y = utils.world_to_screen(x, y, xcamera, ycamera, scale)
        screen.blit(utils.scale_image(self.image, scale), [round(screen_x), round(screen_y)])
        pygame.draw.rect(screen, [255, 0, 0], [
            round(screen_x + 55 * scale),
            round(screen_y + 27 * scale),
            round(self.val / self.maxval * 80 * scale),
            max(1, round(10 * scale)),
        ])
