#import sys
from draw.printer import Printer
from main.algos.process import Process


#   Main app
class MyApp(object):
    def __init__(self):
        self.initUI()

    def initUI(self):
        #   Set UI design
        pass

    def event_H(self):
        #   Event Handler
        pass

    # Posible more events
    #   0   Image process
    #   1   PDF generator
    #   2   2D generator
    #   3   3D generator
    def e_StartButton(self, opt, info):     # opt and info from event
        pro = Process(opt)                  # Type of process
        pro.start(info)                     # PDFs or Imgs or 2Dplot or Coef
        drawer = Printer(pro.result)
        drawer.show()


#   Run main app with UI
def main():
    #   Set UI environment and run application
    #app = QtGui.QApplication(sys.argv)
    main_win = MyApp()
    main_win.show()
    #app.exec_()

if __name__ == '__main__':
    main()
