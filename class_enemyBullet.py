import pygame
import math
class EnemyBullet(object):
    def __init__(self, x, y, objPlayer):
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

