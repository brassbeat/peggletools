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


class PeggleDataWriter:
    def __init__(self, file: BinaryIO):
        self.file = file
        self.position = 0

    def write_int(self, data: int):
        self.file.write(struct.pack("<i", data))
        _logger.debug(f"Wrote int data point {data!r} at position {self.position}.")
        self.position += 4

    def write_short(self, data: int):
        self.file.write(struct.pack("<h", data))
        _logger.debug(f"Wrote short data point {data!r} at position {self.position}.")
        self.position += 2

    def write_byte(self, data: int):
        self.file.write(struct.pack("<b", data))
        _logger.debug(f"Wrote byte data point {data!r} at position {self.position}.")
        self.position += 1

    def write_float(self, data: float):
        self.file.write(struct.pack("<f", data))
        _logger.debug(f"Wrote int data point {data!r} at position {self.position}.")
        self.position += 4

    def write_bitfield(self, data: int, size: int):
        self.file.write(data.to_bytes(size, byteorder="little", signed=False))
        _logger.debug(f"Wrote bitfield data point {data!r} of size {size} at position {self.position}.")
        self.position += size

    def write_string(self, data: str):
        size = len(data)
        bytes_data = data.encode(encoding="ascii")
        self.file.write(struct.pack(f"<H{size}s", size, bytes_data))
        _logger.debug(f"Wrote string data point {data!r} of size {size+2} at position {self.position}.")
        self.position += size + 2

    def write_raw(self, data: bytes):
        self.file.write(data)
        _logger.debug(f"Wrote raw data point {data!r} of size {len(data)} at position {self.position}.")
        self.position += len(data)


def main():
    pass


if __name__ == "__main__":
    main()
