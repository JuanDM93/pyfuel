import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def initGL(width, height):
    glClearColor(0.0, 0.0, 0.0, 0.0)    # Define clear color [0.0-1.0]

    glEnable(GL_DEPTH_TEST)             # Enable GL depth functions.

    glShadeModel(GL_FLAT)               # Define lines as polygon instead of full polygon: GL_SMOOTH.

    resizeGL(width, height)             # Call to the resize function.


def resizeGL(width, height):
    fov_angle = 60.0                    # Angle of eye view.
    z_near = 2.0                        # Distance from the user from the screen.
    z_far = 1000.0                      # Distance in depth.

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


class Printer(object):
    def __init__(self):
        w = 720
        h = 480

        pygame.init()
        display = (int(w), int(h))
        pygame.display.set_mode(
            display, OPENGL | DOUBLEBUF, 32
        )
        initGL(w, h)

    def show(self, result):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    pass

            pygame.display.flip()
            pygame.time.wait(10)
