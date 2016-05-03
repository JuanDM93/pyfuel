import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from main.algos.SA import *

import time

class Printer(object):
    def __init__(self, data, w, h):
        self.w = w
        self.h = h
        self.d = min(w, h)
        self.data = data

        self.main()

    def main(self):
        width = 1024.0
        height = 720.0

        pygame.init()       # We initialise the pygame module.
        pygame.display.set_caption('Fuel3D')

        pygame.display.set_mode(
            (int(width), int(height)),          # We set the window width and height
            HWSURFACE | OPENGL | DOUBLEBUF,     # We set flags.
            24)                                 # Indicator colors are coded on 24 bits.
        self.initGL(width, height)              # Call to initialise function.
        self.mainloop()                         # We call our display function: mainloop.

    def initGL(self, width, height):

        glClearColor(0.5, 0.5, 0.5, 0.5)    # Define clear color [0.0-1.0]

        glEnable(GL_DEPTH_TEST)             # Enable GL depth functions.

        glShadeModel(GL_SMOOTH)             # Define lines as polygon instead of full polygon: GL_SMOOTH, GL_FLAT

        glRotate(30, 1, 1, 0)

        self.resizeGL(width, height)        # Call to the resize function.

    def resizeGL(self, width, height):
        fov_angle = 90.0                    # Angle of eye view.
        z_near = 1                          # Distance from the user from the screen.
        z_far = 100                         # Distance in depth.

        glMatrixMode(GL_PROJECTION)         # Enable Projection matrix configuration.
        glLoadIdentity()
        gluPerspective(
            fov_angle,
            float(width)/float(height),
            z_near,
            z_far)

        glLoadIdentity()
        glOrtho(-30.0,                      # Left coordinates value.   ( x_min )
                30.0,                       # Right coordinates value.  ( x_max )
                -30.0,                      # Bottom coordinates value. ( y_min )
                30.0,                       # Top coordinates value.    ( y_max )
                -30.0,                      # Near coordinates value.   ( z_min )
                30.0)                       # Far coordinates value.    ( z_max )

        glMatrixMode(GL_MODELVIEW)          # Enable modelview matrix as current matrix.

    def djent(self, flag, pos, l_pos, z):
        if flag is True:
            x, y = pos
            # Get it better
            v_x = x - l_pos[0]
            v_y = y - l_pos[1]

            glRotatef(z * 0.3, v_y, v_x, 0)

    def mainloop(self):
        # Algo
        a = Algo(self.data, self.w, self.h, self.d)
        action = 0
        flag = False

        # Djent
        active = False
        pos = (0, 0)
        l_pos = pos
        z = 5.0

        while True:
            if pos is not l_pos:
                self.resizeGL(self.w, self.h)
                self.djent(active, pos, l_pos, z)
            l_pos = pos
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                elif event.type == KEYUP:
                    flag = not flag
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button is 4:
                        if z < 10:
                            z += 1
                    elif event.button is 5:
                        if z > 1:
                            z -= 1
                    pos = pygame.mouse.get_pos()
                    active = True
                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                elif event.type == MOUSEBUTTONUP:
                    active = False
                # Should get more functions...
            """
            # Main functions:
            if f is True:
                self.img3d(a.rand_img)
            else:
                self.img2d()
            #self.histo(a.ref)

            glRotate(1, 1, 1, 1)
            """
            if a.change() and flag:
                start = time.clock()
                action += 1
                if action is 1:
                    print 'start: ' + str(start)
                    flag = a.pre_start()
                    print 'Circled: ' + str(time.clock() - start)
                elif action is 2:
                    print 'start: ' + str(start)
                    flag = a.refill()
                    print 'Filled: ' + str(time.clock() - start)
                elif action is 3:
                    print 'start: ' + str(start)
                    flag = a.after_fill()
                    print 'Prestarted!!!: ' + str(time.clock() - start)
                    # flag = a.sa_start()
                else:
                    action = 0

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.img3d(a.rand_img, z)

            # self.img2d()
            pygame.display.flip()
            # pygame.time.wait(30)

    def img3d(self, pixls, s):
        glEnable(GL_TEXTURE_3D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(s * 0.5)

        size = s * 0.05
        x_dif, y_dif, z_dif = [
            self.w / 2.0,
            self.h / 2.0,
            self.d / 2.0
        ]

        glBegin(GL_POINTS)
        for p in pixls:
            glColor3f(0, p.val, 0)
            glVertex3f(
                size * (p.x - x_dif),
                size * (p.y - y_dif),
                size * (p.z - z_dif)
            )
        glEnd()

    def img2d(self):
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(1)

        data = self.data

        glBegin(GL_POINTS)
        for i in range(self.h):
            for j in range(self.w):
                glColor3f(
                    data[(self.w * i) + j],
                    data[(self.w * i) + j],
                    1
                )
                glVertex2f(
                    0.3 * (i - self.w / 2.0),
                    0.3 * (j - self.h / 2.0)
                )
        glEnd()

    def histo(self, pix):
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

