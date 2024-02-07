# -*- coding: utf-8 -*-
"""
Created on 2023/12/02

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
from objects.flags import BrickFlagA, BrickFlagAExtended, BrickFlagB
from objects.point_2d import Point2D

_DEFAULT_CURVE_POINTS = 2

_DEFAULT_WIDTH = 20.0

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

_FLAG_A_EXTENDED_MIN_VERSION = int("0x23", 16)


@dataclass
class Brick:
    length: float
    rotation_angle: float
    unknown_bytes: list[int]

    unknown_a0: bool
    unknown_a1: int | None
    unknown_a2: float | None
    unknown_a3: float | None
    position: Point2D | None
    unknown_a5: float | None
    unknown_a6: bool
    unknown_a7: bool
    unknown_a8: int | None
    unknown_a9: int | None
    unknown_a10: int | None
    unknown_a11: bool
    unknown_a12: bool
    unknown_a13: bool
    unknown_a14: bool
    unknown_a15: bool

    unknown_b0: bool
    unknown_b1: bool
    unknown_b2: int | None
    curve_points: int
    sector_angle: int | None
    left_slant: float | None
    unknown_b6: float | None
    right_slant: float | None
    width: float
    unknown_b8: float | None
    unknown_b9: float | None
    is_flipped_texture: bool
    unknown_b11: bool
    unknown_b12: bool
    unknown_b13: bool
    unknown_b14: bool
    unknown_b15: bool

    TYPE_VALUE: int = dataclasses.field(default=6, init=False, repr=False)

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader, **kwargs) -> Self:
        _logger.debug("reading in flag A...")
        flag_a = BrickFlagA(f.read_bitfield(1))
        if file_version >= _FLAG_A_EXTENDED_MIN_VERSION:
            _logger.debug("reading in flag A extension...")
            flag_a_extended = BrickFlagAExtended(f.read_bitfield(1))

        unknown_a0 = BrickFlagA.UNKNOWN_0 in flag_a

        if BrickFlagA.UNKNOWN_2 in flag_a:
            _logger.debug("Reading in unknown a2...")
            unknown_a2 = f.read_float()
        else:
            unknown_a2 = None
        if BrickFlagA.UNKNOWN_3 in flag_a:
            _logger.debug("Reading in unknown a3...")
            unknown_a3 = f.read_float()
        else:
            unknown_a3 = None
        if BrickFlagA.UNKNOWN_5 in flag_a:
            _logger.debug("Reading in unknown a5...")
            unknown_a5 = f.read_float()
        else:
            unknown_a5 = None
        if BrickFlagA.UNKNOWN_1 in flag_a:
            _logger.debug("Reading in unknown a1...")
            unknown_a1 = f.read_byte()
        else:
            unknown_a1 = None
        if BrickFlagA.HAS_FIXED_COORDINATES in flag_a:
            _logger.debug("Reading in coordinates...")
            position = Point2D(f.read_float(), f.read_float())
        else:
            position = None

        unknown_a6 = BrickFlagA.UNKNOWN_6 in flag_a
        unknown_a7 = BrickFlagA.UNKNOWN_7 in flag_a

        if file_version < _FLAG_A_EXTENDED_MIN_VERSION:
            unknown_a8 = None
            unknown_a9 = None
            unknown_a10 = None
            unknown_a11 = False
            unknown_a12 = False
            unknown_a13 = False
            unknown_a14 = False
            unknown_a15 = False
        else:
            # noinspection PyUnboundLocalVariable
            if BrickFlagAExtended.UNKNOWN_8 in flag_a_extended:
                _logger.debug("Reading in unknown a8...")
                unknown_a8 = f.read_byte()
            else:
                unknown_a8 = None
            if BrickFlagAExtended.UNKNOWN_9 in flag_a_extended:
                _logger.debug("Reading in unknown a9...")
                unknown_a9 = f.read_int()
            else:
                unknown_a9 = None
            if BrickFlagAExtended.UNKNOWN_10 in flag_a_extended:
                _logger.debug("Reading in unknown a10...")
                unknown_a10 = f.read_short()
            else:
                unknown_a10 = None

            unknown_a11 = BrickFlagAExtended.UNKNOWN_11 in flag_a_extended
            unknown_a12 = BrickFlagAExtended.UNKNOWN_12 in flag_a_extended
            unknown_a13 = BrickFlagAExtended.UNKNOWN_13 in flag_a_extended
            unknown_a14 = BrickFlagAExtended.UNKNOWN_14 in flag_a_extended
            unknown_a15 = BrickFlagAExtended.UNKNOWN_15 in flag_a_extended

        _logger.debug("Reading in flag B...")
        flag_b = BrickFlagB(f.read_bitfield(2))

        if BrickFlagB.UNKNOWN_8 in flag_b:
            _logger.debug("Reading in unknown b8...")
            unknown_b8 = f.read_float()
        else:
            unknown_b8 = None
        if BrickFlagB.UNKNOWN_9 in flag_b:
            _logger.debug("Reading in unknown b9...")
            unknown_b9 = f.read_float()
        else:
            unknown_b9 = None

        unknown_b0 = BrickFlagB.UNKNOWN_0 in flag_b
        unknown_b1 = BrickFlagB.UNKNOWN_1 in flag_b

        if BrickFlagB.UNKNOWN_2 in flag_b:
            _logger.debug("Reading in unknown b2...")
            unknown_b2 = f.read_byte()
        else:
            unknown_b2 = None
        if BrickFlagB.HAS_CUSTOM_CURVE_POINTS in flag_b:
            _logger.debug("Reading in curve points...")
            curve_points = f.read_byte()
        else:
            curve_points = _DEFAULT_CURVE_POINTS
        if BrickFlagB.HAS_LEFT_SLANT in flag_b:
            _logger.debug("Reading in left slant...")
            left_slant = f.read_float()
        else:
            left_slant = None
        if BrickFlagB.HAS_RIGHT_SLANT in flag_b:
            _logger.debug("Reading in unknown b6...")
            unknown_b6 = f.read_float()
            _logger.debug("Reading in right slant...")
            right_slant = f.read_float()
        else:
            unknown_b6 = None
            right_slant = None
        if BrickFlagB.HAS_SECTOR_ANGLE in flag_b:
            _logger.debug("Reading in sector angle...")
            sector_angle = f.read_float()
        else:
            sector_angle = None
        if BrickFlagB.HAS_CUSTOM_WIDTH in flag_b:
            _logger.debug("Reading in width...")
            width = f.read_float()
        else:
            width = _DEFAULT_WIDTH

        is_flipped_texture = BrickFlagB.IS_FLIPPED_TEXTURE in flag_b
        unknown_b11 = BrickFlagB.UNKNOWN_11 in flag_b
        unknown_b12 = BrickFlagB.UNKNOWN_12 in flag_b
        unknown_b13 = BrickFlagB.UNKNOWN_13 in flag_b
        unknown_b14 = BrickFlagB.UNKNOWN_14 in flag_b
        unknown_b15 = BrickFlagB.UNKNOWN_15 in flag_b

        _logger.debug("Reading in length...")
        length = f.read_float()
        _logger.debug("Reading in rotation angle...")
        rotation_angle = f.read_float()
        _logger.debug("Reading in mystery bytes...")
        unknown_bytes = list(f.read_raw(4))

        return cls(
                length=length,
                rotation_angle=rotation_angle,
                unknown_bytes=unknown_bytes,
                unknown_a0=unknown_a0,
                unknown_a1=unknown_a1,
                unknown_a2=unknown_a2,
                unknown_a3=unknown_a3,
                position=position,
                unknown_a5=unknown_a5,
                unknown_a6=unknown_a6,
                unknown_a7=unknown_a7,
                unknown_a8=unknown_a8,
                unknown_a9=unknown_a9,
                unknown_a10=unknown_a10,
                unknown_a11=unknown_a11,
                unknown_a12=unknown_a12,
                unknown_a13=unknown_a13,
                unknown_a14=unknown_a14,
                unknown_a15=unknown_a15,
                unknown_b0=unknown_b0,
                unknown_b1=unknown_b1,
                unknown_b2=unknown_b2,
                curve_points=curve_points,
                sector_angle=sector_angle,
                left_slant=left_slant,
                unknown_b6=unknown_b6,
                right_slant=right_slant,
                width=width,
                unknown_b8=unknown_b8,
                unknown_b9=unknown_b9,
                is_flipped_texture=is_flipped_texture,
                unknown_b11=unknown_b11,
                unknown_b12=unknown_b12,
                unknown_b13=unknown_b13,
                unknown_b14=unknown_b14,
                unknown_b15=unknown_b15,
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        write_queue_a: deque[Callable[[], None]] = deque()

        flag_a = BrickFlagA(0)

        if self.unknown_a0:
            flag_a |= BrickFlagA.UNKNOWN_0
        if self.unknown_a2 is not None:
            flag_a |= BrickFlagA.UNKNOWN_2
            write_queue_a.append(ft.partial(f.write_float, self.unknown_a2))
        if self.unknown_a3 is not None:
            flag_a |= BrickFlagA.UNKNOWN_3
            write_queue_a.append(ft.partial(f.write_float, self.unknown_a3))
        if self.unknown_a5 is not None:
            flag_a |= BrickFlagA.UNKNOWN_5
            write_queue_a.append(ft.partial(f.write_float, self.unknown_a5))
        if self.unknown_a1 is not None:
            flag_a |= BrickFlagA.UNKNOWN_1
            write_queue_a.append(ft.partial(f.write_byte, self.unknown_a1))
        if self.position is not None:
            flag_a |= BrickFlagA.HAS_FIXED_COORDINATES
            write_queue_a.append(ft.partial(f.write_float, self.position.x))
            write_queue_a.append(ft.partial(f.write_float, self.position.y))
        if self.unknown_a6:
            flag_a |= BrickFlagA.UNKNOWN_6
        if self.unknown_a7:
            flag_a |= BrickFlagA.UNKNOWN_7

        f.write_bitfield(flag_a, 1)

        if file_version >= _FLAG_A_EXTENDED_MIN_VERSION:
            flag_a_extended = BrickFlagAExtended(0)

            if self.unknown_a8 is not None:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_8
                write_queue_a.append(ft.partial(f.write_byte, self.unknown_a8))
            if self.unknown_a9 is not None:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_9
                write_queue_a.append(ft.partial(f.write_int, self.unknown_a9))
            if self.unknown_a10 is not None:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_10
                write_queue_a.append(ft.partial(f.write_short, self.unknown_a10))
            if self.unknown_a11:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_11
            if self.unknown_a12:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_12
            if self.unknown_a13:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_13
            if self.unknown_a14:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_14
            if self.unknown_a15:
                flag_a_extended |= BrickFlagAExtended.UNKNOWN_15

            f.write_bitfield(flag_a_extended, 1)

        for write_action in write_queue_a:
            write_action()

        write_queue_b: deque[Callable[[], None]] = deque()
        flag_b = BrickFlagB(0)

        if self.unknown_b8 is not None:
            flag_b |= BrickFlagB.UNKNOWN_8
            write_queue_b.append(ft.partial(f.write_float, self.unknown_b8))
        if self.unknown_b9 is not None:
            flag_b |= BrickFlagB.UNKNOWN_9
            write_queue_b.append(ft.partial(f.write_float, self.unknown_b9))
        if self.is_flipped_texture:
            flag_b |= BrickFlagB.IS_FLIPPED_TEXTURE
        if self.unknown_b11:
            flag_b |= BrickFlagB.UNKNOWN_11
        if self.unknown_b12:
            flag_b |= BrickFlagB.UNKNOWN_12
        if self.unknown_b13:
            flag_b |= BrickFlagB.UNKNOWN_13
        if self.unknown_b14:
            flag_b |= BrickFlagB.UNKNOWN_14
        if self.unknown_b15:
            flag_b |= BrickFlagB.UNKNOWN_15

        if self.unknown_b0:
            flag_b |= BrickFlagB.UNKNOWN_0
        if self.unknown_b1:
            flag_b |= BrickFlagB.UNKNOWN_1
        if self.unknown_b2 is not None:
            flag_b |= BrickFlagB.UNKNOWN_2
            write_queue_b.append(ft.partial(f.write_byte, self.unknown_b2))
        if self.curve_points != _DEFAULT_CURVE_POINTS:
            flag_b |= BrickFlagB.HAS_CUSTOM_CURVE_POINTS
            write_queue_b.append(ft.partial(f.write_byte, self.curve_points))
        if self.left_slant is not None:
            flag_b |= BrickFlagB.HAS_LEFT_SLANT
            write_queue_b.append(ft.partial(f.write_float, self.left_slant))
        if self.unknown_b6 is not None:
            flag_b |= BrickFlagB.HAS_RIGHT_SLANT
            write_queue_b.append(ft.partial(f.write_float, self.unknown_b6))
            write_queue_b.append(ft.partial(f.write_float, self.right_slant))
        if self.sector_angle is not None:
            flag_b |= BrickFlagB.HAS_SECTOR_ANGLE
            write_queue_b.append(ft.partial(f.write_float, self.sector_angle))
        if self.width != _DEFAULT_WIDTH:
            flag_b |= BrickFlagB.HAS_CUSTOM_WIDTH
            write_queue_b.append(ft.partial(f.write_float, self.width))

        f.write_bitfield(flag_b, 2)

        for write_action in write_queue_b:
            write_action()

        f.write_float(self.length)
        f.write_float(self.rotation_angle)
        f.write_raw(bytes(self.unknown_bytes))


def main():
    pass


if __name__ == "__main__":
    main()
