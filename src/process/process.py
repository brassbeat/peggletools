# -*- coding: utf-8 -*-
"""
Created on 2023/11/19

@author: brassbeat
"""
import pymem

from enums import PeggleVersion
from entry import Entry


class PeggleProcess:
    def __init__(self, process: pymem.Pymem):
        self.process = process
        self.base_address = process.base_address
        self.version = PeggleVersion.from_process(process)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.close_process()

    def resolve_offsets(self, entry: Entry):
        read_method = self.process.read_uint

        addr = read_method(self.base_address + entry.base_address)
        for offset in entry.offsets[:-1]:
            addr = read_method(addr + offset)
            if not addr:
                return None

        return addr + entry.offsets[-1]

    def read_int_entry(self, entry: Entry) -> int | None:
        # noinspection PyTypeChecker
        address = self.resolve_offsets(entry)
        if not address:
            return None
        return self.process.read_int(address)

    def read_float_entry(self, entry: Entry) -> float:
        # noinspection PyTypeChecker
        address = self.resolve_offsets(entry)
        return self.process.read_float(address)


def main():
    base_offset = int("0x286768", base=16)
    timer_entry = Entry(base_offset, (1976, 188, 332))

    pm = pymem.Pymem("Peggle.exe")
    with PeggleProcess(pm) as process:

        address = process.resolve_offsets(timer_entry)
        print(hex(address))
        print(process.read_int_entry(timer_entry))


if __name__ == "__main__":
    main()
