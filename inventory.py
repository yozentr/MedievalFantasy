import utils

inv = {}
imginv = utils.glueimagesgrid('images/UI Elements/UI Elements/Wood Table/WoodTable.png', 1, 3, 3)
wood_resource = utils.loadimg('images/Terrain/Resources/Wood/Wood Resource/Wood Resource.png', 1)
font = pygame.font.Font(None, 30)

def add(name, count):
    if name not in inv:
        inv[name] = count
    else:
        inv[name] += count
def render(screen):
    screen.blit(imginv, (0, 0))
    for i in inv:
        if inv[i] > 0:
            if i == 'Wood Resource':
                screen.blit(wood_resource, (0, 0))
    