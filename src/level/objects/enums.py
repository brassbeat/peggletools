# -*- coding: utf-8 -*-
"""
Created on 2023/11/27

@author: brassbeat
"""

from enum import Enum, StrEnum


class PegColor(Enum):
    BLUE = 1
    ORANGE = 2
    PURPLE = 3
    GREEN = 4


class MovementType(StrEnum):
    NO_MOVEMENT = "No Movement"
    VERTICAL_CYCLE = "Vertical Cycle"
    HORIZONTAL_CYCLE = "Horizontal Cycle"
    CIRCLE = "Circle"
    HORIZONTAL_INFINITY = "Horizontal Infinity"
    VERTICAL_INFINITY = "Vertical Infinity"
    HORIZONTAL_ARC = "Horizontal Arc"
    VERTICAL_ARC = "Vertical Arc"
    ROTATE = "Rotate"
    ROTATE_BACK_AND_FORTH = "Rotate Back and Forth"
    VERTICAL_WRAP = "Vertical Wrap"
    HORIZONTAL_WRAP = "Horizontal Wrap"
    ROTATE_AROUND_CIRCLE = "Rotate Around Circle"
    RETRACE_CIRCLE = "Retrace Circle"

    @classmethod
    def from_int(cls, id_: int):
        return _MOVEMENT_LIST[id_]

    def __int__(self):
        return _MOVEMENT_LIST.index(self)


_MOVEMENT_LIST = [
        MovementType.NO_MOVEMENT,
        MovementType.VERTICAL_CYCLE,
        MovementType.HORIZONTAL_CYCLE,
        MovementType.CIRCLE,
        MovementType.HORIZONTAL_INFINITY,
        MovementType.VERTICAL_INFINITY,
        MovementType.HORIZONTAL_ARC,
        MovementType.VERTICAL_ARC,
        MovementType.ROTATE,
        MovementType.ROTATE_BACK_AND_FORTH,
        None,
        MovementType.VERTICAL_WRAP,
        MovementType.HORIZONTAL_WRAP,
        MovementType.ROTATE_AROUND_CIRCLE,
        MovementType.RETRACE_CIRCLE,
]
