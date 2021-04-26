import os
from os.path import abspath

from kivy.core.image import Image as CoreImage
from kivy3 import Geometry, Material, Vector2, Face3

from lib.betterLogger import BetterLogger
from resources.textures import EmptyClass


class Materials(BetterLogger):
    __log_name__ = "Materials"
    _mtl_contents: dict = {}

    def register_mtl(self, mtl_str: str):
        self.log_trace("Registering mtl file")

        for line in mtl_str.splitlines():
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'newmtl':
                mtl = self._mtl_contents[values[1]] = {}
                continue
            elif mtl is None:
                raise ValueError("mtl doesn't start with newmtl statement")
            mtl[values[0]] = values[1:]


        for mtl in self._mtl_contents:
            material = Material()

            for k in self._mtl_contents[mtl]:
                setattr(material, k, self._mtl_contents[mtl][k])


            last = self
            parts = str(mtl).split(".")
            parts.pop(0)
            parts.pop(-1)

            for part in parts:
                setattr(last, part, EmptyClass)
                last = getattr(last, part)

            part = str(mtl).split(".")[-1]
            setattr(last, part, material)



    def register_image(self, section: str, option: str, core_image: CoreImage):
        self.log_trace("Registering material", core_image, "for", section, option)

        parts = str(option).split(".")
        last: Material = self

        for part in parts:
            last = getattr(last, str(part).title())

        last.map = core_image



Materials: Materials = Materials()
