from jaimes_alg import Contador
from lil_funt import *


class First(object):

    def __init__(self):
        self.runs = 0
        self.id = random.randint(0, 10)

    def start(self, source):
        txt = pix_txt(source)
        size = len(txt)
        data = {
            'head': read_Data(txt, 0, 2),
            'data': read_Data(txt, 2, size)
        }
        self.w = data.get('head')[0]
        self.h = data.get('head')[1]
        self.cont = Contador(self.w, self.h)
        data = data.get('data')

        #   Gen 0
        self.q3 = self.w * self.h
        self.rand = start_random(self.q3)
        self.lines = self.caracter(data)
        self.error = self.gen()

    def caracter(self, data):
        result = self.cont.lines(data)
        return result

    def gen(self):
        #   Random image generate
        self.rand = random_pix(self.rand)
        lines_rand = self.caracter(self.rand)

        #   Error check
        error = self.cont.errors(self.lines, lines_rand)
        return error

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

        print runs

    #   Will print OpenGL
    def show(self):
        pass

    def close(self):
        result = 0
        writeOUT(result, 'outfile_%s' % self.id)


program = First()
program.start('infile')
program.process()
program.show()
