from PyQt4 import QtCore
from gl_wid import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class dummyWidget(QtGui.QWidget):
    def __init__(self, parent, layout):
        super(dummyWidget, self).__init__(parent)
        self.setLayout(layout)


class MiddleWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(MiddleWidget, self).__init__(parent)
        self.parent = parent
        self.algo = None

        self.grid = QtGui.QVBoxLayout()
        self.setLayout(self.grid)
        self.isShown = False

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10)

        # String labels
        self.lay_1 = QtGui.QFormLayout()

        labl_c = QtGui.QLabel('Size')
        # labl_c.setAlignment(QtCore.Qt.AlignCenter)
        self.size = QtGui.QLineEdit()
        self.lay_1.addRow(labl_c, self.size)

        labl_r = QtGui.QLabel('Vol Frac %')
        # labl_r.setAlignment(QtCore.Qt.AlignCenter)
        self.vol = QtGui.QLineEdit()
        self.lay_1.addRow(labl_r, self.vol)

        # Radios
        labl_1 = QtGui.QLabel('Sphere (radios)')
        # labl_1.setAlignment(QtCore.Qt.AlignCenter)
        labl_2 = QtGui.QLabel('Vol %')
        # labl_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lay_1.addRow(labl_1, labl_2)

        self.radios = []
        self.r_vols = []

        self.radio_1 = QtGui.QLineEdit()
        self.r_vol_1 = QtGui.QLineEdit()
        self.radios.append(self.radio_1)
        self.r_vols.append(self.r_vol_1)

        self.radio_2 = QtGui.QLineEdit()
        self.r_vol_2 = QtGui.QLineEdit()
        self.radios.append(self.radio_2)
        self.r_vols.append(self.r_vol_2)

        self.radio_3 = QtGui.QLineEdit()
        self.r_vol_3 = QtGui.QLineEdit()
        self.radios.append(self.radio_3)
        self.r_vols.append(self.r_vol_3)

        for i in range(3):
            self.lay_1.addRow(self.radios[i], self.r_vols[i])

        self.top = dummyWidget(self, self.lay_1)
        self.grid.addWidget(self.top)

        # Gls
        self.gl2 = self.initGl()
        lay = QtGui.QGridLayout()
        lay.addWidget(self.gl2)
        self.gls = QtGui.QWidget()
        self.gls.setLayout(lay)
        self.gls.hide()
        self.grid.addWidget(self.gls)

        # Plot
        lay_2 = QtGui.QVBoxLayout()
        self.figure = plt.figure()
        plt.xlabel('Flux')
        self.histo = FigureCanvas(self.figure)
        lay_2.addWidget(self.histo)
        lay_2.addStretch()
        self.matplot = QtGui.QWidget()
        self.matplot.setLayout(lay_2)
        self.matplot.hide()
        self.grid.addWidget(self.matplot)

        # Buttons
        self.button = QtGui.QPushButton('Run')
        self.button.clicked.connect(self.buttonClicked)
        self.grid.addWidget(self.button)

        self.progress = QtGui.QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(101)
        QtCore.QObject.connect(
            self.timer, QtCore.SIGNAL('timeout()'), self.setProgress
        )

    def setProgress(self):
        if self.algo.third:
            self.progress.hide()
            self.gls.hide()
            self.plot()
            self.matplot.show()
        else:
            self.parent.setStatusTip(self.algo.status)
            val = self.algo.setVal()
            if val < 100:
                self.progress.setValue(val)

    def initGl(self):
        gl = GLWidget(self.parent)
        QtCore.QObject.connect(
            self.timer, QtCore.SIGNAL('timeout()'), gl.spin
        )
        return gl

    def plot(self):

        data = self.algo.calores

        ax = self.figure.add_subplot(111)

        self.figure.set_label('Relacion de flujo en Z')

        ax.hold(False)
        ax.plot(data, '*-')

        self.histo.draw()

    def buttonClicked(self):
        self.isShown = not self.isShown
        if self.isShown:
            self.withGl()
        else:
            self.notGL()

    def withGl(self):
        size = int(self.size.text())
        vol = int(self.vol.text())
        radios = []
        for i in range(3):
            radio = int(self.radios[i].text())
            r_vol = int(self.r_vols[i].text())
            radios.append((radio, r_vol))
        radios.sort(reverse=True)

        self.button.setText('Stop')

        self.algo = Algo(1, 'algo', size, vol, radios)
        self.algo.start()

        self.gl2.setImg(self.algo, size)
        self.gls.show()

        self.grid.addWidget(self.progress)
        self.top.hide()

        self.timer.start()
        self.parent.setFixedSize(800, 720)

    def notGL(self):
        self.timer.stop()
        self.gl2.close()
        self.parent.restart()

