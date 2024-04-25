"""
这个工程使用的python3.11版本（太高了）
因为这个版本与pyside2不兼容，所以只能使用pyside6
pyside6与pyside2中有一些区别（但不大）
其中比较多的就是将很多不是很常用的函数和类进行了重新归类和放置
就好比接下来这段代码中的OpenGL相关的所有模块，都进行的移位
而且在Qt6中，对于OpenGL的内存管理机制进行了更严格的升级
所以曾经对于Qt5中的一些不太安全的做法，在Qt6中会直接报错

"""
import numpy as np
import pyrr.matrix44
from PySide6 import QtCore, QtWidgets, QtGui, QtOpenGLWidgets
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader, QOpenGLTexture, QOpenGLVertexArrayObject, \
    QOpenGLBuffer
from PySide6.QtWidgets import QApplication, QWidget
import numpy
import PIL.Image as pimage
import OpenGL
import analysis_obj
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import ctypes
from OpenGL.GL.shaders import compileShader, compileProgram

float_size = ctypes.sizeof(ctypes.c_float)
def mk_tuple(x, y):
    _l = []
    for i in range(y):
      _l.append(x)
    return _l
class open_widget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super(open_widget, self).__init__(parent=parent)
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.model = None
        self.set_model = pyrr.matrix44.create_identity(dtype=np.float32)
        scale = pyrr.matrix44.create_from_scale(mk_tuple(0.01, 3), dtype=np.float32)
        self.set_model = pyrr.matrix44.multiply(self.set_model, scale)
        self.resize(500, 500)
        self.zoom = 2
        self.setWindowTitle('open_widget')
        # self.timmer = QtCore.QTimer()
        # self.timmer.timeout.connect(self.update)
        # self.timmer.start(1000/60)

    def initializeGL(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        with open("vertex2.glsl", "r") as f:
            shader_ver_source = f.read()
        with open("fragment2.glsl", "r") as f:
            shader_frag_source = f.read()

        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, shader_ver_source)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, shader_frag_source)
        self.program.bindAttributeLocation("a_Pos", 0)
        self.program.bindAttributeLocation("a_Nor", 1)
        self.program.bindAttributeLocation("a_Tex", 2)
        self.program.link()
        self.program.bind()
        self.shaderProgram = self.program.programId()

        self.texture = QOpenGLTexture(QOpenGLTexture.Target.Target2D)
        self.texture.create()
        self.texture.setData(QtGui.QImage("test.jpg"))
        self.texture.setMinificationFilter(QOpenGLTexture.Linear)
        self.texture.setMagnificationFilter(QOpenGLTexture.Linear)
        self.texture.setWrapMode(QOpenGLTexture.ClampToEdge)

        self.model = analysis_obj.Model.make_model("test.obj")
        self.model.gen_buffer(self.program)

        print("initialized")
        glEnable(GL_DEPTH_TEST)
        glUseProgram(self.shaderProgram)
        glClearColor(0, 0.1, 0.1, 1)

    def resizeGL(self, w, h):
        print("resizeGL")
        glViewport(0, 0, w, h)
        self.set_project = QtGui.QMatrix4x4()
        self.set_project.setToIdentity()
        self.set_project.perspective(45.0, float(w) / float(h), 0.01, 10000)
        self.set_project = pyrr.matrix44.create_perspective_projection_matrix(45.0, float(w) / float(h), 0.01, 10000, dtype=np.float32)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindVertexArray(self.model.VAO)

        self.program.bind()

        set_view = pyrr.matrix44.create_look_at((0, 0, self.zoom), (0, 0, 0), (0, 1, 0), dtype=np.float32)

        set_mvp = pyrr.matrix44.multiply(self.set_model, pyrr.matrix44.create_identity(dtype=np.float32))
        set_mvp = pyrr.matrix44.multiply(set_mvp, set_view)
        set_mvp = pyrr.matrix44.multiply(set_mvp, self.set_project)


        uMVP = glGetUniformLocation(self.shaderProgram, "uMVP")
        glUniformMatrix4fv(uMVP, 1, GL_FALSE, set_mvp)

        self.texture.bind()
        # glDrawElements(GL_TRIANGLES, self.model.indices[0].size, GL_UNSIGNED_INT, None)
        glDrawArrays(GL_TRIANGLES, 0, len(self.model.component))


    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.enableRot = True
            self.last_pos = event.globalPosition()
        else:
            self.enableRot = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.enableRot:
            anglex = -0.008 * (event.globalPosition().x() - self.last_pos.x())
            angley = -0.008 * (event.globalPosition().y() - self.last_pos.y())

            self.program.bind()
            temp = pyrr.matrix44.multiply(
                pyrr.matrix44.create_from_y_rotation(anglex, dtype=np.float32),
                pyrr.matrix44.create_from_x_rotation(angley, dtype=np.float32),
                )
            self.set_model = pyrr.matrix44.multiply(
                self.set_model,
                temp
            )
            self.last_pos = event.globalPosition()
            self.update()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        # print(event.angleDelta())
        self.zoom += event.angleDelta().y() / 1200 * -1
        self.update()


class mainW(QWidget):
    def __init__(self):
        super(mainW, self).__init__()
        self.resize(500, 500)
        self.label = QtWidgets.QLabel(self)
        self.label.setText("测试")
        self.label.setMaximumHeight(50)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.gl = open_widget(self)
        # format = QtGui.QSurfaceFormat()
        # format.setSamples(8)
        # self.gl.setFormat(format)
        self.layout.addWidget(self.gl)


if __name__ == '__main__':
    # QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    app = QApplication(sys.argv)
    window = mainW()
    window.show()
    sys.exit(app.exec())
