#               Randomness
import random


def neigh(n, x, lim):
        vec = []
        if x > 0:
            vec.append(-1)
        if x < lim - 1:
            vec.append(1)
        neig = []
        for v in vec:
            neig.append(x + v)

        return neig


class MyRandom(object):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.d = max(w, h)
        self.image = self.start_random()
        self.best = self.image

    def start_random(self):
        img3 = []
        for i in range(self.d):
            for j in range(self.h):
                for k in range(self.w):
                    p = Pix(k, j, i, self.w)
                    img3.append(p)
        return img3

    def rand_pix(self):
        self.checkN()
        for i in self.image:
            i.change()

    def checkN(self):
        for i in self.image:
            rs = self.w
            ss = self.w * self.h
            off = [1, rs, ss]
            pos = [i.x, i.y, i.z]
            lim = [self.w, self.h, self.d]
            for n in range(3):
                vec = neigh(n, pos[n], lim[n])
                for v in vec:
                    other = i.pos + (v - pos[n])*off[n]
                    val = self.image[other].val
                    i.flag += i.val ^ val

    def go(self):
        self.best = self.image

    def reset(self):
        self.image = self.best
        for i in self.image:
            i.reset()

    def getImg(self):
        image = []
        for i in self.image:
            image.append(i.val)
        return image


class Pix(object):
    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.pos = z*size*size + y*size + x
        self.val = random.randint(0, 1)
        self.flag = 0
        self.changes = 0

    def change(self):
        if self.flag > 3 > self.changes:
            self.val = ~self.val + 2
            self.changes += 1

    def reset(self):
        self.changes = 0

