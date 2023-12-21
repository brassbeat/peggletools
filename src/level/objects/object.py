# -*- coding: utf-8 -*-
"""
Created on 2023/11/27

@author: brassbeat
"""
import dataclasses
import functools
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

        return max(map(lambda obj: obj.complexity, subobjects_with_complexity))

    # ahhh frick this is too arcane
    def get_unresolved_link_ids(self) -> Iterator[tuple[int, Callable[[Any], None]]]:
        """
        ...
        :return: Iterator yielding (`id`, `setter`) tuples, where `id` is the link id that needs to be looked up,
        and `setter` is a setter function for its corresponding attribute.
        """
        # this needs to avoid yielding an attribute slot and then rereading it
        # sorry future brass (not really)
        if self.generic_data.movement_link_id is not None:
            yield self.generic_data.movement_link_id, functools.partial(setattr, self, "movement_data")
        elif self.movement_data is not None:  # grr
            movement = self.movement_data
            while movement.submovement_ is not None:
                movement = movement.submovement_

            if movement.submovement_link_id is not None:
                yield movement.submovement_link_id, self.link_submovement

    def get_linked_entries(self) -> Iterator[tuple[Any, Callable[[int], None]]]:
        """
        ...
        :return: Iterator yielding (`obj`, `setter`) tuples, where `obj` is the object whose link id needs to be
        looked up,
        and `setter` is a setter function for its corresponding attribute.
        """
        _logger.debug("Searching for submovement...")
        if (movement := self.movement_data) is not None:
            _logger.debug("Found movement data...")
            if movement.submovement_ is not None:
                yield movement.submovement_, self.unlink_submovement

    def link_submovement(self, movement: Movement):
        assert isinstance(movement, Movement)

        parent_movement = self.movement_data
        while parent_movement.submovement_ is not None:
            parent_movement = parent_movement.submovement_

        parent_movement.submovement_ = movement
        parent_movement.submovement_link_id = None

    def unlink_submovement(self, link_id: int):
        _logger.debug(f"Unlinking submovement ({link_id=})..")
        self.movement_data.submovement_ = None
        self.movement_data.submovement_link_id = link_id

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader, **kwargs) -> Self:
        _logger.info("==========Reading in new object==========")
        _logger.debug(f"Staring on position {f.position}")
        _ = f.read_int()
        _logger.debug("Reading in object type...")
        object_type = _OBJECT_TYPES.get(f.read_int(), InvalidPeggleObject)
        _logger.debug(f"Found object type: {object_type.__name__}")

        generic_data = GenericObject.read_data(file_version, f, **kwargs)
        specific_data = object_type.read_data(file_version, f, **kwargs)

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
