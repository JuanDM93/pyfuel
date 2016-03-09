from process import Process
from rand import MyRandom
import time


def norm(pdf):
    for i in pdf:
        if i is not 'total':
            for j in range(len(pdf[i])):
                pdf[i][j] /= pdf['total'][j] * 1.000
    return pdf


def message(data, start):
    return '%3s in %.4s sec E: %.8s' % \
           (data[0], time.time() - start, data[1])


class Algorithm(Process):

    def __init__(self, cont, data):
        Process.__init__(self, 'algo')
        w = cont.w
        h = cont.h
        self.cont = cont
        lines = self.cont.lines(data, 1)
        # circles = self.caracter(False, data)       # Not sure if works
        self.lines = norm(lines)
        # circles = norm(circles)

        self.time = time.time()

    def start(self, options):
        opt = options
        opt += self.runs

        #   Compare results
        min_error = 0.001
        run_limit = 10000

        # Gen 0
        self.rand = MyRandom(self.cont.w, self.cont.h)
        rand_L0 = self.caracter(True, self.rand.getImg())
        rand_L0 = norm(rand_L0)
        # rand_C0 = self.caracter(False, self.rand.getImg())
        # rand_C0 = norm(rand_C0)

        best1 = self.check_error(self.lines, rand_L0)
        # best2 = self.check_error(self.circles, rand_C0)

        x = best1   # + best2 / 2                       #  May be something different than '2'
        x_last = x
        while self.runs < run_limit:
            tm = [self.runs, x]
            if min_error < x:
                x = self.gen(x)
                if x_last > x:
                    x_last = x
                    print message(tm, self.time)
                self.runs += 1
            else:
                print "Well, IT may exist... " + \
                      message(tm, self.time)
                break
        else:
            print "God does not exist!!! " + \
                  message(tm, self.time)

    def gen(self, best):
        #   Random image generate
        self.rand.rand_pix()
        lines_rand = self.caracter(True, self.rand.getImg())
        lines_rand = norm(lines_rand)
        # circles_rand = self.caracter(False, self.rand.getImg())
        # circles_rand = norm(circles_rand)

        #   Error check
        e1 = self.check_error(self.lines, lines_rand)
        # e2 = self.check_error(self.circles, circles_rand)

        error = e1  # + e2 / 2

        if self.rand.resets < 2:
            if best <= error:
                self.rand.reset()
                return best
            else:
                self.rand.go()
                return error
        else:
            self.rand.restart()
            return best

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
