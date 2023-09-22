import random
class Adversary(object):
    def __init__(self, rank, adversary_p, adversary_m, adversary_g, sw, sh):
        self.rank = rank
        if self.rank == 1:
            self.image = adversary_p
            self.w = 50
            self.h = 50
        elif self.rank == 2:
            self.image = adversary_m
            self.w = 60
            self.h = 60
        else:
            self.image = adversary_g
            self.w = 70
            self.h = 70

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
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
