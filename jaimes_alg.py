def opera(t, x, y):
    if t == 0:
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
        self.r_min = 2
        self.r_max = 20
        self.w = width
        self.h = height

    def errors(self, old, new):

        value = len(old)
        keys = []
        for i in old.keys():
            keys.append(i)
        errors = setCont(value, keys)

        for k in errors:
            if k is not 'total':
                for i in range(len(errors) - 1):
                    error = old[k][i] - new[k][i]
                    error *= error
                    errors[k][i] = error                ##  May not need
                    errors['total'][i] += error

        for i in range(len(errors['total'])):
            error += errors['total'][i]

        error /= 2.0 * value
        return error

    def circles(self, pixels):

        width = self.w
        height = self.h
        val = self.r_max
        names = ['PS1', 'PS0', 'total']
        cont = setCont(val, names)

        maxH = height - self.r_min
        maxW = width - self.r_min
        for r in range(self.r_min, maxH):
            for c in range(self.r_min, maxW):
                first_pix = pixels[r * width + c]
                if first_pix == 0:
                    flag = 1                                        # Negado
                    cradio = min(self.r_max, c, width - c, r, height - r)
                    for radio in range(self.r_min, cradio):
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
        val = max(width, height)
        names = ['f2s1', 'flp1', 'f2s0', 'flp0', 'total']
        cont = setCont(val, names)

        for r in range(0, height):
            for c in range(0, width):
                first_pix = pixels[r * width + c]

                #   Code redu by args           #### Checked!!!      B)

                #   t --> Opera 't'
                if first_pix == 1:              # Find '1'
                    a = 'f2s1'
                    b = 'flp1'
                    t = 0
                else:                           # Find '0'
                    a = 'f2s0'
                    b = 'flp0'
                    t = 1

                #   I
                ls = 0
                x_r = [r, r + ls]
                x_ls = [ls, 0]
                limit = [width - c, height - r]

                #   Accountant
                first_pix = 1
                for i in range(2):
                    flag = 1
                    for ls in range(limit[i]):
                                                    # All
                        cont['total'][ls] += 1
                                                    # F2
                        cont[a][ls] += opera(
                            t, first_pix, pixels[
                                x_r[i] * width + c + x_ls[i]
                            ]
                        )
                                                    # FL-check
                        flag &= opera(
                            t, first_pix, pixels[
                                x_r[i] * width + c + x_ls[i]
                            ]
                        )
                                                    # FL
                        cont[b][ls] += flag
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
