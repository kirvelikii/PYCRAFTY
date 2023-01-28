import random

import pygame

enemy_img = [pygame.image.load('Bird0.png'), pygame.image.load('Bird1.png'), pygame.image.load('Bird2.png'),
            pygame.image.load('Bird3.png')]
class Enemy:
    def __init__(self, x, away_y):
        self.x = x
        self.y = away_y
        self.ay = away_y
        self.speed = 3
        self.dest_y = self.speed * random().randrange(20, 70)
        self.img_cnt = 0
        self.cd_hide = 0
        self.come = True
        self.go_away = False

    def draw(self):
        if self.img_cnt == 30:
            self.img_cnt = 0

        screen.blit()



