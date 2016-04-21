from algos.SA import *
from main.algos.printer import Printer


class First(Process):
    def start(self, source):
        io = self.io
        txt = io.pix_txt(source)
        size = len(txt)
        #   HEADER SIZE ???
        # 0xfff 0xfff --> 0xfff(w)0xfff(h)data:01010101010
        data = {
            'head': io.read_Head(txt, 0, 10),
            'data': io.read_Data(txt, 10, size)
        }

        w = data.get('head')[0]
        h = data.get('head')[1]

        data = data.get('data')
        printer = Printer(data, w, h)

pro = First(1)
pro.start('main/infile')