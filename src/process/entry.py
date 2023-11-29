# -*- coding: utf-8 -*-
"""
Created on 2023/11/19

@author: brassbeat
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    base_address: int
    offsets: tuple[int]
