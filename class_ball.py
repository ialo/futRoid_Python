import pygame


class Ball(object):
    def __init__(self, objPlayer):
        self.point = objPlayer.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = objPlayer.cos
        self.s = objPlayer.sin
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self, sw, sh):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True
