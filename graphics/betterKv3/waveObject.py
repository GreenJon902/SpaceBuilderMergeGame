from os.path import abspath, dirname, join, exists

from kivy.core.image import Image
from kivy3 import Geometry, Material, Face3, Vector2, Mesh
from kivy3.loaders.objloader import WaveObject as kv3WaveObject, folder as objLoader_folder

from lib.betterLogger import BetterLogger


class WaveObject(BetterLogger, kv3WaveObject):
    def __init__(self, loader,  name=''):
        self.name = name
        self.faces = []
        self.loader = loader
        self.mtl_name = None

        BetterLogger.__init__(self)

        from resources import Textures  # Circular import fix
        self.textures = Textures

        kv3WaveObject.__init__(self, loader,  name='')

    def convert_to_mesh(self, vertex_format=None):  # Ripped from kivy3/loaders/objloader.py and edited by GJ
        """Converts data gotten from the .obj definition
        file and create Kivy3 Mesh object which may be used
        for drawing object in the scene
        """

        geometry = Geometry()
        material = Material()
        mtl_dirname = abspath(dirname(self.loader.mtl_source))  # We don't need this as we arnt loading any images
        # but just in case we keep it

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
                _k = self._mtl_map.get(k, None)
                if k in ["map_Kd", ]:
                    self.log_warning("the tag map_kd should not be used as a material, use map_id and give the texture"
                                     " id (ini section and option)")
                    map_path = join(mtl_dirname, v[0])
                    if not exists(map_path):
                        msg = u'Texture not found <{}>'
                        self.log_warning(msg.format(map_path))
                        continue
                    tex = Image(map_path).texture
                    material.map = tex
                    continue
                if k in ["map_id", ]:

                    tex = self.textures.get("Materials", str(v[0]))
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
            self.log_warning("No material given or used wrong name -", self.mtl_name, "(if nothing here then you "
                                                                                      "provided no mtl file)")
            material.map = Image(objLoader_folder + '/empty.png').texture
            material.texture_ratio = 0.0
        mesh = Mesh(geometry, material)
        return mesh