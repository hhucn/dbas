from enum import IntEnum


class FuzzyMode(IntEnum):
    START_STATEMENT = 0
    EDIT_STATEMENT = 1
    START_PREMISE = 2
    ADD_REASON = 3
    FIND_DUPLICATE = 4
    FIND_USER = 5
    FIND_MERGESPLIT = 6
    FIND_STATEMENT = 7
