import random
import time


class MyRandom(object):
    def __init__(self, w):
        self.w = w
        self.h = w
        self.d = w
        self.rs = w
        self.ss = w ** 2
        self.resets = 0
        self.starts = 1

        self.image = []
        self.cords = []
        self.cask = []
        self.used = []

        self.ones = []
        self.zeros = []

    def new(self, val):
        size = self.w
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    p = (i, j, k)
                    self.cords.append(p)
                    self.image.append(val)
        return self.image

    def casked(self, radio):
        # TODO flush ifses
        cask = []
        # radio += 1
        dif = self.w - radio
        for p in self.cords:
            i, j, k = p
            if (p not in self.used) and (radio <= i < dif) and (radio <= j < dif) and (radio <= k < dif):
                cask.append(p)
        return cask

    def circled(self, r_vct, radio, val):
        cont = 0
        vol = 0
        area = 1.3 * 3.14 * radio**3
        val = ~val + 2
        cask = self.casked(radio)

        while True:
            pix = random.choice(cask)
            cask.remove(pix)
            self.used.append(pix)
            vol += int(1.33 * 3.14 * radio**3)
            result = self.circled_grow3(pix, radio, val)
            cont += result
            # time.sleep(.001)
            if cont > r_vct - area:
                break
        return cont

    def circled_grow3(self, pix, radio, val):
        rs = self.rs
        ss = self.ss
        d, r, c = pix
        pos = d * ss + r * rs + c
        if self.image[pos] is val:
            cont = 0
        else:
            self.image[pos] = val
            cont = 1

        radio2 = radio ** 2
        for d2 in range(-radio, radio + 1):
            for r2 in range(-radio, radio + 1):
                for c2 in range(-radio, radio + 1):
                    x = d2 ** 2 + r2 ** 2 + c2 ** 2
                    if x <= radio2:
                        offset = d2 * ss + r2 * rs + c2
                        other = pos + offset
                        if self.image[other] is not val:
                            self.image[other] = val
                            cont += 1
        return cont

    def f_swap(self, cont):
        spots = []
        rs = self.rs
        ss = self.ss
        args = 1.0
        up = True
        if cont < 0:
            cont *= -1
            args = .0
            up = False
        while cont > 0:
            if len(spots) < 1:
                spots = self.getNeighs3(up)
                if args > .3:
                    args -= .3
                else:
                    args += .3
                # time.sleep(.001)
            d, r, c = random.choice(spots)
            spots.remove((d, r, c))
            pos = d * ss + r * rs + c
            #  TODO Re-think this logic refill
            if up and self.image[pos] < args:
                cont -= 1
            elif not up and self.image[pos] > args:
                cont -= 1
            self.image[pos] = args

    def getNeighs3(self, up):

        pix_change = []
        rs = self.rs
        ss = self.ss
        off = [ss, rs, 1]
        lim = [self.d, self.h, self.w]
        for i in self.cords:
            flag = 0
            d, r, c = i
            pos = d * ss + r * rs + c
            #  TODO Re-think this logic neighs
            for n in range(3):
                vec = self.neigh(i[n], lim[n])
                for v in vec:
                    other = pos + (v - i[n]) * off[n]
                    if self.image[other] is not self.image[pos]:
                        if up and self.image[other] is 1:
                                flag += 1
                        elif not up and self.image[other] is 0:
                                flag += 1
            if flag > 0:
                pix_change.append(i)
        return pix_change

    def neigh(self, x, lim):
        # TODO get rid of this neighs
        vec = []
        neig = []
        if x > 0:
            vec.append(-1)
        if x < lim - 1:
            vec.append(1)
        for v in vec:
            neig.append(x + v)
        return neig
