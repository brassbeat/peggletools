# -*- coding: utf-8 -*-
"""
Created on 2023/11/23

@author: brassbeat
"""

import struct
from typing import BinaryIO


class PeggleDataWriter:
    def __init__(self, file: BinaryIO):
        self.file = file

    def write_int(self, data: int):
        self.file.write(struct.pack("<i", data))

    def write_short(self, data: int):
        self.file.write(struct.pack("<h", data))

    def write_byte(self, data: int):
        self.file.write(struct.pack("<b", data))

    def write_float(self, data: float):
        self.file.write(struct.pack("<f", data))

    def write_bitfield(self, data: int, size: int):
        self.file.write(data.to_bytes(size, byteorder="little", signed=False))

    def write_string(self, data: str):
        size = len(data)
        bytes_data = data.encode(encoding="ascii")
        self.file.write(struct.pack(f"<H{size}s", size, bytes_data))

    def write_raw(self, data: bytes):
        self.file.write(data)


def main():
    pass


if __name__ == "__main__":
    main()
