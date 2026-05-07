import pygame
pygame.init()
font = pygame.font.Font(None, 40)

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
    def render(self, screen):
        for i in self.button:
            i.render(screen)
class Button:
    def __init__(self, text, color, x, y):
        self.textimg = font.render(text, True, color)
        self.slot = None
        self.x = x
        self.y = y
    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, 150, 60])
        screen.blit(self.textimg, (self.x, self.y))