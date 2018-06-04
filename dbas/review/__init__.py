from enum import Enum, auto


class FlaggedBy(Enum):
    user = auto()
    other = auto()


class ReviewDeleteReasons(Enum):
    offtopic = 'offtopic'
    harmful = 'harmful'
