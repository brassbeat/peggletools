# -*- coding: utf-8 -*-
"""
Created on 2023/11/20

@author: brassbeat
"""
from dataclasses import dataclass

from .enums import Direction


@dataclass
class ParsedShot:
    x: int
    y: int
    tap_direction: Direction | None
    tap_count: int
    timing: int | None
    period: int
