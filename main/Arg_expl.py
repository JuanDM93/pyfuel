import sys

from PyQt4 import QtGui

class MyApp(QtGui.QWidget):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):

        labl_V = QtGui.QLabel("Video:")
        labl_A = QtGui.QLabel("Audio:")
        labl_G = QtGui.QLabel("AppGinga:")
        labl_R = QtGui.QLabel("Directorio:")

        self.get_V = QtGui.QLineEdit()
        self.get_A = QtGui.QLineEdit()
        self.get_G = QtGui.QLineEdit()
        self.get_R = QtGui.QLineEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(labl_R,1,0)
        grid.addWidget(self.get_R,1,1)

        grid.addWidget(labl_V,2,0)
        grid.addWidget(self.get_V,2,1)

        grid.addWidget(labl_A,3,0)
        grid.addWidget(self.get_A,3,1)

        grid.addWidget(labl_G,4,0)
        grid.addWidget(self.get_G,4,1)

        button = QtGui.QPushButton("Aceptar")
        button.clicked.connect(self.buttonClicked)

        grid.addWidget(button)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Streamer")
        self.show()

    def buttonClicked(self):
        pass


def main():

    app = QtGui.QApplication(sys.argv)
    main_win = MyApp()
    main_win.show()
    app.exec_()

if __name__ == '__main__':
    main()
