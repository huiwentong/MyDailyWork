import sys

import numpy as np
from OpenGL import GL as gl
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode, BulletWorld
from panda3d.core import Point3, Quat, TransformState, Vec3
from PySide6.QtCore import QElapsedTimer, QFile, QIODevice, Qt, QTimer
from PySide6.QtGui import (QImage, QMatrix4x4, QQuaternion, QSurfaceFormat,
                           QVector3D)
from PySide6.QtOpenGL import (QOpenGLBuffer, QOpenGLShader,
                              QOpenGLShaderProgram, QOpenGLTexture)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication
from PySide6.QtXml import QDomDocument




class VertexBuffers:
    def __init__(self):
        self.vertex_pos_buffer = None
        self.normal_buffer = None
        self.tex_coord_buffer = None
        self.amount_of_vertices = None


class Locations:
    def __init__(self):
        self.mvp_matrix_location = None
        self.model_matrix_location = None
        self.normal_matrix_location = None


class Object3D:
    def __init__(self, vert_buffers, locations, texture, world, mass, pos):
        self.position = QVector3D(0, 0, 0)
        self.rotation = QVector3D(0, 0, 0)
        self.scale = QVector3D(1, 1, 1)
        self.mvp_matrix = QMatrix4x4()
        self.model_matrix = QMatrix4x4()
        self.normal_matrix = QMatrix4x4()

        self.vert_pos_buffer = vert_buffers.vert_pos_buffer
        self.normal_buffer = vert_buffers.normal_buffer
        self.tex_coord_buffer = vert_buffers.tex_coord_buffer
        self.amount_of_vertices = vert_buffers.amount_of_vertices

        self.mvp_matrix_location = locations.mvp_matrix_location
        self.model_matrix_location = locations.model_matrix_location
        self.normal_matrix_location = locations.normal_matrix_location

        self.texture = texture

        self.shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.node = BulletRigidBodyNode("Box")

        self.position = pos
        self.mass = mass
        self.node.setMass(self.mass)

        p = Point3(self.position.x(), self.position.y(), self.position.z())
        q = Quat.identQuat()
        s = Vec3(1, 1, 1)

        self.transform = TransformState.make_pos_quat_scale(p, q, s)
        self.node.setTransform(self.transform)

        self.node.addShape(self.shape)
        self.world = world
        self.world.attachRigidBody(self.node)

    def draw(self, program, proj_view_matrix):
        program.bind()

        self.vert_pos_buffer.bind()
        program.setAttributeBuffer(0, gl.GL_FLOAT, 0, 3, 24)
        program.enableAttributeArray(0)

        program.setAttributeBuffer(1, gl.GL_FLOAT, 12, 3, 24)
        program.enableAttributeArray(1)
        # self.normal_buffer.bind()

        # self.tex_coord_buffer.bind()
        # program.setAttributeBuffer(2, gl.GL_FLOAT, 0, 2)
        # program.enableAttributeArray(2)

        self.position.setX(self.node.getTransform().pos.x)
        self.position.setY(self.node.getTransform().pos.y)
        self.position.setZ(self.node.getTransform().pos.z)
        hpr = self.node.getTransform().getHpr()
        pandaQuat = Quat()
        pandaQuat.setHpr(hpr)
        quat = QQuaternion(pandaQuat.getX(), pandaQuat.getY(), pandaQuat.getZ(), pandaQuat.getW())

        self.model_matrix.setToIdentity()
        self.model_matrix.translate(self.position)
        self.model_matrix.rotate(quat)
        self.model_matrix.scale(self.scale)
        self.mvp_matrix = proj_view_matrix * self.model_matrix

        self.normal_matrix = self.model_matrix.inverted()
        self.normal_matrix = self.normal_matrix[0].transposed()

        program.bind()
        program.setUniformValue(self.mvp_matrix_location, self.mvp_matrix)
        program.setUniformValue(self.model_matrix_location, self.model_matrix)
        program.setUniformValue(self.normal_matrix_location, self.normal_matrix)

        self.texture.bind()

        # gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.amount_of_vertices)
        gl.glDrawElements(gl.GL_TRIANGLES, self.amount_of_vertices, gl.GL_UNSIGNED_INT, 0)


class Window(QOpenGLWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("panda3d.bullet, OpenGL 3.3, PySide2")
        self.resize(400, 400)

    def initializeGL(self):
        gl.glClearColor(0.2, 0.2, 0.2, 1)
        gl.glEnable(gl.GL_DEPTH_TEST)
        vertShaderSrc = """
            #version 330

            in vec4 aPosition;
            in vec4 aNormal;
            in vec2 aTexCoord;

            uniform mat4 uMvpMatrix;
            uniform mat4 uModelMatrix;
            uniform mat4 uNormalMatrix;

            out vec3 vPosition;
            out vec3 vNormal;
            out vec2 vTexCoord;

            void main()
            {
                gl_Position = uMvpMatrix * aPosition;
                vPosition = vec3(uModelMatrix * aPosition);
                vNormal = normalize(vec3(uNormalMatrix * aNormal));
                vTexCoord = aTexCoord;
            }
        """
        fragShaderSrc = """
            #version 330

            const vec3 lightColor = vec3(0.8, 0.8, 0.8);
            const vec3 lightPosition = vec3(5.0, 7.0, 2.0);
            const vec3 ambientLight = vec3(0.3, 0.3, 0.3);

            uniform sampler2D uSampler;

            in vec3 vPosition;
            in vec3 vNormal;
            in vec2 vTexCoord;

            void main()
            {
                vec4 color = texture2D(uSampler, vTexCoord);
                vec3 normal = normalize(vNormal);
                vec3 lightDirection = normalize(lightPosition - vPosition);
                float nDotL = max(dot(lightDirection, normal), 0.0);
                vec3 diffuse = lightColor * color.rgb * nDotL;
                vec3 ambient = ambientLight * color.rgb;
                gl_FragColor = vec4(diffuse + ambient, color.a);
            }
        """
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertShaderSrc)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragShaderSrc)
        self.program.bindAttributeLocation("aPosition", 0)
        self.program.bindAttributeLocation("aNormal", 1)
        self.program.bindAttributeLocation("aTexCoord", 2)
        self.program.link()
        self.program.bind()
        locations = Locations()
        # self.program.bind()
        locations.mvp_matrix_location = self.program.uniformLocation("uMvpMatrix")
        locations.model_matrix_location = self.program.uniformLocation("uModelMatrix")
        locations.normal_matrix_location = self.program.uniformLocation("uNormalMatrix")
        self.vert_buffers = self.initVertexBuffers("asset/cube.dae")
        self.proj_view_matrix = QMatrix4x4()
        self.proj_matrix = QMatrix4x4()
        self.view_matrix = QMatrix4x4()
        self.view_matrix.lookAt(
            QVector3D(2, 3, 5),
            QVector3D(0, 0, 0),
            QVector3D(0, 1, 0))

        self.texture = QOpenGLTexture(QOpenGLTexture.Target2D)
        self.texture.create()
        self.texture.setData(QImage("asset/cube.png"))
        self.texture.setMinMagFilters(QOpenGLTexture.Linear, QOpenGLTexture.Linear)
        self.texture.setWrapMode(QOpenGLTexture.ClampToEdge)

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, -9.81, 0))

        self.obj = Object3D(self.vert_buffers, locations, self.texture, self.world, mass=0, pos=QVector3D(0, -3, 0))
        self.obj2 = Object3D(self.vert_buffers, locations, self.texture, self.world, mass=1, pos=QVector3D(0.8, 3, 0))

        self.timer = QTimer()
        # self.timer.timeout.connect(self.animationLoop)
        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()
        self.delta_time = 0
        self.timer.start(1000 // 60)

    def animationLoop(self):
        self.delta_time = self.elapsed_timer.elapsed()
        self.elapsed_timer.restart()
        self.world.doPhysics(self.delta_time / 1000)
        self.update()

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.proj_view_matrix = self.proj_matrix * self.view_matrix
        self.obj.draw(self.program, self.proj_view_matrix)
        self.obj2.draw(self.program, self.proj_view_matrix)

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        self.proj_matrix.setToIdentity()
        self.proj_matrix.perspective(50, float(w) / float(h), 0.1, 100)

    def initVertexBuffers(self, path):
        xml_doc = QDomDocument()
        file = QFile(path)
        if not file.open(QIODevice.ReadOnly):
            print("Failed to open the file: " + path)
        xml_doc.setContent(file)
        file.close()

        vert_pos_array = []
        normal_array = []
        tex_coord_array = []
        index_array = []

        root = xml_doc.documentElement()
        dae_elem = root.firstChildElement()
        while not dae_elem.isNull():
            if dae_elem.tagName() == "library_geometries":
                geom_elem = dae_elem.firstChildElement()
                if geom_elem.tagName() == "geometry":
                    mesh_elem = geom_elem.firstChildElement()
                    if mesh_elem.tagName() == "mesh":
                        mesh_child_elem = mesh_elem.firstChildElement()
                        while not mesh_child_elem.isNull():
                            float_array_elem = mesh_child_elem.firstChildElement()
                            str_array = float_array_elem.firstChild().toText().data().split(" ")
                            if mesh_child_elem.attribute("id").endswith("-mesh-positions"):
                                vert_pos_array = list(map(float, str_array))
                            if mesh_child_elem.attribute("id").endswith("-mesh-normals"):
                                normal_array = list(map(float, str_array))
                            if mesh_child_elem.attribute("id").endswith("-mesh-map-0"):
                                tex_coord_array = list(map(float, str_array))
                            if mesh_child_elem.tagName() == "triangles" or mesh_child_elem.tagName() == "polylist":
                                p_child_elem = mesh_child_elem.firstChildElement()
                                while not p_child_elem.isNull():
                                    if p_child_elem.tagName() == "p":
                                        str_indices = p_child_elem.firstChild().toText().data().split(" ")
                                        index_array = list(map(int, str_indices))
                                    p_child_elem = p_child_elem.nextSiblingElement()
                            mesh_child_elem = mesh_child_elem.nextSiblingElement()
            dae_elem = dae_elem.nextSiblingElement()
        # print(vert_pos_array)
        # print(normal_array)
        # print(tex_coord_array)
        # print(index_array)

        num_of_attributes = 3
        vert_positions = []
        normals = []
        tex_coords = []
        for i in range(0, len(index_array), num_of_attributes):
            vert_pos_index = index_array[i + 0]
            vert_positions.append(vert_pos_array[vert_pos_index * 3 + 0])
            vert_positions.append(vert_pos_array[vert_pos_index * 3 + 1])
            vert_positions.append(vert_pos_array[vert_pos_index * 3 + 2])

            normal_index = index_array[i + 1]
            normals.append(normal_array[normal_index * 3 + 0])
            normals.append(normal_array[normal_index * 3 + 1])
            normals.append(normal_array[normal_index * 3 + 2])

            tex_coord_index = index_array[i + 2]
            tex_coords.append(tex_coord_array[tex_coord_index * 2 + 0])
            tex_coords.append(tex_coord_array[tex_coord_index * 2 + 1])
        # print(vert_positions)
        # print(normals)
        # print(tex_coords)

        output = {}

        self.vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                         0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                         -0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
                         0.5, 0.5, 0.0, 1.0, 1.0, 1.0,
                         0.0, 0.75, 0.0, 1.0, 1.0, 0.0]
        self.indices = [0, 1, 2,
                        1, 2, 3,
                        2, 3, 4]

        vert_positions = np.array(self.vertices, dtype=np.float32)
        vert_pos_buffer = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
        vert_pos_buffer.create()
        vert_pos_buffer.bind()
        vert_pos_buffer.allocate(vert_positions, len(vert_positions) * 4)

        normals = np.array(self.indices, dtype=np.float32)
        normal_buffer = QOpenGLBuffer(QOpenGLBuffer.Type.IndexBuffer)
        normal_buffer.create()
        normal_buffer.bind()
        normal_buffer.allocate(normals, len(normals) * 4)

        # tex_coords = np.array(tex_coords, dtype=np.float32)
        # tex_coord_buffer = QOpenGLBuffer()
        # tex_coord_buffer.create()
        # tex_coord_buffer.bind()
        # tex_coord_buffer.allocate(tex_coords, len(tex_coords) * 4)

        vert_buffers = VertexBuffers()
        vert_buffers.vert_pos_buffer = vert_pos_buffer
        vert_buffers.normal_buffer = normal_buffer
        # vert_buffers.tex_coord_buffer = tex_coord_buffer
        vert_buffers.amount_of_vertices = int(len(index_array) / 3)

        return vert_buffers


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    app = QApplication(sys.argv)

    format = QSurfaceFormat()
    format.setSamples(8)

    w = Window()
    w.setFormat(format)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()