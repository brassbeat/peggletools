# -*- coding: utf-8 -*-
"""
Created on 2023/11/23

@author: brassbeat
"""
from typing import Protocol, Self

from level.level_reader import PeggleDataReader
from level.level_writer import PeggleDataWriter


class PeggleObjectData(Protocol):
    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader) -> Self:
        ...

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        ...


class SpecificObjectData(PeggleObjectData):
    TYPE_VALUE: int


def main():
    pass


if __name__ == "__main__":
    main()
