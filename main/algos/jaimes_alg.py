def opera(t, x, y):
    if t:
        return y
    else:
        return x ^ y


def norm(pdf, total):
    for i in pdf:
        if i is not 'total':
            for j in range(len(pdf[i])):
                pdf[i][j] /= total * 1.000
    return pdf


def setCont(limit, names):
    cont = {}
    for i in names:
        cont[i] = [0] * limit
    return cont

#   Define HEADER x bytes
#   0123 <-Type (cir, lin, etc) 4567 <-(size, width, height, etc)


class Contador(object):

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.d = min(width, height)

        # Info for faster revert ???
        self.pix = 0

        self.ones = 0
        self.zeros = 0

        line_names = ['f2s1', 'flp1', 'f2s0', 'flp0', 'total']
        self.line_ref = setCont(min(width, height), line_names)

        # Max Radius = 20
        circle_names = ['PS1', 'PS0', 'total']
        self.circle_ref = setCont(min(width, height, 20), circle_names)

        self.line_result, self.circle_result = self.set_cont()

    def set_cont(self):
        l_name = ['f2s1', 'flp1', 'f2s0', 'flp0', 'total']
        c_name = ['PS1', 'PS0', 'total']

        line = setCont(min(self.w, self.h), l_name)
        circle = setCont(min(self.w, self.h, 20), c_name)
        return line, circle

    def errors(self, old, new):             # PDFs DIFF   --> To define...
        errors = 0
        for k in old.keys():
            if k is not 'total':
                for i in range(len(old[k])):
                    error = old[k][i] - new[k][i]
                    error *= error
                    errors += error
        errors /= len(old['total'])
        return errors

    def get_one(self, data):
        cont = 0
        for i in data:
            cont += i
        return 1.0 * cont / len(data), (len(data) - cont) * 1.0 / len(data)

    def set_one(self, data):
        cont = 0
        for p in data:
            cont += p.val
        #return cont, len(data) - cont
        return 1.0 * cont / len(data), (len(data) - cont) * 1.0 / len(data)

    def getImg(self, data):
        image = []
        for i in data:
            image.append(i.val)
        return image

    def corr(self, data, pix=1):
        self.pix = pix
        if pix == 1:
            l_res = self.lines(data, self.line_ref, pix)
            c_res = self.circles(data, self.circle_ref, pix)
        else:
            data = self.getImg(data)
            self.line_result, self.circle_result = self.set_cont()
            l_res = self.lines(data, self.line_result)
            c_res = self.sphere(data, self.circle_result)
        return norm(l_res, len(data)), norm(c_res, len(data))
        #return l_res, c_res

    def circles(self, pixels, cont, first=0):

        width = self.w
        height = self.h
        rmin = 0                        # Should be 2
        rmax = min(width, height, 20)

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
                            if min(x, radio2) == x:
                                valor = pixels[
                                    (r + r2) * width + c + c2
                                ]
                            else:
                                valor = 1
                            flag &= valor
                    cont['PS1'][radio] += flag
                    cont['total'][radio] += 1
        return cont

    def sphere(self, pixels, cont, first=0):

        width = self.w
        height = self.h
        depth = min(width, height)
        rmin = 0
        rmax = min(width, height, 20)
        rs = width
        ss = width * height

        maxD = depth - rmin
        maxH = height - rmin
        maxW = width - rmin

        for d in range(rmin, maxD):
            for r in range(rmin, maxH):
                for c in range(rmin, maxW):

                    first_pix = pixels[d * ss + r * rs + c]

                    #flag = 1  # Negado
                    flag = first_pix
                    cradio = min(
                        rmax, c, width - c - 1, r, height - r - 1, d, depth - d - 1
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
                                    if min(x, radio2) == x:
                                        valor = pixels[
                                            (d + d2) * ss +
                                            (r + r2) * rs +
                                            (c + c2)
                                            ]
                                    else:
                                        valor = 1
                                    flag &= valor
                        cont['PS1'][radio] += flag
                        cont['total'][radio] += 1
        return cont

    def lines(self, pixels, cont, first=0):
        if first == 0:
            dim = 3
            depth = self.d
        else:
            dim = 2
            depth = 1
        width = self.w
        height = self.h
        rs = width
        ss = width * height

        for d in range(depth):
            for r in range(height):
                for c in range(width):
                    first_pix = pixels[
                        d*ss + r*rs + c
                    ]

                    #   t --> Opera 't'
                    if first_pix == 1:      # Find '1'
                        a = 'f2s1'
                        b = 'flp1'
                        t = True
                    else:                   # Find '0'
                        a = 'f2s0'
                        b = 'flp0'
                        t = False

                    delta_offset = [1, rs, ss]
                    limit = [width - c, height - r, depth - d]

                    #   Accountant
                    first_pix = 1
                    for i in range(dim):
                        flag = 1
                        offset = d*ss + r*rs + c
                        for ls in range(limit[i]):
                            # All
                            cont['total'][ls] += 1
                            # F2
                            cont[a][ls] += opera(
                                t, first_pix, pixels[
                                    offset
                                ]
                            )
                            # FL-check
                            flag &= opera(
                                t, first_pix, pixels[
                                    offset
                                ]
                            )
                            # FL
                            cont[b][ls] += flag
                            offset += delta_offset[i]
        return cont
