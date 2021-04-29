from kivy3 import Object3D
from kivy3.loaders import OBJLoader

from lib.betterLogger import BetterLogger
from pprint import pprint


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
