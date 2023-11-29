# -*- coding: utf-8 -*-
"""
Created on 2023/11/24

@author: brassbeat
"""
import logging
from dataclasses import dataclass
from typing import Self

from .flags import GenericFlag, FlipperFlag
from .peg_info import PegInfo
from ..level_reader import PeggleDataReader
from ..level_writer import PeggleDataWriter

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class GenericObject:
    rolliness: float = 1.0
    bounciness: float = 1.0
    peg_data: PegInfo | None = None
    movement_data: None = None
    unknown_4: int | None = None
    has_collision: bool = True
    is_visible: bool = True
    can_move: bool = True
    fill_color: list[int] | None = None
    outline_color: list[int] | None = None
    image_name: str | None = None
    image_dx: float | None = None
    image_dy: float | None = None
    image_rotation: float | None = None
    is_background: bool = False
    is_base_object: bool = False
    unknown_16: int | None = None
    id: str | None = None
    unknown_18: int | None = None
    sound: int | None = None
    is_ball_stop_reset: bool = False
    logic: str | None = None
    is_foreground: bool = False
    max_bounce_velocity: float | None = None
    is_draw_sort: bool = False
    is_foreground2: bool = False
    sub_id: int | None = None
    flipper_flags: FlipperFlag | None = None
    is_draw_float: bool = False
    unknown_29: bool = False
    has_shadow: bool = True
    unknown_31: bool = False

    @property
    def flag(self) -> GenericFlag:
        returned_flag = GenericFlag(0)

        if self.rolliness != 1.0:
            returned_flag |= GenericFlag.HAS_CUSTOM_ROLLINESS

        return returned_flag

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader) -> Self:
        _logger.debug("reading in generic flags...")
        flag = GenericFlag(f.read_bitfield(4))

        if GenericFlag.HAS_CUSTOM_ROLLINESS in flag:
            _logger.debug("Reading in rolliness...")
            rolliness = f.read_float()
        else:
            rolliness = 1.0
        if GenericFlag.HAS_CUSTOM_BOUNCINESS in flag:
            _logger.debug("Reading in bounciness...")
            bounciness = f.read_float()
        else:
            bounciness = 1.0

        if GenericFlag.UNKNOWN_4 in flag:
            _logger.debug("Reading in unknown 4...")
            unknown_4 = f.read_int()
        else:
            unknown_4 = None

        has_collision = GenericFlag.HAS_COLLISION in flag
        is_visible = GenericFlag.IS_VISIBLE in flag
        can_move = GenericFlag.CAN_MOVE in flag

        if GenericFlag.HAS_FILL_COLOR in flag:
            _logger.debug("Reading in fill color...")
            fill_color = list(f.read_byte() for _ in range(4))
        else:
            fill_color = None

        if GenericFlag.HAS_OUTLINE_COLOR in flag:
            _logger.debug("Reading in outline color...")
            outline_color = list(f.read_byte() for _ in range(4))
        else:
            outline_color = None

        if GenericFlag.HAS_IMAGE_DATA in flag:
            _logger.debug("Reading in image name...")
            image_name = f.read_string()
        else:
            image_name = None
        if GenericFlag.HAS_IMAGE_DX in flag:
            _logger.debug("Reading in image dx...")
            image_dx = f.read_float()
        else:
            image_dx = None
        if GenericFlag.HAS_IMAGE_DY in flag:
            _logger.debug("Reading in image dy...")
            image_dy = f.read_float()
        else:
            image_dy = None
        if GenericFlag.HAS_IMAGE_ROTATION in flag:
            _logger.debug("Reading in image rotation...")
            image_rotation = f.read_float()
        else:
            image_rotation = None

        is_background = GenericFlag.IS_BACKGROUND in flag
        is_base_object = GenericFlag.IS_BASE_OBJECT in flag

        if GenericFlag.UNKNOWN_16 in flag:
            _logger.debug("Reading in unknown 16...")
            unknown_16 = f.read_int()
        else:
            unknown_16 = None
        if GenericFlag.HAS_ID in flag:
            _logger.debug("Reading in ID...")
            id_ = f.read_string()
        else:
            id_ = None

        if GenericFlag.UNKNOWN_18 in flag:
            _logger.debug("Reading in unknown 18...")
            unknown_18 = f.read_int()
        else:
            unknown_18 = None

        if GenericFlag.HAS_SOUND in flag:
            _logger.debug("Reading in sound...")
            sound = f.read_byte()
        else:
            sound = None

        is_ball_stop_reset = GenericFlag.BALL_STOP_RESET in flag

        if GenericFlag.HAS_LOGIC in flag:
            _logger.debug("Reading in logic...")
            logic = f.read_string()
        else:
            logic = None

        is_foreground = GenericFlag.FOREGROUND in flag

        if GenericFlag.HAS_MAX_BOUNCE_VELOCITY in flag:
            _logger.debug("Reading in max bounce velocity...")
            max_bounce_velocity = f.read_float()
        else:
            max_bounce_velocity = None

        is_draw_sort = GenericFlag.DRAW_SORT in flag
        is_foreground2 = GenericFlag.FOREGROUND_2 in flag

        if GenericFlag.HAS_SUB_ID in flag:
            _logger.debug("Reading in sub-ID...")
            sub_id = f.read_int()
        else:
            sub_id = None
        if GenericFlag.HAS_FLIPPER_FLAGS in flag:
            _logger.debug("Reading in flipper flags...")
            flipper_flags = FlipperFlag(f.read_bitfield(1))
        else:
            flipper_flags = None

        is_draw_float = GenericFlag.DRAW_FLOAT in flag
        unknown_29 = GenericFlag.UNKNOWN_29 in flag

        if file_version >= int("0x50", 16):
            has_shadow = GenericFlag.HAS_SHADOW in flag
        else:
            has_shadow = True

        unknown_31 = GenericFlag.UNKNOWN_31 in flag

        peg_data = PegInfo.read_data(file_version, f)
        movement_data = None  # placeholder!

        return cls(
                rolliness=rolliness,
                bounciness=bounciness,
                peg_data=peg_data,
                movement_data=movement_data,
                unknown_4=unknown_4,
                has_collision=has_collision,
                is_visible=is_visible,
                can_move=can_move,
                fill_color=fill_color,
                outline_color=outline_color,
                image_name=image_name,
                image_dx=image_dx,
                image_dy=image_dy,
                image_rotation=image_rotation,
                is_background=is_background,
                is_base_object=is_base_object,
                unknown_16=unknown_16,
                id=id_,
                unknown_18=unknown_18,
                sound=sound,
                is_ball_stop_reset=is_ball_stop_reset,
                logic=logic,
                is_foreground=is_foreground,
                max_bounce_velocity=max_bounce_velocity,
                is_draw_sort=is_draw_sort,
                is_foreground2=is_foreground2,
                sub_id=sub_id,
                flipper_flags=flipper_flags,
                is_draw_float=is_draw_float,
                unknown_29=unknown_29,
                has_shadow=has_shadow,
                unknown_31=unknown_31,
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        ...


def main():
    pass


if __name__ == "__main__":
    main()
