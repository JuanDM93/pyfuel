def opera(t, x, y):
    if t:
        return y
    else:
        return x ^ y


def setCont(limit, names):
    cont = {}
    for i in names:
        cont[i] = [0] * limit
    return cont

#   Definir HEADER de x bytes para los archivos
#   0123 <-Tipo (cir, lin, etc) 4567 <-(size, width, height, etc)


class Contador(object):

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.d = 1

    def gH(self):
        return self.h

    def gW(self):
        return self.w

        #   PDFs DIFF
    def errors(self, old, new):         # Who is old?   Should be original & bestOld ??? Just Original?

        value = len(old)
        keys = []
        for i in old.keys():
            keys.append(i)
        errors = setCont(value, keys)

        error = 0
        for k in errors:
            if k is not 'total':
                for i in range(len(errors) - 1):
                    error = old[k][i] - new[k][i]
                    error *= error
                    errors[k][i] = error            # <---  May not be needed
                    errors['total'][i] += error

        for i in range(len(errors['total'])):
            error += errors['total'][i]

        error /= 2.0 * value
        return error

    def circles(self, pixels):

        width = self.w
        height = self.h
        rmin = 2
        rmax = 20
        val = rmax
        names = ['PS1', 'PS0', 'total']
        cont = setCont(val, names)

        maxH = height - rmin
        maxW = width - rmin
        for r in range(rmin, maxH):
            for c in range(rmin, maxW):
                first_pix = pixels[r * width + c]
                if first_pix == 0:
                    flag = 1                                        # Negado
                    cradio = min(rmax, c, width - c, r, height - r)
                    for radio in range(rmin, cradio):
                        radio2 = radio * radio
                        for r2 in range(-radio, radio):
                            for c2 in range(-radio, radio):
                                if flag == 0:
                                    break
                                x = r2**2 + c2**2
                                if min(x, radio2) == x:
                                    valor = pixels[
                                        (r + r2)*width + c2 + c
                                    ]
                                else:
                                    valor = 1
                                flag &= valor
                            cont['PS1'][radio] += flag
        return cont

    def lines(self, pixels):

        width = self.w
        height = self.h
        depth = self.d
        rs = width
        ss = width * height
        val = max(width, height)
        names = ['f2s1', 'flp1', 'f2s0', 'flp0', 'total']
        cont = setCont(val, names)

        for d in range(depth):
            for r in range(height):
                for c in range(width):
                    first_pix = pixels[d*ss + r*rs + c]

                    #   Code redu by args   #### Checked!!!     B)

                    #   t --> Opera 't'
                    if first_pix == 1:      # Find '1'
                        a = 'f2s1'
                        b = 'flp1'
                        t = True
                    else:                   # Find '0'
                        a = 'f2s0'
                        b = 'flp0'
                        t = False

                    #   I
                    delta_offset = [1, rs, ss]
                    limit = [width - c, height - r, depth - d]

                    #   Accountant
                    first_pix = 1
                    for i in delta_offset:
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

"""
                Original

if first_pix == 1:
    flag = first_pix
    for ls in range(0, width - c):
        cont['total'][ls] += 1
        cont['f2s1'][ls] += first_pix & pixels[
            r*width + c + ls
        ]
        flag = flag & pixels[r*width + c + ls]
        cont['flp1'][ls] += flag

    flag = first_pix
    for ls in range(0, height - r):
        cont['total'][ls] += 1
        cont['f2s1'][ls] += first_pix & pixels[
            (r + ls)*width + c
        ]
        flag = flag & pixels[(r + ls)*width + c]
        cont['flp1'][ls] += flag

else:
    first_pix = 1
    flag = 1
    for ls in range(0, width-c):
        cont['total'][ls] += 1
        cont['f2s0'][ls] += first_pix ^ pixels[
            r*width + c + ls
        ]
        flag = flag & (first_pix ^ pixels[r*width + c + ls])
        cont['flp0'][ls] += flag

    flag = 1
    for ls in range(0, height-r):
        cont['total'][ls] += 1
        cont['f2s0'][ls] += first_pix ^ pixels[
            (r + ls)*width + c
        ]
        flag = flag & (first_pix ^ pixels[(r + ls)*width + c])
        cont['flp0'][ls] += flag

"""
