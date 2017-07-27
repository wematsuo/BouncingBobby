import pygame
import random
import math
import sys
import time
from pygame.locals import *
from PlatformBase import Platform
from PlayerBase import Player
from PlatformBottom import PlatformBase
from PlatformTop import PlatformTop
from Flashing import Flash

#music
pygame.mixer.pre_init(44100,16,3,512)
pygame.mixer.init()
pygame.init()

pygame.mixer.music.load("Tobu.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

bounceSound = pygame.mixer.Sound("Bounce.wav")
hitSound = pygame.mixer.Sound("Hit.wav")

#Sensitivity
num = input("Insert Sensitivity From 1 - 14 (recomended 7): ")
num = int(num)

#screen
screen = pygame.display.set_mode((640, 460))
background =  pygame.Surface((640, 460), 0, screen)
background.fill((255, 255, 255))
screen.blit(background, (0, 0))
font = pygame.font.SysFont(None, 36)
pygame.display.set_caption('Bouncing Bobby!')
pygame.display.set_icon(pygame.image.load('Bobby.png'))

alive = 0
score = 0
finalScore = 0
results = []
scored = False
HighScore = 0

with open('highScore', 'r') as inputfile:
    for line in inputfile:
        results.append(float( (line.strip().rstrip('\n')) ))
    HighScore = max(results)
        
#Base grouping
BasePlatform = pygame.sprite.Group()

#create rect for Base group
platformBase = PlatformBase(0, 460, 650, 10)
BasePlatform.add(platformBase)

#Top Grouping
TopPlatform = pygame.sprite.Group()

#create rect for Top Group 
platformTop = PlatformTop(0, 1, 640, 1)
TopPlatform.add(platformTop)

#Group for flashing
flashs = pygame.sprite.Group()

#rect for flashs group list
Flash1 = Flash(380, 105, 50, 50)
flashs.add(Flash1)

#creating group to hold the pipe things
platforms = pygame.sprite.Group()

plat_speed = 8

#Creates a rect and adds it to the platform list.
platform1 = Platform(920, 300, 70, 500, plat_speed)
platforms.add(platform1)
platform2 = Platform(920, -400, 70, 500, plat_speed)
platforms.add(platform2)

platform3 = Platform(1270, 350, 70, 500, plat_speed)
platforms.add(platform3)
platform4 = Platform(1270, -350, 70, 500, plat_speed)
platforms.add(platform4)

platform5 = Platform(1620, 415, 70, 500, plat_speed)
platforms.add(platform5)
platform6 = Platform(1620, -275, 70, 500, plat_speed)
platforms.add(platform6)

platform7 = Platform(1970, 300, 70, 500, plat_speed)
platforms.add(platform7)
platform8 = Platform(1970, -400, 70, 500, plat_speed)
platforms.add(platform8)

platform9 = Platform(2320, 400, 70, 500, plat_speed)
platforms.add(platform9)
platform10 = Platform(2320, -300, 70, 500, plat_speed)
platforms.add(platform10)

platform11 = Platform(2670, 300, 70, 500, plat_speed)
platforms.add(platform11)
platform12 = Platform(2670, -400, 70, 500, plat_speed)
platforms.add(platform12)


draw_group = pygame.sprite.Group()
for i in platforms:
    draw_group.add(i)



draw_group.add(platformBase)
draw_group.add(flashs)
#player's x and y's
x = 50
y = 50

#creates a player
player = Player(x, y, 55, 55, 10)

draw_group.add(player)

draw_group.clear(screen, background)
pop_background = pygame.image.load("background.png").convert_alpha()
pop_background = pygame.transform.scale(pop_background, (640, 460))
screen.blit(pop_background, (0,0))
draw_group.draw(screen)



def draw_text(display_string, font, surface, x_pos, y_pos, rgb):
    text_display = font.render(display_string, 1, rgb)
    surface.blit(text_display, (x_pos, y_pos))

main_clock = pygame.time.Clock()

#jumping
jump_state = 0
jump_timer = 0
grounded = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #Pressing Space To Jump
        if event.type == KEYDOWN:
            if alive == 0:
                if event.key == K_SPACE:
                    if jump_state == 0 or jump_state == 1:
                        jump_state = 1
                        jump_timer = 0
                        chan = pygame.mixer.find_channel(True)
                        chan.stop()
                        chan.set_volume(.2)
                        chan.play(bounceSound)
        if event.type == KEYUP:
            if alive == 1:
                if event.key == K_RETURN:
                    score = 0
                    platform1.rect.x = 920
                    platform2.rect.x = 920
                    platform3.rect.x = 1270
                    platform4.rect.x = 1270
                    platform5.rect.x = 1620
                    platform6.rect.x = 1620
                    platform7.rect.x = 1970
                    platform8.rect.x = 1970
                    platform9.rect.x = 2320
                    platform10.rect.x = 2320
                    platform11.rect.x = 2670
                    platform12.rect.x = 2670
                    plat_speed = 8
                    alive = 0
                    scored = False

    main_clock.tick(50)

#Stop player from going up

    if pygame.sprite.spritecollideany(player, TopPlatform) != None:
            sprite_rect = pygame.sprite.spritecollideany(player, TopPlatform).rect
            y = sprite_rect.bottom + 50
    

#sets the player's position above the Bottom platform
   
    if pygame.sprite.spritecollideany(player, BasePlatform) != None:
            sprite_rect = pygame.sprite.spritecollideany(player, BasePlatform).rect
            y = sprite_rect.top - 12
            grounded = True

#hitting the pipe things
    if pygame.sprite.spritecollideany(player, platforms) !=None:
        sprite_rect = pygame.sprite.spritecollideany(player, platforms).rect
        grounded = True
        alive = 1
        chan2 = pygame.mixer.find_channel(True)
        chan2.stop()
        chan2.set_volume(.2)
        chan2.play(hitSound)

#Jumping

    if jump_state == 0:
        if jump_timer == 0:
            if pygame.sprite.spritecollideany(player, platforms):
                grounded = True
            else:
                grounded = False
                y += num
    elif jump_state == 1:
        jump_timer += main_clock.get_time()
        grounded = False
        y -= num
        if jump_timer >= 275:
            jump_state = 2
    elif jump_state == 2:
        jump_timer = 0
        jump_state = 0

    #adding points
    for platform in platforms:
        if not platform.passed and platform.rect.x <= player.rect.x:
            score += .5
            platform.passed = True

    if score%10 == 0 and score > 0:
        plat_speed += .05
            
    
    for platform in platforms:
        #Sets the platform to the right side of the screen when it hits the left.
        if platform.rect.x <= 0 - 250:
            platform.rect.x = 1850
            platform.passed = False
            continue
        
        #Moves the platform to the left
        else:
            platform.rect.x -= plat_speed
            continue


    draw_group.clear(screen, background)
    screen.blit(pop_background, (0,0))
    draw_group.draw(screen)
    
    #moves the player down the screen if they are not moving
    player.rect.y = y - 45
    
    #Failed
    
    if alive == 0:
        draw_text('Score: %s' %(score), font, screen, 5, 5, (255,255,255))
        draw_text('High Score: %s' %(HighScore), font, screen, 450, 5, (255, 255, 255))
        
    else:
        draw_text('Game Over', font, screen, 180, 5, (255,255,255))
        draw_text('Press Enter to Play Again', font, screen, 180, 50, (255,255,255))
        draw_text('Score of: %s' %(score), font, screen, 180, 100, (255,255,255))
        draw_text('High Score: %s' %(HighScore), font, screen, 180, 150, (255, 255, 255))
        draw_text('All Time Low: -10 by Quantum', font, screen, 180, 200, (255, 255, 255))
        plat_speed = 0
        jump = 0
        finalScore = score
        #High Score
        if scored == False:
            with open('highScore', 'a') as file:
                file.write(str(finalScore) + "\n")
                scored = True

        
    pygame.display.update()
