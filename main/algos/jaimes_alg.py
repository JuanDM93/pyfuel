import time


def norm(pdf):
    for i in pdf:
        if i is not 0:
            for j in range(len(pdf[i])):
                if pdf[0][j] is not 0:
                    pdf[i][j] /= pdf[0][j] * 1.000
    return pdf


def setCont(limit, names):
    cont = {}
    for i in names:
        cont[i] = [0] * limit
    return cont


class Contador(object):
    def __init__(self, width, height, depth):
        self.w = width
        self.h = height
        self.d = depth

        # Info for faster revert ???
        # self.pix = 0

        self.cords_ones = []
        self.cords_zeros = []
        self.line_ref, self.circle_ref = self.set_cont()
        self.line_result, self.circle_result = self.set_cont()

    def set_cont(self):
        l_name = [4, 3, 2, 1, 0]
        c_name = [1, 0]

        line = setCont(max(self.w, self.h), l_name)
        # Min or max??? --> cradio + 1?
        circle = setCont(min(self.w, self.h, 21), c_name)
        return line, circle

    def corr(self, data, pix=1):
        if pix is 0:
            start = time.clock()
            l_res = self.lines(data, self.line_ref)             # 1 secs
            print '    lines %s' % (time.clock() - start)
            start = time.clock()
            c_res = self.circles(data, self.circle_ref)         # 6-8 secs
            print '    circles %s' % (time.clock() - start)
        else:
            start = time.clock()
            self.line_result, self.circle_result = self.set_cont()
            l_res = self.new_lines(data, self.line_result)      # 4-5 secs
            print '    new lines %s' % (time.clock() - start)
            start = time.clock()
            c_res = self.sphere(data, self.circle_result)       # 20 mins
            print '    spheres %s' % (time.clock() - start)
        ones = data.count(1)
        zeros = len(data) - ones
        ones /= len(data) * 1.0
        zeros /= len(data) * 1.0
        l_res = norm(l_res)
        c_res = norm(c_res)
        return l_res, c_res, ones, zeros

    def errors(self, old, new):             # PDFs DIFF   --> To define...
        errors = 0
        for k in old.keys():
            if k is not 0:
                for i in range(len(old[k])):
                    error = old[k][i] - new[k][i]
                    error *= error
                    errors += error
        errors /= len(old[0])
        return errors

    def lines(self, pixels, cont):
        dim = 2
        width = self.w
        height = self.h
        rs = width

        for r in range(height):
            for c in range(width):
                first_pix = pixels[r * rs + c]

                delta_offset = [1, rs]
                limit = [width - c, height - r]

                if first_pix is 1:  # Find '1'
                    a = 4
                    b = 3
                    #   Accountant
                    for i in range(dim):
                        flag = 1
                        offset = r * rs + c
                        for ls in range(limit[i]):
                            # All
                            cont[0][ls] += 1
                            # F2
                            cont[a][ls] += pixels[offset]
                            # FL-check
                            flag &= pixels[offset]
                            # FL
                            cont[b][ls] += flag
                            offset += delta_offset[i]
                else:  # Find '0'
                    a = 2
                    b = 1
                    # Accountant
                    for i in range(dim):
                        flag = 1
                        offset = r * rs + c
                        for ls in range(limit[i]):
                            # All
                            cont[0][ls] += 1
                            # F2
                            cont[a][ls] += 1 ^ pixels[offset]
                            # FL-check
                            flag &= 1 ^ pixels[offset]
                            # FL
                            cont[b][ls] += flag
                            offset += delta_offset[i]
        return cont

    def circles(self, pixels, cont):
        width = self.w
        height = self.h
        rmin = 0                        # Should be 2
        rmax = min(width / 2, height / 2, 20)
        maxH = height - rmin
        maxW = width - rmin
        for r in range(rmin, maxH):
            for c in range(rmin, maxW):
                first_pix = pixels[r * width + c]
                if first_pix == 0:
                    continue
                flag = 1            # Negado
                cradio = min(
                    rmax, c, width - c - 1, r, height - r - 1
                )
                for radio in range(rmin, cradio + 1):
                    radio2 = radio ** 2
                    for r2 in range(-radio, radio + 1):
                        if flag == 0:
                            break
                        for c2 in range(-radio, radio + 1):
                            if flag == 0:
                                break
                            x = r2 ** 2 + c2 ** 2
                            if x <= radio2:
                                valor = pixels[
                                    (r + r2) * width + c + c2
                                ]
                            else:
                                valor = 1
                            flag &= valor
                    cont[1][radio] += flag
        for radio in range(rmin, rmax + 1):
            w2 = max(self.w - 2*radio, 0)
            h2 = max(self.h - 2*radio, 0)
            cont[0][radio] = w2*h2
        return cont

    def new_lines(self, pixels, cont):
        dim = 3
        depth = self.d

        width = self.w
        height = self.h
        rs = width
        ss = width * height

        delta = [ss, rs, 1, ss, rs]
        limit = [depth, height, width, depth, height]
        w_vector = [0] * max(depth, height, width)

        for d in range(dim):
            for i in range(limit[d]):
                for j in range(limit[d + 1]):
                    main_offset = i * delta[d] + j * delta[d + 1]
                    for k in range(limit[d + 2]):
                        w_vector[k] = pixels[main_offset + k * delta[d + 2]]
                    for k in range(limit[d + 2]):
                        first_pix = w_vector[k]
                        flag = 1
                        if first_pix is 1:  # Find '1'
                            a = 4
                            b = 3
                            for ls in range(limit[d]-k):
                                # All
                                cont[0][ls] += 1
                                # F2
                                cont[a][ls] += w_vector[k]
                                # FL-check
                                flag &= w_vector[k]
                                # FL
                                cont[b][ls] += flag
                                k += 1
                        else:  # Find '0'
                            a = 2
                            b = 1
                            for ls in range(limit[d]-k):
                                # All
                                cont[0][ls] += 1
                                # F2
                                cont[a][ls] += 1 ^ w_vector[k]
                                # FL-check
                                flag &= 1 ^ w_vector[k]
                                # FL
                                cont[b][ls] += flag
                                k += 1

        return cont

    def sphere(self, pixels, cont):
        width = self.w
        height = self.h
        depth = self.d
        ss = width * height
        rs = width
        rmin = 0
        rmax = min(width / 2, height / 2, 20)

        maxD = depth - rmin
        maxH = height - rmin
        maxW = width - rmin

        for d in range(rmin, maxD):
            for r in range(rmin, maxH):
                for c in range(rmin, maxW):
                    first_pix = pixels[d * ss + r * rs + c]
                    flag = first_pix
                    cradio = min(
                        rmax,
                        c, width - c - 1,
                        r, height - r - 1,
                        d, depth - d - 1
                    )
                    for radio in range(rmin, cradio + 1):
                        radio2 = radio ** 2
                        for d2 in range(-radio, radio + 1):
                            if flag == 0:
                                break
                            for r2 in range(-radio, radio + 1):
                                if flag == 0:
                                    break
                                for c2 in range(-radio, radio + 1):
                                    if flag == 0:
                                        break
                                    x = r2 ** 2 + c2 ** 2 + d2 ** 2
                                    if x <= radio2:
                                        valor = pixels[
                                            (d + d2) * ss +
                                            (r + r2) * rs +
                                            (c + c2)
                                        ]
                                    else:
                                        valor = 1
                                    flag &= valor
                        cont[1][radio] += flag
        for radio in range(rmin, rmax + 1):
            w2 = max(self.w - 2 * radio, 0)
            h2 = max(self.h - 2 * radio, 0)
            d2 = max(self.d - 2 * radio, 0)
            cont[0][radio] = w2 * h2 * d2
        return cont
