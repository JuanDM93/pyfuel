from jaimes_alg import Contador
from lil_funt import *
from printer import Printer


class First(object):

    def __init__(self):
        self.runs = 0
        self.id = random.randint(0, 10)

    def start(self, source):
        txt = pix_txt(source)
        size = len(txt)
        #   HEADER SIZE ???
        data = {
            'head': read_Data(txt, 0, 2),
            'data': read_Data(txt, 2, size)
        }
        w = data.get('head')[0]
        h = data.get('head')[1]
        self.cont = Contador(w, h)
        data = data.get('data')

        #   Gen 0
        self.rand = start_random(w * h)
        self.lines = self.caracter(True, data)
        self.circles = self.caracter(False, data)       # Not sure if works
        self.error = self.gen()

    def caracter(self, t, data):
        if t:
            result = self.cont.lines(data)
        else:
            result = self.cont.circles(data)
        return result

    def gen(self):
        #   Random image generate
        self.rand = random_pix(self.rand)
        lines_rand = self.caracter(self.rand)
        circles_rand = self.caracter(self.rand)

        #   Error check
        e1 = self.cont.errors(self.lines, lines_rand)
        e2 = self.cont.errors(self.circles, circles_rand)
        error = e1 + e2
        return error / 2

    #   Evolve
    def process(self):
        #   Compare results
        x = 2
        runs = 0
        min_error = 1.0
        run_limit = 100

        while min_error < x and runs < run_limit:
            x = self.gen()
            runs += 1

        # Only testing...
        print runs

    #   Will print OpenGL
    def show(self):
        p = Printer()
        p.show()

    def close(self):
        result = 0
        writeOUT(result, 'outfile_%s' % self.id)


program = First()
program.start('infile')
program.process()
program.show()
