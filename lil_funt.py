import random


#           Basic IO

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


#               Randomness

#       New random image.... Pure RANDOM(0,1) ???
def start_random(size):
    values = []
    for i in range(size):
        values.append(random.randint(0, 1))
    return values


#       Check neighbours    ??Condition??
def random_pix(old):
    # for i in range(len(old)): old = old
    old = start_random(len(old))
    return old
