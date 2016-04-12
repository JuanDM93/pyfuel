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
        algo = Algo(data, w, h)
        self.result = algo.result

pro = First(1)
pro.start('main/infile')
drawer = Printer()
drawer.show(pro.result)
