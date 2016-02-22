import random
from jaimes_alg import Contador


def read_Data(txt, start, end):
    data = []
    for i in range(start, end):
        data.append(int(txt[i]))
    return data


def pix_txt(path):
    with open(path) as f:
        txt = f.read()
    f.close()
    return txt


def writeOUT(data, path):
    out = open(path, 'w')
    for i in data:
        out.write(i)
    out.close()


def random_pix(size):
    values = []
    for i in range(size):
        values.append(random.randint(0, 1))
    return values

class First(object):

    def __init__(self):
        self.id = random.randint(0, 10)

    def readIN(self, source):
        self.txt = pix_txt(source)

    def start(self):
        size = len(self.txt)
        self.head = read_Data(self.txt, 0, 2)
        self.data = read_Data(self.txt, 2, size)


    def process(self):
        cont = Contador()
        self.lines = cont.lines(
            self.data, self.head[0], self.head[1]
        )

        #   Random image generate
        self.rand = random_pix(16)
        self.lines_rand = cont.lines(
                self.rand, self.head[0], self.head[1]
        )

        #   Compare results
        flag = True
        j = 0
        while flag:
            ### randomness
            for i in self.lines:
                if i != self.lines_rand[j]:
                    flag = False
                    break
                j += 1


    def close(self):
        writeOUT(self.lines, 'outfile_%s' % self.id)


program = First()
program.readIN('infile')
program.start()
program.process()
program.close()
