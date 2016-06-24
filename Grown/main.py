import os
import sys

from widgets import *


def restart():
    p = sys.executable
    os.execl(p, p, * sys.argv)


class MyApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Expociencias 2016: DEMO')
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.statusBar()
        self.setStyleSheet(
            "background-image: url(./uqroo.gif)"
        )

        middle = MiddleWidget(self)
        self.setCentralWidget(middle)

    def restart(self):
        restart()


def main():
    app = QtGui.QApplication(sys.argv)
    main_win = MyApp()
    main_win.show()
    app.exec_()

if __name__ == '__main__':
    main()
