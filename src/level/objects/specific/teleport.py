# -*- coding: utf-8 -*-
"""
Created on 2023/12/26

@author: brassbeat
"""
import dataclasses
import functools as ft
import logging
from collections import deque
from dataclasses import dataclass
from typing import Self, Callable

from level.level_reader import PeggleDataReader
from level.level_writer import PeggleDataWriter
from level.objects.flags import TeleportFlag
from level.objects.point_2d import Point2D
from level.protocols import PeggleObjectData

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class Teleport:
    width: int
    height: int
    unknown_0: bool
    unknown_1: int | None
    entry_coordinates: Point2D | None
    unknown_3: int | None
    subobject: PeggleObjectData | None
    subobject_link_id: int | None
    unknown_5: int | None
    unknown_6: Point2D | None
    unknown_7: bool

    TYPE_VALUE: int = dataclasses.field(default=8, init=False, repr=False)

    @classmethod
    def read_data(
            cls,
            file_version: int,
            f: PeggleDataReader,
            *,
            object_callback: Callable[[int, PeggleDataReader], PeggleObjectData],
            **kwargs
    ) -> Self:
        _logger.debug("Reading in teleport flags...")
        flag = TeleportFlag(f.read_bitfield(1))

        _logger.debug("Reading in width...")
        width = f.read_int()
        _logger.debug("Reading in height...")
        height = f.read_int()

        unknown_0 = TeleportFlag.UNKNOWN_0 in flag
        if TeleportFlag.UNKNOWN_1 in flag:
            _logger.debug("Reading in unknown 1...")
            unknown_1 = f.read_short()
        else:
            unknown_1 = None
        if TeleportFlag.UNKNOWN_3 in flag:
            _logger.debug("Reading in unknown 3...")
            unknown_3 = f.read_int()
        else:
            unknown_3 = None
        if TeleportFlag.UNKNOWN_5 in flag:
            _logger.debug("Reading in unknown 5...")
            unknown_5 = f.read_int()
        else:
            unknown_5 = None

        if TeleportFlag.HAS_EXIT_SUBOBJECT in flag:
            _logger.debug("Reading in subobject...")
            subobject = object_callback(file_version, f)
            subobject_link_id = None
        else:
            subobject_link_id = None
            subobject = None

        if TeleportFlag.HAS_ENTRY_COORDINATES in flag:
            _logger.debug("Reading in entry coordinates...")
            entry_coordinates = Point2D(f.read_float(), f.read_float())
        else:
            entry_coordinates = None
        if TeleportFlag.UNKNOWN_6 in flag:
            _logger.debug("Reading in unknown 6...")
            unknown_6 = Point2D(f.read_float(), f.read_float())
        else:
            unknown_6 = None
        unknown_7 = TeleportFlag.UNKNOWN_7 in flag

        return cls(
                width=width,
                height=height,
                unknown_0=unknown_0,
                unknown_1=unknown_1,
                entry_coordinates=entry_coordinates,
                unknown_3=unknown_3,
                subobject=subobject,
                subobject_link_id=subobject_link_id,
                unknown_5=unknown_5,
                unknown_6=unknown_6,
                unknown_7=unknown_7,
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        write_queue: deque[Callable[[], None]] = deque()

        flag = TeleportFlag(0)

        if self.unknown_0:
            flag |= TeleportFlag.UNKNOWN_0
        if self.unknown_1 is not None:
            flag |= TeleportFlag.UNKNOWN_1
            write_queue.append(ft.partial(f.write_short, self.unknown_1))
        if self.unknown_3 is not None:
            flag |= TeleportFlag.UNKNOWN_3
            write_queue.append(ft.partial(f.write_int, self.unknown_3))
        if self.unknown_5 is not None:
            flag |= TeleportFlag.UNKNOWN_5
            write_queue.append(ft.partial(f.write_int, self.unknown_5))
        if self.subobject_link_id is not None:
            flag |= TeleportFlag.HAS_EXIT_SUBOBJECT
            write_queue.append(ft.partial(f.write_int, self.subobject_link_id))
        if self.entry_coordinates is not None:
            flag |= TeleportFlag.HAS_ENTRY_COORDINATES
            write_queue.append(ft.partial(f.write_float, self.entry_coordinates.x))
            write_queue.append(ft.partial(f.write_float, self.entry_coordinates.y))
        if self.unknown_6 is not None:
            flag |= TeleportFlag.UNKNOWN_6
            write_queue.append(ft.partial(f.write_float, self.unknown_6.x))
            write_queue.append(ft.partial(f.write_float, self.unknown_6.y))
        if self.unknown_7:
            flag |= TeleportFlag.UNKNOWN_7

        f.write_bitfield(flag, 1)
        f.write_int(self.width)
        f.write_int(self.height)

        for write_action in write_queue:
            write_action()
