from kivy3 import Object3D, Mesh

from graphics import graphicsConfig
from graphics.betterKv3 import OBJLoader
from lib.betterLogger import BetterLogger


class Models(BetterLogger):
    loader: OBJLoader = OBJLoader()
    mtl_file_loaded: bool = False
    _all_meshes: dict[str, list[Mesh]] = {}

    def load_materials(self, path: str):
        self.log_trace("Loading materials")

        self.loader.mtl_source = path
        self.loader.load_mtl()
        self.mtl_file_loaded = True

        self.log_debug("Loaded materials")

    def load_model(self, path: str) -> list[Mesh]:
        self.log_trace("Loading model -", path)

        if not self.mtl_file_loaded:
            self.log_warning("Loading model before materials!")

        # _obj = self.loader.load(path, swapyz=graphicsConfig.getboolean("General", "swap_object_yz"))
        meshes = self.loader.get_meshes(path, swapyz=graphicsConfig.getboolean("General", "swap_object_yz"))
        self.log_trace("Loaded model-", path)
        return meshes  # _obj

    def register_model(self, option: str, meshes: list[Mesh]):
        self._all_meshes[option] = meshes

    def get(self, section: str) -> Object3D:
        meshes = self._all_meshes[section]

        obj = Object3D()

        for mesh in meshes:
            obj.add(mesh)

        return obj


Models: Models = Models()
