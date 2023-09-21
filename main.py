import pygame
import math
import random
import class_player
import class_ball
import class_adversary

pygame.init()

DEFAULT_IMAGE_SIZE = (50, 50)

DEFAULT_IMAGE_SIZE_50 = (80, 80)

DEFAULT_IMAGE_SIZE_100 = (100, 100)

DEFAULT_IMAGE_SIZE_150 = (150, 150)

global escudo_player, sw, sh, objPlayer, adversario_50, adversario_100, adversario_150

sw = 768
sh = 1024

background = pygame.image.load('images/_campo.png')
background = pygame.transform.scale(background, (sw, sh))
ball = pygame.image.load('images/_bola.png')
ball = pygame.transform.scale(ball, (5, 5))
enemy = pygame.image.load('images/fifa.png')
enemy = pygame.transform.scale(enemy, DEFAULT_IMAGE_SIZE_150)
escudo_player = pygame.image.load('images/gremio-256.png')
escudo_player = pygame.transform.scale(escudo_player, DEFAULT_IMAGE_SIZE)
bonus = pygame.image.load('images/_bola_dourada.png')
adversario_50 = pygame.image.load('images/corinthians-256.png')
adversario_50 = pygame.transform.scale(adversario_50, DEFAULT_IMAGE_SIZE_50)
adversario_100 = pygame.image.load('images/flamengo-256.png')
adversario_100 = pygame.transform.scale(adversario_100, DEFAULT_IMAGE_SIZE_100)
adversario_150 = pygame.image.load('images/internacional-256.png')
adversario_150 = pygame.transform.scale(adversario_150, DEFAULT_IMAGE_SIZE_150)

shoot = pygame.mixer.Sound('audio/kick.mp3')
SoundHitL = pygame.mixer.Sound('audio/ballHit.mp3')
SoundHitS = pygame.mixer.Sound('audio/ballHit.mp3')
shoot.set_volume(.25)
SoundHitL.set_volume(.25)
SoundHitS.set_volume(.25)

pygame.display.set_caption('futRoid')
win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0
rapidFire = False
rfStart = -1
isSoundOn = True
highScore = 0


class Star(object):
    def __init__(self):
        self.img = bonus
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw // 2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Alien(object):
    def __init__(self):
        self.img = enemy
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw // 2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class AlienBullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 4
        self.dx, self.dy = objPlayer.x - self.x, objPlayer.y - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
        self.xv = self.dx * 5
        self.yv = self.dy * 5

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])


def redrawGameWindow():
    win.blit(background, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    livesText = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Play Again', 1, (255, 255, 255))
    scoreText = font.render('Score: ' + str(score), 1, (255, 255, 255))
    highScoreText = font.render('High Score: ' + str(highScore), 1, (255, 255, 255))

    objPlayer.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    for s in stars:
        s.draw(win)
    for a in aliens:
        a.draw(win)
    for b in alienBullets:
        b.draw(win)

    if rapidFire:
        pygame.draw.rect(win, (0, 0, 0), [sw // 2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [sw // 2 - 50, 20, 100 - 100 * (count - rfStart) / 500, 20])

    if gameover:
        win.blit(playAgainText, (sw // 2 - playAgainText.get_width() // 2, sh // 2 - playAgainText.get_height() // 2))

    win.blit(scoreText, (sw - scoreText.get_width() - 25, 25))
    win.blit(livesText, (25, 25))
    win.blit(highScoreText, (sw - highScoreText.get_width() - 25, 35 + scoreText.get_height()))
    pygame.display.update()


objPlayer = class_player.Player(escudo_player, sw, sh)
playerBullets = []
asteroids = []
count = 0
stars = []
aliens = []
alienBullets = []
run = True


while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1, 1, 1, 2, 2, 3])
            asteroids.append(class_adversary.Adversary(ran, adversario_50, adversario_100, adversario_150, sw, sh))
        if count % 1000 == 0:
            stars.append(Star())
        if count % 750 == 0:
            aliens.append(Alien())
        for i, a in enumerate(aliens):
            a.x += a.xv
            a.y += a.yv
            if a.x > sw + 150 or a.x + a.w < -100 or a.y > sh + 150 or a.y + a.h < -100:
                aliens.pop(i)
            if count % 160 == 0:
                alienBullets.append(AlienBullet(a.x + a.w // 2, a.y + a.h // 2))

            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        aliens.pop(i)
                        if isSoundOn:
                            SoundHitL.play()
                        score += 50
                        break

        for i, b in enumerate(alienBullets):
            b.x += b.xv
            b.y += b.yv
            if (
                    b.x >= objPlayer.x - objPlayer.w // 2 and b.x <= objPlayer.x + objPlayer.w // 2) or b.x + b.w >= objPlayer.x - objPlayer.w // 2 and b.x + b.w <= objPlayer.x + objPlayer.w // 2:
                if (
                        b.y >= objPlayer.y - objPlayer.h // 2 and b.y <= objPlayer.y + objPlayer.h // 2) or b.y + b.h >= objPlayer.y - objPlayer.h // 2 and b.y + b.h <= objPlayer.y + objPlayer.h // 2:
                    lives -= 1
                    alienBullets.pop(i)
                    break

        objPlayer.updateLocation(sw, sh)
        for b in playerBullets:
            b.move()
            if b.checkOffScreen(sw, sh):
                playerBullets.pop(playerBullets.index(b))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= objPlayer.x - objPlayer.w // 2 and a.x <= objPlayer.x + objPlayer.w // 2) or (
                    a.x + a.w <= objPlayer.x + objPlayer.w // 2 and a.x + a.w >= objPlayer.x - objPlayer.w // 2):
                if (a.y >= objPlayer.y - objPlayer.h // 2 and a.y <= objPlayer.y + objPlayer.h // 2) or (
                        a.y + a.h >= objPlayer.y - objPlayer.h // 2 and a.y + a.h <= objPlayer.y + objPlayer.h // 2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if isSoundOn:
                        SoundHitL.play()
                    break

            # bullet collision
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            if isSoundOn:
                                SoundHitL.play()
                            score += 10
                            na1 = class_adversary.Adversary(2, adversario_50, adversario_100, adversario_150, sw, sh)
                            na2 = class_adversary.Adversary(2, adversario_50, adversario_100, adversario_150, sw, sh)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            if isSoundOn:
                                SoundHitS.play()
                            score += 20
                            na1 = class_adversary.Adversary(1, adversario_50, adversario_100, adversario_150, sw, sh)
                            na2 = class_adversary.Adversary(1, adversario_50, adversario_100, adversario_150, sw, sh)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                            if isSoundOn:
                                SoundHitS.play()
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        break

        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break
            for b in playerBullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if lives <= 0:
            gameover = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            objPlayer.turnLeft()
        if keys[pygame.K_RIGHT]:
            objPlayer.turnRight()
        if keys[pygame.K_UP]:
            objPlayer.moveForward()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                playerBullets.append(class_ball.Ball(objPlayer))
                if isSoundOn:
                    shoot.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        playerBullets.append(class_ball.Ball(objPlayer))
                        if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_s:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                lives = 3
                asteroids.clear()
                aliens.clear()
                alienBullets.clear()
                stars.clear()
                if score > highScore:
                    highScore = score
                score = 0

    redrawGameWindow()
pygame.quit()
