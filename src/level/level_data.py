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
from level.objects.movement_data import Movement
from level.objects.object import PeggleObject

import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class Level:
    """
    Represents level data contained in a .dat file.
    """
    def __init__(
            self,
            file_version: int,
            objects: Iterable[PeggleObject] | None = None
    ):
        self.file_version = file_version
        self.level_objects: list[PeggleObject] = list(objects) if objects else list()
        self.movement_pool: list[Movement] = []

    @classmethod
    def read_data(cls, f: PeggleDataReader) -> Self:
        file_version = f.read_int()
        f.read_byte()

        object_count = f.read_int()
        level = cls(file_version)

        for _ in range(object_count):
            level.read_object(file_version, f)

        level.resolve_link_ids()

        return level

    @classmethod
    def read_and_dump_no_linking(cls, src: PeggleDataReader, dst: TextIO) -> Self:
        file_version = src.read_int()
        src.read_byte()

        object_count = src.read_int()
        level = cls(file_version)

        for _ in range(object_count):
            level.read_object(file_version, src)

        level.dump_json(dst)

        return level

    @classmethod
    def read_and_dump_link_and_unlink(cls, src: PeggleDataReader, dst: TextIO) -> Self:
        file_version = src.read_int()
        src.read_byte()

        object_count = src.read_int()
        level = cls(file_version)

        for _ in range(object_count):
            level.read_object(file_version, src)

        level.unlink_nested_objects()

        level.dump_json(dst)

        return level

    def write_data(self, f: PeggleDataWriter) -> None:
        self.sort_level_objects()
        self.unlink_nested_objects()

        f.write_int(self.file_version)
        f.write_byte(1)
        f.write_int(len(self.level_objects))
        for obj in self.level_objects:
            obj.write_data(self.file_version, f)

    def dump_json(self, f: TextIO):
        json.dump(
                {
                        "file_version": self.file_version,
                        "level_objects": [dataclasses.asdict(obj) for obj in self.level_objects]
                },
                f,
                indent=2,
        )

    def get_joint_object_list(self) -> list[Movement | PeggleObject | None]:
        """
        Preparation function to dereference link ids of loaded objects.
        :return: list of level objects L, where L[id] resolves to the correct object for how Peggle stores link ids.
        """
        joint_list: list[Movement | PeggleObject | None] = [None, None, None]
        for obj in self.level_objects:
            joint_list.append(obj)

            movement = obj.movement_data

            while movement is not None:
                _logger.debug(f"Found movement of type {type(movement).__name__}")
                joint_list.append(movement)
                movement = movement.submovement_

        return joint_list

    def get_normal_joint_object_list(self) -> list[Movement | PeggleObject | None]:
        """
        Preparation function unlink nested objects and replace them with link id references.
        :return: list of level objects L, where L[id] resolves to the correct object for how Peggle stores link ids.
        """
        joint_list: list[Movement | PeggleObject | None] = [None, None, None]
        for obj in self.level_objects:
            joint_list.append(obj)

            if (movement := obj.movement_data) is not None:
                joint_list.append(movement)

        return joint_list

    def resolve_link_ids(self) -> None:
        """
        Replace implicit references to other objects in the form of numeric link ids with proper object references.
        """
        joint_list = self.get_joint_object_list()
        for obj in self.level_objects:
            for link_id, setter in obj.get_unresolved_link_ids():
                attr = joint_list[link_id]
                setter(attr)

    def unlink_nested_objects(self) -> None:
        joint_list = self.get_normal_joint_object_list()
        for obj in self.level_objects:
            _logger.debug("Looking for entries to unlink...")
            for sub_obj, setter in obj.get_linked_entries():
                link_id = joint_list.index(sub_obj)
                _logger.debug(f"Found link id to set: {link_id}")
                setter(link_id)

    def sort_level_objects(self):
        self.level_objects.sort(key=lambda obj: obj.complexity)

    def read_object(self, file_version: int, f: PeggleDataReader) -> PeggleObject:
        """
        Register a level object from the data stream and return it.
        :param file_version: ...
        :param f: Data stream to be read from.
        :return: Object registered.
        """
        obj = PeggleObject.read_data(
                file_version,
                f,
                object_callback=self.read_object,
                movement_callback=self.read_movement,
        )
        self.level_objects.append(obj)
        return obj

    def read_movement(self, file_version: int, f: PeggleDataReader) -> Movement:
        """
        Register a level movement from the data stream and return it.
        :param file_version: ...
        :param f: Data stream to be read from.
        :return: Movement registered.
        """
        obj = Movement.read_data(
                file_version,
                f,
                object_callback=self.read_object,
                movement_callback=self.read_movement,
        )
        self.movement_pool.append(obj)
        return obj


def main():
    with open("test/baseball.dat", "rb") as f:
        r = PeggleDataReader(f)
        level_ = Level.read_data(r)

    with open("test/baseball.json", "w") as f:
        level_.dump_json(f)


if __name__ == "__main__":
    main()
