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

OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import ctypes
from OpenGL.GL.shaders import compileShader, compileProgram

float_size = ctypes.sizeof(ctypes.c_float)


class open_widget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super(open_widget, self).__init__(parent=parent)
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.set_model = pyrr.matrix44.create_identity(dtype=np.float32)
        self.resize(500, 500)
        self.setWindowTitle('open_widget')

    def initializeGL(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
                         0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                         -0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0,
                         0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                         0.0, 0.75, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0,
                         ]
        self.indices = [0, 1, 2,
                        1, 2, 3,
                        2, 3, 4
                        ]
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)

        # glEnable(GL_ALPHA_TEST)
        with open("vertex.glsl", "r") as f:
            shader_ver_source = f.read()
        with open("fragment.glsl", "r") as f:
            shader_frag_source = f.read()


        # 使用GL.shaders 中的集成方法
        # ver = compileShader(shader_ver_source, GL_VERTEX_SHADER)
        # fra = compileShader(shader_frag_source, GL_FRAGMENT_SHADER)
        # self.shaderProgram = compileProgram(ver, fra)

        # 使用Qt中的方式创建shader
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, shader_ver_source)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, shader_frag_source)
        self.program.bindAttributeLocation("a_Pos", 0)
        self.program.bindAttributeLocation("a_Col", 1)
        self.program.bindAttributeLocation("ccc", 2)
        self.program.link()
        self.program.bind()
        self.shaderProgram = self.program.programId()

        # 使用API原生方法创建shader
        # ver = glCreateShader(GL_VERTEX_SHADER)
        # fra = glCreateShader(GL_FRAGMENT_SHADER)
        # glShaderSource(ver, shader_ver_source)
        # glShaderSource(fra, shader_frag_source)
        # glCompileShader(ver)
        # glCompileShader(fra)
        # self.shaderProgram = glCreateProgram()
        # glAttachShader(self.shaderProgram, ver)
        # glAttachShader(self.shaderProgram, fra)
        # glLinkProgram(self.shaderProgram)
        # glDeleteShader(ver)
        # glDeleteShader(fra)

        # 使用Qt自带的方法创建Texture，每次绘制前绑定即可
        self.texture = QOpenGLTexture(QOpenGLTexture.Target.Target2D)
        self.texture.create()
        self.texture.setData(QtGui.QImage("test.jpg"))
        self.texture.setMinificationFilter(QOpenGLTexture.Linear)
        self.texture.setMagnificationFilter(QOpenGLTexture.Linear)
        self.texture.setWrapMode(QOpenGLTexture.ClampToEdge)

        self.make_buffer()

        print("initialized")
        glEnable(GL_DEPTH_TEST)
        glUseProgram(self.shaderProgram)
        glClearColor(0, 0.1, 0.1, 1)

    def resizeGL(self, w, h):
        print("resizeGL")
        glViewport(0, 0, w, h)
        self.set_project = QtGui.QMatrix4x4()
        self.set_project.setToIdentity()
        self.set_project.perspective(45.0, float(w) / float(h), 0.01, 100)
        # 如果是要在这里直接改写shader的uniform属性的话，我们需要前面重新绑定一下shaderprogram，太麻烦了，所以我们在这记录一下即可，等到paintGL的时候我们再统一的
        # 对shader进行更改

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #使用VAO模式的话每次只需要重新将VAO从内存载入缓冲区即可
        glBindVertexArray(self.VAO)

        self.program.bind()
        # 在Qt中就算是想要使用原生的shader属性写入方式，也需要在这个context中提前进行shaderprogram绑定，否则会报错
        set_view = pyrr.matrix44.create_look_at((0, 0, 2), (0, 0, 0), (0, 1, 0), dtype=np.float32)
        view = glGetUniformLocation(self.shaderProgram, "uV")
        glUniformMatrix4fv(view, 1, GL_FALSE, set_view)

        # self.set_model = pyrr.matrix44.create_from_translation((0, 0, 2), dtype=np.float32)
        model = glGetUniformLocation(self.shaderProgram, "uMo")
        glUniformMatrix4fv(model, 1, GL_FALSE, self.set_model)

        # 使用Qt QOpenGLShaderProgram中的写入uniform属性函数
        projection = glGetUniformLocation(self.shaderProgram, "uPer")
        self.program.setUniformValue(projection, self.set_project)


        # transpose = glGetUniformLocation(self.shaderProgram, "transpose")
        # set_tran = QtGui.QMatrix2x2()
        # set_tran.setToIdentity()
        # # set_tran.transposed()
        # self.program.setUniformValue(transpose, set_tran)

        #但是如果想要重新将顶点属性载入进shader，还是需要单独绑定VBO
        self.VBO.bind()
        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3, 8 * float_size)

        self.program.enableAttributeArray(1)
        self.program.setAttributeBuffer(1, GL_FLOAT, 3 * float_size, 3, 8 * float_size)

        # Qt的材质绑定方法
        self.texture.bind()
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)
        # glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))

    def make_buffer(self):
        # 使用原生的方式创建vertexarray
        if not self.VAO:
            self.VAO = glGenVertexArrays(1)
            glBindVertexArray(self.VAO)

        # 使用Qt的方式创建VertexBuffer
        if not self.VBO:
            self.VBO = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
            self.VBO.create()
        self.VBO.bind()
        self.VBO.allocate(self.vertices, self.vertices.nbytes)

        # Qt EBO
        # self.EBO = QOpenGLBuffer(QOpenGLBuffer.Type.IndexBuffer)
        # self.EBO.create()
        # self.EBO.bind()
        # self.EBO.allocate(self.indices, self.indices.nbytes)

        # 原生 VBO
        # self.VBO = glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        # glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        #

        # 原生 EBO
        if not self.EBO:
            self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # 注意创建完VBO后，在当前的context下不需要再次绑定VBO往shader中写入属性，多此一举
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 3, 8 * float_size)
        self.program.enableAttributeArray(0)

        self.program.setAttributeBuffer(1, GL_FLOAT, 3 * float_size, 3, 8 * float_size)
        self.program.enableAttributeArray(1)

        self.program.setAttributeBuffer(2, GL_FLOAT, 6 * float_size, 2, 8 * float_size)
        self.program.enableAttributeArray(2)
        # 我的理解是shader中的定点属性只和VBO相关 EBO记录的是VBO中的顶点顺序，他的层级会更高，VAO会比EBO更高，所以我们如果想替换当前缓存中的顶点属性，只需要重新绑定VBO然后更改即可
        # 这样的 挂载VBO的EBO和VAO也同时因为底层的数据更改而发生改变

        # 下面是一种原生方式的更改shader中顶点属性的方式，不多赘述，值得注意的一点是，如果我们的shader文件的输入属性并没有使用的话（只是声明），那么我们在glGetAttribLocation时会得到-1
        # 这时我们再去glVertexAttribPointer的时候会报错，无论是原生方式还是 Qt方式都会报错，这是不是可能与Qt内部的内存管理分配机制有关（我瞎猜的）
        # ccc = glGetAttribLocation(self.shaderProgram, "ccc")
        # color = glGetAttribLocation(self.shaderProgram, "a_Col")
        # position = glGetAttribLocation(self.shaderProgram, "a_Pos")
        # print(color, position, ccc)
        #
        # glEnableVertexAttribArray(position)
        # glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 6 * float_size, ctypes.c_void_p(0))
        #
        # glEnableVertexAttribArray(color)
        # glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 6 * float_size, ctypes.c_void_p(3 * float_size))
        # 最后我们已经将一切属性都记录在内存中，这时我们先把这些数据从缓冲中退出来，等到用的时候我们再从内存中拿到缓冲区
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        # print(QtCore.Qt.MouseButton.LeftButton)
        # print(event.button().name)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.enableRot = True
            self.last_pos = event.position()

            self.vertices = [
                [-0.2, -0.2, 0.0, 1.0, 0.0, 0.0,0,0,
                 0.4, -0.3, 0.0, 0.0, 1.0, 0.0,0,1,
                 -0.7, 0.9, 0.0, 0.0, 0.0, 1.0,1,0,
                 0.3, 0.6, 0.0, 1.0, 1.0, 1.0,1,1,
                 0.0, 0.66, 0.0, 1.0, 1.0, 0.0,1,1,
                 ]
            ]
            self.vertices = np.array(self.vertices, dtype=np.float32)
            self.make_buffer()
            self.update()

        else:
            self.enableRot = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.enableRot:
            anglex = -0.001 * (event.position().x() - self.last_pos.x())
            angley = 0.001 * (event.position().y() - self.last_pos.y())

            self.program.bind()
            temp = pyrr.matrix44.multiply(
                pyrr.matrix44.create_from_y_rotation(anglex, dtype=np.float32),
                pyrr.matrix44.create_from_x_rotation(angley, dtype=np.float32),
                )
            self.set_model = pyrr.matrix44.multiply(
                self.set_model,
                temp
            )
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
