from jaimes_alg import Contador
from rand import MyRandom
from process import Process
import time


class Algo(Process):
    def __init__(
            self, threadID, name, img, w, h, d):
        Process.__init__(self, threadID, name)
    # def __init__(self, img, w, h, d):
        self.w, self.h, self.d = w, h, d

        self.tol = 0.0001
        self.max_ite = 1000
        self.ite = 0
        self.ite_fail = 0

        self.action = 0

        self.cont = Contador(w, h, d)
        self.rand = MyRandom(w, h, d)

        start = time.clock()
        self.rand_img, self.printed = self.rand.new()     # 2-3 secs
        print '  Newed %s' % (time.clock() - start)

        self.ref = self.cont.corr(img, 0)
        self.result = []

        self.start_res = []
        self.ene = 0

    def main(self):
        action = self.action
        draw = self.change()
        if draw:
            # start = time.clock()
            action += 1
            if action is 1:
                start = time.clock()
                flag = self.pre_start()
                print '  Pre_started!!!: %s' % (time.clock() - start)
            # elif action is 2:
                start = time.clock()
                flag = self.refill()
                print '  Refilled!!!: %s' % (time.clock() - start)
            # elif action is 3:
                start = time.clock()
                flag = self.after_fill()
                print '  Correlated!!!: %s' % (time.clock() - start)
                # return True
            elif action is 4:
                flag = self.sa_start()
                return True
            else:
                self.action = 0
        self.action = action
        return False

    def change(self):
        changer, val, cords = self.rand.get_change()
        if changer > 0:
            for i in range(changer):
                self.rand_img[cords[i]] = val
            print '  Last: %s' % (time.clock())
            return False
        else:
            return True

    def pre_start(self):
        lim = min(self.w, self.h, 21)
        cont = [0] * lim
        for radio in range(lim):
            w2 = max(self.w - 2 * radio, 0)
            h2 = max(self.h - 2 * radio, 0)
            d2 = max(self.d - 2 * radio, 0)
            cont[radio] = w2 * h2 * d2
        self.rand.circled(self.cont.circle_ref, cont)
        return False

    def refill(self):
        n_ones = self.rand_img.count(1)
        ones = self.ref[2] * len(self.rand_img)
        self.rand.f_swap(int(ones - n_ones))
        return False

    def after_fill(self):
        self.start_res = self.cont.corr(self.rand_img)
        return False

    def sa_start(self):                                # Normal swapping (RANDOM)
        f_ene = self.cont.errors(self.ref, self.start_res)
        self.ene = f_ene
        accept = True
        thrs = 0.1
        while self.ene > self.tol * 100:                     # Initial tolerance
            self.rand.simple_swap()
            n_ref = self.cont.corr(self.rand_img)
            self.ene = self.cont.errors(f_ene, n_ref)
            if self.ene < thrs:
                thrs = self.ene
                accept = True
            else:
                accept = False
        return False

    def pos_start(self, info=None):                                    # DPN swapping with threshold
        img = self.rand_img
        ini_ite = 10
        p = 0.8                                         # More reading
        delta_e = []
        e_th = 0
        while self.ene > self.tol and self.ite_fail < self.max_ite:
            s_img, pix = self.rand.simple_swap(img)            # Swap worst pixel
            s_ref = self.cont.corr(img, 0)
            n_ene = self.cont.errors(self.ref, s_ref)
            d_e = n_ene - self.ene
            delta_e.append(d_e)
            if self.ite < ini_ite:                      # Need more reading... :(
                img = s_img
                if delta_e > 0:
                    self.note()
            else:
                if self.ite == ini_ite + 1:
                    ave = sum(delta_e) / len(delta_e)
                    e_th = p * ave                      # Need....... more... FR
                e_th *= p
                if d_e < e_th:
                    img = s_img
                    self.ite_fail = 0
                    self.ene = n_ene
                else:
                    self.ite_fail += 1
                    self.revert(img, pix)
            self.ite += 1
            p = self.ite_fail - 1 / self.ite
            p *= p
        return img

    # Threshold
    def thres(self, tres):
        # tres += 1
        return tres

    # Back to previous img
    def revert(self, img, pix):
        img = img - pix
        return img

    # Note it down???
    def note(self):
        pass
