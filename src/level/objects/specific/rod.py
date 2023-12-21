# -*- coding: utf-8 -*-
"""
Created on 2023/12/04

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
from level.objects.flags import RodFlag
from level.objects.point_2d import Point2D

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class Rod:
    point_a: Point2D
    point_b: Point2D
    unknown_0: float | None = None
    unknown_1: float | None = None
    unknown_2: bool = False
    unknown_3: bool = False
    unknown_4: bool = False
    unknown_5: bool = False
    unknown_6: bool = False
    unknown_7: bool = False
    TYPE_VALUE: int = dataclasses.field(default=2, init=False, repr=False)

    @classmethod
    def read_data(cls, _: int, f: PeggleDataReader, **kwargs) -> Self:
        flag = RodFlag(f.read_bitfield(1))

        point_a = Point2D(f.read_float(), f.read_float())
        point_b = Point2D(f.read_float(), f.read_float())

        if RodFlag.UNKNOWN_0 in flag:
            unknown_0 = f.read_float()
        else:
            unknown_0 = None
        if RodFlag.UNKNOWN_1 in flag:
            unknown_1 = f.read_float()
        else:
            unknown_1 = None

        unknown_2 = RodFlag.UNKNOWN_2 in flag
        unknown_3 = RodFlag.UNKNOWN_3 in flag
        unknown_4 = RodFlag.UNKNOWN_4 in flag
        unknown_5 = RodFlag.UNKNOWN_5 in flag
        unknown_6 = RodFlag.UNKNOWN_6 in flag
        unknown_7 = RodFlag.UNKNOWN_7 in flag

        return cls(
                point_a=point_a,
                point_b=point_b,
                unknown_0=unknown_0,
                unknown_1=unknown_1,
                unknown_2=unknown_2,
                unknown_3=unknown_3,
                unknown_4=unknown_4,
                unknown_5=unknown_5,
                unknown_6=unknown_6,
                unknown_7=unknown_7,
        )

    def write_data(self, _: int, f: PeggleDataWriter) -> None:
        write_queue: deque[Callable[[], None]] = deque()
        flag = RodFlag(0)

        if self.unknown_0 is not None:
            flag |= RodFlag.UNKNOWN_0
            write_queue.append(ft.partial(f.write_float, self.unknown_0))
        if self.unknown_1 is not None:
            flag |= RodFlag.UNKNOWN_1
            write_queue.append(ft.partial(f.write_float, self.unknown_1))
        if self.unknown_2:
            flag |= RodFlag.UNKNOWN_2
        if self.unknown_3:
            flag |= RodFlag.UNKNOWN_3
        if self.unknown_4:
            flag |= RodFlag.UNKNOWN_4
        if self.unknown_5:
            flag |= RodFlag.UNKNOWN_5
        if self.unknown_6:
            flag |= RodFlag.UNKNOWN_6
        if self.unknown_7:
            flag |= RodFlag.UNKNOWN_7

        f.write_bitfield(flag, 1)
        f.write_float(self.point_a.x)
        f.write_float(self.point_a.y)
        f.write_float(self.point_b.x)
        f.write_float(self.point_b.y)

        for write_action in write_queue:
            write_action()
