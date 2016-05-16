from algos.io_func import FileIO
from algos.printer import Printer
from algos.SA import Algo

import time
import cProfile


def main():
    io = FileIO()
    data, w, h = io.readAll('infile2.csv')
    # data, w, h = io.readAll('infile')
    d = min(w, h)

    start = time.clock()
    # Algo
    algo = Algo(
        2, 'algo',
        data, w, h, d
    )
    # algo.setDaemon(True)
    print 'Referenced ', time.clock() - start
    printer = Printer(
        # 1, 'draw',
        data, w, h, d, algo
    )

# cProfile.run('main()')
main()
