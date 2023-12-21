# -*- coding: utf-8 -*-
"""
Created on _

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
from level.objects.flags import PolygonFlag, PolygonFlagExtended
from level.objects.point_2d import Point2D

_FLAG_EXTENDED_MIN_VERSION = int("0x23", 16)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class Polygon:
    vertices: list[Point2D]

    unknown_0: bool
    normal_direction: int | None
    rotation_angle: float | None
    unknown_3: float | None
    position: Point2D | None
    scale: float | None
    unknown_6: bool
    unknown_7: bool

    unknown_8: int | None
    grow_type: int | None
    unknown_10: bool
    unknown_11: bool
    unknown_12: bool
    unknown_13: bool
    unknown_14: bool
    unknown_15: bool

    TYPE_VALUE: int = dataclasses.field(default=3, init=False, repr=False)

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader, **kwargs) -> Self:
        flag = PolygonFlag(f.read_bitfield(1))
        if file_version >= _FLAG_EXTENDED_MIN_VERSION:
            flag_extended = PolygonFlagExtended(f.read_bitfield(1))

        unknown_0 = PolygonFlag.UNKNOWN_0 in flag
        if PolygonFlag.HAS_ROTATION_VALUE in flag:
            rotation_angle = f.read_float()
        else:
            rotation_angle = None
        if PolygonFlag.UNKNOWN_3 in flag:
            unknown_3 = f.read_float()
        else:
            unknown_3 = None
        if PolygonFlag.HAS_SCALE in flag:
            scale = f.read_float()
        else:
            scale = None
        if PolygonFlag.HAS_NORMAL_DIRECTION in flag:
            normal_direction = f.read_byte()
        else:
            normal_direction = None
        if PolygonFlag.HAS_FIXED_COORDINATES in flag:
            position = Point2D(f.read_float(), f.read_float())
        else:
            position = None
        unknown_6 = PolygonFlag.UNKNOWN_6 in flag
        unknown_7 = PolygonFlag.UNKNOWN_7 in flag

        vertex_count = f.read_int()
        vertices = [Point2D(f.read_float(), f.read_float()) for _ in range(vertex_count)]

        if file_version < _FLAG_EXTENDED_MIN_VERSION:
            unknown_8 = None
            grow_type = None
            unknown_10 = False
            unknown_11 = False
            unknown_12 = False
            unknown_13 = False
            unknown_14 = False
            unknown_15 = False
        else:
            # noinspection PyUnboundLocalVariable
            if PolygonFlagExtended.UNKNOWN_8 in flag_extended:
                unknown_8 = f.read_byte()
            else:
                unknown_8 = None
            if PolygonFlagExtended.HAS_GROW_TYPE in flag_extended:
                grow_type = f.read_int()
            else:
                grow_type = None

            unknown_10 = PolygonFlagExtended.UNKNOWN_10 in flag_extended
            unknown_11 = PolygonFlagExtended.UNKNOWN_11 in flag_extended
            unknown_12 = PolygonFlagExtended.UNKNOWN_12 in flag_extended
            unknown_13 = PolygonFlagExtended.UNKNOWN_13 in flag_extended
            unknown_14 = PolygonFlagExtended.UNKNOWN_14 in flag_extended
            unknown_15 = PolygonFlagExtended.UNKNOWN_15 in flag_extended

        return cls(
                vertices=vertices,
                unknown_0=unknown_0,
                normal_direction=normal_direction,
                rotation_angle=rotation_angle,
                unknown_3=unknown_3,
                position=position,
                scale=scale,
                unknown_6=unknown_6,
                unknown_7=unknown_7,
                unknown_8=unknown_8,
                grow_type=grow_type,
                unknown_10=unknown_10,
                unknown_11=unknown_11,
                unknown_12=unknown_12,
                unknown_13=unknown_13,
                unknown_14=unknown_14,
                unknown_15=unknown_15,
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        write_queue: deque[Callable[[], None]] = deque()

        flag = PolygonFlag(0)

        if self.unknown_0:
            flag |= PolygonFlag.UNKNOWN_0
        if self.rotation_angle is not None:
            flag |= PolygonFlag.HAS_ROTATION_VALUE
            write_queue.append(ft.partial(f.write_float, self.rotation_angle))
        if self.unknown_3 is not None:
            flag |= PolygonFlag.UNKNOWN_3
            write_queue.append(ft.partial(f.write_float, self.unknown_3))
        if self.scale is not None:
            flag |= PolygonFlag.HAS_SCALE
            write_queue.append(ft.partial(f.write_float, self.scale))
        if self.normal_direction is not None:
            flag |= PolygonFlag.HAS_NORMAL_DIRECTION
            write_queue.append(ft.partial(f.write_byte, self.normal_direction))
        if self.position is not None:
            flag |= PolygonFlag.HAS_FIXED_COORDINATES
            write_queue.append(ft.partial(f.write_float, self.position.x))
            write_queue.append(ft.partial(f.write_float, self.position.y))

        f.write_bitfield(flag, 1)

        write_queue.append(ft.partial(f.write_int, len(self.vertices)))
        for vertex in self.vertices:
            write_queue.append(ft.partial(f.write_float, vertex.x))
            write_queue.append(ft.partial(f.write_float, vertex.y))

        if file_version >= _FLAG_EXTENDED_MIN_VERSION:
            flag_extended = PolygonFlagExtended(0)

            if self.unknown_8 is not None:
                flag_extended |= PolygonFlagExtended.UNKNOWN_8
                write_queue.append(ft.partial(f.write_byte, self.unknown_8))
            if self.grow_type is not None:
                flag_extended |= PolygonFlagExtended.HAS_GROW_TYPE
                write_queue.append(ft.partial(f.write_int, self.grow_type))
            if self.unknown_10:
                flag_extended |= PolygonFlagExtended.UNKNOWN_10
            if self.unknown_11:
                flag_extended |= PolygonFlagExtended.UNKNOWN_11
            if self.unknown_12:
                flag_extended |= PolygonFlagExtended.UNKNOWN_12
            if self.unknown_13:
                flag_extended |= PolygonFlagExtended.UNKNOWN_13
            if self.unknown_14:
                flag_extended |= PolygonFlagExtended.UNKNOWN_14
            if self.unknown_15:
                flag_extended |= PolygonFlagExtended.UNKNOWN_15

            f.write_bitfield(flag_extended, 1)

        for write_action in write_queue:
            write_action()
