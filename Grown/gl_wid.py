from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *

import matplotlib.pyplot as plt

from SA import *


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent):
        super(GLWidget, self).__init__(parent)
        self.parent = parent

        self.cuenta = 0

        self.z = 0.5
        self.d = 0
        self.w = self.d
        self.h = self.d
        self.yRotDeg = 0.0

        self.img = []
        self.temp = []
        self.pixls = []
        self.algo = None
        self.first = False
        self.second = False
        self.third = False

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(150, 150, 150))
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, width, height):
        if height is 0:
            height = 1
        aspect = width / float(height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)

        glLoadIdentity()
        glOrtho(-30.0,  # Left coordinates value.   ( x_min )
                30.0,   # Right coordinates value.  ( x_max )
                -30.0,  # Bottom coordinates value. ( y_min )
                30.0,   # Top coordinates value.    ( y_max )
                -30.0,  # Near coordinates value.   ( z_min )
                30.0)   # Far coordinates value.    ( z_max )
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        z = self.z
        glLoadIdentity()
        glScale(z, z, z)

        if self.first:
            # TODO get rotation better
            self.yRotDeg = (self.yRotDeg + 10) % 360.0
            glRotate(self.yRotDeg, .1, .8, .1)
            self.draw_lines()
            glEnable(GL_TEXTURE_3D)
            glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
            glEnable(GL_POINT_SMOOTH)
            glPointSize(self.z * 10)
            # self.img3d()
            self.img_temp()
        else:
            z = self.d * .5
            glTranslate(-z, -z, -z)
            self.img2D()

    def draw_lines(self):
        rs = self.d * 0.5
        z = self.d * 0.5
        vertices = (
            (rs, -rs, -rs),
            (rs, rs, -rs),
            (-rs, rs, -rs),
            (-rs, -rs, -rs),
            (rs, -rs, rs),
            (rs, rs, rs),
            (-rs, -rs, rs),
            (-rs, rs, rs)
        )

        edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)
        )

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
        glTranslate(-z, -z, -z)

    def img2D(self):
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(self.z * 10)

        rs = self.d ** 2
        k = int(self.d * 0.5)

        glBegin(GL_POINTS)
        for i in range(self.d):
            for j in range(self.d):
                glColor3f(0, self.img[k * rs + self.d * i + j], 0)
                glVertex2i(i, j)
        glEnd()

    def img3d(self):

        ss = self.d ** 2
        sr = self.d
        glBegin(GL_POINTS)
        for i in range(sr):
            for j in range(sr):
                for k in range(sr):
                    pos = i * ss + j * sr + k
                    color = self.img[pos]

                    # TODO Parametrizar
                    if color > 0.5:     # not 0
                        glColor3f(0, color, 0)
                        glVertex3f(i, j, k)
        glEnd()

    def img_temp(self):

        ss = self.d ** 2
        rs = self.d

        # TODO solve automated mapcolor
        division = 8    # Should be argumented

        colors = [      # Automated
            [1.0, 0, 0], [1.0, 0.3, 0], [1.0, 0.7, 0],
            [1.0, 1.0, 0], [0.7, 1.0, 0], [0.3, 1.0, 0],
            [0, 1.0, 0], [0, 1.0, 0.3], [0, 1.0, 0.7],
            [0, 1.0, 1.0], [0, 0.7, 1.0], [0, 0.3, 1.0],
            [0, 0, 1.0]
        ]
        i_temp = 300    # Should be argumented 2

        glBegin(GL_POINTS)
        for i in range(rs):
            for j in range(rs):
                for k in range(rs):
                    pos = i * ss + j * rs + k
                    if self.img[pos] is not 0:
                        temp = self.temp[k][j][i] - i_temp
                        color = colors[len(colors) - int(temp//division) - 1]
                        glColor3f(color[0], color[1], color[2])
                        glVertex3f(k, j, i)
        glEnd()

    def setImg(self, algo, size):
        self.setSize(size)

        self.first = algo.first
        self.second = algo.second
        self.img = algo.rand_img

        self.temp = algo.temp
        self.pixls = algo.con
        self.algo = algo

    def setSize(self, size):
        self.d = size
        # TODO colormaped styled size
        if 20 <= size < 50:
            self.z = .8
        elif 50 <= size < 100:
            self.z = .6
        elif 100 <= size < 200:
            self.z = .3
        elif 200 <= size < 300:
            self.z = .2
        elif 300 <= size:
            self.z = .1

    def spin(self):
        self.first = self.algo.first
        self.second = self.algo.second
        self.third = self.algo.third
        self.updateGL()
