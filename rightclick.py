import pygame
import utils

pygame.init()
font = pygame.font.Font('font BikiniBottom-Regular.otf', 30)
img1 = utils.loadimg('images/UI Elements/UI Elements/Buttons/SmallBlueSquareButton_Pressed.png', 1)
img1 = img1.subsurface(img1.get_bounding_rect())
img2 = utils.loadimg('images/UI Elements/UI Elements/Buttons/SmallRedSquareButton_Pressed.png', 1)
img2 = img2.subsurface(img2.get_bounding_rect())

img1 = pygame.transform.scale(img1, (200, 60))
img2 = pygame.transform.scale(img2, (200, 60))

class Menu:
    def __init__(self, x, y, names):
        self.x = x
        self.y = y
        self.button = []
        yy = self.y
        for i in names:
            b = Button(i, 'white', self.x, yy)
            self.button.append(b)
            yy += 60
    def render(self, screen, click):
        for i in self.button:
            i.render(screen, click)
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, 150, 60 * len(self.button))
class Button:
    def __init__(self, text, color, x, y):
        self.textimg = font.render(text, True, color)
        self.slot = None
        self.x = x
        self.y = y
    def render(self, screen, click):
        hitbox = screen.blit(img1, (self.x, self.y))
        if hitbox.collidepoint(pygame.mouse.get_pos()):
            hitbox = screen.blit(img2, (self.x, self.y))
            if click == True:
                self.slot()
        screen.blit(self.textimg, (self.x + 40, hitbox.centery - self.textimg.get_height() / 2))
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, 150, 60)