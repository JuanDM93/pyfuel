from process import Process
from rand import MyRandom
import time


def norm(pdf):
    for i in pdf:
        if i is not 'total':
            for j in range(len(pdf[i])):
                pdf[i][j] /= pdf['total'][j] * 1.000
    return pdf


class Algorithm(Process):

    def __init__(self, cont, data):
        Process.__init__(self, 'algo')
        w = cont.w
        h = cont.h
        self.cont = cont
        self.rand = MyRandom(w, h)
        lines = self.cont.lines(data, 1)
        # circles = self.caracter(False, data)       # Not sure if works
        self.lines = norm(lines)
        # circles = norm(circles)

    def start(self, options):
        opt = options
        opt += self.runs
        #   Compare results
        min_error = 0.00001
        run_limit = 1000

        # Gen 0
        line0 = self.caracter(True, self.rand.getImg())
        rand_L0 = norm(line0)
        # circle0 = self.caracter(False, self.rand.image)
        # rand_C0 = norm(circle0)

        best1 = self.check_error(self.lines, rand_L0)
        # best2 = self.check_error(self.circles, rand_C0)

        x = best1   # + best2 / 2
        while min_error < x and self.runs < run_limit:
            x = self.gen(x)
            self.runs += 1

            # Checking time
            if self.runs % 100 == 0:
                print time.time()

    def gen(self, best):
        #   Random image generate
        self.rand.rand_pix()
        lines_rand = self.caracter(True, self.rand.getImg())
        # circles_rand = self.caracter(False, self.rand.getImg())

        #   Error check
        e1 = self.check_error(self.lines, lines_rand)
        # e2 = self.check_error(self.circles, circles_rand)

        error = e1  # + e2 / 2

        if best < error:
            self.rand.reset()
            return best
        else:
            return error

    def check_error(self, original, rand):
        error = self.cont.errors(original, rand)
        return error

    def caracter(self, t, data):
        if t:
            result = self.cont.lines(data)
        else:
            result = self.cont.circles(data)
        return result

    # Nonsense
    def get_Info(self, opt, x, mask):
        a = opt[x]
        return a | mask

    def set_Info(self, opt, x, mask):
        a = opt[x]
        return a & mask
