import random
from io_func import *


def contador(args):        # Argument counter
        value = 0x0
        mask = 0x1
        for i in args:
            if not i:
                value |= mask
            mask <<= 1
        return value


class Process(object):

    def __init__(self, opt):
        self.opt = opt

        self.runs = 0
        self.id = random.randint(0, 10)
        self.io = FileIO()

        self.result = None
        self.info = None

    def start(self, info):
        self.result = info
        self.runs += 1

    def getState(self):
        print str(self.runs) + ' runs dude!'

    def close(self):
        self.io.writeOUT(self.result, 'outfile_%s' % self.id)
