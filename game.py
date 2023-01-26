#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

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

camera = Camera(camera_configure, total_level_width, total_level_height)
def get_click(pos):
    global level, entities, camera
    x, y = pos
    level[y // 32][x // 32] = ' '
    print(camera.state)
    platformss = [i.delete(camera.state[0] + x, camera.state[1] + y) for i in platforms]
    '''entities.remove(Platform(x // 32 * 32, y // 32 * 32))
    print(platforms.pop(platforms.index(Platform(x // 32 * 32, y // 32 * 32))))'''
    g = open('level.txt', mode='w')
    for i in range(len(level)):
        print(''.join(level[i]), end='',  file=g)

def main():
    global level, entities, platforms, trees
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("PYCRAFT") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
    bg2 = pygame.image.load('fon.jpg')                                     # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    
    hero = Player(0,0) # создаем героя по (x,y) координатам
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
    pygame.mixer.music.load("audios/birds.mp3")
    pygame.mixer.music.play(-1)
    
    while 1: # Основной цикл программы
        timer.tick(45)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == pygame.MOUSEBUTTONDOWN:
                camera.update(hero)
                get_click(e.pos)

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
                    if flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        screen.blit(bg2, (0,0))      # Каждую итерацию необходимо всё перерисовывать


         # центризируем камеру относительно персонажа
        # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        camera.update(hero)
        hero.update(left, right, up, platforms)
        
        pygame.display.update()     # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
