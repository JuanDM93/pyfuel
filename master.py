from algorithms import *


class Process(object):

    def __init__(self, opt):
        self.result
        self.info
        self.opt = opt
        if self.check_self():
            self.alg = Algorithm(opt)
        else:
            self.alg = lambda x: x     #    Function(opt)

    def check_self(self):
        if self.__class__ is Algorithm:
            return True
        else:
            return False

    def start(self, info):
        if self.check_self():
            self.result = self.alg.solve(info)
        else:
            self.result = self.alg(info)

    def set(self, args):        #   Argument counter
        value = 0x0
        mask = 0x1
        for i in args:
            if not i:
                value |= mask
            mask <<= 1
        return value

    def get(self):
        return self.result

    def a_Exmpl(self, info):
        x = Algorithm(info)     #       External Algorithms Module
        return x
