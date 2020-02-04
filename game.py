#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pygame
from random import randint

#方便存储所需的设置
class Settings(object):
    """Settings"""
    def __init__(self):
        # 初始化游戏设置变量

        # 界面设置
        self.bg_color = (42,42,42)
        self.tile_size = 32
        
        # 存储关卡数据
        # 0 = 空 -1 = 墙  1 = 人 2 = 箱 3 = 点
        self.level =[[-1,-1,-1,-1,-1,-1,-1,],
                     [-1, 0, 0, 0, 0, 0,-1,],
                     [-1, 1, 2, 0, 3, 0,-1,],
                     [-1, 0, 0, 0, 0, 0,-1,],
                     [-1,-1,-1,-1,-1,-1,-1,]]
                      
        self.screen_width = 400
        self.screen_height = 300
        self.total_size = len(self.level[0])*len(self.level)
        self.decoration = []
        
#存储及读取图像数据
_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = 'img' + os.sep + path + '.png'
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

#存储及读取并转换地图数据
_level_library = {}
def get_level(path):
    global _level_library
    level = _level_library.get(path)
    if level == None:
        canonicalized_path = 'level' + os.sep + path + '.txt'
        f = open(canonicalized_path,"r",encoding="utf-8")
        level_cache = f.read().split('\n')
        level = []
        for i in level_cache:
            row = []
            for j in i:
                # 0 = 空 -1 = 墙  1 = 人 2 = 箱 3 = 点
                if j == '空':
                    row.append(0)
                elif j == '墙':
                    row.append(-1)
                elif j == '人':
                    row.append(1)
                elif j == '箱':
                    row.append(2)                    
                elif j == '点':
                    row.append(3)
                else:
                    raise ValueError('读取关卡数据错误！请检查' + canonicalized_path)
            level.append(row)
        
        _image_library[path] = level
    return level
                
#玩家类
class Player():

    def __init__(self,screen):
        #initialize player and its location
        self.screen = screen
        # load image and get rectangle
        self.image = get_image('playerR')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.x = 1
        self.y = 1
        self.rect.centerx = self.x * 32 + 1
        self.rect.centery = self.y * 32 + 1

    def blitme(self):
        #buld character at the specific location
        self.screen.blit(self.image,self.rect)

#箱子类
class Box():
    def __init__(self,screen):
        #initialize boxes and location
        self.screen = screen
        # load image and get rectangle
        self.image = get_image('box_normal')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.x = 1
        self.y = 1
        self.rect.centerx = self.x * 32 + 1
        self.rect.centery = self.y * 32 + 1

    def blitme(self):
        #buld box at the specific location
        self.screen.blit(self.image,self.rect)


#刷新当前状态
def redraw(game,screen,player,boxes):
    size = game.tile_size
    game.screen_width = len(game.level[0]) * size+2
    game.screen_height = len(game.level) * size+2
    screen = pygame.display.set_mode((game.screen_width, game.screen_height))

    if len(game.decoration) <= game.total_size:
        game.decoration=[str(randint(1,4)) for x in range(game.total_size+10)]

    y = 0
    z = 0
    tempList = list(game.level)

    for i in tempList:
        x = 0
        for j in i:
            # 0 = 空 -1 = 墙  1 = 人 2 = 箱 3 = 点
            if j == -1:
                item_name = 'wall'
            elif j == 1:
                player.x = x 
                player.y = y
                item_name = 'floor'
                game.level[y][x]=0

            elif j == 2:
                box0 = Box(screen)
                box0.x = x
                box0.y = y
                boxes.append(box0)
                item_name = 'floor'
                game.level[y][x]=0
            elif j == 3:
                item_name = 'target'
            else:
                item_name = 'floor'

            screen.blit(get_image(item_name + game.decoration[z]), (x * game.tile_size, y * game.tile_size))
            x += 1
            z += 1
        y += 1

    player.rect.centerx = (player.x + 0.5) * game.tile_size + 1
    player.rect.centery = (player.y + 0.5) * game.tile_size + 1

    player.blitme()

    for box0 in boxes:
        box0.rect.centerx = (box0.x + 0.5) * game.tile_size + 1
        box0.rect.centery = (box0.y + 0.5) * game.tile_size + 1
        box0.blitme()
                
    pygame.display.flip()

#响应事件        
def check_events(game,screen,player,boxes):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x +=1
                player.image = get_image('playerR')
            if event.key == pygame.K_LEFT:
                player.x -=1
                player.image = get_image('playerL')
            if event.key == pygame.K_UP:
                player.y -=1
            if event.key == pygame.K_DOWN:
                player.y +=1
    

#主进程
def run_game():

    pygame.init()
    game = Settings()
    pygame.display.set_caption("推箱子")
    pygame.display.set_icon(get_image('icon2'))
    screen = pygame.display.set_mode((game.screen_width, game.screen_height))
    player = Player(screen)
    boxes =[]
    
    clock = pygame.time.Clock()
    
    game.level = get_level('2')
    
    while True:
        check_events(game,screen,player,boxes)
        
        redraw(game,screen,player,boxes)

        clock.tick(60)

run_game()
