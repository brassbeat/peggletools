# -*- coding: utf-8 -*-
"""
Created on 2023/11/27

@author: brassbeat
"""
import dataclasses
import functools
import itertools
import json
import logging
from collections.abc import Iterator, Callable
from dataclasses import dataclass
from typing import Self, TextIO, Any

from level.objects.movement_data import Movement
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
    is_parent_object: bool = True

    @property
    def movement_data(self) -> Movement | None:
        return self.generic_data.movement_data

    @movement_data.setter
    def movement_data(self, value):
        if value:
            self.generic_data.movement_link_id = None
        self.generic_data.movement_data = value

    # noinspection PyUnreachableCode
    @property
    def subobject_data(self) -> Self | None:
        return None

        if not isinstance(self.specific_data, ...):
            return None

        ...

    @property
    def complexity(self) -> int:
        subobjects_with_complexity = []

        if self.movement_data is not None:
            subobjects_with_complexity.append(self.movement_data)

        if self.subobject_data is not None:
            subobjects_with_complexity.append(self.movement_data)

        if not subobjects_with_complexity:
            return 0

        return 1 + max(map(lambda obj: obj.complexity, subobjects_with_complexity))

    def get_linked_entries(self) -> Iterator[tuple[Any, Callable[[int], None]]]:
        """
        ...
        :return: Iterator yielding (`obj`, `setter`) tuples, where `obj` is the object whose link id needs to be
        looked up,
        and `setter` is a setter function for its corresponding attribute.
        """
        _logger.debug("Searching for submovement to unlink...")
        if (movement := self.movement_data) is not None:
            _logger.debug("Found movement data...")
            if movement.submovement_ is not None:
                yield movement.submovement_, self.unlink_submovement

    def unlink_submovement(self, link_id: int):
        _logger.debug(f"Unlinking submovement ({link_id=})..")
        self.movement_data.submovement_ = None
        self.movement_data.submovement_link_id = link_id

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader, **kwargs) -> Self:
        _logger.debug("Reading in object type...")
        object_type = _OBJECT_TYPES.get(f.read_int(), InvalidPeggleObject)
        _logger.debug(f"Found object type: {object_type.__name__}")

        generic_data = GenericObject.read_data(file_version, f, **kwargs)
        specific_data = object_type.read_data(file_version, f, **kwargs)

        return cls(generic_data, specific_data)

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        f.write_int(self.specific_data.TYPE_VALUE)
        self.generic_data.write_data(file_version, f)
        self.specific_data.write_data(file_version, f)

    def export_json(self, f: TextIO):
        json.dump(dataclasses.asdict(self), f, indent=2)


def main():
    pass


if __name__ == "__main__":
    main()
