import time
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Printer(object):
    def __init__(self, data, w, h, d, algo):
        self.w = w
        self.h = h
        self.d = d
        self.data = data

        self.dif = (
            w / 2.0,
            h / 2.0,
            d / 2.0
        )
        self.size = 0.5

        self.rand_img = algo.rand_img
        self.printed = algo.printed
        self.algo = algo

        s_width = 1024.0
        s_height = 720.0

        pygame.init()                               # We initialise the pygame module.
        pygame.display.set_caption('Fuel3D')

        pygame.display.set_mode(
            (int(s_width), int(s_height)),          # We set the window width and height
            HWSURFACE | OPENGL | DOUBLEBUF,         # We set flags.
            32)                                     # Indicator colors are coded on 32 bits.
        self.initGL(s_width, s_height)                   # Call to initialise function.

        """
        TESTIN
        """
        self.main()

    def main(self):
        # mouse
        pos = (0, 0)
        l_pos = pos
        active = False

        # mainloop
        while True:
            start = time.clock()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.resizeGL(self.w, self.h)
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button is 4:
                        if self.size < 1:
                            self.size += 0.1
                    elif event.button is 5:
                        if self.size > 0.1:
                            self.size -= 0.1
                    pos = pygame.mouse.get_pos()
                    active = True
                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                elif event.type == MOUSEBUTTONUP:
                    active = False
                    pos = pygame.mouse.get_pos()
                elif event.type == KEYUP:           # Start algorithm process button
                    # Should get more functions...
                    if self.algo.isAlive():
                        print 'Algo runnin: %s' % self.algo.action
                    else:
                        print 'Algo start: %s' % time.clock()
                        self.algo.start()

            # Main functions:
            self.img3d()
            if active:
                l_pos = self.djent(pos, l_pos)                # mouse motion
                print 'Printed1 %s' % (time.clock() - start)
            pygame.display.flip()

    def initGL(self, width, height):

        glClearColor(0.5, 0.5, 0.5, 0.5)  # Define clear color [0.0-1.0]
        glEnable(GL_DEPTH_TEST)  # Enable GL depth functions.
        glShadeModel(GL_SMOOTH)  # Define lines as polygon instead of full polygon: GL_SMOOTH, GL_FLAT
        glRotate(30, 1, 1, 0)

        self.resizeGL(width, height)  # Call to the resize function.

    def resizeGL(self, width, height):
        fov_angle = 90.0  # Angle of eye view.
        z_near = 1  # Distance from the user from the screen.
        z_far = 100  # Distance in depth.

        glMatrixMode(GL_PROJECTION)  # Enable Projection matrix configuration.
        glLoadIdentity()
        gluPerspective(
            fov_angle,
            float(width) / float(height),
            z_near,
            z_far)

        glLoadIdentity()
        glOrtho(-30.0,  # Left coordinates value.   ( x_min )
                30.0,  # Right coordinates value.  ( x_max )
                -30.0,  # Bottom coordinates value. ( y_min )
                30.0,  # Top coordinates value.    ( y_max )
                -30.0,  # Near coordinates value.   ( z_min )
                30.0)  # Far coordinates value.    ( z_max )

        glMatrixMode(GL_MODELVIEW)  # Enable modelview matrix as current matrix.

    def djent(self, pos, l_pos):
        if pos is not l_pos:
            x, y = pos
            d_x, d_y = l_pos

            # Get it better
            v_x = x - d_x
            v_y = y - d_y
            glRotatef(self.size * 10, v_y, v_x, 0)
        return pos

    def img3d(self):
        glEnable(GL_TEXTURE_3D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(self.size)

        z = self.size * 0.1
        rs = self.w
        ss = self.w * self.h

        glBegin(GL_POINTS)
        for i in range(len(self.printed)):
            d, r, c = self.printed[i]
            pos = d * ss + r * rs + c
            glColor3f(0, self.rand_img[pos], 0)
            glVertex3f(
                z * (d - self.dif[0]),
                z * (r - self.dif[1]),
                z * (c - self.dif[2]),
            )
        glEnd()

    def img2d(self):
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(5)

        data = self.data

        glBegin(GL_POINTS)
        for i in range(self.h):
            for j in range(self.w):
                glColor3f(0, data[(self.w * i) + j], 0)
                glVertex2f(
                    0.3 * (i - self.w / 2.0),
                    0.3 * (j - self.h / 2.0)
                )
        glEnd()

    def histo(self):
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(10)
        glLineWidth(10)

        pix = (
            (-10, 10),
            (-5, -5),
            (0, 0),
            (5, -5),
            (10, 10)
        )

        glBegin(GL_POINTS)
        for i in range(len(pix)):
            glColor3f(0, 0, 1)
            glVertex2i(pix[i][0], pix[i][1])
        glEnd()

        glBegin(GL_LINE_STRIP)
        for i in range(len(pix)):
            glColor3f(1, 1, 1)
            glVertex2i(pix[i][0], pix[i][1])
        glEnd()
