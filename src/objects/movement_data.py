# -*- coding: utf-8 -*-
"""
Created on 2023/12/05

@author: brassbeat
"""
import functools as ft
import itertools
import logging
from collections import deque
from dataclasses import dataclass
from typing import Self, Callable

from level.level_reader import PeggleDataReader
from level.level_writer import PeggleDataWriter
from objects.enums import MovementType
from objects.flags import MovementFlag
from objects.point_2d import Point2D

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

_INDEXER = itertools.count()


@dataclass
class Movement:
    main_link_id: int
    is_reversed: bool
    movement_type: MovementType
    anchor_point: Point2D
    time_period: int
    initial_frame: int | None
    radius_1: int | None
    radius_2: int | None
    initial_phase: float | None
    move_rotation: float | None
    pause_1_duration: int | None
    pause_2_duration: int | None
    pause_1_phase_percentage: int | None
    pause_2_phase_percentage: int | None
    post_delay_phase: float | None
    max_angle: float | None
    unknown_11: float | None
    rotation_value: float | None
    submovement_offset: Point2D | None
    submovement_link_id: int | None
    submovement_: Self | None
    mystery_point: Point2D | None
    unknown_15: bool

    # _submovement: Self | None = dataclasses.field(default=None, init=False, repr=False)
    #
    # @property
    # def submovement(self) -> Self | None:
    #     return self._submovement
    #
    # @submovement.setter
    # def submovement(self, value: Self | None):
    #     if value:
    #         self.submovement_link_id = None
    #     self._submovement = value

    @classmethod
    def read_data(
            cls,
            file_version: int,
            f: PeggleDataReader,
            *,
            movement_callback: Callable[[int, PeggleDataReader], Self],
            **kwargs,
    ) -> Self:
        main_link_id = 1

        _logger.debug("Reading in movement type + direction...")
        movement_value = f.read_byte()
        is_reversed = movement_value < 0
        movement_type = MovementType.from_int(abs(movement_value))

        _logger.debug("Reading in anchor point...")
        anchor_point = Point2D(f.read_float(), f.read_float())
        _logger.debug("Reading in time period...")
        time_period = f.read_short()

        flag = MovementFlag(f.read_bitfield(2))

        if MovementFlag.HAS_INITIAL_FRAME in flag:
            _logger.debug("Reading in initial frame...")
            initial_frame = f.read_short()
        else:
            initial_frame = None
        if MovementFlag.HAS_RADIUS_1 in flag:
            _logger.debug("Reading in radius 1...")
            radius_1 = f.read_short()
        else:
            radius_1 = None
        if MovementFlag.HAS_INITIAL_PHASE in flag:
            _logger.debug("Reading in initial phase...")
            initial_phase = f.read_float()
        else:
            initial_phase = None
        if MovementFlag.HAS_MOVE_ROTATION in flag:
            _logger.debug("Reading in move rotation...")
            move_rotation = f.read_float()
        else:
            move_rotation = None
        if MovementFlag.HAS_RADIUS_2 in flag:
            _logger.debug("Reading in radius 2...")
            radius_2 = f.read_short()
        else:
            radius_2 = None
        if MovementFlag.HAS_PAUSE_1_DURATION in flag:
            _logger.debug("Reading in pause 1 duration...")
            pause_1_duration = f.read_short()
        else:
            pause_1_duration = None
        if MovementFlag.HAS_PAUSE_2_DURATION in flag:
            _logger.debug("Reading in pause 2 duration...")
            pause_2_duration = f.read_short()
        else:
            pause_2_duration = None
        if MovementFlag.HAS_PAUSE_1_PHASE in flag:
            _logger.debug("Reading in pause 1 phase...")
            pause_1_phase_percentage = f.read_byte()
        else:
            pause_1_phase_percentage = None
        if MovementFlag.HAS_PAUSE_2_PHASE in flag:
            _logger.debug("Reading in pause 2 phase...")
            pause_2_phase_percentage = f.read_byte()
        else:
            pause_2_phase_percentage = None
        if MovementFlag.HAS_POST_DELAY_PHASE in flag:
            _logger.debug("Reading in post delay phase...")
            post_delay_phase = f.read_float()
        else:
            post_delay_phase = None
        if MovementFlag.HAS_MAX_ANGLE in flag:
            _logger.debug("Reading in max angle...")
            max_angle = f.read_float()
        else:
            max_angle = None
        if MovementFlag.UNKNOWN_11 in flag:
            _logger.debug("Reading in unknown 11...")
            unknown_11 = f.read_float()
        else:
            unknown_11 = None
        if MovementFlag.HAS_ROTATION_VALUE in flag:
            _logger.debug("Reading in rotation value...")
            rotation_value = f.read_float()
        else:
            rotation_value = None
        if MovementFlag.HAS_SUBMOVEMENT in flag:
            _logger.debug("Reading in submovement offset...")
            submovement_offset = Point2D(f.read_float(), f.read_float())
            submovement = movement_callback(file_version, f)
            submovement_link_id = None

        else:
            submovement_offset = None
            submovement_link_id = None
            submovement = None
        if MovementFlag.HAS_MYSTERY_POINT in flag:
            _logger.debug("Reading in mystery point...")
            mystery_point = Point2D(f.read_float(), f.read_float())
        else:
            mystery_point = None
        
        unknown_15 = MovementFlag.UNKNOWN_15 in flag
        
        return cls(
                main_link_id=main_link_id,
                is_reversed=is_reversed,
                movement_type=movement_type,
                anchor_point=anchor_point,
                time_period=time_period,
                initial_frame=initial_frame,
                radius_1=radius_1,
                radius_2=radius_2,
                initial_phase=initial_phase,
                move_rotation=move_rotation,
                pause_1_duration=pause_1_duration,
                pause_2_duration=pause_2_duration,
                pause_1_phase_percentage=pause_1_phase_percentage,
                pause_2_phase_percentage=pause_2_phase_percentage,
                post_delay_phase=post_delay_phase,
                max_angle=max_angle,
                unknown_11=unknown_11,
                rotation_value=rotation_value,
                submovement_offset=submovement_offset,
                submovement_link_id=submovement_link_id,
                submovement_=submovement,
                mystery_point=mystery_point,
                unknown_15=unknown_15,
        )

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        write_queue: deque[Callable[[], None]] = deque()

        flag = MovementFlag(0)

        if self.initial_frame is not None:
            flag |= MovementFlag.HAS_INITIAL_FRAME
            write_queue.append(ft.partial(f.write_short, self.initial_frame))
        if self.radius_1 is not None:
            flag |= MovementFlag.HAS_RADIUS_1
            write_queue.append(ft.partial(f.write_short, self.radius_1))
        if self.initial_phase is not None:
            flag |= MovementFlag.HAS_INITIAL_PHASE
            write_queue.append(ft.partial(f.write_float, self.initial_phase))
        if self.move_rotation is not None:
            flag |= MovementFlag.HAS_MOVE_ROTATION
            write_queue.append(ft.partial(f.write_float, self.move_rotation))
        if self.radius_2 is not None:
            flag |= MovementFlag.HAS_RADIUS_2
            write_queue.append(ft.partial(f.write_short, self.radius_2))
        if self.pause_1_duration is not None:
            flag |= MovementFlag.HAS_PAUSE_1_DURATION
            write_queue.append(ft.partial(f.write_short, self.pause_1_duration))
        if self.pause_2_duration is not None:
            flag |= MovementFlag.HAS_PAUSE_2_DURATION
            write_queue.append(ft.partial(f.write_short, self.pause_2_duration))
        if self.pause_1_phase_percentage is not None:
            flag |= MovementFlag.HAS_PAUSE_1_PHASE
            write_queue.append(ft.partial(f.write_byte, self.pause_1_phase_percentage))
        if self.pause_2_phase_percentage is not None:
            flag |= MovementFlag.HAS_PAUSE_2_PHASE
            write_queue.append(ft.partial(f.write_byte, self.pause_2_phase_percentage))
        if self.post_delay_phase is not None:
            flag |= MovementFlag.HAS_POST_DELAY_PHASE
            write_queue.append(ft.partial(f.write_float, self.post_delay_phase))
        if self.max_angle is not None:
            flag |= MovementFlag.HAS_MAX_ANGLE
            write_queue.append(ft.partial(f.write_float, self.max_angle))
        if self.unknown_11 is not None:
            flag |= MovementFlag.UNKNOWN_11
            write_queue.append(ft.partial(f.write_float, self.unknown_11))
        if self.rotation_value is not None:
            flag |= MovementFlag.HAS_ROTATION_VALUE
            write_queue.append(ft.partial(f.write_float, self.rotation_value))
        if self.submovement_offset is not None:
            flag |= MovementFlag.HAS_SUBMOVEMENT
            write_queue.append(ft.partial(f.write_float, self.submovement_offset.x))
            write_queue.append(ft.partial(f.write_float, self.submovement_offset.y))
            write_queue.append(ft.partial(f.write_int, self.submovement_link_id))
        if self.mystery_point is not None:
            flag |= MovementFlag.HAS_MYSTERY_POINT
            write_queue.append(ft.partial(f.write_float, self.mystery_point.x))
            write_queue.append(ft.partial(f.write_float, self.mystery_point.y))

        f.write_int(self.main_link_id)
        movement_value = -int(self.movement_type) if self.is_reversed else int(self.movement_type)
        f.write_byte(movement_value)
        f.write_float(self.anchor_point.x)
        f.write_float(self.anchor_point.y)
        f.write_short(self.time_period)
        f.write_bitfield(flag, 2)

        for write_action in write_queue:
            write_action()

    @property
    def complexity(self) -> int:
        if self.submovement_ is None:
            return 0

        return self.submovement_.complexity + 1


def main():
    pass


if __name__ == "__main__":
    main()
