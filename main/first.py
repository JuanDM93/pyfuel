from algos.io_func import FileIO
from algos.printer import Printer
from algos.SA import Algo

import time
import cProfile


def main():
    io = FileIO()
    # data, w, h = io.readAll('infile2.csv')          # 4 hrs
    data, w, h = io.readAll('infile3.csv')          # 30 min
    # For neighbours image bigger than 10 by size
    # data, w, h = io.readAll('infile')           # 1 sec
    d = min(w, h)

    start = time.clock()
    # Algo
    algo = Algo(
        2, 'algo',
        data, w, h, d
    )
    algo.setDaemon(True)
    print 'Referenced ', time.clock() - start
    printer = Printer(
        # 1, 'draw',
        data, w, h, d, algo
    )

# cProfile.run('main()')
main()
