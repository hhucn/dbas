function AjaxReviewHandler() {
}

/**
 *
 * @param uid
 * @param reason
 * @param is_argument
 * @param extra_uid
 */
AjaxReviewHandler.prototype.flagArgumentOrStatement = function (uid, reason, is_argument, extra_uid) {
    'use strict';
    var url = 'flag_argument_or_statement';
    var data = {
        uid: uid,
        reason: reason,
        extra_uid: extra_uid,
        is_argument: is_argument
    };
    var done = function ajaxFlagArgumentOrStatementDone(data) {
        if (data.info.length !== 0) {
            setGlobalInfoHandler('Ohh!', data.info);
        } else {
            setGlobalSuccessHandler('Yeah!', data.success);
        }
        $('#popup-duplicate-statement').modal('hide');
    };
    var fail = function ajaxFlagArgumentOrStatementFail(data) {
        setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', data, done, fail);
};

/**
 *
 * @param pgroup_uid
 * @param key
 * @param text_values
 */
AjaxReviewHandler.prototype.splitOrMerge = function (pgroup_uid, key, text_values) {
    'use strict';
    var is_premisegroup = typeof text_values === "undefined";
    var url = 'split_or_merge_' + (is_premisegroup ? 'premisegroup' : 'statement');
    var data = {
        uid: parseInt(pgroup_uid),
        key: key,
        text_values: text_values
    };
    var done = function ajaxSplitOrMergeStatementsDone(data) {
        if (data.info.length !== 0) {
            setGlobalInfoHandler('Ohh!', data.info);
        } else {
            setGlobalSuccessHandler('Yeah!', data.success);
        }
    };
    var fail = function ajaxSplitOrMergeStatementsFail(data) {
        setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', data, done, fail);
};

/**
 *
 * @param review_uid
 * @param should_lock is true, when the review should be locked and false otherwise
 * @param review_instance
 */
AjaxReviewHandler.prototype.un_lockOptimizationReview = function (review_uid, should_lock, review_instance) {
    'use strict';
    var url = 'review_lock';
    var data = {
        'review_uid': parseInt(review_uid),
        'lock': should_lock
    };
    var done = function un_lockOptimizationReviewDone(data) {
        if (should_lock) {
            new ReviewCallbacks().forReviewLock(data, review_instance);
        } else {
            new ReviewCallbacks().forReviewUnlock(data);
        }
    };
    var fail = function un_lockOptimizationReviewFail(data) {
        if (should_lock) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        }
    };
    ajaxSkeleton(url, 'POST', data, done, fail);
};

AjaxReviewHandler.prototype.__ajax_skeleton = function (url, data) {
    'use strict';
    var done = function () {
        if (window.location.href.indexOf('/review/')) {
            new Review().reloadPage();
        }
    };
    var fail = function (data) {
        setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', data, done, fail);
};

/**
 *
 * @param should_delete
 * @param review_uid
 */
AjaxReviewHandler.prototype.reviewDeleteArgument = function (should_delete, review_uid) {
    'use strict';
    var url = 'review_delete_argument';
    var data = {
        should_delete: should_delete,
        review_uid: parseInt(review_uid)
    };
    this.__ajax_skeleton(url, data, false);
};

/**
 *
 * @param is_edit_okay
 * @param review_uid
 */
AjaxReviewHandler.prototype.reviewEditArgument = function (is_edit_okay, review_uid) {
    'use strict';
    var url = 'review_edit_argument';
    var data = {
        is_edit_okay: is_edit_okay,
        review_uid: parseInt(review_uid)
    };
    this.__ajax_skeleton(url, data, false);
};

/**
 *
 * @param is_duplicate
 * @param review_uid
 */
AjaxReviewHandler.prototype.reviewDuplicateStatement = function (is_duplicate, review_uid) {
    'use strict';
    var url = 'review_duplicate_statement';
    var data = {
        is_duplicate: is_duplicate,
        review_uid: parseInt(review_uid)
    };
    this.__ajax_skeleton(url, data, false);
};

/**
 *
 * @param should_optimized
 * @param review_uid
 * @param new_data (Important: must be JSON.stringify(...))
 */
AjaxReviewHandler.prototype.reviewOptimizationArgument = function (should_optimized, review_uid, new_data) {
    'use strict';
    var url = 'review_optimization_argument';
    var data = {
        should_optimized: should_optimized,
        review_uid: parseInt(review_uid),
        new_data: new_data
    };
    var done = function reviewOptimizationArgumentDone() {
        if (window.location.href.indexOf('/review/')) {
            new Review().reloadPageAndUnlockData();
        }
    };
    var fail = function reviewOptimizationArgumentFail(data) {
        setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', data, done, fail);
};

/**
 *
 * @param should_merge
 * @param review_uid
 */
AjaxReviewHandler.prototype.reviewMergeStatement = function (should_merge, review_uid) {
    'use strict';
    var url = 'review_merged_premisegroup';
    var data = {
        should_merge: should_merge,
        review_uid: parseInt(review_uid)
    };
    this.__ajax_skeleton(url, data, false);
};

/**
 *
 * @param should_split
 * @param review_uid
 */
AjaxReviewHandler.prototype.reviewSplitStatement = function (should_split, review_uid) {
    'use strict';
    var url = 'review_splitted_premisegroup';
    var data = {
        should_split: should_split,
        review_uid: parseInt(review_uid)
    };
    this.__ajax_skeleton(url, data, false);
};

/**
 *
 * @param queue
 * @param uid
 */
AjaxReviewHandler.prototype.undoReview = function (queue, uid) {
    'use strict';
    var url = 'undo_review';
    var data = {
        queue: queue,
        uid: parseInt(uid)
    };
    this.__ajax_skeleton(url, data, true, uid);
};

/**
 *
 * @param queue
 * @param uid
 */
AjaxReviewHandler.prototype.cancelReview = function (queue, uid) {
    'use strict';
    var url = 'cancel_review';
    var data = {
        queue: queue,
        uid: parseInt(uid)
    };
    this.__ajax_skeleton(url, data, true, uid);
};

AjaxReviewHandler.prototype.__ajax_skeleton = function (url, data, remove_element_on_success, uid) {
    'use strict';
    var done = function (data) {
        if ($.type(data) === 'object' && 'info' in data && data.info.length !== 0) {
            setGlobalInfoHandler(_t(ohsnap), data.info);
        } else {
            setGlobalSuccessHandler('Yep!', data);
            if (remove_element_on_success) {
                $('#' + queue + uid).remove();
            }
            new Review().reloadPage();
        }
    };
    var fail = function (data) {
        setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', data, done, fail);
};
