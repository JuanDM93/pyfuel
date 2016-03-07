import sys

from PyQt4 import QtGui

class MyApp(QtGui.QWidget):
    def __init__(self):
        # super(MyApp, self).__init__()
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

        self.setGeometry(300,300,350,300)
        self.setWindowTitle("Streamer")
        self.show()

    def buttonClicked(self):

        video_path = str(self.get_V.text())
        audio_path = str(self.get_A.text())
        ginga_path = str(self.get_G.text())
        result_path = str(self.get_R.text())

        args = [
            video_path, audio_path, ginga_path
            ]
        value = 0x0
        mask = 0x1
        for i in args:
            if i != '':
                value = value | mask
            mask = mask << 1

        if result_path == '':
            self.initUI()
        elif video_path != '' or audio_path != '' or ginga_path != '':
            self.fun = Fun(
                value, result_path, video_path, audio_path, ginga_path
                )
            QtGui.QMessageBox.about(self, 'Finished', "Path = %sresult.ts" % (result_path))
        else:
            QtGui.QMessageBox.about(self, 'Error', "No hay archivos especificados")

def main():

    app = QtGui.QApplication(sys.argv)
    main_win = MyApp()
    main_win.show()
    app.exec_()

if __name__ == '__main__':
    main()
