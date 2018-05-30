from enum import Enum, auto

from dbas.database.discussion_model import ReviewDelete, ReviewOptimization, ReviewEdit, ReviewDuplicate, ReviewSplit, \
    ReviewMerge
from dbas.strings.keywords import Keywords as _

# If you want to add a new queue, please
#  - add a key_<your_queue_name>
#  - add a model_mapping key_<your_queue_name>: <your_db_table>
#  - add a reputation_icon key_<your_queue_name>: <your_font_awesome_icon>
#  - please add the translation string like queue<Yourname> and priv_access_<queuename>_access (respect the capitals)

max_lock_time_in_sec: int = 180
key_edit: str = 'edit'
key_delete: str = 'delete'
key_duplicate: str = 'duplicate'
key_optimization: str = 'optimization'
key_merge: str = 'merge'
key_split: str = 'split'
key_history: str = 'history'  # this queue has it's own route
key_ongoing: str = 'ongoing'  # this queue has it's own route

# list of queues where reviews can be done
review_queues = [
    key_edit,
    key_delete,
    key_duplicate,
    key_optimization,
    key_merge,
    key_split
]

# list of all queues, including the voted reviews as well as the ongoing ones
all_queues = review_queues + [key_history, key_ongoing]

# key value pairs of the queue key and a title string
title_mapping = {key: _.get_key_by_string(_.queue.value + key[0:1].upper() + key[1:]) for key in review_queues}

# key value pairs of the queue key and the table object
model_mapping = {
    key_edit: ReviewEdit,
    key_delete: ReviewDelete,
    key_duplicate: ReviewDuplicate,
    key_optimization: ReviewOptimization,
    key_merge: ReviewMerge,
    key_split: ReviewSplit
}


class Code(Enum):
    DOESNT_EXISTS = auto()
    DUPLICATE = auto()
    SUCCESS = auto()
    ERROR = auto()


smallest_border = 30
reputation_borders = {**{key: smallest_border for key in review_queues}, **{key_history: 150, key_ongoing: 300}}

reputation_icons = {
    key_edit: 'fa fa-pencil-square-o',
    key_delete: 'fa fa-trash-o',
    key_duplicate: 'fa fa-files-o',
    key_optimization: 'fa fa-compress',
    key_merge: 'fa fa-flag',
    key_split: 'fa fa-expand',
    key_history: 'fa fa-history',
    key_ongoing: 'fa fa-clock-o'
}

# every reason by its name
rep_reason_first_position = 'rep_reason_first_position'
rep_reason_first_justification = 'rep_reason_first_justification'
rep_reason_first_argument_click = 'rep_reason_first_argument_click'
rep_reason_first_confrontation = 'rep_reason_first_confrontation'
rep_reason_first_new_argument = 'rep_reason_first_new_argument'
rep_reason_new_statement = 'rep_reason_new_statement'
rep_reason_success_flag = 'rep_reason_success_flag'
rep_reason_success_edit = 'rep_reason_success_edit'
rep_reason_success_duplicate = 'rep_reason_success_duplicate'
rep_reason_bad_flag = 'rep_reason_bad_flag'
rep_reason_bad_edit = 'rep_reason_bad_edit'
rep_reason_bad_duplicate = 'rep_reason_bad_duplicate'


max_votes = 5  # highest count of votes
min_difference = 3  # least count of difference between okay / not okay