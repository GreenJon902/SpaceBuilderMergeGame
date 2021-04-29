from os.path import abspath, dirname, join, exists

from kivy.core.image import Image
from kivy3 import Object3D, Geometry, Material, Face3, Vector2, Mesh
from kivy3.loaders import OBJLoader as kv3OBJLoader
from kivy3.loaders.objloader import WaveObject as kv3WaveObject, folder as objLoader_folder

from lib.betterLogger import BetterLogger
from pprint import pprint

from resources.textures import Textures




class WaveObject(BetterLogger, kv3WaveObject):
    def __init__(self, loader, *args,  name='', **kwargs):
        self.name = name
        self.faces = []
        self.loader = loader
        self.mtl_name = None

        BetterLogger.__init__(self)

    def convert_to_mesh(self, vertex_format=None):  # Ripped from kivy3/loaders/objloader.py and edited by GJ
        """Converts data gotten from the .obj definition
        file and create Kivy3 Mesh object which may be used
        for drawing object in the scene
        """

        geometry = Geometry()
        material = Material()
        mtl_dirname = abspath(dirname(self.loader.mtl_source))  # We don't need this as we arnt loading any images
        # but just incase we keep it

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

        # apply material for object
        if self.mtl_name in self.loader.mtl_contents:
            raw_material = self.loader.mtl_contents[self.mtl_name]
            # shader ignores values
            zeros = ['0', '0.0', '0.00', '0.000', '0.0000',
                     '0.00000', '0.000000']
            for k, v in raw_material.items():
                print("hihihi", v)
                _k = self._mtl_map.get(k, None)
                if k in ["map_Kd", ]:
                    self.log_warning("the tag map_kd should not be used as a material, use map_id and give the texture"
                                     " id (ini section and option)")
                    map_path = join(mtl_dirname, v[0])
                    if not exists(map_path):
                        msg = u'Texture not found <{}>'
                        self.log_warning.warning(msg.format(map_path))
                        continue
                    tex = Image(map_path).texture
                    material.map = tex
                    continue
                if k in ["map_id", ]:

                    tex = Textures.get("Materials", str(v[0]))
                    material.map = tex

                if _k:
                    if len(v) == 1:
                        v[0] = '0.000001' if v[0] in zeros else v[0]
                        v = float(v[0])
                        if k == 'Tr':
                            v = 1. - v
                        setattr(material, _k, v)
                    else:
                        v = list(map(lambda x: float(x), v))
                        setattr(material, _k, v)

        if not material.map:
            material.map = Image(objLoader_folder + '/empty.png').texture
            material.texture_ratio = 0.0
        mesh = Mesh(geometry, material)
        return mesh


class OBJLoader(kv3OBJLoader):
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
                if not self.mtl_source:
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



class Models(BetterLogger):
    loader: OBJLoader = OBJLoader()
    mtl_file_loaded: bool = False
    _models: dict[str, Object3D] = {}

    def load_materials(self, path: str):
        self.log_trace("Loading materials")

        self.loader.mtl_source = path
        self.loader.load_mtl()
        self.mtl_file_loaded = True

        self.log_debug("Loaded materials")

    def load_model(self, path: str) -> Object3D:
        self.log_trace("Loading model -", path)
        print(self.loader.mtl_source)
        pprint(self.loader.mtl_contents)

        if not self.mtl_file_loaded:
            self.log_warning("Loading model before materials!")

        obj = self.loader.load(path)
        self.log_trace("Loaded model-", path)
        return obj

    def register_model(self, option: str, model: Object3D):
        print("hi", option, model)
        self._models[option] = model
        print(self._models)

    def get(self, section: str) -> Object3D:
        return self._models[section]


Models: Models = Models()
