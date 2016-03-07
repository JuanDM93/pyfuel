#           Basic IO
class FileIO(object):
    def read_Data(self, txt, start, end):
        data = []
        for i in range(start, end):
            data.append(int(txt[i]))
        return data

    def pix_txt(self, path):
        with open(path) as f:
            txt = f.read()
        f.close()
        return txt

    def writeOUT(self, data, path):
        out = open(path, 'w')
        for i in data:
            out.write(i)
        out.close()
