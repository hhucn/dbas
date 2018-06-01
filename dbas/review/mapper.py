from dbas.database.discussion_model import ReviewEdit, ReviewDelete, ReviewDuplicate, ReviewOptimization, ReviewMerge, \
    ReviewSplit, LastReviewerEdit, LastReviewerDelete, LastReviewerDuplicate, LastReviewerOptimization, \
    LastReviewerMerge, LastReviewerSplit
from dbas.review.queue import review_queues, key_edit, key_delete, key_duplicate, key_optimization, key_merge, key_split
from dbas.review.queue.delete import DeleteQueue
from dbas.review.queue.duplicate import DuplicateQueue
from dbas.review.queue.edit import EditQueue
from dbas.review.queue.merge import MergeQueue
from dbas.review.queue.optimization import OptimizationQueue
from dbas.review.queue.split import SplitQueue
from dbas.strings.keywords import Keywords as _

# key value pairs of the queue key and a title string
from dbas.strings.lib import start_with_capital

title_mapping = {key: _.get_key_by_string(_.queue.value + start_with_capital(key)) for key in review_queues}

# key value pairs of the queue key and the table object
model_mapping = {
    key_edit: ReviewEdit,
    key_delete: ReviewDelete,
    key_duplicate: ReviewDuplicate,
    key_optimization: ReviewOptimization,
    key_merge: ReviewMerge,
    key_split: ReviewSplit
}

# key value pairs of the queue key and the queue object
queue_mapping = {
    key_edit: EditQueue,
    key_delete: DeleteQueue,
    key_duplicate: DuplicateQueue,
    key_optimization: OptimizationQueue,
    key_merge: MergeQueue,
    key_split: SplitQueue
}

# key value pairs of the queue key and the last reviewer object
reviewer_mapping = {
    key_edit: LastReviewerEdit,
    key_delete: LastReviewerDelete,
    key_duplicate: LastReviewerDuplicate,
    key_optimization: LastReviewerOptimization,
    key_merge: LastReviewerMerge,
    key_split: LastReviewerSplit
}
