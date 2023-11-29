# -*- coding: utf-8 -*-
"""
Created on _

@author: brassbeat
"""
import os.path
from collections.abc import Iterator
from io import BytesIO
from unittest import TestCase

from level.level_data import Level
from level.level_reader import PeggleDataReader

import logging

logging.basicConfig(filename="./logs/logs.txt")
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class TestLevel(TestCase):
    @staticmethod
    def get_levels(directory: str | os.PathLike) -> Iterator[tuple[BytesIO, str]]:
        assert os.path.exists(directory)
        print(os.listdir(directory))
        for filename in os.listdir(directory):
            root_filename, _ = os.path.splitext(filename)
            file_path = f"{directory}/{filename}"
            with open(file_path, "rb") as f:
                yield f, root_filename

    def setUp(self) -> None:
        self.dump_directory = "./level_tests/dumps"

    def test_read_data_pegs_only(self):
        level_directory = "./level_tests/levels/1a) pegs only"
        for f, filename in self.get_levels(level_directory):
            with self.subTest(filename=filename):
                reader = PeggleDataReader(f)
                level = Level.read_data(reader)
                dump_location = f"{self.dump_directory}/{filename}.json"
                with open(dump_location, "w") as d:
                    level.dump_json(d)

