import rand

class alg_SA(object):
    def __init__(self):

        old_team = {}
        for i in range(16):
            if i % 2 != 0:
                old_team[i] = 0
            else:
                old_team[i] = 1

        s_team = {}
        for i in range(16):
            s_team[i] = rand.randint(0, 1)

        for k in range(16):
            s = rand.choice(s_team.keys())
            v = s_team.get(s)
            s['v'] += 1

    def start(self):
        pass


class particle():
    def __init__(self):
        self.state = 0
        self.neigh = []


a = alg_SA()
a.start()


