import threading
import time


def contador(args):        # Argument counter
        value = 0x0
        mask = 0x1
        for i in args:
            if not i:
                value |= mask
            mask <<= 1
        return value


class Process(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

        self.runs = 0

        self.result = None
        self.info = None

    def run(self):
        self.runs += 1

        print "Starting " + self.name + ' ' + str(time.clock())
        self.main()
        print "Exiting " + self.name + ' ' + str(time.clock())

    def main(self):
        pass

    def getState(self):
        print str(self.runs) + ' runs dude!'

    # def close(self):
    #     self.io.writeOUT(self.result, 'outfile_%s' % self.id)
