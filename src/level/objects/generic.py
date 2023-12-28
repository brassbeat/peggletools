# -*- coding: utf-8 -*-
"""
Created on 2023/11/24

@author: brassbeat
"""
import functools as ft
import logging
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from level.objects.movement_data import Movement
from level.protocols import PeggleObjectData
from .flags import GenericFlag, FlipperFlag
from .peg_info import PegInfo
from ..level_reader import PeggleDataReader
from ..level_writer import PeggleDataWriter

_FLAG_EXTENSION_FIRST_VERSION = 5

_SHADOW_FIELD_MIN_VERSION = int("0x50", 16)

_DEFAULT_BOUNCINESS = 1.0

_DEFAULT_ROLLINESS = 1.0

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


@dataclass
class GenericObject:
    rolliness: float | None
    bounciness: float | None
    peg_data: PegInfo | None
    movement_data: Movement | None
    unknown_4: int | None
    has_collision: bool
    is_visible: bool
    can_move: bool
    fill_color: list[int] | None
    outline_color: list[int] | None
    image_name: str | None
    image_dx: float | None
    image_dy: float | None
    image_rotation: float | None
    is_background: bool
    is_base_object: bool
    unknown_16: int | None
    id: str | None
    unknown_18: int | None
    sound: int | None
    is_ball_stop_reset: bool
    logic: str | None
    is_foreground: bool
    max_bounce_velocity: float | None
    is_draw_sort: bool
    is_foreground2: bool
    sub_id: int | None
    flipper_flags: FlipperFlag | None
    is_draw_float: bool
    unknown_29: bool
    has_shadow: bool
    unknown_31: bool

    movement_link_id: int | None = None

    @classmethod
    def read_data(
            cls,
            file_version: int,
            f: PeggleDataReader,
            *,
            movement_callback: Callable[[int, PeggleDataReader], Movement],
            **kwargs
    ) -> Self:
        _logger.debug("reading in generic flags...")
        flag_length = 4 if file_version >= _FLAG_EXTENSION_FIRST_VERSION else 3
        flag = GenericFlag(f.read_bitfield(flag_length))

        if GenericFlag.HAS_CUSTOM_ROLLINESS in flag:
            _logger.debug("Reading in rolliness...")
            rolliness = f.read_float()
        else:
            rolliness = None
        if GenericFlag.HAS_CUSTOM_BOUNCINESS in flag:
            _logger.debug("Reading in bounciness...")
            bounciness = f.read_float()
        else:
            bounciness = None

        if GenericFlag.UNKNOWN_4 in flag:
            _logger.debug("Reading in unknown 4...")
            unknown_4 = f.read_int()
        else:
            unknown_4 = None

        has_collision = GenericFlag.IS_INTERACTIBLE in flag
        is_visible = GenericFlag.IS_VISIBLE in flag
        can_move = GenericFlag.IS_MOVABLE in flag

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

        is_foreground = GenericFlag.IS_FOREGROUND in flag

        if GenericFlag.HAS_MAX_BOUNCE_VELOCITY in flag:
            _logger.debug("Reading in max bounce velocity...")
            max_bounce_velocity = f.read_float()
        else:
            max_bounce_velocity = None

        is_draw_sort = GenericFlag.IS_DRAW_SORT in flag
        is_foreground2 = GenericFlag.IS_FOREGROUND_2 in flag

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

        is_draw_float = GenericFlag.IS_DRAW_FLOAT in flag
        unknown_29 = GenericFlag.UNKNOWN_29 in flag

        if file_version >= _SHADOW_FIELD_MIN_VERSION:
            has_shadow = GenericFlag.HAS_SHADOW in flag
        else:
            has_shadow = True

        unknown_31 = GenericFlag.UNKNOWN_31 in flag

        if GenericFlag.HAS_PEG_INFO in flag:
            _logger.debug("Reading in peg info...")
            peg_data = PegInfo.read_data(file_version, f)
        else:
            peg_data = None

        if GenericFlag.HAS_MOVEMENT_DATA in flag:
            # _logger.debug("Reading in movement link id...")
            # main_link_id = f.read_int()
            # if main_link_id == 1:
            #     _logger.debug("Reading in movement data...")
            #     movement_data = movement_callback(file_version, f)
            #     movement_link_id = None
            # else:
            #     movement_data = None
            #     movement_link_id = main_link_id
            _logger.debug("Reading in movement data...")
            movement_data = movement_callback(file_version, f)
            movement_link_id = None
        else:
            movement_data = None
            movement_link_id = None

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
                movement_link_id=movement_link_id,
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:

        write_queue = deque()
        flag = GenericFlag(0)

        if self.rolliness is not None:
            flag |= GenericFlag.HAS_CUSTOM_ROLLINESS
            write_queue.append(ft.partial(f.write_float, self.rolliness))
        if self.bounciness is not None:
            flag |= GenericFlag.HAS_CUSTOM_BOUNCINESS
            write_queue.append(ft.partial(f.write_float, self.bounciness))
        if self.unknown_4 is not None:
            flag |= GenericFlag.UNKNOWN_4
            write_queue.append(ft.partial(f.write_int, self.unknown_4))
        if self.has_collision:
            flag |= GenericFlag.IS_INTERACTIBLE
        if self.is_visible:
            flag |= GenericFlag.IS_VISIBLE
        if self.can_move:
            flag |= GenericFlag.IS_MOVABLE
        if self.fill_color is not None:
            flag |= GenericFlag.HAS_FILL_COLOR
            write_queue.extend(ft.partial(f.write_byte, n) for n in self.fill_color)
        if self.outline_color is not None:
            flag |= GenericFlag.HAS_OUTLINE_COLOR
            write_queue.extend(ft.partial(f.write_byte, n) for n in self.outline_color)
        if self.image_name is not None:
            flag |= GenericFlag.HAS_IMAGE_DATA
            write_queue.append(ft.partial(f.write_string, self.image_name))
        if self.image_dx is not None:
            flag |= GenericFlag.HAS_IMAGE_DX
            write_queue.append(ft.partial(f.write_float, self.image_dx))
        if self.image_dy is not None:
            flag |= GenericFlag.HAS_IMAGE_DY
            write_queue.append(ft.partial(f.write_float, self.image_dy))
        if self.image_rotation is not None:
            flag |= GenericFlag.HAS_IMAGE_ROTATION
            write_queue.append(ft.partial(f.write_float, self.image_rotation))
        if self.is_background:
            flag |= GenericFlag.IS_BACKGROUND
        if self.is_base_object:
            flag |= GenericFlag.IS_BASE_OBJECT
        if self.unknown_16 is not None:
            flag |= GenericFlag.UNKNOWN_16
            write_queue.append(ft.partial(f.write_int, self.unknown_16))
        if self.id is not None:
            flag |= GenericFlag.HAS_ID
            write_queue.append(ft.partial(f.write_string, self.id))
        if self.unknown_18 is not None:
            flag |= GenericFlag.UNKNOWN_18
            write_queue.append(ft.partial(f.write_int, self.unknown_18))
        if self.sound is not None:
            flag |= GenericFlag.HAS_SOUND
            write_queue.append(ft.partial(f.write_byte, self.sound))
        if self.is_ball_stop_reset:
            flag |= GenericFlag.BALL_STOP_RESET
        if self.logic is not None:
            flag |= GenericFlag.HAS_LOGIC
            write_queue.append(ft.partial(f.write_string, self.logic))
        if self.is_foreground:
            flag |= GenericFlag.IS_FOREGROUND
        if self.max_bounce_velocity is not None:
            flag |= GenericFlag.HAS_MAX_BOUNCE_VELOCITY
            write_queue.append(ft.partial(f.write_float, self.max_bounce_velocity))
        if self.is_draw_sort:
            flag |= GenericFlag.IS_DRAW_SORT
        if self.is_foreground2:
            flag |= GenericFlag.IS_FOREGROUND_2
        if self.sub_id is not None:
            flag |= GenericFlag.HAS_SUB_ID
            write_queue.append(ft.partial(f.write_int, self.sub_id))
        if self.flipper_flags is not None:
            flag |= GenericFlag.HAS_FLIPPER_FLAGS
            write_queue.append(ft.partial(f.write_bitfield, self.flipper_flags, 1))
        if self.is_draw_float:
            flag |= GenericFlag.IS_DRAW_FLOAT
        if self.unknown_29:
            flag |= GenericFlag.UNKNOWN_29
        if self.has_shadow and file_version >= _SHADOW_FIELD_MIN_VERSION:
            flag |= GenericFlag.HAS_SHADOW
        if self.unknown_31:
            flag |= GenericFlag.UNKNOWN_31
        if self.peg_data is not None:
            flag |= GenericFlag.HAS_PEG_INFO
            write_queue.append(ft.partial(self.peg_data.write_data, file_version, f))

        if self.movement_link_id is not None:
            flag |= GenericFlag.HAS_MOVEMENT_DATA
            write_queue.append(ft.partial(f.write_int, self.movement_link_id))
        elif self.movement_data is not None:
            flag |= GenericFlag.HAS_MOVEMENT_DATA
            write_queue.append(ft.partial(self.movement_data.write_data, file_version, f))

        flag_length = 4 if file_version >= _FLAG_EXTENSION_FIRST_VERSION else 3
        f.write_bitfield(flag, flag_length)
        for write_action in write_queue:
            write_action()


def main():
    pass


if __name__ == "__main__":
    main()
