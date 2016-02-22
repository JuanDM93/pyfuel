def check(x, y):
    if x < y:
        return x
    else:
        return y


def opera(t, x, y):
    if t == 0:
        return x & y
    else:
        return x | y

#   Definir HEADER de x bytes para los archivos
#   0123 <-Tipo (cir, lin, etc) 4567 <-(size, width, height, etc)

class Contador(object):

    def __init__(self):                                             ###### FATAL ERROR  #####
        self.cont = {}                                              # cont podria ser un diccionario
        self.r_min = 2
        self.r_max = 20

    def circles(self, pixels, width, height):

        cont = []
        maxH = height - self.r_min
        maxW = width - self.r_min
        for r in range(self.r_min, maxH):
            for c in range(self.r_min, maxW):
                first_pix = pixels[r * width + c]
                if first_pix == 0:
                    flag = 1                                        # Negado
                    cz = check(c, width - c)
                    rz = check(r, height - r)
                    cz = check(cz, rz)
                    cradio = check(self.r_max, cz)
                    for radio in range(self.r_min, cradio):
                        radio2 = radio * radio
                        for r2 in range(-radio, radio):
                            for c2 in range(-radio, radio):
                                if flag == 0:
                                    break
                                x = r2**2 + c2**2
                                if check(x, radio2) == x:
                                    valor = pixels[
                                        (r + r2)*width + c2 + c
                                    ]
                                else:
                                    valor = 1
                                flag &= valor
                            cont[radio] += flag
        return cont

    def lines(self, pixels, width, height):
        cont = []
        for r in range(0, height):
            for c in range(0, width):
                first_pix = pixels[r * width + c]

                ######################################################################################

                if first_pix == 1:
                    flag = first_pix
                    for ls in range(0, width - c):
                        cont[4][ls] += 1
                        cont[0][ls] += first_pix & pixels[
                            r*width + c + ls
                        ]
                        flag = flag & pixels[r*width + c + ls]
                        cont[1][ls] += flag

                    flag = first_pix
                    for ls in range(0, height - r):
                        cont[4][ls] += 1
                        cont[0][ls] += first_pix & pixels[
                            (r + ls)*width + c
                        ]
                        flag = flag & pixels[(r + ls)*width + c]
                        cont[1][ls] += flag

                else:
                    first_pix = 1
                    flag = 1
                    for ls in range(0, width-c):
                        cont[4][ls] += 1
                        cont[2][ls] += first_pix | pixels[
                            r*width + c + ls
                        ]
                        flag = flag & (first_pix | pixels[r*width + c + ls])
                        cont[3][ls] += flag

                    flag = 1
                    for ls in range(0, height-r):
                        cont[4][ls] += 1
                        cont[2][ls] += first_pix | pixels[
                            (r + ls)*width + c
                        ]
                        flag = flag & (first_pix | pixels[(r + ls)*width + c])
                        cont[3][ls] += flag

                ######################################################################################

                """
                #   Code redu by args

                if first_pix == 1:
                    a = 0
                    b = 1
                else:
                    a = 2
                    b = 3

                #   I
                ls = 0
                x_r = [r, r + ls]
                x_ls = [ls, 0]
                x = [width - c, height - r]

                #   Accountant
                first_pix = 1
                for i in range(2):
                    flag = 1
                    for ls in range(x[i]):
                        cont[4][ls] += 1
                        cont[a][ls] += opera(
                            a, first_pix, pixels[
                                (x_r[i]) * width + c + x_ls[i]
                            ]
                        )
                        #   Duda a reducir... first_pixel ???
                        flag = flag & pixels[x_r * width + c + x_ls[i]]

                        cont[b][ls] += flag
                """

        return cont



