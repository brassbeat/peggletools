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

    def write_byte(self, data: int):
        self.file.write(struct.pack("<b", data))

    def write_float(self, data: float):
        self.file.write(struct.pack("<f", data))

    def write_bitfield(self, data: int):
        self.file.write(data.to_bytes(-(-data.bit_length() // 8), byteorder="little", signed=False))

    def write_string(self, data: str):
        size = len(data)
        self.file.write(struct.pack(f"<H{size}s", size, data))

    def write_raw(self, data: bytes):
        self.file.write(data)


def main():
    pass


if __name__ == "__main__":
    main()
