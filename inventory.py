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
_count_surfaces = {}
_resource_positions = {
    'Wood Resource': (wood_resource, (ix + 80, iy + 75), (ix + 80 + 75, iy + 75 + 70)),
    'Stone Resource': (stone_resource, (ix + 80 * 2, iy + 75), (ix + 80 * 2 + 75, iy + 75 + 70)),
}

def add(name, count):
    if name not in inv:
        inv[name] = count
    else:
        inv[name] += count
    _count_surfaces.pop(name, None)


def get_count_surface(name):
    value = inv[name]
    cached = _count_surfaces.get(name)
    if cached is not None and cached[0] == value:
        return cached[1]
    surface = font.render(str(value), True, 'white')
    _count_surfaces[name] = (value, surface)
    return surface


def render(screen):
    screen.blit(imginv, (ix, iy))
    for name, value in inv.items():
        if value <= 0 or name not in _resource_positions:
            continue
        image, image_pos, count_pos = _resource_positions[name]
        screen.blit(image, image_pos)
        screen.blit(get_count_surface(name), count_pos)
            
                
