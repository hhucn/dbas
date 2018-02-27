/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxReviewHandler() {
	'use strict';
	
	/**
	 *
	 * @param uid
	 * @param reason
	 * @param is_argument
	 * @param extra_uid
	 */
	this.flagArgumentOrStatement = function (uid, reason, is_argument, extra_uid) {
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
	this.splitOrMerge = function (pgroup_uid, key, text_values) {
		var is_premisegroup = typeof text_values === "undefined";
		var url = 'split_or_merge_' + (is_premisegroup ? 'premisegroup' : 'statement');
		var data = {
			uid: parseInt(pgroup_uid),
			key: key,
			text_values: text_values
		};
		var done = function ajaxSplitOrMergeStatementsDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData.info.length !== 0) {
				setGlobalInfoHandler('Ohh!', parsedData.info);
			} else {
				setGlobalSuccessHandler('Yeah!', parsedData.success);
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
	this.un_lockOptimizationReview = function (review_uid, should_lock, review_instance) {
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
	
	/**
	 *
	 * @param should_delete
	 * @param review_uid
	 */
	this.reviewDeleteArgument = function (should_delete, review_uid) {
		var url = 'review_delete_argument';
		var data = {
			should_delete: should_delete,
			review_uid: parseInt(review_uid)
		};
		var done = function reviewDeleteArgumentDone() {
			if (window.location.href.indexOf('/review/')) {
				new Review().reloadPageAndUnlockData(false);
			}
		};
		var fail = function reviewDeleteArgumentFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param is_edit_okay
	 * @param review_uid
	 */
	this.reviewEditArgument = function (is_edit_okay, review_uid) {
		var url = 'review_edit_argument';
		var data = {
			is_edit_okay: is_edit_okay,
			review_uid: parseInt(review_uid)
		};
		var done = function reviewDeleteArgumentDone() {
			if (window.location.href.indexOf('/review/')) {
				new Review().reloadPageAndUnlockData(false);
			}
		};
		var fail = function reviewDeleteArgumentFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param is_duplicate
	 * @param review_uid
	 */
	this.reviewDuplicateStatement = function (is_duplicate, review_uid) {
		var url = 'review_duplicate_statement';
		var data = {
			is_duplicate: is_duplicate,
			review_uid: parseInt(review_uid)
		};
		var done = function reviewDuplicateStatementDone() {
			if (window.location.href.indexOf('/review/')) {
				new Review().reloadPageAndUnlockData(false);
			}
		};
		var fail = function reviewDuplicateStatementFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param should_optimized
	 * @param review_uid
	 * @param new_data (Important: must be JSON.stringify(...))
	 */
	this.reviewOptimizationArgument = function (should_optimized, review_uid, new_data) {
		var url = 'review_optimization_argument';
		var data = {
			should_optimized: should_optimized,
			review_uid: parseInt(review_uid),
			new_data: new_data
		};
		var done = function reviewDeleteArgumentDone() {
			if (window.location.href.indexOf('/review/')) {
				new Review().reloadPageAndUnlockData(false);
			}
		};
		var fail = function reviewDeleteArgumentFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param should_merged
	 * @param review_uid
	 */
	this.reviewMergeStatement = function (should_merged, review_uid) {
		var url = 'review_merged_premisegroup';
		var data = {
			should_merge: should_merge,
			review_uid: parseInt(review_uid)
		};
		var done = function reviewDuplicateStatementDone() {
			if (window.location.href.indexOf('/review/')) {
				new Review().reloadPageAndUnlockData(false);
			}
		};
		var fail = function reviewDuplicateStatementFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param should_split
	 * @param review_uid
	 */
	this.reviewSplitStatement = function (should_split, review_uid) {
		var url = 'review_split_premisegroup';
		var data = {
			should_split: should_split,
			review_uid: parseInt(review_uid)
		};
		var done = function reviewDuplicateStatementDone() {
			if (window.location.href.indexOf('/review/')) {
				new Review().reloadPageAndUnlockData(false);
			}
		};
		var fail = function reviewDuplicateStatementFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param queue
	 * @param uid
	 */
	this.undoReview = function (queue, uid) {
		var url = 'undo_review';
		var data = {
			queue: queue,
			uid: parseInt(uid)
		};
		var done = function reviewUndoDone(data) {
			if (data.info.length !== 0) {
				setGlobalInfoHandler(_t(ohsnap), data.info);
			} else {
				setGlobalSuccessHandler('Yep!', data.success);
				$('#' + queue + uid).remove();
			}
		};
		var fail = function reviewUndoFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
	
	/**
	 *
	 * @param queue
	 * @param uid
	 */
	this.cancelReview = function (queue, uid) {
		var url = 'cancel_review';
		var data = {
			queue: queue,
			uid: parseInt(uid)
		};
		var done = function reviewCancelDone(data) {
			if (data.info.length !== 0) {
				setGlobalInfoHandler(_t(ohsnap), data.info);
			} else {
				setGlobalSuccessHandler('Yep!', data.success);
				$('#' + queue + uid).remove();
			}
		};
		var fail = function reviewCancelFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', data, done, fail);
	};
}
