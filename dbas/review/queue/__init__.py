from enum import Enum, auto

# If you want to add a new queue, please
#  - add a key_<your_queue_name>
#  - add a model_mapping key_<your_queue_name>: <your_db_table>  in mapper.py
#  - add a reputation_icon key_<your_queue_name>: <your_font_awesome_icon> in reputation.py
#  - please add the translation string like queue<Yourname> and priv_access_<queuename>_access (respect the capitals)


max_votes = 5  # highest count of votes
min_difference = 3  # least count of difference between okay / not okay

# list of queues where reviews can be done
key_edit: str = 'edit'
key_delete: str = 'delete'
key_duplicate: str = 'duplicate'
key_optimization: str = 'optimization'
key_merge: str = 'merge'
key_split: str = 'split'

review_queues = [
    key_edit,
    key_delete,
    key_duplicate,
    key_optimization,
    key_merge,
    key_split
]

# list of all queues, including the voted reviews as well as the ongoing ones
key_history: str = 'history'  # this queue has it's own route
key_ongoing: str = 'ongoing'  # this queue has it's own route
all_queues = review_queues + [key_history, key_ongoing]
max_lock_time_in_sec: int = 180


class Code(Enum):
    DOESNT_EXISTS = auto()
    DUPLICATE = auto()
    SUCCESS = auto()
    ERROR = auto()
