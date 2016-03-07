from algos.algorithms import Algorithm
from algos.jaimes_alg import Contador
from algos.process import Process
from draw.printer import *


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
        cont = Contador(w, h)
        algo = Algorithm(cont, data)
        try:
            algo.start()
        except Exception:
            "Something went wrong there, mate"


pro = First(1)
pro.start('infile')
drawer = Printer(pro.result)
drawer.show()
