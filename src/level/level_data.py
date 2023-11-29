# -*- coding: utf-8 -*-
"""
Created on 2023/11/23

@author: brassbeat
"""
import dataclasses
import json
from collections.abc import Iterable
from typing import Self, TextIO

from level.level_reader import PeggleDataReader
from level.level_writer import PeggleDataWriter
from level.objects.object import PeggleObject

import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class Level:
    def __init__(self, file_version: int, objects: Iterable[PeggleObject]):
        self.file_version = file_version
        self.level_objects = list(objects)
        self.movement_pool: ...

    @classmethod
    def read_data(cls, f: PeggleDataReader) -> Self:
        file_version = f.read_int()
        f.read_byte()
        object_count = f.read_int()
        level_objects = [PeggleObject.read_data(file_version, f) for _ in range(object_count)]
        return cls(file_version, level_objects)

    def write_data(self, f: PeggleDataWriter) -> None:
        ...

    def dump_json(self, f: TextIO):
        json.dump(
                {
                        "file_version": self.file_version,
                        "level_objects": [dataclasses.asdict(obj) for obj in self.level_objects]
                },
                f,
                indent=2,
        )


def main():
    with open("test/baseball.dat", "rb") as f:
        r = PeggleDataReader(f)
        level_ = Level.read_data(r)

    with open("test/baseball.json", "w") as f:
        level_.dump_json(f)


if __name__ == "__main__":
    main()
