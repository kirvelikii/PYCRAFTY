
from pygame import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами
#определяем каждый класс блока
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/ground.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.pos = (x, y)

    def delete(self, x, y):
        if 0 <= x - self.pos[0] <= 32 and -1 <  y // 32 - self.pos[1] // 32 < 1:
            self.image = Surface((0, 0))
            self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
            self.rect = Rect(0, 0, 0, 0)
            return 'gr'
class Tree(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/wood.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.pos = (x, y)

    def delete(self, x, y):
        if 0 <= x - self.pos[0] <= 32 and -1 < y // 32 - self.pos[1] // 32 < 1:
            self.image = Surface((0, 0))
            self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
            self.rect = Rect(0, 0, 0, 0)
            return 'wood'

class Listva(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/listva.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.pos = (x, y)

    def delete(self, x, y):
        if 0 <= x - self.pos[0] <= 32 and -1 < y // 32 - self.pos[1] // 32 < 1:
            self.image = Surface((0, 0))
            self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
            self.rect = Rect(0, 0, 0, 0)
            return 'list'

class Earth(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/earth.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.pos = (x, y)

    def delete(self, x, y):
        if 0 <= x - self.pos[0] <= 32 and -1 < y // 32 - self.pos[1] // 32 < 1:
            self.image = Surface((0, 0))
            self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
            self.rect = Rect(0, 0, 0, 0)
            return 'gr'

class Stone(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/stone.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.pos = (x, y)

    def delete(self, x, y):
        if 0 <= x - self.pos[0] <= 32 and -1 < y // 32 - self.pos[1] // 32 < 1:
            self.image = Surface((0, 0))
            self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
            self.rect = Rect(0, 0, 0, 0)
            return 'stone'

class Rude(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/ruda.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.pos = (x, y)

    def delete(self, x, y):
        if 0 <= x - self.pos[0] <= 32 and -1 < y // 32 - self.pos[1] // 32 < 1:
            self.image = Surface((0, 0))
            self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
            self.rect = Rect(0, 0, 0, 0)
            return 'rude'