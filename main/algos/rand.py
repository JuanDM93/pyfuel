#               Randomness
import random


def neigh(x, lim):
        neig = []
        if x > 0:
            neig.append(
                x - 1
            )
        if x < lim - 1:
            neig.append(
                x + 1
            )
        return neig


class MyRandom(object):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.d = w
        self.image = self.start_random()
        self.best = self.image

    def start_random(self):
        img3 = []
        for i in range(self.d):
            img2 = []
            for j in range(self.w):
                row = []
                for k in range(self.h):
                    p = Pix(i, j, k, self.w)
                    row.append(p)
                img2.append(row)
            img3.append(img2)
        return img3

    def rand_pix(self):
        self.checkN()
        for i in self.image:
            for j in i:
                for k in j:
                    k.change()

    def checkN(self):
        for i in self.image:
            for j in i:
                for k in j:
                    nx = neigh(k.x, self.w)
                    ny = neigh(k.y, self.h)
                    nz = neigh(k.z, self.d)
                    for l in nx:
                        for m in ny:
                            for n in nz:
                                k.flag += k.val ^ self.image[l][m][n].val

    def reset(self):
        self.image = self.best
        for i in self.image:
            for j in i:
                for k in j:
                    k.reset()

    def getImg(self):
        image = []
        for i in self.image:
            for j in i:
                for k in j:
                    image.append(k.val)
        return image



class Pix(object):
    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.pos = z*size*size + x*size + y
        self.val = random.randint(0, 1)
        self.flag = 0
        self.changes = 0

    def change(self):
        if self.flag and self.changes < 3:
            self.val = ~self.val + 2
            self.changes += 1

    def reset(self):
        self.changes = 1

