import re
import math
import numpy as np

class Model(object):
    def __init__(self):
        self.vertex = [] #type:np.Arrayterator
        self.indices = [[], [], []] #type:np.Arrayterator
        self.normal = [] #type:np.Arrayterator
        self.tex_coord = [] #type:np.Arrayterator
        self.amount_of_vertices = 0
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
                for _t in t.split(' '):
                    if not str(_t).isalpha():
                        instance.tex_coord.append(_t)
            instance.amount_of_vertices = int(len(instance.vertex)/3)
            id = re.search("f [\s\S]*", file).group()
            for i in id.split("\n"):
                if not i.startswith('f'):
                    continue
                for _i in i.split(' '):
                    if _i != "f":
                        instance.indices[0].append(_i.split('/')[0])
                        instance.indices[1].append(_i.split('/')[1])
                        instance.indices[2].append(_i.split('/')[2])
        instance.make_array()
        return instance

    def make_array(self):
        self.indices = np.array(self.indices, dtype=np.uint32)
        self.vertex = np.array(self.vertex, dtype=np.float32)
        self.normal = np.array(self.normal, dtype=np.float32)
        self.tex_coord = np.array(self.tex_coord, dtype=np.float32)


if __name__ == "__main__":
    mod = Model.make_model("test.obj")
    print(mod.vertex.size/3)
    print(mod.normal.size/3)
    print(mod.tex_coord.size/3)
    print(mod.indices[0])
