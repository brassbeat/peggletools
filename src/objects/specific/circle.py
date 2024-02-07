# -*- coding: utf-8 -*-
"""
Created on 2023/11/28

@author: brassbeat
"""
import dataclasses
import functools as ft
import logging
from collections import deque
from dataclasses import dataclass
from typing import Self

from level.level_reader import PeggleDataReader
from level.level_writer import PeggleDataWriter
from objects.flags import CircleFlag, CircleExtendedFlag
from objects.point_2d import Point2D

_EXTENDED_FLAG_MIN_VERSION = int("0x52", 16)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class Circle:
    radius: float
    
    has_normal_physics: bool
    position: Point2D | None
    unknown_2: bool
    unknown_3: bool
    unknown_4: bool
    unknown_5: bool
    unknown_6: bool
    unknown_7: bool
    
    extended_flag: CircleExtendedFlag | None
    TYPE_VALUE: int = dataclasses.field(default=5, init=False, repr=False)

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader, **kwargs) -> Self:
        _logger.debug("reading in circle flags...")
        flag = CircleFlag(f.read_bitfield(1))

        if file_version >= _EXTENDED_FLAG_MIN_VERSION:
            _logger.debug("reading in extended circle flags...")
            extended_flag = CircleExtendedFlag(f.read_bitfield(1))
        else:
            extended_flag = None

        has_normal_physics = CircleFlag.HAS_NORMAL_PHYSICS in flag

        if CircleFlag.HAS_FIXED_COORDINATES in flag:
            _logger.debug("Reading in coordinates...")
            position = Point2D(f.read_float(), f.read_float())
        else:
            position = None

        unknown_2 = CircleFlag.UNKNOWN_2 in flag
        unknown_3 = CircleFlag.UNKNOWN_3 in flag
        unknown_4 = CircleFlag.UNKNOWN_4 in flag
        unknown_5 = CircleFlag.UNKNOWN_5 in flag
        unknown_6 = CircleFlag.UNKNOWN_6 in flag
        unknown_7 = CircleFlag.UNKNOWN_7 in flag

        _logger.debug("Reading in radius...")
        radius = f.read_float()

        return cls(
                has_normal_physics=has_normal_physics,
                position=position,
                unknown_2=unknown_2,
                unknown_3=unknown_3,
                unknown_4=unknown_4,
                unknown_5=unknown_5,
                unknown_6=unknown_6,
                unknown_7=unknown_7,
                extended_flag=extended_flag,
                radius=radius
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        flag = CircleFlag(0)
        write_queue = deque()

        if self.has_normal_physics:
            flag |= CircleFlag.HAS_NORMAL_PHYSICS
        if self.position is not None:
            flag |= CircleFlag.HAS_FIXED_COORDINATES
            write_queue.append(ft.partial(f.write_float, self.position.x))
            write_queue.append(ft.partial(f.write_float, self.position.y))
        if self.unknown_2:
            flag |= CircleFlag.UNKNOWN_2
        if self.unknown_3:
            flag |= CircleFlag.UNKNOWN_3
        if self.unknown_4:
            flag |= CircleFlag.UNKNOWN_4
        if self.unknown_5:
            flag |= CircleFlag.UNKNOWN_5
        if self.unknown_6:
            flag |= CircleFlag.UNKNOWN_6
        if self.unknown_7:
            flag |= CircleFlag.UNKNOWN_7

        f.write_bitfield(flag, 1)

        if file_version >= _EXTENDED_FLAG_MIN_VERSION:
            f.write_bitfield(self.extended_flag, 1)

        for write_action in write_queue:
            write_action()

        f.write_float(self.radius)


def main():
    pass


if __name__ == "__main__":
    main()
