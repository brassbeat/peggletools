# -*- coding: utf-8 -*-
"""
Created on 2023/11/19

@author: brassbeat
"""
import pymem

from .enums import PeggleVersion
from .entry import Entry


class PeggleProcess:
    def __init__(self, process: pymem.Pymem):
        self.process = process
        self.base_address = process.base_address
        self.version = PeggleVersion.from_process(process)

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.close_process()

    def read_int_entry(self, entry: Entry) -> int:
        # noinspection PyTypeChecker
        address = self.process.resolve_offsets(entry.base_address, entry.offsets)
        return self.process.read_int(address)

    def read_float_entry(self, entry: Entry) -> float:
        # noinspection PyTypeChecker
        address = self.process.resolve_offsets(entry.base_address, entry.offsets)
        return self.process.read_float(address)


def main():
    pass


if __name__ == "__main__":
    main()
