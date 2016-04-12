from algos.SA import *
from draw.printer import Printer

class First(Process):

    def start(self, source):
        io = self.io
        txt = io.pix_txt(source)
        size = len(txt)
        #   HEADER SIZE ???
        data = {
            'head': io.read_Data(txt, 0, 2),
            'data': io.read_Data(txt, 2, size)
        }
        w = data.get('head')[0]
        h = data.get('head')[1]
        data = data.get('data')
        printer = Printer(data, w, h)
        self.result = printer.result

pro = First(1)
pro.start('main/infile')