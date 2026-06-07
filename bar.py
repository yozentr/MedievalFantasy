import utils
import pygame

smallbar = utils.loadimages('images/UI Elements/UI Elements/Bars/SmallBar_Base.png', 1, 5)
_smallbar_converted = False


def _prepare_smallbar():
    global smallbar, _smallbar_converted
    if _smallbar_converted:
        return smallbar
    if pygame.display.get_init() and pygame.display.get_surface() is not None:
        smallbar = [image.convert_alpha() for image in smallbar]
        _smallbar_converted = True
    return smallbar


class Bar:
    def __init__(self, maxval):
        self.maxval = maxval
        self.val = maxval
        self._scaled_images = {}
        self.image = pygame.Surface([3 * 64, 64], pygame.SRCALPHA)
        bar_images = _prepare_smallbar()
        self.image.blit(bar_images[0], [0, 0])
        self.image.blit(bar_images[2], [64, 0])
        self.image.blit(bar_images[4], [128, 0])
    def get_image(self, scale):
        scale_key = round(float(scale), 4)
        if scale_key == 1:
            return self.image
        image = self._scaled_images.get(scale_key)
        if image is None:
            image = utils.scale_image(self.image, scale_key)
            self._scaled_images[scale_key] = image
        return image
    def render(self, screen, x, y, xcamera, ycamera, scale=1):
        screen_x, screen_y = utils.world_to_screen(x, y, xcamera, ycamera, scale)
        screen.blit(self.get_image(scale), [round(screen_x), round(screen_y)])
        pygame.draw.rect(screen, [255, 0, 0], [
            round(screen_x + 55 * scale),
            round(screen_y + 27 * scale),
            round(self.val / self.maxval * 80 * scale),
            max(1, round(10 * scale)),
        ])
