import pygame
import random

import class_bonus
import class_enemy
import class_enemyBullet
import class_player
import class_ball
import class_adversary

pygame.init()

DEFAULT_IMAGE_SIZE = (50, 50)

DEFAULT_IMAGE_SIZE_P = (50, 50)

DEFAULT_IMAGE_SIZE_M = (60, 60)

DEFAULT_IMAGE_SIZE_G = (70, 70)

global escudo_player, sw, sh, objPlayer, adversario_p, adversario_m, adversario_g, enemy, bonus

sw = 768
sh = 1024

background = pygame.image.load('images/_campo.png')
background = pygame.transform.scale(background, (sw, sh))
ball = pygame.image.load('images/_bola.png')
ball = pygame.transform.scale(ball, (5, 5))
enemy = pygame.image.load('images/fifa.png')
enemy = pygame.transform.scale(enemy, DEFAULT_IMAGE_SIZE_G)
escudo_player = pygame.image.load('images/gremio-256.png')
escudo_player = pygame.transform.scale(escudo_player, DEFAULT_IMAGE_SIZE)
bonus = pygame.image.load('images/_bola_dourada.png')
bonus = pygame.transform.scale(bonus, DEFAULT_IMAGE_SIZE)
adversario_p = pygame.image.load('images/corinthians-256.png')
adversario_p = pygame.transform.scale(adversario_p, DEFAULT_IMAGE_SIZE_P)
adversario_m = pygame.image.load('images/flamengo-256.png')
adversario_m = pygame.transform.scale(adversario_m, DEFAULT_IMAGE_SIZE_M)
adversario_g = pygame.image.load('images/internacional-256.png')
adversario_g = pygame.transform.scale(adversario_g, DEFAULT_IMAGE_SIZE_G)

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


def redrawGameWindow():
    win.blit(background, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    livesText = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Play Again', 1, (255, 255, 255))
    scoreText = font.render('Score: ' + str(score), 1, (255, 255, 255))
    highScoreText = font.render('High Score: ' + str(highScore), 1, (255, 255, 255))

    objPlayer.draw(win)
    for a in adversary_list:
        a.draw(win)
    for b in playerBalls_list:
        b.draw(win)
    for s in bonus_list:
        s.draw(win)
    for a in enemy_list:
        a.draw(win)
    for b in enemyBullets_list:
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
playerBalls_list = []
adversary_list = []
count = 0

bonus_list = []
# bonus_list.append(class_bonus.Bonus(bonus, sh, sw))

enemy_list = []
# enemy_list.append(class_enemy.Enemy(enemy, sh, sw))

enemyBullets_list = []
run = True

while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1, 1, 1, 2, 2, 3])
            adversary_list.append(class_adversary.Adversary(ran, adversario_p, adversario_m, adversario_g, sw, sh))
        if count % 1000 == 0:
            bonus_list.append(class_bonus.Bonus(bonus, sh, sw))
        # if count % 750 == 0:
        # class_enemy.Enemy(enemy, sh, sw
        for i, a in enumerate(enemy_list):
            a.x += a.xv
            a.y += a.yv
            if a.x > sw + a.w or a.x + a.w < -100 or a.y > sh + 150 or a.y + a.h < -100:
                enemy_list.pop(i)
            if count % 160 == 0:
                enemyBullets_list.append(class_enemyBullet.EnemyBullet(a.x + a.w // 2, a.y + a.h // 2, objPlayer))
            for b in playerBalls_list:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        enemy_list.pop(i)
                        if isSoundOn:
                            SoundHitL.play()
                        score += 50
                        break

        for i, b in enumerate(enemyBullets_list):
            b.x += b.xv
            b.y += b.yv
            if (
                    b.x >= objPlayer.x - objPlayer.w // 2 and b.x <= objPlayer.x + objPlayer.w // 2) or b.x + b.w >= objPlayer.x - objPlayer.w // 2 and b.x + b.w <= objPlayer.x + objPlayer.w // 2:
                if (
                        b.y >= objPlayer.y - objPlayer.h // 2 and b.y <= objPlayer.y + objPlayer.h // 2) or b.y + b.h >= objPlayer.y - objPlayer.h // 2 and b.y + b.h <= objPlayer.y + objPlayer.h // 2:
                    lives -= 1
                    enemyBullets_list.pop(i)
                    break

        objPlayer.updateLocation(sw, sh)
        for b in playerBalls_list:
            b.move()
            if b.checkOffScreen(sw, sh):
                playerBalls_list.pop(playerBalls_list.index(b))

        for a in adversary_list:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= objPlayer.x - objPlayer.w // 2 and a.x <= objPlayer.x + objPlayer.w // 2) or (
                    a.x + a.w <= objPlayer.x + objPlayer.w // 2 and a.x + a.w >= objPlayer.x - objPlayer.w // 2):
                if (a.y >= objPlayer.y - objPlayer.h // 2 and a.y <= objPlayer.y + objPlayer.h // 2) or (
                        a.y + a.h >= objPlayer.y - objPlayer.h // 2 and a.y + a.h <= objPlayer.y + objPlayer.h // 2):
                    lives -= 1
                    adversary_list.pop(adversary_list.index(a))
                    if isSoundOn:
                        SoundHitL.play()
                    break

            # bullet collision
            for b in playerBalls_list:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            if isSoundOn:
                                SoundHitL.play()
                            score += 10
                            na1 = class_adversary.Adversary(2, adversario_p, adversario_m, adversario_g, sw, sh)
                            na2 = class_adversary.Adversary(2, adversario_p, adversario_m, adversario_g, sw, sh)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            adversary_list.append(na1)
                            adversary_list.append(na2)
                        elif a.rank == 2:
                            if isSoundOn:
                                SoundHitS.play()
                            score += 20
                            na1 = class_adversary.Adversary(1, adversario_p, adversario_m, adversario_g, sw, sh)
                            na2 = class_adversary.Adversary(1, adversario_p, adversario_m, adversario_g, sw, sh)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            adversary_list.append(na1)
                            adversary_list.append(na2)
                        else:
                            score += 30
                            if isSoundOn:
                                SoundHitS.play()
                        adversary_list.pop(adversary_list.index(a))
                        playerBalls_list.pop(playerBalls_list.index(b))
                        break

        for s in bonus_list:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                bonus_list.pop(bonus_list.index(s))
                break
            for b in playerBalls_list:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        bonus_list.pop(bonus_list.index(s))
                        playerBalls_list.pop(playerBalls_list.index(b))
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
                playerBalls_list.append(class_ball.Ball(objPlayer))
                if isSoundOn:
                    shoot.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        playerBalls_list.append(class_ball.Ball(objPlayer))
                        if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_s:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                lives = 3
                adversary_list.clear()
                enemy_list.clear()
                enemyBullets_list.clear()
                bonus_list.clear()
                if score > highScore:
                    highScore = score
                score = 0

    redrawGameWindow()
pygame.quit()
