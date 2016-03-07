from process import Process
from rand import MyRandom


class Algorithm(Process):

    def __init__(self, cont, data):
        self.cont = cont
        w = cont.gW
        h = cont.gH
        # Gen 0
        self.rand = MyRandom(w, h)
        self.lines = self.caracter(True, data)
        self.circles = self.caracter(False, data)       # Not sure if works

    def start(self):
        #   Compare results
        x = 2
        runs = 0
        min_error = 1.0
        run_limit = 100

        while min_error < x and runs < run_limit:
            x = self.gen()
            # Temperature???
            if runs > 70:
                runs = 30
            runs += 1

    def gen(self):
        #   Random image generate
        rand = self.rand.rand_pix()
        lines_rand = self.caracter(True, rand)
        circles_rand = self.caracter(False, rand)

        #   Error check
        e1 = self.cont.errors(self.lines, lines_rand)
        e2 = self.cont.errors(self.circles, circles_rand)
        error = e1 + e2
        return error / 2

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
