# -*- coding: utf-8 -*-
"""
Created on 2023/11/20

@author: brassbeat
"""

# noinspection PyUnresolvedReferences
import pyautogui

from .enums import Direction
from ..process.process import PeggleProcess


class PeggleBot:
    def __init__(self, process: PeggleProcess):
        self.process = process

    def read_level_cycle(self) -> int:
        ...

    def read_level_state(self) -> int:
        ...

    def line_up_timing(self, frame: int, period: int):
        ...

    def scroll(self, direction: Direction, amount: int):
        ...

    def move_to_pixel(self, x: int, y: int):
        ...


def main():
    pass


if __name__ == "__main__":
    main()
