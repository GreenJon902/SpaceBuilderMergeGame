from kivy3 import Geometry, Vector2, Face3, Mesh
from kivy3.loaders import objloader

from resources.materials import Materials


class WaveObject(objloader.WaveObject):
    def convert_to_mesh(self, vertex_format=None):
        """Converts data gotten from the .obj definition
        file and create Kivy3 Mesh object which may be used
        for drawing object in the scene
        """

        geometry = Geometry()

        v_idx = 0
        # create geometry for mesh
        for f in self.faces:
            verts = f[0]
            norms = f[1]
            tcs = f[2]
            face3 = Face3(0, 0, 0)
            for i, e in enumerate(['a', 'b', 'c']):
                # get normal components
                n = (0.0, 0.0, 0.0)
                if norms[i] != -1:
                    n = self.loader.normals[norms[i] - 1]
                face3.vertex_normals.append(n)

                # get vertex components
                v = self.loader.vertices[verts[i] - 1]
                geometry.vertices.append(v)
                setattr(face3, e, v_idx)
                v_idx += 1

                # get texture coordinate components
                t = (0.0, 0.0)
                if tcs[i] != -1:
                    t = self.loader.texcoords[tcs[i] - 1]
                tc = Vector2(t[0], 1. - t[1])
                geometry.face_vertex_uvs[0].append(tc)

            geometry.faces.append(face3)


        m = Materials.get(self.mtl_name)
        print(m, m.map)

        mesh = Mesh(geometry, m)
        return mesh


class OBJLoader(objloader.OBJLoader):
    def _load_meshes(self):

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
