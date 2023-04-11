from pygame import *
from random import randint 
from time import time as timer

img_enemy = "ufo.png"
img_back = "galaxy.jpg"
img_hero = "asteroid.png"
img_bullet = "bullet.png"
img_rocket = "rocket.png"

score = 0
lost = 0
max_lost = 3
goal = 10

#! 
#TODO 
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load(img_back), (win_width, win_height))
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None,80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial',36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed,):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 25, -35)
        bullets.add(bullet)

class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


player = Player(img_hero, 5, win_height - 100, 80, 100, 80)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -90, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

rockets = sprite.Group()
for i in range(1,4):
    rocket = Enemy(img_rocket, randint(80, win_width - 80), -90, 70, 100, randint(1,5))
    rockets.add(rocket)

game = True
real_time = False
num_fire = 0
finish = False


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True
    
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text,(10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(10, 50))

        player.update()
        monsters.update()
        bullets.update()
        rockets.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        rockets.draw(window)

        if real_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                real_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -90, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        display.update() 
    


    time.delay(50)