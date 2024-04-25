import re
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Model(object):
    def __init__(self):
        self.vertex = [] #type:np.Arrayterator
        self.indices = [[], [], []] #type:np.Arrayterator
        self.normal = [] #type:np.Arrayterator
        self.tex_coord = [] #type:np.Arrayterator
        self.component = [] #type:np.Arrayterator
        self.amount_of_vertices = 0
        self.VAO = None
        pass

    @classmethod
    def make_model(cls, obj_file=None):
        # instance = object.__new__(cls)
        # return instance
        instance = cls()
        with open(obj_file, "r") as f:

            file = f.read()
            vertex = re.search("\n\nv[\s\S]*?#", file).group()
            for v in vertex.split("\n"):
                if not v.startswith('v'):
                    continue
                for _v in v.split(' '):
                    if not str(_v).isalpha():
                        instance.vertex.append(_v)
            normal = re.search("\n\nvn[\s\S]*?#", file).group()
            for n in normal.split("\n"):
                if not n.startswith('vn'):
                    continue
                for _n in n.split(' '):
                    if not str(_n).isalpha():
                        instance.normal.append(_n)
            tex = re.search("\n\nvt[\s\S]*?#", file).group()
            for t in tex.split("\n"):
                if not t.startswith('vt'):
                    continue
                for index, _t in enumerate(t.split(' ')):
                    if index == 3:
                        continue
                    if not str(_t).isalpha():
                        instance.tex_coord.append(_t)
            instance.amount_of_vertices = int(len(instance.vertex)/3)
            id = re.search("f [\s\S]*", file).group()
            for i in id.split("\n"):
                if not i.startswith('f'):
                    continue
                segment = i.split(' ')
                if len(segment) > 4:
                    new_seg = [segment[1], segment[2], segment[3], segment[1], segment[3], segment[4]]
                    for _ii in new_seg:
                        instance.indices[0].append(int(_ii.split('/')[0])-1)
                        instance.indices[1].append(int(_ii.split('/')[1])-1)
                        instance.indices[2].append(int(_ii.split('/')[2])-1)
                else:
                    for _i in segment:
                        if _i != "f":
                            instance.indices[0].append(int(_i.split('/')[0])-1)
                            instance.indices[1].append(int(_i.split('/')[1])-1)
                            instance.indices[2].append(int(_i.split('/')[2])-1)

        for vert in instance.indices[0]:
            # vert += 1
            instance.component.append(instance.vertex[vert*3])
            instance.component.append(instance.vertex[vert*3+1])
            instance.component.append(instance.vertex[vert*3+2])
            instance.component.append(instance.normal[vert*3])
            instance.component.append(instance.normal[vert*3+1])
            instance.component.append(instance.normal[vert*3+2])
            instance.component.append(instance.tex_coord[vert*2])
            instance.component.append(instance.tex_coord[vert*2+1])

        instance.make_array()
        instance.VAO = glGenVertexArrays(1)
        return instance

    def make_array(self):
        for index, i in enumerate(self.indices):
            self.indices[index] = np.array(i, dtype=np.uint32)
        self.vertex = np.array(self.vertex, dtype=np.float32)/100
        self.normal = np.array(self.normal, dtype=np.float32)
        self.tex_coord = np.array(self.tex_coord, dtype=np.float32)
        self.component = np.array(self.component, dtype=np.float32)
        print(self.component)


    def gen_buffer(self, shader):

        shader.bind()
        glBindVertexArray(self.VAO)

        VBO_pos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_pos)
        glBufferData(GL_ARRAY_BUFFER, self.component.nbytes, self.component, GL_STATIC_DRAW)

        # EBO_pos = glGenBuffers(1)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_pos)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices[0].nbytes, self.indices[0], GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.component.itemsize * 8, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, self.component.itemsize * 8, ctypes.c_void_p(12))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self.component.itemsize * 8, ctypes.c_void_p(24))

        glBindBuffer(GL_ARRAY_BUFFER, 0)


        # VBO_nor = glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER, VBO_nor)
        # glBufferData(GL_ARRAY_BUFFER, self.normal.nbytes, self.normal, GL_STATIC_DRAW)
        #
        # glEnableVertexAttribArray(1)
        # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, self.vertex.itemsize*3, ctypes.c_void_p(0))
        #
        # VBO_tex = glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER, VBO_tex)
        # glBufferData(GL_ARRAY_BUFFER, self.tex_coord.nbytes, self.tex_coord, GL_STATIC_DRAW)
        #
        # EBO_tex = glGenBuffers(1)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_tex)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices[1].nbytes, self.indices[1], GL_STATIC_DRAW)
        #
        # glEnableVertexAttribArray(2)
        # glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self.vertex.itemsize*2, ctypes.c_void_p(0))

if __name__ == "__main__":
    mod = Model.make_model("test.obj")

    # print(mod.vertex.size/3)
    # print(mod.normal.size/3)
    print(mod.tex_coord.size/2)
    print(mod.tex_coord)
