from jaimes_alg import Contador
from rand import MyRandom
from process import Process

import time


class Algo(Process):
    def __init__(self, img, w, h, d):        # img[]
        Process.__init__(self, 'SA')

        self.tol = 0.0001
        self.max_ite = 1000
        self.ite = 0
        self.ite_fail = 0

        self.cont = Contador(w, h, d)
        self.rand = MyRandom(w, h, d)

        self.ref = self.cont.corr(img)
        self.start_ref = {}
        self.one_ref = self.cont.get_one(img)
        self.one_res = (0, 0)
        self.ene = 0
        self.rand_img = self.rand.new()
        # self.rand_img, self.ene = self.pos_init()
        # self.pre_start()

    def change(self):
        changer, val = self.rand.get_change()
        if len(changer) > 0:
            if len(changer) is 1:
                print 'last: ' + str(time.clock())
                pix = changer.pop()
                pix.val = val
            for i in range(int(len(changer) / 2.0)):
                pix = changer.pop()
                pix.val = val
            return False
        else:
            return True

    def pre_start(self):
        self.rand.circled(self.cont.circle_ref)
        return False

    def refill(self):
        self.rand.count_zeros()
        self.one_res = self.cont.set_one(self.rand_img)
        lmax = self.one_ref[0] * len(self.rand_img)
        lmin = self.one_res[0] * len(self.rand_img)
        self.rand.f_swap(int(lmax - lmin))
        return False

    def after_fill(self):
        self.one_res = self.cont.set_one(self.rand_img)
        self.start_ref = self.cont.corr(self.cont.getImg(self.rand_img))
        return False

    def sa_start(self):                                # Normal swapping (RANDOM)
        self.ene = self.cont.corr(self.rand_img, 0)
        accept = True
        thrs = 0.1
        while self.ene > self.tol * 100:                     # Initial tolerance
            self.rand.simple_swap()
            n_ref = self.cont.corr(self.cont.getImg(self.rand_img))
            self.ene = self.cont.errors(self.ref, n_ref)
            if self.ene < thrs:
                thrs = self.ene
                accept = True
            else:
                accept = False
        return False

    def start(self, info=None):                                    # DPN swapping with threshold
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
