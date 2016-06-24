from SA import *


def get_test():
    size = 30

    radio = 5
    r_vol = 100
    radios = [(radio, r_vol)]

    poros = [50, 30]

    for i in range(2):
        for poro in poros:
            print 'Start Poro %i' % poro
            algo = Algo('poros_%i' % poro, size, poro, radios)
            algo.main()
        print ' Done M%i %f' % (i, time.clock())


def get_porosidad():
    size = 80
    radio = 10
    r_vol = 100

    radios = [(radio, r_vol)]

    poros = [70, 50, 30]

    for i in range(4):
        for poro in poros:
            print 'Start Poro %i' % poro
            algo = Algo('poros_%i' % poro, size, poro, radios)
            algo.main()
        print ' Done M%i %f' % (i, time.clock())


def get_radios():
    size = 80
    poros = 60
    r_vol = 100

    radios = [15, 10, 5]

    for i in range(4):
        for r in radios:
            print 'Start Radio %i' % r
            radio2 = [(r, r_vol)]
            algo = Algo('radios_%i' % r, size, poros, radio2)
            algo.main()
        print ' Done M%i %f' % (i, time.clock())


def get_dist():
    size = 80
    poros = 60

    radios = [16, 12, 6]

    d1 = [50, 30, 20]
    d2 = [30, 50, 20]
    d3 = [30, 20, 50]
    dist = [d1, d2, d3]

    for i in range(4):
        for d in dist:
            radio2 = []
            for j in range(3):
                radio2.append((radios[j], d[j]))
            algo = Algo('dist_d_%i' % i, size, poros, radio2)
            algo.main()
        print ' Done M%i %f' % (i, time.clock())


def main():
    print 'Start %f' % time.clock()
    get_test()
    # get_porosidad()
    # get_radios()
    # get_dist()
    print 'Finish %f' % time.clock()


main()
