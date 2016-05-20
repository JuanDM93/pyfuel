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

    def __init__(self, w, h, d):
        self.w = w
        self.h = h
        self.d = d
        self.rs = w
        self.ss = w * h
        self.resets = 0
        self.starts = 1

        self.image = []
        self.cords = []
        self.i_change = 0
        self.j_change = 0

        self.ones = []
        self.zeros = []

    def new(self):
        printed = []
        for i in range(self.d):
            for j in range(self.h):
                for k in range(self.w):
                    p = (i, j, k)
                    self.image.append(0)
                    self.cords.append(p)
                    if i < 1 or i > self.d - 2\
                            or j < 1 or j > self.h - 2\
                            or k < 1 or k > self.w - 2:
                        printed.append(p)
        return self.image, printed

    def get_change(self):
        if self.i_change < 1 and self.j_change < 1:
            return 0, -1, []
        elif self.i_change > self.j_change:
            return self.i_change, 1, self.ones
        else:
            return self.j_change, 0, self.zeros

    def circled(self, c_ref, n_ref):
        cont0 = 0
        cont1 = 0
        lim = len(c_ref[1]) - c_ref[1].count(0)

        for r in range(lim - 1, 0, -1):
            c = c_ref[1][r] * n_ref[r]
            for p in range(int(c - cont0)):
                pix = random.choice(self.cords)
                self.circled_grow(pix, r, cont1)
                cont1 += 1
            cont0 = cont1 * 5                   # Calculate better

    def circled_grow(self, pix, radius, contador):
        width = self.w
        height = self.h
        depth = self.d
        rs = self.rs
        ss = self.ss
        rmax = min(width, height, radius)
        rmin = 1
        d, r, c = pix
        pos = d * ss + r * rs + c
        self.image[pos] = 1

        cradio = min(
            rmax,
            c, width - c - 1,
            r, height - r - 1,
            d, depth - d - 1
        )

        for radio in range(rmin, cradio):
            radio2 = radio ** 2
            for d2 in range(-radio, radio + 1):
                for r2 in range(-radio, radio + 1):
                    for c2 in range(-radio, radio + 1):
                        x = r2 ** 2 + c2 ** 2 + d2 ** 2
                        if x <= radio2:
                            offset = (d2 * ss) + (r2 * rs) + c2
                            other = pos + offset
                            self.image[other] = 1

    def f_swap(self, cont):
        args = 1
        spots = range(len(self.cords))
        if cont < 0:
            args = 0
            cont *= -1
        while cont > 0:
            pos = random.choice(spots)
            val = self.image[pos]
            self.image[pos] = args
            if val is not args:
                cont -= 1

    def set_zeros(self):
        for i in range(len(self.image)):
            val = self.image[i]
            cord = self.cords[i]
            if val is 1:
                self.ones.append(cord)
            else:
                self.zeros.append(cord)

    def simple_swap(self):
        rs = self.w
        ss = self.w * self.h
        zero = random.choice(self.zeros)
        one = random.choice(self.ones)
        self.zeros.remove(zero)
        self.ones.append(zero)
        self.ones.remove(one)
        self.zeros.append(one)
        d, r, c = zero
        pos = d * ss + r * rs + c
        self.image[pos] = 1
        d, r, c = one
        pos = d * ss + r * rs + c
        self.image[pos] = 0

    def rand_pix(self):
        vec = self.checkN()
        for i in vec:
            i.change()

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

    def reset(self):
        self.image = self.best
        self.resets += 1
        for i in self.image:
            i.reset()