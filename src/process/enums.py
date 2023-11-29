# -*- coding: utf-8 -*-
"""
Created on 2023/11/19

@author: brassbeat
"""
from enum import Enum, auto

import pymem


class PeggleVersion(Enum):
    DELUXE_EN = auto()

    @classmethod
    def from_process(cls, process: pymem.Pymem):
        ...


class PeggleVariable(Enum):
    LEVEL_CYCLE = auto()
    LEVEL_TIMER = auto()
    BOARD_STATE = auto()


def main():
    pass


if __name__ == "__main__":
    main()
