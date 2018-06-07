from enum import Enum, auto


class FlaggedBy(Enum):
    user = auto()
    other = auto()


class ReviewDeleteReasons(Enum):
    offtopic = 'offtopic'
    harmful = 'harmful'


# text length of the elements on the history and ongoing page
# please note, that a hover will always show the full text
txt_len_history_page = 35
