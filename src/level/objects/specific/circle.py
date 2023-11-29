# -*- coding: utf-8 -*-
"""
Created on 2023/11/28

@author: brassbeat
"""
import dataclasses
import logging
from dataclasses import dataclass
from typing import Self

from level.level_reader import PeggleDataReader
from level.level_writer import PeggleDataWriter
from level.objects.flags import CircleFlag


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class Circle:
    radius: float
    x: float | None = None
    y: float | None = None
    TYPE_VALUE: int = dataclasses.field(default=5, init=False, repr=False)

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader) -> Self:
        _logger.debug("reading in circle flags...")
        flag = CircleFlag(f.read_bitfield(1))

        if CircleFlag.HAS_FIXED_COORDINATES in flag:
            _logger.debug("Reading in coordinates...")
            x, y = f.read_float(), f.read_float()
        else:
            x, y = None, None

        _logger.debug("Reading in radius...")
        radius = f.read_float()

        return cls(
                x=x,
                y=y,
                radius=radius
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        ...


def main():
    pass


if __name__ == "__main__":
    main()
