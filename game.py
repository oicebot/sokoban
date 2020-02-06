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

        self.level_name = "1"
        
        # 存储关卡数据
        # 0 = 空 -1 = 墙  1 = 人 2 = 箱 3 = 点
        self.level =[[-1,-1,-1,-1,-1,-1,-1,],
                     [-1, 0, 0, 0, 0, 0,-1,],
                     [-1, 1, 2, 0, 3, 0,-1,],
                     [-1, 0, 0, 0, 0, 0,-1,],
                     [-1,-1,-1,-1,-1,-1,-1,]]
                      
        self.screen_width = 1920
        self.screen_height = 1080
        #TODO: 屏幕宽高初始化太小时，背景 bg 显示不正确

        self.total_size = len(self.level[0])*len(self.level)

        self.boxes = {}
        
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

#读取并转换地图数据
def get_level(path):
    canonicalized_path = 'level' + os.sep + path + '.txt'
    f = open(canonicalized_path,"r",encoding="utf-8")
    level_cache = f.read().split('\n')
    f.close()
    level = []
    for i in level_cache:
        #去掉可能出现的空行
        if not i:
            continue
        row = []
        for j in i:
            # 0 = 空 -1 = 墙  1 = 人 2 = 箱 3 = 点
            if j == '空' or j == "_" or j=="-":
                row.append(0)
            elif j == '墙' or j =="#":
                row.append(-1)
            elif j == '人' or j =="@":
                row.append(1)
            elif j == '箱' or j =="$":
                row.append(2)                    
            elif j == '点' or j ==".":
                row.append(3)
            else:
                raise ValueError('读取关卡数据错误！请检查' + canonicalized_path)
        level.append(row)

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


def loadlevel(game,screen,bg,player):
    """每次关卡只载入一次，读取并绘制整个关卡的背景，
    初始化元素位置。
    """
    game.boxes = {}
    boxes = {}

    size = game.tile_size
    game.screen_width = len(game.level[0]) * size+2
    game.screen_height = len(game.level) * size+2
    screen = pygame.display.set_mode((game.screen_width, game.screen_height))

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
                #不在数组里追踪对象位置
            elif j == 2:
                box0 = Box(screen)
                box0.x = x
                box0.y = y
                boxes[(x,y)] = box0
                item_name = 'floor'
                game.level[y][x]=0
                #不在数组里追踪箱子位置
            elif j == 3:
                item_name = 'target'
            else:
                item_name = 'floor'

            bg.blit(get_image(item_name + str(randint(1,4))), (x * game.tile_size, y * game.tile_size))
            #将所有图形绘制到 bg 对象上
            x += 1
            z += 1
        y += 1
    
    game.boxes = boxes
    

#刷新当前状态
def redraw(game,screen,bg,player):
    boxes = game.boxes
    size = game.tile_size

    screen.blit(bg,(0,0))

    player.rect.centerx = (player.x + 0.5) * size + 1
    player.rect.centery = (player.y + 0.5) * size + 1
    player.blitme()

    total = len(boxes)
    done = 0
    for pos,box0 in boxes.items():
        box0.rect.centerx = (pos[0] + 0.5) * size + 1
        box0.rect.centery = (pos[1] + 0.5) * size + 1
        if game.level[box0.y][box0.x] == 3:
            box0.image = get_image("box_done")
            done += 1
        else:
            box0.image = get_image("box_normal")
        box0.blitme()

    
    pygame.display.flip()


#响应事件        
def check_events(game,screen,bg,player):
    boxes = game.boxes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key >= 49 and event.key <= 57:
                #key 1 - 9
                number = event.key-48
                print("Loading level:", number)
                game.box = {}
                game.level_name = str(number)
                game.level = get_level(game.level_name)
                loadlevel(game,screen,bg,player)
                break

            if event.key == pygame.K_F5:
                #Reset Game
                game.boxes = {} 
                game.level = get_level(game.level_name)
                loadlevel(game,screen,bg,player)
                break

            # 0 = 空 -1 = 墙  1 = 人 2 = 箱 3 = 点
            x = player.x
            y = player.y
            if event.key == pygame.K_RIGHT:
                #右边一格有箱子
                if (x+1,y) in boxes.keys(): 
                    #右边两个没有箱子，而且是地板或是点
                    if not boxes.get((x+2,y)) and ( game.level[y][x+2] == 0 or game.level[y][x+2] == 3 ):
                        box0 = boxes.pop((x+1,y)) #取出箱子对象
                        box0.x = x+2              #移动
                        boxes[(x+2,y)]=box0       #放回数组里
                        player.x +=1              #移动玩家
                #右边一格是地板或是点
                elif game.level[y][x+1] == 0 or game.level[y][x+1] == 3:
                    player.x +=1
                player.image = get_image('playerR')

            if event.key == pygame.K_LEFT:
                if (x-1,y) in boxes.keys(): 
                    if not boxes.get((x-2,y)) and ( game.level[y][x-2] == 0 or game.level[y][x-2] == 3 ):
                        box0 = boxes.pop((x-1,y)) #取出箱子对象
                        box0.x = x-2              #移动
                        boxes[(x-2,y)]=box0       #放回数组里
                        player.x -=1              #移动玩家
                elif game.level[y][x-1] == 0 or game.level[y][x-1] == 3:
                    player.x -=1
                player.image = get_image('playerL')
            if event.key == pygame.K_UP:
                if (x,y-1) in boxes.keys(): 
                    if not boxes.get((x,y-2)) and ( game.level[y-2][x] == 0 or game.level[y-2][x] == 3 ):
                        box0 = boxes.pop((x,y-1)) #取出箱子对象
                        box0.y = y-2              #移动
                        boxes[(x,y-2)]=box0       #放回数组里
                        player.y -=1              #移动玩家
                elif game.level[y-1][x] == 0 or game.level[y-1][x] == 3:
                    player.y -=1
            if event.key == pygame.K_DOWN:
                if (x,y+1) in boxes.keys(): 
                    if not boxes.get((x,y+2)) and ( game.level[y+2][x] == 0 or game.level[y+2][x] == 3 ):
                        box0 = boxes.pop((x,y+1)) #取出箱子对象
                        box0.y = y+2              #移动
                        boxes[(x,y+2)]=box0       #放回数组里
                        player.y +=1              #移动玩家
                elif game.level[y+1][x] == 0 or game.level[y+1][x] == 3:
                    player.y +=1
    

#主进程
def run_game():

    pygame.init()
    game = Settings()
    pygame.display.set_caption("推箱子")
    pygame.display.set_icon(get_image('icon'))

    screen = pygame.display.set_mode((game.screen_width, game.screen_height))
    bg = pygame.Surface((game.screen_width, game.screen_height), 
                        pygame.SRCALPHA, 32)

    player = Player(screen)

    game.boxes = {} #{(3,5): box0,(4, 3): box1}
    
    clock = pygame.time.Clock()
    
    game.level_name = "1"
    game.level = get_level(game.level_name)

    loadlevel(game,screen,bg,player)
    
    #print("paused for debug")

    while True:
        check_events(game,screen,bg,player)
        
        redraw(game,screen,bg,player)

        clock.tick(30)

run_game()

