from jaimes_alg import Contador
from rand import MyRandom
from process import Process


class Algo(Process):
    def __init__(self, img, w, h):        # img[]
        Process.__init__(self, 'SA')
        self.ref, self.ene = [None, None]

        self.tol = 0.0001
        self.max_ite = 1000
        self.ite = 0
        self.ite_fail = 0

        self.cont = Contador(w, h)
        self.rand = MyRandom(w, h)

        self.ref = self.cont.corr(img)
        self.one_ref = self.cont.get_one(img)
        self.one_res = (0, 0)
        self.ene = 0
        self.rand_img = self.rand.new()
        #self.rand_img, self.ene = self.pos_init()
        #self.pre_start()

    def change(self):
        if len(self.rand.i_change) > 0:
            pix = self.rand.i_change.pop()
            pix.val = 1
            return False
        else:
            return True

    def pre_start(self):
        self.rand_img = self.rand.circled(self.cont.circle_ref)
        self.ene = self.cont.corr(self.rand_img, 0)
        self.one_res = self.cont.set_one(self.rand_img)
        return False

    def refill(self):
        lmax = self.one_ref[0] * len(self.rand_img)
        lmin = self.one_res[0] * len(self.rand_img)
        self.rand.swap(int(lmax - lmin))
        self.one_res = self.cont.set_one(self.rand_img)
        self.ene = self.cont.corr(self.rand_img, 0)
        return False

    def sa_start(self):                                # Normal swapping (RANDOM)
        rand_img = self.rand_img
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

    def start(self, info=None):                                    # DPN swapping with threshold
        img = self.rand_img
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
