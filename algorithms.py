from master import *


class Algorithm(Process):

    def solve(self, info):
        for i in range(3):
            if (self.opt & i) == i:
                pass
            else:
                pass

        x = self.a_PSO(info)
        return x

    #   PSO, SA, PSO-SA, ETC...
    def a_PSO(self, info):
        x = info
        return x

    #   Simulated Annealing
    def a_SA(self):
        pass

    #---    ---#
    def a_PSO_SA(self):
        pass

    def get_Info(self, opt, x, mask):
        a = opt[x]
        return a | mask

    def set_Info(self, opt, x, mask):
        a = opt[x]
        return a & mask
