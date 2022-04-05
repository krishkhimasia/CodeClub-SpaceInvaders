import pygame
import math
import random
from pygame import mixer

# initialising pygame
pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('spaceback.png')

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# caption & icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('displayicon.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0
playerY_change=0

# enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(30)

# bullet
# ready - cant see bullet on screen
# fired - bullet currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX=playerX
bulletY=480
bulletX_change=0
bulletY_change=-1
bullet_state = "ready"

# score
score_value=0
font = pygame.font.Font('freesansbold.ttf', 32)

textX=10
textY=10

# GAME OVER text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text= over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # color of screen
    screen.fill((0, 0, 0))

    #background
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        #event to quit game
        if event.type == pygame.QUIT:
            running = False
    
        # check if keystroke is right/left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-0.8
                
            if event.key == pygame.K_RIGHT:
                playerX_change=0.8
                
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('bullet.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_change=0

    # BOUNDARIES            
    playerX+=playerX_change
    if playerX <=0:
        playerX=0
    elif playerX>=736:
        playerX=736    
    
    # enemy movement
    for i in range(num_of_enemies):
    # game over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
    
    
        enemyX[i]+=enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i]=0.5
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-0.5
            enemyY[i]+=enemyY_change[i]
        
        # collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i],enemyY[i], i)

    # bullet movement

    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state is "fired":
        fire_bullet(bulletX,bulletY)
        bulletY+=bulletY_change

    

    # calling player() to show it on screen
    
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()