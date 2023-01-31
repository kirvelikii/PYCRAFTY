#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random, randrange
import math
from Gen import generate
# Импортируем библиотеку pygame
import pygame
from pygame import *
'''from player import *'''
from blocks import *
import math
# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#90EEFD"

enemy_img = [pygame.image.load('Bird0.png'), pygame.image.load('Bird1.png'), pygame.image.load('Bird2.png'),
             pygame.image.load('Bird3.png')]

MOVE_SPEED = 10
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 8
GRAVITY = 0.8  # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.2  # скорость смены кадров
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
                   ('%s/mario/r2.png' % ICON_DIR),
                   ('%s/mario/r3.png' % ICON_DIR),
                   ('%s/mario/r4.png' % ICON_DIR),
                   ('%s/mario/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/mario/l1.png' % ICON_DIR),
                  ('%s/mario/l2.png' % ICON_DIR),
                  ('%s/mario/l3.png' % ICON_DIR),
                  ('%s/mario/l4.png' % ICON_DIR),
                  ('%s/mario/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/mario/0.png' % ICON_DIR, 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def Shoot(self):
        fixspeed = 20
        posx = pygame.mouse.get_pos()[0]
        posy = pygame.mouse.get_pos()[1]

        self.a = posx - self.rect.right
        self.b = self.rect.centery - posy
        self.c = math.hypot(self.a, self.b)
        self.t = self.c / fixspeed
        speedx = self.a / self.t
        speedy = -self.b / self.t
        bullet = Bullet(self.rect.right, self.rect.centery, speedx, speedy)
        entities.add(bullet)
        bullets.add(bullet)

    def update(self, left, right, up, platforms):

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False;  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def getpos(self):
        return (self.rect.x, self.rect.y)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.top > WIN_HEIGHT or self.rect.left > WIN_WIDTH:
            self.kill()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def getpos(self):
        return (self.state[0], self.state[1])

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2 + 10, -t + WIN_HEIGHT / 2 + 10

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


generate(40, 400, 'level.txt')
level = open('level.txt').readlines()
entities = pygame.sprite.Group()  # Все объекты
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
platforms = []  # то, во что мы будем врезаться или опираться
trees = []
camera = ''
total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
hero = Player(0, 0)  # создаем героя по (x,y) координатам
camera = Camera(camera_configure, total_level_width, total_level_height)
pygame.init()  # Инициация PyGame, обязательная строчка
screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко


def get_click(pos):
    global level, entities, camera, platforms
    x, y = pos
    dop = camera.getpos()
    print(dop)
    level[y // 32][x // 32] = ' '
    platformss = [i.delete(dop[0] + x, 9 * 32 + dop[1] + y) for i in platforms]
    trr = [i.delete(dop[0] + x, 9 * 32 + dop[1] + y) for i in trees]
    '''entities.remove(Platform(x // 32 * 32, y // 32 * 32))
    print(platforms.pop(platforms.index(Platform(x // 32 * 32, y // 32 * 32))))'''
    g = open('level.txt', mode='w')
    for i in range(len(level)):
        print(''.join(level[i]), end='', file=g)


class Enemy:
    def __init__(self, away_y):
        self.x = randrange(550, 730)
        self.y = away_y
        self.ay = away_y
        self.speed = 3
        self.dest_y = self.speed * randrange(20, 70)
        self.img_cnt = 0
        self.cd_hide = 0
        self.come = True
        self.go_away = False

    def draw(self):
        if self.img_cnt == 30:
            self.img_cnt = 0

        screen.blit(enemy_img[self.img_cnt // 3], (self.x, self.y))

        if self.come and self.cd_hide == 0:
            if self.y < self.dest_y:
                self.y += self.speed
            else:
                self.come = False
                self.go_away = True
                self.dest_y = self.ay
        elif self.go_away:
            if self.y > self.dest_y:
                self.y -= self.speed
            else:
                self.come = True
                self.go_away = False
                self.x = randrange(550, 730)
                self.dest_y = self.speed * randrange(20, 70)
                self.cd_hide = 80
        elif self.cd_hide > 0:
            self.cd_hide -= 1


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 40))
        self.image.fill('BLUE')
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIN_WIDTH / 2, WIN_WIDTH)
        self.rect.y = randrange(10, WIN_HEIGHT)
        self.speedy = 0
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > WIN_HEIGHT + 10 or self.rect.left < -10 or self.rect.right > WIN_WIDTH + 10:
            self.rect.x = random.randrange(WIN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 8)


for i in range(2):
    mob = Mob()
    entities.add(mob)
    mobs.add(mob)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def main():
    global level, entities, platforms, trees
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("PYCRAFT")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    bg2 = pygame.image.load('fon.jpg')  # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    trees = []
    entities.add(hero)
    generate(40, 400, 'level.txt')
    level = open('level.txt').readlines()
    level = [[i for i in a] for a in level]
    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == '|':
                pf = Tree(x, y)
                entities.add(pf)
                trees.append(pf)
            elif col == '*':
                pf = Listva(x, y)
                entities.add(pf)
                trees.append(pf)
            elif col == 'E':
                pf = Earth(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == 'S':
                pf = Stone(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == 'R':
                pf = Rude(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    flPause = False
    # pygame.mixer.music.load("audios/birds.ogg")
    # pygame.mixer.music.play(-1)
    enemy1 = Enemy(-80)
    clock = pygame.time.Clock()

    counter, text = 0, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Comic Sans', 20)
    hp = 3
    hp_img = pygame.image.load("mario/hp_full.png").convert()
    hp_img = pygame.transform.scale(hp_img, (30, 30))
    hp_img.set_colorkey('black')
    while 1:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.MOUSEBUTTONDOWN:
                hero.Shoot()
                '''get_click(e.pos)'''
            if e.type == pygame.USEREVENT:
                counter += 1
                mi = counter // 60
                counter = counter % 60
                text = ('Время выживания   ' + str(mi) + ':' + str(counter)).rjust(7)
            if e.type == QUIT:
                raise SystemExit

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    flPause = not flPause
                #    if flPause:
                #       pygame.mixer.music.pause()
            #      else:
            #          pygame.mixer.music.unpause()
        playerhits = pygame.sprite.spritecollide(hero, mobs, False)
        bullethits = pygame.sprite.groupcollide(bullets, mobs, True, True)
        if playerhits:
            hp -= 1
        for hit in bullethits:
            mob = Mob()
            entities.add(mob)
            mobs.add(mob)
        for t in bullets:
            t.update()
        screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        draw_lives(screen, 30, 550, hp, hp_img)
        pygame.display.flip()
        screen.blit(bg2, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        enemy1.draw()
        if hp == 0:
            print('Game Over, your time -', mi, ':', counter)
            raise SystemExit
        # центризируем камеру относительно персонажа
        # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        camera.update(hero)
        hero.update(left, right, up, platforms)

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
