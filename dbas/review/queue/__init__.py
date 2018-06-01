from dbas.review import key_edit, key_delete, key_duplicate, key_optimization, key_merge, key_split, key_history, \
    key_ongoing

max_votes = 5  # highest count of votes
min_difference = 3  # least count of difference between okay / not okay

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
