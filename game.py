import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader

class App:
    def __init__(self):
        # inits the pygame window
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)

        # inits clock (update function basically)
        self.clock = pg.time.Clock()

        # sets bg colour
        glClearColor(0.1, 0.2, 0.2, 1)
        # parses the file names of the shaders
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        # have a shader in use before passing through any data
        glUseProgram(self.shader)
        # inits the triangle
        self.triangle = Triangle()
        self.mainLoop()

    # drawing literally anything with opengl requires a shader
    def createShader(self, vertexFilepath, fragmentFilepath):
        # reads the vertex shader
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()

        # reads the fragment shader
        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        # compiles the shader
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self):
        running = True

        # game loop
        while (running):
            for event in pg.event.get():
                # check if close window, then stop loop
                if (event.type == pg.QUIT):
                    running = False

            # honestly no clue, prob displays the colour or smth
            glClear(GL_COLOR_BUFFER_BIT)

            # reset shader (doesnt need to but best practice)
            glUseProgram(self.shader)
            # get the current model triangle thats gonna be drawn
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            # ticks the clock
            self.clock.tick(60)
        self.quit()

    def quit(self):
        # frees up vao and vbo
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:
    def __init__(self):

        # x (left/right), y (up/down), z (depth), r, g, b
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0
        )

        # numpy is built for C style data type, since python doesn't have any prebuilt interpreters
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        # tells opengl how to interpret the data (ex. pos, colour; or colour, pos)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        # vertex buffer object: storage container
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # tells opengl what to do with the given data, draw it in this case (i think)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        # attribute 0 is position
        glEnableVertexAttribArray(0)
        # monke function needs a void pointer as final parameter
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        # attribute 1 is colour
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    # frees up the memory
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

if __name__ == '__main__':
    myApp = App()