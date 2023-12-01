# -*- coding: utf-8 -*-
"""
Created on 2023/11/23

@author: brassbeat
"""

import struct
from typing import BinaryIO

import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class PeggleDataReader:
    def __init__(self, file: BinaryIO):
        self.file = file

    def read_int(self) -> int:
        data = struct.unpack("<i", self.file.read(4))[0]
        _logger.debug(f"Read int data point {data}.")
        return data

    def read_byte(self) -> int:
        data = struct.unpack("<b", self.file.read(1))[0]
        _logger.debug(f"Read byte data point {data}.")
        return data

    def read_float(self) -> float:
        data = struct.unpack("<f", self.file.read(4))[0]
        _logger.debug(f"Read float data point {data}.")
        return data

    def read_bitfield(self, size: int) -> int:  # I chose IntFlags to represent these internally, so return an int
        raw_data = self.file.read(size)
        _logger.debug(f"Read raw bitfield data {raw_data}")
        data = int.from_bytes(raw_data, byteorder="little", signed=False)
        _logger.debug(f"Read bitfield data point {data} of size {size}.")
        return data

    def read_string(self) -> str:
        size: int = struct.unpack("<H", self.file.read(2))[0]
        _logger.debug(f"Found string size of {size}.")
        data = struct.unpack(f"<{size}s", self.file.read(size))[0]
        _logger.debug(f"Read string data point {data}.")
        return data

    def read_raw(self, size: int) -> bytes:
        data = self.file.read(size)
        _logger.debug(f"Read raw data point {data} of size {size}.")
        return data


def main():
    pass


if __name__ == "__main__":
    main()
