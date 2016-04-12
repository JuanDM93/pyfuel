from rand import MyRandom
from jaimes_alg import Contador
from process import Process

from main.draw.printer import *


class Algo(Process):
    def __init__(self, img, w, h):        # img[]
        Process.__init__(self, 'SA')
        self.tol = 0.0001
        self.max_ite = 1000

        self.cont = Contador(w, h)
        self.rand = MyRandom(w, h)

        self.ref = self.cont.corr(img)
        rand_img, self.ene = self.pre_start()

        self.ite = 0
        self.ite_fail = 0
        self.start(rand_img)

    # Normal swapping (RANDOM)
    def pre_start(self):
        rand_img = self.rand.new()
        rand_ref = self.cont.corr(rand_img, 0)
        ene = self.cont.errors(self.ref, rand_ref)
        while ene > self.tol * 100:                     # Initial tolerance
            n_img, pix = self.rand.simple_swap()
            rand_ref = self.cont.corr(n_img, pix)
            n_ene = self.cont.errors(self.ref, rand_ref)
            if n_ene < ene:
                rand_img = n_img
                ene = n_ene
        return rand_img, ene

    # DPN swapping with threshold
    def start(self, img):
        ini_ite = 0
        p = 0.5                                         # More reading
        delta_e = []
        while ene > self.tol and self.ite_fail < self.max_ite:
            s_img, pix = self.rand.swap(img)            # Swap worst pixel
            s_ref = self.cont.corr(s_img, pix)
            n_ene = self.cont.errors(self.ref, s_ref)
            delta_e.append(n_ene - ene)
            if self.ite < ini_ite:                      # Need more reading... :(
                img = s_img
                if delta_e > 0:
                    self.note()
            else:
                if self.ite == ini_ite + 1:
                    ave = sum(delta_e) / len(delta_e)
                    e_th = p * ave                      # Need....... more... FR
                e_th = self.thres(e_th)
                if delta_e < e_th:
                    img = s_img
                    self.ite_fail = 0
                    ene = n_ene
                else:
                    self.ite_fail += 1
                    self.revert(img, pix)
            self.ite += 1
        return img

    # Threshold
    def thres(self, tres):
        tres += 1
        return tres

    # Back to previous img
    def revert(self, img, pix):
        img = img - pix
        return img

    # Note it down???
    def note(self):
        pass
