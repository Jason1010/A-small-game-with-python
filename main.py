# 0 - 模块区
import os
import sys
import math
import random
import pygame
import datetime
from pygame.locals import *

# 主要的工作区域
if __name__ == '__main__':

    # 1 - 设置区

    # 1.1 - 窗口设置区
    white = (255, 255, 255)
    screen_width, screen_height = 800, 600
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game")

    # 1.2 - 基础设置区
    pygame.init()
    distance = 350

    keys = [False, False, False, False]
    playerpos = [50, 550]

    acc = [0, 0]
    arrows = []

    badtimer = 100
    badtimer1 = 0
    badguys = [[640, 100]]
    healthvalue = 194
    health_value = 194
    health_value_max = 194
    fin_time = 20
    # start_time = datetime.datetime.now()

    running = 0
    win = 0

    start = 0
    # 参数区：在这块区域初始化参数

    fig_path = 'F:/Project/python/game/资源包/'
    paper = pygame.image.load(fig_path + 'desert.png').convert_alpha()

    wall = pygame.image.load(fig_path + 'tower.png').convert_alpha()
    wall_width = wall.get_width()
    wall_height = wall.get_height()

    player = pygame.image.load(fig_path + 'tank.png').convert_alpha()

    arrow = pygame.image.load(fig_path + 'arrow.png').convert_alpha()

    badguyimg1 = pygame.image.load(fig_path + 'bad.png').convert_alpha()
    badguyimg = badguyimg1

    health_bar_img = pygame.image.load(fig_path + "health_bar.png")
    health_bar_height = health_bar_img.get_height()

    health_img = pygame.image.load(fig_path + "health.png")
    health_height = health_img.get_height()

    victory = pygame.image.load(fig_path + 'vvv.png').convert_alpha()
    game_over = pygame.image.load(fig_path + 'game_over.png')

    start_img = pygame.image.load(fig_path + 'sss.png').convert_alpha()

    # 图片区：在这块区域加载图片

    # 2 - 游戏区

    while not start:
        screen.fill(white)
        screen.blit(start_img, (0, 0))
        pygame.font.init()
        font = pygame.font.Font(None, 84)
        text = font.render("Press Space to Start !",
                           True, (250, 50, 200))
        text_Rect = text.get_rect()
        text_Rect.centerx = screen.get_rect().centerx
        text_Rect.centery = screen.get_rect().centery + 200
        screen.blit(text, text_Rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    start = 1
                    running = 1
                    pygame.mixer.music.load(fig_path + "Checkpoint.mp3")
                    pygame.mixer.music.play(1, 0.0)
                    pygame.mixer.music.set_volume(0.15)
                    start_time = datetime.datetime.now()
                    clock = pygame.time.get_ticks()
    # 2.2 - 游戏进行区
    while running:
        # 2.2.1 - 游戏显示区

        badtimer -= 1
        screen.fill(white)
        screen.blit(paper, (0, 0))

        for bullet in arrows:
            index = 0
            velx = math.cos(bullet[0]) * 10
            vely = math.sin(bullet[0]) * 10
            bullet[1] += velx
            bullet[2] += vely
            if bullet[1] < 0 or bullet[1] > 800 or bullet[2] < 0 or bullet[2] > 600:
                arrows.pop(index)
            index += 1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))

        if badtimer == 0:
            badguys.append([random.randint(50, 750), 0])
            badtimer = 100 - (badtimer1 * 2)
            if badtimer1 >= 35:
                badtimer1 = 35
            else:
                badtimer1 += 2
        index = 0
        for badguy in badguys:
            if badguy[1] > 600:
                badguys.pop(index)
            badguy[1] += 1
            badrect = pygame.Rect(badguyimg.get_rect())
            badrect.top = badguy[1]
            badrect.left = badguy[0]
            if badrect.top > 350:
                health_value -= random.randint(5, 20)
                badguys.pop(index)
            index1 = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[1]
                bullrect.top = bullet[2]
                if badrect.colliderect(bullrect):
                    acc[0] += 1
                    badguys.pop(index)
                    arrows.pop(index1)
                index1 += 1
            index += 1
        for badguy in badguys:
            screen.blit(badguyimg, badguy)
        # 游戏显示区的代码更新区域

        for height in range(0, 800, 100):
            screen.blit(wall, (height, distance))

        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
        playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
        playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
        screen.blit(playerrot, playerpos1)

        font = pygame.font.Font(None, 42)
        cur_time = datetime.datetime.now()
        play_time = (cur_time - start_time).seconds
        if play_time % 60 < 10:
            time_str = ":0"
        else:
            time_str = ":"
        survived_text = font.render(
            str(play_time // 60) +
            time_str +
            str(play_time % 60),
            True, (0, 0, 0)
        )
        text_Rect = survived_text.get_rect()
        text_Rect.topright = [screen_width - 5, 5]
        screen.blit(survived_text, text_Rect)

        health_bar_img = pygame.transform.scale(health_bar_img,
                                                (health_value_max, health_bar_height))
        screen.blit(health_bar_img, [0, 5])

        if health_value < 0:
            health_value = 0
        health_img = pygame.transform.scale(health_img,
                                            (health_value, health_height))
        screen.blit(health_img, [0, 5])

        pygame.display.flip()

        # 2.2.2 - 游戏操作区
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    keys[0] = True
                elif event.key == K_a:
                    keys[1] = True
                elif event.key == K_s:
                    keys[2] = True
                elif event.key == K_d:
                    keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys[0] = False
                elif event.key == pygame.K_a:
                    keys[1] = False
                elif event.key == pygame.K_s:
                    keys[2] = False
                elif event.key == pygame.K_d:
                    keys[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                acc[1] += 1
                arrows.append([math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)),
                               playerpos1[0] + 32, playerpos1[1] + 32])

        if keys[0]:
            playerpos[1] -= 3
        elif keys[2]:
            playerpos[1] += 3
        if keys[1]:
            playerpos[0] -= 3
        elif keys[3]:
            playerpos[0] += 3
        # 2.2.3 - 结束判断区
        if pygame.time.get_ticks() - clock >= fin_time * 1000:
            running = 0
            win = 1
        if health_value == 0:
            running = 0
            win = 0

    while not running and start:
        pygame.mixer.music.stop()
        if win:
            screen.blit(victory, (0, 0))
            pygame.font.init()
            font = pygame.font.Font(None, 84)
            text = font.render("Victory !",
                               True, (250, 50, 200))
            text_Rect = text.get_rect()
            text_Rect.centerx = screen.get_rect().centerx + 20
            text_Rect.centery = screen.get_rect().centery - 250
            screen.blit(text, text_Rect)
        if not win:
            screen.blit(game_over, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
