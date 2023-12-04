# -*- coding: utf-8 -*-
"""
Created on 2023/11/27

@author: brassbeat
"""
import dataclasses
import json
import logging
from dataclasses import dataclass
from typing import Self, TextIO

from level.objects.specific.brick import Brick
from level.objects.specific.circle import Circle
from level.objects.specific.invalid import InvalidPeggleObject
from level.objects.specific.polygon import Polygon
from level.objects.specific.rod import Rod
from ..level_reader import PeggleDataReader
from ..level_writer import PeggleDataWriter
from .generic import GenericObject
from ..protocols import SpecificObjectData


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


_OBJECT_TYPES: dict[int, type[SpecificObjectData]] = {
    object_data_type.TYPE_VALUE: object_data_type
    for object_data_type
    in [Circle, Brick, Rod, Polygon]
}


@dataclass
class PeggleObject:
    generic_data: GenericObject
    specific_data: SpecificObjectData

    @property
    def movement_data(self) -> ...:
        return self.generic_data.movement_data

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader) -> Self:
        _ = f.read_int()
        _logger.debug("Reading in object type...")
        object_type = _OBJECT_TYPES.get(f.read_int(), InvalidPeggleObject)
        _logger.debug(f"Found object type: {object_type.__name__}")

        generic_data = GenericObject.read_data(file_version, f)
        specific_data = object_type.read_data(file_version, f)

        return cls(generic_data, specific_data)

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        f.write_int(1)
        f.write_int(self.specific_data.TYPE_VALUE)
        self.generic_data.write_data(file_version, f)
        self.specific_data.write_data(file_version, f)

    def export_json(self, f: TextIO):
        json.dump(dataclasses.asdict(self), f, indent=2)


def main():
    pass


if __name__ == "__main__":
    main()
