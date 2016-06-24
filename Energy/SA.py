from rand import *
import csv


class Algo(object):
    def __init__(self, name, size, vol, radios):
        # self.status = 'Startin'
        self.name = name
        self.cuenta = 0
        self.calores = []
        self.temp = [[size * [400] for i in range(size)] for i in range(size)]
        self.con = [[size * [.001] for i in range(size)] for i in range(size)]

        self.size = size
        self.vol = vol * .01
        self.vct = size**3 * self.vol

        self.radios = radios

        self.rand = MyRandom(size)
        # TODO is val always started with 0??
        self.val = 0
        self.rand_img = self.rand.new(self.val)

    def main(self):
        n_ones = 0
        all_vct = 0
        for r in self.radios:
            if r[1] is not 0:
                # self.status = 'Growin %s' % (self.vct - n_ones)
                r_vct = self.vct * r[1] * .01
                all_vct += r_vct
                n_ones += self.rand.circled(r_vct, r[0], self.val)
        print '     Grown %s' % time.clock()
        # self.status = 'Fillin'
        self.rand.f_swap(int(all_vct - n_ones))
        print '     Filled %s' % time.clock()
        # self.first = True

        # self.second = True
        # self.status = 'Pre-heating'
        finished = True
        temp_h = 400
        temp_low = 300

        z = self.size

        for k in range(z):
            for j in range(z):
                for i in range(z):
                    pos = k * z**2 + j * z + i
                    if self.rand_img[pos] is not 0:
                        self.con[i][j][k] = 100

        # Cask
        # for i in range(size):
        #     for j in range(size):
        #         self.con[0][i][j] = 100
        #         self.con[i][0][j] = 100
        #         self.con[i][j][0] = 100
        #         self.con[size - 1][i][j] = 100
        #         self.con[i][size - 1][j] = 100
        #         self.con[i][j][size - 1] = 100

        t_init = temp_h
        for k in range(z):
            for j in range(z):
                for i in range(z):
                    self.temp[i][j][k] = t_init
            t_init -= ((temp_h - temp_low) / z)

        con = self.con
        old_temp = self.temp
        new_temp = [[z * [0] for i in range(z)] for i in range(z)]

        front_bottom = temp_h
        front_top = temp_low

        converge = 5e-2

        a = [0] * z
        b = [0] * z
        c = [0] * z
        d = [0] * z

        p = [0] * z
        q = [0] * z

        tn, ts, tb, tt, te, tw = 0, 0, 0, 0, 0, 0

        print '     Prepared %s' % time.clock()

        while finished:
            self.cuenta += 1
            # self.status = 'Coolin: %s' % self.cuenta
            for k in range(z):
                for j in range(z):
                    for i in range(z):

                        if i is z - 1:
                            ke = 0
                        else:
                            ke = (2 * con[i][j][k] * con[i + 1][j][k]) / (con[i][j][k] + con[i + 1][j][k])
                            te = old_temp[i + 1][j][k]

                        if i is 0:
                            kw = 0
                        else:
                            kw = (2 * con[i][j][k] * con[i - 1][j][k]) / (con[i][j][k] + con[i - 1][j][k])
                            tw = old_temp[i - 1][j][k]

                        if j is z - 1:
                            kn = 0
                        else:
                            kn = (2 * con[i][j][k] * con[i][j + 1][k]) / (con[i][j][k] + con[i][j + 1][k])
                            tn = old_temp[i][j + 1][k]

                        if j is 0:
                            ks = 0
                        else:
                            ks = (2 * con[i][j][k] * con[i][j - 1][k]) / (con[i][j][k] + con[i][j - 1][k])
                            ts = old_temp[i][j - 1][k]

                        if k is z - 1:
                            kt = 4 * con[i][j][k]
                            tt = front_top
                        else:
                            kt = (2 * con[i][j][k] * con[i][j][k + 1]) / (con[i][j][k] + con[i][j][k + 1])
                            tt = old_temp[i][j][k + 1]

                        if k is 0:
                            kb = 4 * con[i][j][k]
                            tb = front_bottom
                        else:
                            kb = (2 * con[i][j][k] * con[i][j][k - 1]) / (con[i][j][k] + con[i][j][k - 1])
                            tb = old_temp[i][j][k - 1]

                        a[i] = ke + kw + kn + ks + kt + kb
                        b[i] = ke
                        c[i] = kw
                        d[i] = kn * tn + ks * ts + kt * tt + kb * tb

                        if i is 0:
                            p[i] = b[i] / a[i]
                            q[i] = d[i] / a[i]
                        else:
                            p[i] = b[i] / (a[i] - c[i] * p[i - 1])
                            c_1 = d[i] + c[i] * q[i - 1]
                            c_2 = a[i] - c[i] * p[i - 1]
                            q[i] = c_1 / c_2

                    new_temp[z - 1][j][k] = q[z - 1]
                    for i in range(z - 2, -1, -1):
                        new_temp[i][j][k] = p[i] * new_temp[i + 1][j][k] + q[i]

            # self.status = 'Deltas'
            delta_max = converge * .001
            for k in range(z):
                for j in range(z):
                    for i in range(z):
                        delta = new_temp[i][j][k] - old_temp[i][j][k]
                        if delta < 0:
                            delta *= -1.0
                        if delta > delta_max:
                            delta_max = delta
                        old_temp[i][j][k] = new_temp[i][j][k]

            if self.cuenta % 10 is 0:
                print '     Cuenta %i: %f t: %f' % (self.cuenta, delta_max, time.clock())

            # TODO or cuenta is 100, 1000...? deltas
            if (delta_max < converge) or (self.cuenta > 150):
                finished = not finished

        # self.status = 'Fluxes'
        print '     Writin %s' % time.clock()

        dx = 1
        flux = 0
        for k in range(z - 1):
            calor_flux_k = 0
            for j in range(z - 1):
                for i in range(z - 1):
                    kk = 2 * con[i][j][k] * con[i][j][k + 1] / (con[i][j][k] + con[i][j][k + 1])
                    d_temp = new_temp[i][j][k] - new_temp[i][j][k + 1]
                    calor_f = kk * d_temp * dx
                    calor_flux_k += calor_f
            flux += calor_flux_k
            self.calores.append(calor_flux_k)

        # self.status = 'Writin'
        # TODO save flux_k and plot
        calor = flux/len(self.calores)
        with open('promedios_%s.csv' % self.name, 'a') as result:
            wr = csv.writer(result)
            wr.writerow([calor])

        with open('planos_%s.csv' % self.name, 'a') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(self.calores)
