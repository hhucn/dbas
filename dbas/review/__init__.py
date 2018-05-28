from enum import Enum, auto

from dbas.database.discussion_model import ReviewDelete, ReviewOptimization, ReviewEdit, ReviewDuplicate, ReviewSplit, \
    ReviewMerge
from dbas.strings.keywords import Keywords as _

max_lock_time_in_sec = 180
key_edits = 'edits'
key_deletes = 'deletes'
key_duplicates = 'duplicates'
key_optimizations = 'optimizations'
key_merge = 'merges'
key_split = 'splits'
key_history = 'history'
key_ongoing = 'ongoing'

review_queues = [
    key_deletes,
    key_optimizations,
    key_edits,
    key_duplicates,
    key_merge,
    key_split
]

title_mapping = {
    key_deletes: _.queueDelete,
    key_optimizations: _.queueOptimization,
    key_edits: _.queueEdit,
    key_duplicates: _.queueDuplicates,
    key_split: _.queueSplit,
    key_merge: _.queueMerge
}

model_mapping = {
    key_deletes: ReviewDelete,
    key_optimizations: ReviewOptimization,
    key_edits: ReviewEdit,
    key_duplicates: ReviewDuplicate,
    key_split: ReviewSplit,
    key_merge: ReviewMerge
}


class Code(Enum):
    DOESNT_EXISTS = auto()
    DUPLICATE = auto()
    SUCCESS = auto()
    ERROR = auto()
