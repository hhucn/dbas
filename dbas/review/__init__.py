from enum import Enum, auto

# If you want to add a new queue, please
#  - add a key_<your_queue_name>
#  - add a model_mapping key_<your_queue_name>: <your_db_table>  in mapper.py
#  - add a reputation_icon key_<your_queue_name>: <your_font_awesome_icon> in reputation.py
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


class Code(Enum):
    DOESNT_EXISTS = auto()
    DUPLICATE = auto()
    SUCCESS = auto()
    ERROR = auto()
