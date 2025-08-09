from pygame import *

init()
window = display.set_mode((1000, 800))
display.set_caption('Пинг-Понг')
background = transform.scale(image.load('dark.jpg'), (1000, 800))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_height, player_weight):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_weight, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): 
    def update(self):
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 650:
            self.rect.y += self.speed
    def dateup(self):
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 650:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_height, player_weight, player_speedY):
        super().__init__(player_image, player_x, player_y, player_speed, player_height, player_weight)
        self.speedY = player_speedY
    def ball_move(self):
        self.rect.x += self.speed
        self.rect.y += self.speedY

clock = time.Clock()
FPS = 60

player_1 = Player('PingPon.png', 870, 400, 5, 150, 25)
player_2 = Player('PingPon.png', 120, 400, 5, 150, 25)
ball = Ball('ball.png', 500, 400, 5, 50, 50, 5)

letter = font.SysFont('Comic Sans Ms', 60)
vinner_1 = letter.render('Игрок 1 победил!', True, (254, 161, 172))
vinner_2 = letter.render('Игрок 2 победил!', True, (104, 137, 179))

mixer.music.load('BackM.ogg')
mixer.music.set_volume(1)
mixer.music.play(loops = -1)
rebound = mixer.Sound("pong.wav")

points = 0
points_2 = 0

game = True
finish = False
while game:
    if finish != True:
        window.blit(background, (0, 0))
        keys_pressed = key.get_pressed()
        player_1.reset()
        player_1.update()
        player_2.reset()
        player_2.dateup()
        ball.reset()
        ball.ball_move()
        if ball.rect.x > 950:
            points_2 = points_2 + 1
            ball.rect.x = 500
            ball.rect.y = 400
        if ball.rect.x < 10:
            points = points + 1
            ball.rect.x = 500
            ball.rect.y = 400
        check = letter.render("Счет: " + str(points_2) + (':') + str(points), True, (255, 255, 255))
        window.blit(check, (430, 10))
        if sprite.collide_rect(player_1, ball):
            rebound.play()
            ball.speed *= -1
        if sprite.collide_rect(player_2, ball):
            rebound.play()
            ball.speed *= -1
        if ball.rect.y < 5:
            rebound.play()
            ball.speedY *= -1
        if ball.rect.y > 750:
            rebound.play()
            ball.speedY *= -1


        if points_2 >= 5:
            finish = True
            window.blit(vinner_1, (350, 350))
        if points >= 5:
            finish = True
            window.blit(vinner_2, (350, 350))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_r and finish == True:
                finish = False
                points = 0
                points_2 = 0
                ball.rect.x = 480
                ball.rect.y = 380

    clock.tick(FPS)
    display.update()