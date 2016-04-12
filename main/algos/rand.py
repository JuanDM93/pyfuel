#               Randomness
import random


def neigh(x, lim):
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
        self.resets = 0
        self.starts = 1

        self.zeros = []
        self.ones = []

    def new(self):
        img3 = []
        zeros = []
        ones = []
        for i in range(self.d):
            for j in range(self.h):
                for k in range(self.w):
                    p = Pix(k, j, i, self.w)
                    img3.append(p)
                    if p.val == 0:
                        zeros.append(p)
                    else:
                        ones.append(p)
        self.zeros = zeros
        self.ones = ones
        self.image = img3
        return self.getImg()

    # Swap random pixels with different phase
    def simple_swap(self):
        a = random.choice(self.zeros)
        b = random.choice(self.ones)
        pix = [a, b]
        for i in pix:
            i.change()
        return self.getImg(), pix

    # Swap DPN based
    def swap(self, img):
        pix = 0
        pix += 1
        return img, pix

    def rand_pix(self):
        vec = self.checkN()
        for i in vec:
            i.change()

    # Should it check EVERY pixel????
    def checkN(self):
        pix_change =[]
        for i in self.image:
            rs = self.w
            ss = self.w * self.h
            off = [1, rs, ss]
            pos = [i.x, i.y, i.z]
            lim = [self.w, self.h, self.d]
            for n in range(3):
                vec = neigh(pos[n], lim[n])
                for v in vec:
                    other = i.pos + (v - pos[n])*off[n]
                    val = self.image[other].val
                    i.flag += i.val ^ val
            if i.flag > 3 and i.changes < 2:
                pix_change.append(i)
        return pix_change

    def go(self):
        self.best = self.image

    def reset(self):
        self.image = self.best
        self.resets += 1
        for i in self.image:
            i.reset()

    def restart(self):
        self.starts += 1
        self.resets = 0
        self.image = self.start_random()

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
        self.val = random.randint(0, 1)         # May find something better
        self.flag = 0                           # Diff Neighbours
        self.changes = 0

    def change(self):
        self.val = ~self.val + 2
        self.changes += 1

    def reset(self):
        self.changes = 0
        self.flag = 0

