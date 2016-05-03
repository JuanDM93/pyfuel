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

    def __init__(self, w, h, d):
        self.w = w
        self.h = h
        self.d = d
        self.resets = 0
        self.starts = 1

        self.image = []
        self.i_change = []
        self.j_change = []

        self.ones, self.zeros = ([], [])

    def new(self):
        for i in range(self.d):
            for j in range(self.h):
                for k in range(self.w):
                    p = Pix(k, j, i, self.d)
                    self.image.append(p)
        return self.image

    def count_zeros(self):
        for p in self.image:
            if p.val is 0:
                self.zeros.append(p)
            else:
                self.ones.append(p)

    def circled(self, c_ref):
        cont0 = 0
        cont1 = 0

        lim = 0
        for i in c_ref['total']:
            if i is not 0:
                lim += 1

        for r in range(lim - 1, -1, -1):
            c = c_ref['PS1'][r] * c_ref['total'][r]
            if c > 0:
                for p in range(int(c - cont0)):
                    pix = random.choice(self.image)
                    self.circled_grow(pix, r)
                    cont1 += 1
                cont0 = cont1

    def circled_grow(self, pix, radius):
        self.i_change.append(pix)

        width = self.w
        height = self.h
        depth = self.d
        rmin = 1
        rmax = min(width, height, radius)
        rs = width
        ss = width * height
        d, r, c = (pix.z, pix.y, pix.x)

        cradio = min(
            rmax,
            c, self.w - c - 1,
            r, self.h - r - 1,
            d, depth - d - 1
        )

        for radio in range(rmin, cradio):
            radio2 = radio ** 2
            for d2 in range(-radio, radio + 1):
                for r2 in range(-radio, radio + 1):
                    for c2 in range(-radio, radio + 1):
                        x = r2 ** 2 + c2 ** 2 + d2 ** 2
                        if min(x, radio2) == x:
                            other = pix.pos + (d2 * ss) + (r2 * rs) + c2
                            change = self.image[other]
                            self.i_change.append(change)

    def get_change(self):
        if len(self.i_change) < 1 and len(self.j_change) < 1:
            return [], -1
        elif len(self.i_change) > len(self.j_change):
            return self.i_change, 1
        else:
            return self.j_change, 0

    def f_swap(self, cont):
        while cont > 0:
            pix = random.choice(self.zeros)
            self.zeros.remove(pix)
            self.ones.append(pix)
            self.i_change.append(pix)
            cont -= 1

    def simple_swap(self):              # Swap random pixels with different phase
        a = random.choice(self.zeros)
        self.zeros.remove(a)
        self.i_change.append(a)
        # a.val = 1
        b = random.choice(self.ones)
        self.ones.remove(b)
        self.j_change.append(b)
        # b.val = 0
        self.ones.append(a)
        self.zeros.append(b)

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


class Pix(object):
    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.pos = z*size*size + y*size + x
        self.val = 0
        # self.val = random.randint(0, 1)         # May find something better
        self.flag = 0                           # Diff Neighbours
        self.changes = 0

    def change(self):
        self.val = ~self.val + 2
        self.changes += 1

    def reset(self):
        self.changes = 0
        self.flag = 0

