import csv
#           Basic IO
class FileIO(object):
    def __init__(self):
        self.head = 5

    def readAll(self, file_name):
        data = []
        h = 0
        with open(file_name) as f:
            reader = csv.reader(f)
            for row in reader:
                w = len(row)
                h += 1
                for i in range(w):
                    data.append(int(row[i]))
        return data, w, h


    # def read_Head(self, txt, start, end):
    #     data = []
    #     final = []
    #     for i in range(start, end):
    #         data.append(txt[i])
    #     for i in range(2):
    #         result = self.read_Hex(i, data)
    #         final.append(result)
    #     return final
    #
    # def read_Hex(self, i, list):
    #     a = ''
    #     lim = self.head
    #     for i in list[i * lim: (i + 1) * lim]:
    #         a += str(i)
    #     a = int(a, 16)
    #     return a
    #
    # def read_Data(self, txt, start, end):
    #     data = []
    #     for i in range(start, end):
    #         if i is not ',':
    #             data.append(int(txt[i]))
    #     return data
    #
    # def pix_txt(self, path):
    #     with open(path) as f:
    #         txt = f.read()
    #     f.close()
    #     return txt

    def writeOUT(self, data, path):
        out = open(path, 'w')
        for i in data:
            out.write(i)
        out.close()
