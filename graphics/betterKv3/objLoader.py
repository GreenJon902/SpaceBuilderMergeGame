from os.path import abspath, dirname, join

from kivy3.loaders import OBJLoader as kv3OBJLoader

from graphics.betterKv3.waveObject import WaveObject
from lib.betterLogger import BetterLogger


class OBJLoader(BetterLogger, kv3OBJLoader):
    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        kv3OBJLoader.__init__(self, *args, **kwargs)

    def _load_meshes(self):  # Ripped from kivy3/loaders/objloader.py and edited by GJ

        wvobj = WaveObject(self)
        self.vertices = []
        self.normals = []
        self.texcoords = []
        faces_section = False

        for line in open(self.source, "r"):
            if line.startswith('#'):
                continue
            if line.startswith('s'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'o' or values[0] == 'g':
                wvobj.name = values[1]
            elif values[0] == 'mtllib':
                self.log_warning("You should not use mtllib, use the main mtl file thats loaded seperatly by "
                                 "resources/__init__.py")
                if not self.mtl_source == values[1]:
                    _obj_dir = abspath(dirname(self.source))
                    self.mtl_source = join(_obj_dir, values[1])
                    self.load_mtl()
            elif values[0] == 'usemtl':
                wvobj.mtl_name = values[1]
            elif values[0] == 'v':
                if faces_section:
                    # here we yield new mesh object
                    faces_section = False
                    yield wvobj
                    wvobj = WaveObject(self)
                v = list(map(float, values[1:4]))
                if self.swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if self.swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] == 'f':
                if not faces_section:
                    faces_section = True
                # face values
                f = values[1:]
                # triangle
                if len(f) == 3:
                    fcs = [f]
                # square, convert into two triangles
                elif len(f) == 4:
                    fcs = [
                        f[:3],
                        [f[0], f[2], f[3]]
                    ]
                for f in fcs:
                    face = []
                    texcoords = []
                    norms = []
                    for v in f:
                        w = v.split('/')
                        face.append(int(w[0]))
                        if len(w) >= 2 and len(w[1]) > 0:
                            texcoords.append(int(w[1]))
                        else:
                            texcoords.append(-1)
                        if len(w) >= 3 and len(w[2]) > 0:
                            norms.append(int(w[2]))
                        else:
                            norms.append(-1)
                    wvobj.faces.append((face, norms, texcoords))
        yield wvobj