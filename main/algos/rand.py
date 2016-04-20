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

        self.image = []

    def circled(self, c_ref):
        cont0 = 0
        cont1 = 0
        lim = len(c_ref['total'])
        for r in range(lim - 1, -1, -1):
            c = c_ref['PS1'][r] * c_ref['total'][r]
            if c > 0:
                for p in range(int(c - cont0)):
                    pix = random.choice(self.image)
                    self.circled_grow(pix, r)
                    cont1 += 1
                cont0 = cont1
        return self.image

    def circled_grow(self, pix, radius):
        pix.val = 1

        width = self.w
        height = self.h
        depth = min(width, height)
        rmin = 1
        rmax = min(width, height, radius)
        rs = width
        ss = width * height
        d, r, c = (pix.x, pix.y, pix.z)

        cradio = min(
            rmax,
            c, self.w - c - 1,
            r, self.h - r - 1,
            d, depth - d - 1
        )
        #cradio = radius

        for radio in range(rmin, cradio + 1):
            radio2 = radio ** 2
            for d2 in range(-radio, radio + 1):
                for r2 in range(-radio, radio + 1):
                    for c2 in range(-radio, radio + 1):
                        x = r2 ** 2 + c2 ** 2 + d2 ** 2
                        if min(x, radio2) == x:
                            other = pix.pos + (d2 * ss) + (r2 * rs) + c2
                            self.image[other].val = 1

        """
        for n in range(3):
            vec = neigh(pos[n], lim[n])
            for v in vec:
                other = pix.pos + (v - pos[n]) * off[n]
                self.image[other].val = 1

        """


    def new(self):
        img3 = []
        for i in range(self.d):
            for j in range(self.h):
                for k in range(self.w):
                    p = Pix(k, j, i, self.w)
                    img3.append(p)
        self.image = img3

    # Swap random pixels with different phase
    def simple_swap(self):
        a = random.choice(self.zeros)
        b = random.choice(self.ones)
        pix = [a, b]
        for i in pix:
            i.change()
        return self.getImg(), pix

    # Swap DPN based
    def swap(self, cont):
        while cont > 0:
            pix = random.choice(self.image)
            if pix.val is 0:
                pix.val = 1
                cont -= 1
        return self.image

    def rand_pix(self):
        vec = self.checkN()
        for i in vec:
            i.change()

    # Should it check EVERY pixel????
    def checkN(self):
        pix_change = []
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


class Pix(object):
    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.pos = z*size*size + y*size + x
        self.val = 0
        #self.val = random.randint(0, 1)         # May find something better
        self.flag = 0                           # Diff Neighbours
        self.changes = 0

    def change(self):
        self.val = ~self.val + 2
        self.changes += 1

    def reset(self):
        self.changes = 0
        self.flag = 0

