#               Randomness
import random


class MyRandom(object):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.image = self.start_random()

    def start_random(self):
        img2 = []
        for i in range(self.w):
            row = []
            for j in range(self.h):
                p = Pix(i, j, self.w)
                row.append(p)
            img2.append(row)
        return img2


    def rand_pix(self):
        image = []
        for i in self.image:
            for j in i:
                j.change()
                image.append(j.val)
        self.checkN()
        return image

    def checkN(self):
        x = self.w
        y = self.h
        img2 = self.image
        # Get Better...
        for i in img2:
            for j in i:
                neigh = []

                if j.x == 0:
                    neigh.append(
                        img2[j.x + 1][j.y]
                    )
                elif j.x == x - 1:
                    neigh.append(
                        img2[j.x - 1][j.y]
                    )
                else:
                    neigh.append(
                        img2[j.x + 1][j.y]
                    )
                    neigh.append(
                        img2[j.x - 1][j.y]
                    )

                if j.y == 0:
                    neigh.append(
                        img2[j.x][j.y + 1]
                    )
                elif j.y == y - 1:
                    neigh.append(
                        img2[j.x][j.y - 1]
                    )
                else:
                    neigh.append(
                        img2[j.x][j.y + 1]
                    )
                    neigh.append(
                        img2[j.x][j.y - 1]
                    )


                for n in neigh:
                    j.flag += j.val ^ n.val

        self.image = img2


class Pix(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.pos = x*size + y
        self.val = random.randint(0, 1)
        self.flag = 0
        self.changes = 0

    def change(self):
        if self.flag > 2 and self.changes < 3:
            self.val = ~self.val + 2
            self.changes += 1
