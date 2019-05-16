import pygame                   
from pygame.locals import *     
from sys import exit            
import time
from random import randint

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
  
pygame.init()                   
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], 0, 32) 
pygame.display.set_caption("Let's shoot! Have fun~")    
pygame.mixer.init()

score = 0
enemy_speed = 2
span = 10
freq = 30
level = '0'
life = 3
game_over = False

class Bullet(pygame.sprite.Sprite):

    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed = 8

    def update(self):
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            self.kill()
            

class Hero(pygame.sprite.Sprite):
    
    def __init__(self, hero_surface, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = hero_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 16
        self.is_hit = False 
        self.bullets1 = pygame.sprite.Group()

    def single_shoot(self, bullet1_surface):
        bullet1 = Bullet(bullet1_surface, self.rect.midtop)
        self.bullets1.add(bullet1)

    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
            
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y
            
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_surface, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = enemy_speed
        self.down_index = 0

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
    def set_speed(self, speed):
        self.speed = speed
        

def drawText(text, posx , posy, font, textHeight, 
             fontColor = (0,0,0), backgroudColor = (255,255,255)):
        fontObj = pygame.font.Font(font, textHeight)  
        textSurfaceObj = fontObj.render(text, True,fontColor,backgroudColor) 
        textRectObj = textSurfaceObj.get_rect()  
        textRectObj.center = (posx, posy)  
        screen.blit(textSurfaceObj, textRectObj)  
        
def countdown(times = 2):
    pygame.mixer.music.load('countdown.mp3')
    pygame.mixer.music.play(1, 0)
    while times > 0:
        screen.blit(background, (0, 0))
        drawText(str(times), 230, 310, 'figure.ttf', 96, (255, 95, 0), background_color)
        pygame.display.update()
        time.sleep(1)
        times -= 1
    screen.blit(background, (0, 0))
    drawText('GO!', 335, 450, 'figure.ttf', 96, (255, 95, 0), background_color)
    pygame.display.update()
    time.sleep(1)

def display_diff():
    if 0 <= score // 100 <= 5:
        span = 10 - score // 100
    elif 6 <= score // 100 <= 8:
        enemy_speed = (score - 1) * 0.5
    elif score // 100 == 9:
        freq = 20
    else:
        freq = 15
    level = str(score // 100)
    drawText('Difficulty: lv. ' + level, 70, 20, 'Oswald-Medium.ttf', 24, (255, 255, 0), background_color)

FRAME_RATE = 60

ANIMATE_CYCLE = 30

ticks = 0
clock = pygame.time.Clock()
offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}


main_page = pygame.image.load('mainpage04.jpg')
main_page_color1 = (250, 243, 232)
main_page_color2 = (251, 249, 236)

background = pygame.image.load('background02.png')
background_color = (0, 138, 138)

bullet_img = pygame.image.load('bullet.png')
bullet_rect = bullet_img.get_rect()
bullet_surface = bullet_img.subsurface(bullet_rect)

enemy1_img = pygame.image.load('enemy.png')
enemy1_rect = enemy1_img.get_rect()
enemy1_surface = enemy1_img.subsurface(enemy1_rect)
enemy1_down_surface = []
enemy1_down_surface.append(pygame.image.load('enemy_down1.png').subsurface(pygame.image.load('enemy_down1.png').get_rect()))
enemy1_down_surface.append(pygame.image.load('enemy_down2.png').subsurface(pygame.image.load('enemy_down2.png').get_rect()))
enemy1_down_surface.append(pygame.image.load('enemy_down3.png').subsurface(pygame.image.load('enemy_down3.png').get_rect()))
enemy1_down_surface.append(pygame.image.load('enemy_down4.png').subsurface(pygame.image.load('enemy_down4.png').get_rect()))

enemy2_img = pygame.image.load('enemy2.png')
enemy2_rect = enemy2_img.get_rect()
enemy2_surface = enemy2_img.subsurface(enemy2_rect)
enemy2_down_surface = []
enemy2_down_surface.append(pygame.image.load('enemy2_down1.png').subsurface(pygame.image.load('enemy2_down1.png').get_rect()))
enemy2_down_surface.append(pygame.image.load('enemy2_down2.png').subsurface(pygame.image.load('enemy2_down2.png').get_rect()))
enemy2_down_surface.append(pygame.image.load('enemy2_down3.png').subsurface(pygame.image.load('enemy2_down3.png').get_rect()))
enemy2_down_surface.append(pygame.image.load('enemy2_down4.png').subsurface(pygame.image.load('enemy2_down4.png').get_rect()))
enemy2_hit_surface = pygame.image.load('enemy2_hit.png').subsurface(pygame.image.load('enemy2_hit.png').get_rect())

hero_pos = (305, 850)

hero_img1 = pygame.image.load('player02.png')
hero_rect1 = hero_img1.get_rect()
hero_surface1 = hero_img1.subsurface(hero_rect1)



hero_img2 = pygame.image.load('player03.png')
hero_rect2 = hero_img2.get_rect()
hero_surface2 = hero_img2.subsurface(hero_rect2)

hero_surface = []
hero_surface.append(hero_surface1)
hero_surface.append(hero_surface2)

player_down_img = pygame.image.load('player_down.jpg')
player_down_rect = player_down_img.get_rect()
player_down_surface = player_down_img.subsurface(player_down_rect)

gameover_img = pygame.image.load('gameover02.png')
gameover_rect = gameover_img.get_rect()
gameover_surface = gameover_img.subsurface(gameover_rect)

pygame.mixer.music.load('Shout.wav')
pygame.mixer.music.play(-1, 0)
sound = pygame.mixer.Sound('explosion.wav')

while not game_over:
    
    clock.tick(FRAME_RATE)
    screen.blit(main_page, (0,0))
    drawText('JUST SHOOT IT!', 335, 100, 'BRUX.otf', 60, (200,122,150), main_page_color1)
    if ticks % 60 <= 30:
        drawText('Press any key to start!', 335, 450, 'Oswald-Medium.ttf', 48, (0,0,0), main_page_color2)
    ticks += 1
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pygame.mixer.music.stop()
            countdown()
            pygame.mixer.music.load('ajin.wav')
            pygame.mixer.music.play(-1, 0)
            hero = Hero(hero_surface[0], hero_pos)
            enemy1_group = pygame.sprite.Group()
            enemy1_down_group = pygame.sprite.Group()
            enemy2_group = pygame.sprite.Group()
            enemy2_0_group = pygame.sprite.Group()
            enemy2_down_group = pygame.sprite.Group()
            while True:
                clock.tick(FRAME_RATE)
                screen.blit(background, (0, 0))
                drawText('Score: ' + str(score), 600, 20, 'Oswald-Medium.ttf', 24, (255, 255, 0), background_color)
                drawText('Life: ' + str(life), 35, 900, 'Oswald-Medium.ttf', 24, (255, 255, 120), background_color)
                if ticks >= ANIMATE_CYCLE:
                    ticks = 0
                if hero.is_hit:
                    life -= 1
                    if life == 0:
                        sound.play()
                        hero.image = player_down_surface
                        time.sleep(1)
                        pygame.display.update()
                        game_over = True
                        pygame.mixer.music.stop()
                        sound.stop()
                        break
                    hero.is_hit = False
                else:
                    hero.image = hero_surface[ticks//(ANIMATE_CYCLE//2)]
                    
                if ticks % 60 == 0:
                    hero.single_shoot(bullet_surface)
                    sound1 = pygame.mixer.Sound('bullet.wav')
                    sound1.play()

                hero.bullets1.update()

                hero.bullets1.draw(screen)
                
                if ticks % freq == 0 and randint(0, span) != 1:
                    enemy = Enemy(enemy1_surface, [randint(0, SCREEN_WIDTH - enemy1_surface.get_width()), -enemy1_surface.get_height()])
                    enemy1_group.add(enemy)
                enemy1_group.update()
                enemy1_group.draw(screen)
                
                if ticks % freq == 0 and randint(0, span) == 1:
                    enemy = Enemy(enemy2_surface, [randint(0, SCREEN_WIDTH - enemy2_surface.get_width()), -enemy2_surface.get_height()])
                    enemy2_group.add(enemy)
                enemy2_group.update()
                enemy2_group.draw(screen)
                
                enemy1_down = pygame.sprite.groupcollide(enemy1_group, hero.bullets1, False, True)
                if enemy1_down:
                    sound.play()
                    score += 1
                    for sprite1 in enemy1_down.keys():
                        sprite1.kill()
                        enemy1_down_group.add(sprite1)
                        
                enemy2_down = pygame.sprite.groupcollide(enemy2_group, hero.bullets1, False, True)
                if enemy2_down:
                    for sprite2 in enemy2_down.keys():
                        sprite2.kill()
                    enemy = Enemy(enemy2_hit_surface, sprite2.rect.topleft)
                    enemy2_0_group.add(enemy)
                enemy2_0_group.update()
                enemy2_0_group.draw(screen)
                enemy2_0_down = pygame.sprite.groupcollide(enemy2_0_group, hero.bullets1, False, True)
                if enemy2_0_down:
                    sound.play()
                    score += 5
                    for sprite2_0 in enemy2_0_down.keys():
                        sprite2_0.kill()
                        enemy2_down_group.add(sprite2_0)
                
                for each1 in enemy1_down_group:
                    screen.blit(enemy1_down_surface[each1.down_index], each1.rect)
                    if ticks % (ANIMATE_CYCLE//2) == 0:
                        if each1.down_index < 3:
                            each1.down_index += 1
                        else:
                            enemy1_down_group.remove(each1)
                            
                for each2 in enemy2_down_group:
                    screen.blit(enemy2_down_surface[each2.down_index], each2.rect)
                    if ticks % (ANIMATE_CYCLE//2) == 0:
                        if each2.down_index < 3:
                            each2.down_index += 1
                        else:
                            enemy2_down_group.remove(each2)
                enemy1_down_list = pygame.sprite.spritecollide(hero, enemy1_group, True)
                enemy2_0_down_list = pygame.sprite.spritecollide(hero, enemy2_0_group, True)
                enemy2_down_list = pygame.sprite.spritecollide(hero, enemy2_group, True)
                if enemy1_down_list: 
                    enemy1_down_group.add(enemy1_down_list)
                    hero.is_hit = True
                if enemy2_down_list:
                    enemy2_down_group.add(enemy2_down_list)
                    hero.is_hit = True
                if enemy2_0_down_list:
                    enemy2_down_group.add(enemy2_0_down_list)
                    hero.is_hit = True
                    
                display_diff()
                
                screen.blit(hero.image, hero.rect)
                
                ticks += 1
                
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key in offset:
                            offset[event.key] = 3
                    elif event.type == pygame.KEYUP:
                        if event.key in offset:
                            offset[event.key] = 0
                    
                hero.move(offset)
               
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
screen.blit(gameover_surface, (0,0))
pygame.mixer.music.load('lost.wav')
pygame.mixer.music.play(-1, 0)           
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            myfile = open('data.txt', 'r')
            highest = myfile.readlines()[1]
            myfile.close()
            if score > int(highest):
                highest = score 
                print('New history!')
            myfile = open('data.txt', 'w')
            myfile.write(str(score) + '\n' + str(highest))
            myfile.close()
            print('This score:', score, 'Highest Score:', highest)
            exit()
