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
        hitbox = pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, 150, 60])
        if hitbox.collidepoint(pygame.mouse.get_pos()):
            hitbox = pygame.draw.rect(screen, (50, 50, 50), [self.x, self.y, 150, 60])
            if click == True:
                self.slot()
        screen.blit(self.textimg, (self.x, hitbox.centery - self.textimg.get_height() / 2))
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, 150, 60)