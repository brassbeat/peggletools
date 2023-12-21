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
        self.position = 0

    def read_int(self) -> int:
        data = struct.unpack("<i", self.file.read(4))[0]
        _logger.debug(f"Read int data point {data!r} from position {self.position}.")
        self.position += 4
        return data

    def read_short(self) -> int:
        data = struct.unpack("<h", self.file.read(2))[0]
        _logger.debug(f"Read short data point {data!r} from position {self.position}.")
        self.position += 2
        return data

    def read_byte(self) -> int:
        data = struct.unpack("<b", self.file.read(1))[0]
        _logger.debug(f"Read byte data point {data!r} from position {self.position}.")
        self.position += 1
        return data

    def read_float(self) -> float:
        data = struct.unpack("<f", self.file.read(4))[0]
        _logger.debug(f"Read float data point {data!r} from position {self.position}.")
        self.position += 4
        return data

    def read_bitfield(self, size: int) -> int:  # I chose IntFlags to represent these internally, so return an int
        raw_data = self.file.read(size)
        _logger.debug(f"Read raw bitfield data {raw_data} from position {self.position}")
        data = int.from_bytes(raw_data, byteorder="little", signed=False)
        _logger.debug(f"Read bitfield data point {data!r} of size {size}.")
        self.position += size
        return data

    def read_string(self) -> str:
        size: int = struct.unpack("<H", self.file.read(2))[0]
        _logger.debug(f"Found string size of {size}.")
        bytes_data = struct.unpack(f"<{size}s", self.file.read(size))[0]
        data = str(bytes_data, encoding="ascii")
        _logger.debug(f"Read string data point {data!r} from position {self.position}.")
        self.position += size + 2
        return data

    def read_raw(self, size: int) -> bytes:
        data = self.file.read(size)
        _logger.debug(f"Read raw data point {data!r} of size {size} from position {self.position}.")
        self.position += size
        return data


def main():
    pass


if __name__ == "__main__":
    main()
