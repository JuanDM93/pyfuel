import threading
import time

from algos.SA import *
from algos.printer import *
from algos.io_func import *
from algos.process import *

# data, w, h = FileIO().readAll('infile')
# d = min(w, h)
#
# algo = Algo(data, w, h, d)
#
# printer = Printer(data, w, h, d, algo)


class Foo(Process):
    def main(self):
        for i in range(10):
            print time.clock()
            time.sleep(1)


class Mock(Process):
    def __init__(self, threadID, name, process):
        Process.__init__(self, threadID, name)
        self.algo = process
        # self.algo.setDaemon(True)

    def main(self):
        self.algo.start()
        for i in range(5):
            print time.clock()
            time.sleep(2)



algo = Foo(0, 'algo')
algo.setDaemon(True)
printer = Mock(1, 'printer', algo)
# printer.setDaemon(True)
printer.start()
