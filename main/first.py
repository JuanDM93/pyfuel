from algos.SA import *
from main.algos.printer import Printer


class First(Process):
    def start(self, source):
        io = self.io
        data, w, h = io.readAll(source)

        printer = Printer(data, w, h)

pro = First(1)
# pro.start('infile')
pro.start('infile2.csv')
