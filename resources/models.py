from kivy3.loaders import OBJLoader

from lib.betterLogger import BetterLogger


class Models(BetterLogger):
    loader: OBJLoader = OBJLoader()

    def register_materials(self, materials_sting: str):
        self.log_trace("Loading materials")
        self.log_debug("Loaded materials")


Models: Models = Models()
