# -*- coding: utf-8 -*-
"""
Created on 2023/11/29

@author: brassbeat
"""
import dataclasses
from dataclasses import dataclass
from typing import Self

from level.level_reader import PeggleDataReader
from level.level_writer import PeggleDataWriter


@dataclass
class InvalidPeggleObject:
    TYPE_VALUE: int = dataclasses.field(default=5, init=False, repr=False)

    @classmethod
    def read_data(cls, file_version: int, f: PeggleDataReader, **kwargs) -> Self:
        pass

    def write_data(self, file_version: int, f: PeggleDataWriter) -> None:
        raise ...


def main():
    pass


if __name__ == "__main__":
    main()
