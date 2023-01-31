#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random, randrange

from Gen import generate
# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from blocks import *

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#90EEFD"


enemy_img = [pygame.image.load('Bird0.png'), pygame.image.load('Bird1.png'), pygame.image.load('Bird2.png'),
            pygame.image.load('Bird3.png')]

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
    l, t = -l+WIN_WIDTH / 2 + 10, -t+WIN_HEIGHT / 2 + 10

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)
generate(40,  400, 'level.txt')
level = open('level.txt').readlines()
entities = pygame.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться
trees = []
camera = ''
total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
hero = Player(0, 0) # создаем героя по (x,y) координатам
camera = Camera(camera_configure, total_level_width, total_level_height)
pygame.init() # Инициация PyGame, обязательная строчка
screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
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
        print(''.join(level[i]), end='',  file=g)

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


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def main():
    global level, entities, platforms, trees
    pygame.init() # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("PYCRAFT") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
    bg2 = pygame.image.load('fon.jpg')                                     # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    

    left = right = False # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    trees = []
    entities.add(hero)
    generate(40,  400, 'level.txt')
    level = open('level.txt').readlines()
    level = [[i for i in a] for a in level]
    timer = pygame.time.Clock()
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
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
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту
    
    camera = Camera(camera_configure, total_level_width, total_level_height)

    flPause = False
   # pygame.mixer.music.load("audios/birds.ogg")
  # pygame.mixer.music.play(-1)
    enemy1 = Enemy(-80)
    clock = pygame.time.Clock()

    counter, text = 0 , '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Comic Sans', 20)
    hp = 3
    hp_img = pygame.image.load("mario/hp_full.png").convert()
    hp_img = pygame.transform.scale(hp_img, (30, 30))
    hp_img.set_colorkey('black')
    while 1: # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == pygame.MOUSEBUTTONDOWN:
                camera.update(hero)
                get_click(e.pos)
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
        screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        draw_lives(screen, 30, 550, hp, hp_img)
        pygame.display.flip()
        screen.blit(bg2, (0,0))      # Каждую итерацию необходимо всё перерисовывать
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
        
        pygame.display.update()     # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
