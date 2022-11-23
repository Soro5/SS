from pygame import *
from random import randint
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.rect.width = player_width
        self.rect.height = player_height

bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', (self.rect.centerx - 5), self.rect.top, 10, 18, -8)
        bullets.add(bullet)
    def dash(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= 100
        if keys[K_d]:
            self.rect.x += 100

# Подсчет пропущенных и убитых инопришеленцов
killed = 0
lost = 0

class Enemy(GameSprite):
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
        #возникновение в новой точке
            self.kill()
            lost += 1
            enemy = Enemy('ufo.png', randint(0, 435), randint(0, 50), 65, 65, randint(2, 5))
            enemies.add(enemy)

# Звуки для пули
fire = mixer.Sound("fire.ogg")

class Bullet(GameSprite):
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        
# Параметры игрового окна
win_width = 700
win_height = 500
display.set_caption("Shooter! Yay!")
window = display.set_mode((win_width, win_height))
clock = time.Clock()

# Спрайты
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
player = Player('rocket.png', 0, win_height - 65, 50, 50, 6)
enemy1 = Enemy('ufo.png', randint(0, 435), randint(0, 50), 65, 65, 2)
enemy2 = Enemy('ufo.png', randint(0, 435), randint(0, 50), 65, 65, 2)
enemy3 = Enemy('ufo.png', randint(0, 435), randint(0, 50), 65, 65, 2)
enemy4 = Enemy('ufo.png', randint(0, 435), randint(0, 50), 65, 65, 2)
enemy5 = Enemy('ufo.png', randint(0, 435), 0, 65, 65, 2)

enemies = sprite.Group()

enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)

font_end = font.Font(None, 60)
font_game = font.Font(None, 40)

win = 0

win_text = font_end.render("You win!", True, (0, 0, 0))
lose_text = font_end.render("You lost!", True, (0, 0, 0))

game = True
finish = False
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN and finish != True:
            if i.key == K_SPACE:
                player.fire()
            if i.key == K_DOWN:
                player.dash()

    if finish == False:
        window.blit(background, (0, 0))

        kill_text = font_game.render("Killed: " + str(killed), True, (255, 255, 255))
        lost_text = font_game.render("Lost: " + str(lost), True, (255, 255, 255))

        window.blit(kill_text, (5, 5))
        window.blit(lost_text, (5, 30))

        sprites_list = sprite.groupcollide(enemies, bullets, True, True)     
        for collide in sprites_list:
            killed += 1
            enemy = Enemy('ufo.png', randint(0, 435), randint(0, 50), 65, 65, randint(2, 5))
            enemies.add(enemy)

        if lost >= 15:
            win = False
            finish = True
        if killed >= 55:
            win = True
            finish = True

        player.update()
        enemies.update()
        bullets.update()
    else:
        if win == True:
            window.fill((255, 255, 255))
            window.blit(win_text, (win_height // 2, 250))
        else:
            window.fill((255, 255, 255))
            window.blit(win_text, (win_height // 2, 250))

    display.update()
    clock.tick(60)
quit()