# -*- coding: utf-8 -*-
"""
Created on 2023/11/27

@author: brassbeat
"""
import functools as ft
import logging
from collections import deque
from dataclasses import dataclass
from typing import Self

from .flags import PegInfoFlag
from ..level_reader import PeggleDataReader
from ..level_writer import PeggleDataWriter

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class PegInfo:
    type: int
    unknown_0: bool
    can_be_orange: bool
    unknown_2: int | None
    can_quick_disappear: bool
    unknown_4: int | None
    unknown_5: int | None
    unknown_6: bool
    unknown_7: int | None

    @classmethod
    def read_data(cls, _: int, f: PeggleDataReader) -> Self:
        _logger.debug("Reading in peginfo type...")
        type_ = f.read_byte()
        _logger.debug("reading in peginfo flags...")
        flag = PegInfoFlag(f.read_bitfield(1))

        unknown_0 = PegInfoFlag.UNKNOWN_0 in flag
        can_be_orange = PegInfoFlag.CAN_BE_ORANGE in flag
        if PegInfoFlag.UNKNOWN_2 in flag:
            _logger.debug("Reading in peginfo field 2...")
            unknown_2 = f.read_int()
        else:
            unknown_2 = None
        can_quick_disappear = PegInfoFlag.CAN_QUICK_DISAPPEAR in flag
        if PegInfoFlag.UNKNOWN_4 in flag:
            _logger.debug("Reading in peginfo field 4...")
            unknown_4 = f.read_int()
        else:
            unknown_4 = None
        if PegInfoFlag.UNKNOWN_5 in flag:
            _logger.debug("Reading in peginfo field 5...")
            unknown_5 = f.read_byte()
        else:
            unknown_5 = None
        unknown_6 = PegInfoFlag.UNKNOWN_6 in flag
        if PegInfoFlag.UNKNOWN_7 in flag:
            _logger.debug("Reading in peginfo field 7...")
            unknown_7 = f.read_byte()
        else:
            unknown_7 = None

        return cls(
                type=type_,
                unknown_0=unknown_0,
                can_be_orange=can_be_orange,
                unknown_2=unknown_2,
                can_quick_disappear=can_quick_disappear,
                unknown_4=unknown_4,
                unknown_5=unknown_5,
                unknown_6=unknown_6,
                unknown_7=unknown_7,
        )

    def write_data(self, _: int, f: PeggleDataWriter) -> None:
        f.write_byte(self.type)

        write_queue = deque()
        flag = PegInfoFlag(0)

        if self.unknown_0:
            flag |= PegInfoFlag.UNKNOWN_0
        if self.can_be_orange:
            flag |= PegInfoFlag.CAN_BE_ORANGE
        if self.unknown_2 is not None:
            flag |= PegInfoFlag.UNKNOWN_2
            write_queue.append(ft.partial(f.write_int, self.unknown_2))
        if self.can_quick_disappear:
            flag |= PegInfoFlag.CAN_QUICK_DISAPPEAR
        if self.unknown_4 is not None:
            flag |= PegInfoFlag.UNKNOWN_4
            write_queue.append(ft.partial(f.write_int, self.unknown_4))
        if self.unknown_5 is not None:
            flag |= PegInfoFlag.UNKNOWN_5
            write_queue.append(ft.partial(f.write_byte, self.unknown_5))
        if self.unknown_6:
            flag |= PegInfoFlag.UNKNOWN_6
        if self.unknown_7 is not None:
            flag |= PegInfoFlag.UNKNOWN_7
            write_queue.append(ft.partial(f.write_byte, self.unknown_7))

        f.write_bitfield(flag, 1)
        for write_action in write_queue:
            write_action()


def main():
    pass


if __name__ == "__main__":
    main()
