import utils
import pygame
pygame.init()

inv = {
    ('Wood Resource'): 7,
    ('Stone Resource'): 32
}
imginv = utils.loadimg('images/UI Elements/UI Elements/Wood Table/WoodTable_Ai.png', 1.5)
wood_resource = utils.loadimg('images/Terrain/Resources/Wood/Wood Resource/Wood Resource.png', 2)
stone_resource = utils.loadimg('images/Terrain/Decorations/Rocks/Rock2.png', 2)
font = pygame.font.Font(None, 70)
ix = 0
iy = 0

def add(name, count):
    if name not in inv:
        inv[name] = count
    else:
        inv[name] += count
def render(screen):
    screen.blit(imginv, (ix, iy))
    for i in inv:
        if inv[i] > 0:
            if i == 'Wood Resource':
                screen.blit(wood_resource, (ix + 80, iy + 75))
            if i == 'Stone Resource':
                screen.blit(stone_resource, (ix + 80 * 2, iy + 75))
    for i in inv:
        if inv[i] > 0: 
            if i == 'Wood Resource':
                count = font.render(str(inv[('Wood Resource')]), True, 'white')
                screen.blit(count, (ix + 80 + 75, iy + 75 + 70))
            if i == 'Stone Resource':
                count = font.render(str(inv[('Stone Resource')]), True, 'white')
                screen.blit(count, (ix + 80 * 2 + 75, iy + 75 + 70))
            
                
