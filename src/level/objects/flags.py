# -*- coding: utf-8 -*-
"""
Created on 2023/11/23

@author: brassbeat
"""

from enum import IntFlag, auto


class GenericFlag(IntFlag):
    HAS_CUSTOM_ROLLINESS = auto()
    HAS_CUSTOM_BOUNCINESS = auto()
    HAS_PEG_INFO = auto()
    HAS_MOVEMENT_DATA = auto()
    UNKNOWN_4 = auto()
    IS_INTERACTIBLE = auto()
    IS_VISIBLE = auto()
    IS_MOVABLE = auto()
    HAS_FILL_COLOR = auto()
    HAS_OUTLINE_COLOR = auto()
    HAS_IMAGE_DATA = auto()
    HAS_IMAGE_DX = auto()
    HAS_IMAGE_DY = auto()
    HAS_IMAGE_ROTATION = auto()
    IS_BACKGROUND = auto()
    IS_BASE_OBJECT = auto()
    UNKNOWN_16 = auto()
    HAS_ID = auto()
    UNKNOWN_18 = auto()
    HAS_SOUND = auto()
    BALL_STOP_RESET = auto()
    HAS_LOGIC = auto()
    IS_FOREGROUND = auto()
    HAS_MAX_BOUNCE_VELOCITY = auto()
    IS_DRAW_SORT = auto()
    IS_FOREGROUND_2 = auto()
    HAS_SUB_ID = auto()
    HAS_FLIPPER_FLAGS = auto()
    IS_DRAW_FLOAT = auto()
    UNKNOWN_29 = auto()
    HAS_SHADOW = auto()
    UNKNOWN_31 = auto()


class FlipperFlag(IntFlag):
    UNKNOWN_0 = auto()
    UNKNOWN_1 = auto()
    UNKNOWN_2 = auto()
    UNKNOWN_3 = auto()
    UNKNOWN_4 = auto()
    UNKNOWN_5 = auto()
    UNKNOWN_6 = auto()
    UNKNOWN_7 = auto()


class PegInfoFlag(IntFlag):
    UNKNOWN_0 = auto()
    CAN_BE_ORANGE = auto()
    UNKNOWN_2 = auto()
    CAN_QUICK_DISAPPEAR = auto()
    UNKNOWN_4 = auto()
    UNKNOWN_5 = auto()
    UNKNOWN_6 = auto()
    UNKNOWN_7 = auto()


class CircleFlag(IntFlag):
    HAS_NORMAL_PHYSICS = auto()
    HAS_FIXED_COORDINATES = auto()
    UNKNOWN_2 = auto()
    UNKNOWN_3 = auto()
    UNKNOWN_4 = auto()
    UNKNOWN_5 = auto()
    UNKNOWN_6 = auto()
    UNKNOWN_7 = auto()


class CircleExtendedFlag(IntFlag):
    UNKNOWN_0 = auto()
    UNKNOWN_1 = auto()
    UNKNOWN_2 = auto()
    UNKNOWN_3 = auto()
    UNKNOWN_4 = auto()
    UNKNOWN_5 = auto()
    UNKNOWN_6 = auto()
    UNKNOWN_7 = auto()


class BrickFlagA(IntFlag):
    UNKNOWN_0 = auto()
    UNKNOWN_1 = auto()
    UNKNOWN_2 = auto()
    UNKNOWN_3 = auto()
    HAS_FIXED_COORDINATES = auto()
    UNKNOWN_5 = auto()
    UNKNOWN_6 = auto()
    UNKNOWN_7 = auto()


class BrickFlagAExtended(IntFlag):
    UNKNOWN_8 = auto()
    UNKNOWN_9 = auto()
    UNKNOWN_10 = auto()
    UNKNOWN_11 = auto()
    UNKNOWN_12 = auto()
    UNKNOWN_13 = auto()
    UNKNOWN_14 = auto()
    UNKNOWN_15 = auto()


class BrickFlagB(IntFlag):
    UNKNOWN_0 = auto()
    UNKNOWN_1 = auto()
    UNKNOWN_2 = auto()
    HAS_CUSTOM_CURVE_POINTS = auto()
    HAS_SECTOR_ANGLE = auto()
    HAS_LEFT_SLANT = auto()
    HAS_RIGHT_SLANT = auto()
    HAS_CUSTOM_WIDTH = auto()
    UNKNOWN_8 = auto()
    UNKNOWN_9 = auto()
    IS_FLIPPED_TEXTURE = auto()
    UNKNOWN_11 = auto()
    UNKNOWN_12 = auto()
    UNKNOWN_13 = auto()
    UNKNOWN_14 = auto()
    UNKNOWN_15 = auto()


class RodFlag(IntFlag):
    UNKNOWN_0 = auto()
    UNKNOWN_1 = auto()
    UNKNOWN_2 = auto()
    UNKNOWN_3 = auto()
    UNKNOWN_4 = auto()
    UNKNOWN_5 = auto()
    UNKNOWN_6 = auto()
    UNKNOWN_7 = auto()


class PolygonFlag(IntFlag):
    UNKNOWN_0 = auto()
    HAS_NORMAL_DIRECTION = auto()
    HAS_ROTATION_VALUE = auto()
    UNKNOWN_3 = auto()
    HAS_FIXED_COORDINATES = auto()
    HAS_SCALE = auto()
    UNKNOWN_6 = auto()
    UNKNOWN_7 = auto()


class PolygonFlagExtended(IntFlag):
    UNKNOWN_8 = auto()
    HAS_GROW_TYPE = auto()
    UNKNOWN_10 = auto()
    UNKNOWN_11 = auto()
    UNKNOWN_12 = auto()
    UNKNOWN_13 = auto()
    UNKNOWN_14 = auto()
    UNKNOWN_15 = auto()


class MovementFlag(IntFlag):
    HAS_INITIAL_FRAME = auto()
    HAS_RADIUS_1 = auto()
    HAS_INITIAL_PHASE = auto()
    HAS_MOVE_ROTATION = auto()
    HAS_RADIUS_2 = auto()
    HAS_PAUSE_1_DURATION = auto()
    HAS_PAUSE_2_DURATION = auto()
    HAS_PAUSE_1_PHASE = auto()
    HAS_PAUSE_2_PHASE = auto()
    HAS_POST_DELAY_PHASE = auto()
    HAS_MAX_ANGLE = auto()
    UNKNOWN_11 = auto()
    HAS_SUBMOVEMENT = auto()
    HAS_MYSTERY_POINT = auto()
    HAS_ROTATION_VALUE = auto()
    UNKNOWN_15 = auto()
