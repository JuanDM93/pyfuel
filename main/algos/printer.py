import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from main.algos.SA import *


class Printer(object):
    def __init__(self, data, w, h):
        self.w = w
        self.h = h
        self.data = data

        self.main()

    def main(self):
        width = 720.0
        height = 480.0

        pygame.init()       # We initialise the pygame module.

        pygame.display.set_mode(
            (int(width), int(height)),          # We set the window width and height
            HWSURFACE | OPENGL | DOUBLEBUF,     # We set flags.
            32)                                 # Indicator colors are coded on 24 bits.
        self.initGL(width, height)              # Call to initialise function.
        self.mainloop()                         # We call our display function: mainloop.

    def initGL(self, width, height):

        glClearColor(0.0, 0.0, 0.0, 0.0)    # Define clear color [0.0-1.0]

        glEnable(GL_DEPTH_TEST)             # Enable GL depth functions.

        glShadeModel(GL_SMOOTH)               # Define lines as polygon instead of full polygon: GL_SMOOTH. GL_FLAT

        self.resizeGL(width, height)             # Call to the resize function.

    def resizeGL(self, width, height):
        fov_angle = 60.0                    # Angle of eye view.
        z_near = 10.0                        # Distance from the user from the screen.
        z_far = 10000.0                      # Distance in depth.

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
            ### Get it better
            v_x = x - l_pos[0]
            v_y = y - l_pos[1]
            glRotate(v_x, 0, 1, 0)
            glRotate(v_y, 1, 0, 0)
            #glRotate(1,0,0,1)
            glTranslate(0, 0, z)

    def mainloop(self):
        a = Algo(self.data, self.w, self.h)
        active = False
        pos = (0, 0)
        l_pos = pos
        is_cube = False
        z = 0

        while True:
            if pos is not l_pos:
                self.djent(active, pos, l_pos, z)
            l_pos = pos
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                elif event.type == KEYUP:
                    a.circled()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button is 4:
                        z = 1
                    elif event.button == 5:
                        z = -1
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
            self.img3d(a.rand_img)
            pygame.display.flip()
            pygame.time.wait(10)

    def img2d(self):
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(10)

        lim = min(self.w, self.h)
        data = self.data
        c = 0

        glBegin(GL_POINTS)
        for i in range(lim):
            for j in range(lim):
                glColor3f(data[c], data[c], 1)
                glVertex2i(j, i)
        glEnd()

    def img3d(self, pixls):
        glEnable(GL_TEXTURE_3D)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(5)

        glBegin(GL_POINTS)
        for p in pixls:
            glColor3f(p.val, p.val, 1)
            glVertex3f(p.x, p.y, p.z)
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

