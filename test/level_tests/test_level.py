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

from level.level_writer import PeggleDataWriter

_LOGS_PATH = "./logs/logs.txt"

logging.basicConfig(filename=_LOGS_PATH)
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
        self.export_directory = "./level_tests/exports"
        with open(_LOGS_PATH, "w") as _:
            pass

    def read_and_dump_data(self, level_directory: str):
        for f, filename in self.get_levels(level_directory):
            _logger.info("=" * 50)
            _logger.info(f"Reading in level {filename}.dat")
            _logger.info("=" * 50)
            with self.subTest(filename=filename):
                reader = PeggleDataReader(f)
                level = Level.read_data(reader)
                dump_location = f"{self.dump_directory}/{filename}.json"
                with open(dump_location, "w") as d:
                    level.dump_json(d)

    def read_and_unlink_and_dump_data(self, level_directory: str):
        for f, filename in self.get_levels(level_directory):
            _logger.info("=" * 50)
            _logger.info(f"Reading in level {filename}.dat")
            _logger.info("=" * 50)
            with self.subTest(filename=filename):
                reader = PeggleDataReader(f)
                dump_location = f"{self.dump_directory}/{filename}.json"
                with open(dump_location, "w") as d:
                    Level.read_and_dump_link_and_unlink(reader, d)

    def read_and_export_data(self, level_directory: str):
        for f, filename in self.get_levels(level_directory):
            with self.subTest(filename=filename):
                data = f.read()
                f.seek(0)
                reader = PeggleDataReader(f)
                level = Level.read_data(reader)
                dump_location = f"{self.export_directory}/{filename}.dat"
                with open(dump_location, "wb") as d:
                    writer = PeggleDataWriter(d)
                    level.write_data(writer)

                with open(dump_location, "rb") as f2:
                    data2 = f2.read()

                self.assertEqual(data, data2)

    def read_and_export_data_twice(self, level_directory: str):
        for f, filename in self.get_levels(level_directory):
            with self.subTest(filename=filename):
                reader = PeggleDataReader(f)
                level = Level.read_data(reader)
                dump_location = f"{self.export_directory}/{filename}.dat"
                with open(dump_location, "wb") as d:
                    writer = PeggleDataWriter(d)
                    level.write_data(writer)

                with open(dump_location, "rb") as f2:
                    data2 = f2.read()
                    f2.seek(0)
                    reader = PeggleDataReader(f2)
                    level2 = Level.read_data(reader)

                with open(dump_location, "wb") as d:
                    writer = PeggleDataWriter(d)
                    level2.write_data(writer)

                with open(dump_location, "rb") as f3:
                    data3 = f3.read()

                self.assertEqual(data2, data3)

    def test_read_data_pegs_only(self):
        level_directory = "./level_tests/levels/1a) pegs only"
        self.read_and_dump_data(level_directory)

    def test_write_data_pegs_only(self):
        level_directory = "./level_tests/levels/1a) pegs only"
        self.read_and_export_data(level_directory)

    def test_read_data_straight_bricks(self):
        level_directory = "./level_tests/levels/2) straight bricks"
        self.read_and_dump_data(level_directory)

    def test_write_data_straight_bricks(self):
        level_directory = "./level_tests/levels/2) straight bricks"
        self.read_and_export_data(level_directory)

    def test_read_data_curved_bricks(self):
        level_directory = "./level_tests/levels/3) curved bricks"
        self.read_and_dump_data(level_directory)

    def test_write_data_curved_bricks(self):
        level_directory = "./level_tests/levels/3) curved bricks"
        self.read_and_export_data(level_directory)

    def test_read_data_fever(self):
        level_directory = "./level_tests/levels/3b) fever"
        self.read_and_dump_data(level_directory)

    def test_read_data_rods(self):
        level_directory = "./level_tests/levels/4) rods"
        self.read_and_dump_data(level_directory)

    def test_write_data_rods(self):
        level_directory = "./level_tests/levels/4) rods"
        self.read_and_export_data(level_directory)

    def test_read_data_polygons(self):
        level_directory = "./level_tests/levels/5) polygons"
        self.read_and_dump_data(level_directory)

    def test_write_data_polygons(self):
        level_directory = "./level_tests/levels/5) polygons"
        self.read_and_export_data(level_directory)
        self.read_and_export_data(level_directory)

    def test_read_data_basic_movements(self):
        level_directory = "./level_tests/levels/6) basic movements"
        self.read_and_dump_data(level_directory)

    def test_write_data_basic_movements(self):
        level_directory = "./level_tests/levels/6) basic movements"
        self.read_and_export_data(level_directory)

    def test_read_data_submovements(self):
        level_directory = "./level_tests/levels/7) submovements"
        self.read_and_dump_data(level_directory)

    def test_unlink_data_submovements(self):
        level_directory = "./level_tests/levels/7) submovements"
        self.read_and_unlink_and_dump_data(level_directory)

    def test_write_data_submovements(self):
        # this test needs to be different since we normalize object hierarchy
        level_directory = "./level_tests/levels/7) submovements"
        self.read_and_export_data_twice(level_directory)
