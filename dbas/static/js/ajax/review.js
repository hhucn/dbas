/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxReviewHandler(){
	'use strict';

	/**
	 *
	 * @param uid
	 * @param reason
	 * @param is_argument
	 * @param extra_uid
	 */
	this.flagArgumentOrStatement = function(uid, reason, is_argument, extra_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_flag_argument_or_statement',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				uid: uid,
				reason: reason,
				extra_uid: extra_uid,
				is_argument: is_argument
			}),
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxFlagArgumentOrStatementDone(data) {
			if (data.info.length !== 0) {
				setGlobalInfoHandler('Ohh!', data.info);
			} else {
				setGlobalSuccessHandler('Yeah!', data.success);
			}
			$('#popup-duplicate-statement').modal('hide');

		}).fail(function ajaxFlagArgumentOrStatementFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
		});
	};

	/**
	 *
	 * @param pgroup_uid
	 * @param key
	 * @param text_values
	 */
	this.splitOrMerge = function(pgroup_uid, key, text_values){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var is_premisegroup = typeof text_values === "undefined";
		var url = 'ajax_split_or_merge_' + (is_premisegroup? 'premisegroup' : 'statement');
		$.ajax({
			url: url,
			method: 'POST',
			data: {
				pgroup_uid: pgroup_uid,
				key: key,
				text_values: JSON.stringify(text_values)
			},
			global: false,
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSplitOrMergeStatementsDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData.error.length !== 0){
				setGlobalErrorHandler(_t(ohsnap), parsedData.error);
			} else if (parsedData.info.length !== 0) {
				setGlobalInfoHandler('Ohh!', parsedData.info);
			} else {
				setGlobalSuccessHandler('Yeah!', parsedData.success);
			}

		}).fail(function ajaxSplitOrMergeStatementsFail() {
			setGlobalErrorHandler('', _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param review_uid
	 * @param should_lock is true, when the review should be locked and false otherwise
	 * @param review_instance
	 */
	this.un_lockOptimizationReview = function (review_uid, should_lock, review_instance) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_lock',
			method: 'POST',
			data:{ 'review_uid': review_uid, 'lock': should_lock },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			if (should_lock) {
				new ReviewCallbacks().forReviewLock(data, review_instance);
			} else {
				new ReviewCallbacks().forReviewUnlock(data);
			}
		}).fail(function reviewDeleteArgumentFail() {
			if (should_lock) {
				setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			}
		});
	};

	/**
	 *
	 * @param should_delete
	 * @param review_uid
	 */
	this.reviewDeleteArgument = function(should_delete, review_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_delete_argument',
			method: 'POST',
			data:{ 'should_delete': should_delete, 'review_uid': review_uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewCallbacks().forReviewArgumentOrStatement(data);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param is_edit_okay
	 * @param review_uid
	 */
	this.reviewEditArgument = function(is_edit_okay, review_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_edit_argument',
			method: 'POST',
			data:{ 'is_edit_okay': is_edit_okay, 'review_uid': review_uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewCallbacks().forReviewArgumentOrStatement(data);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param is_duplicate
	 * @param review_uid
	 */
	this.reviewDuplicateStatement = function(is_duplicate, review_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_duplicate_statement',
			method: 'POST',
			data:{ 'is_duplicate': is_duplicate, 'review_uid': review_uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDuplicateStatementDone(data) {
			new ReviewCallbacks().forReviewArgumentOrStatement(data);
		}).fail(function reviewDuplicateStatementFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param should_optimized
	 * @param review_uid
	 * @param new_data (Important: must be JSON.stringify(...))
	 */
	this.reviewOptimizationArgument = function(should_optimized, review_uid, new_data){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_optimization_argument',
			type: 'POST',
			data:{
				'should_optimized': should_optimized,
				'review_uid': review_uid,
				'new_data': JSON.stringify(new_data) },
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewCallbacks().forReviewArgumentOrStatement(data);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param should_merged
	 * @param review_uid
	 */
	this.reviewMergeStatement = function(should_merged, review_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_merged_premisegroup',
			method: 'POST',
			data:{ 'should_merge': should_merge, 'review_uid': review_uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDuplicateStatementDone(data) {
			new ReviewCallbacks().forReviewArgumentOrStatement(data);
		}).fail(function reviewDuplicateStatementFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param should_split
	 * @param review_uid
	 */
	this.reviewSplitStatement = function(should_split, review_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_split_premisegroup',
			method: 'POST',
			data:{ 'should_split': should_split, 'review_uid': review_uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDuplicateStatementDone(data) {
			new ReviewCallbacks().forReviewArgumentOrStatement(data);
		}).fail(function reviewDuplicateStatementFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});

	};

	/**
	 *
	 * @param queue
	 * @param uid
	 */
	this.undoReview = function(queue, uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_undo_review',
			method: 'GET',
			data:{ 'queue': queue, uid: uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewUndoDone(data) {
			new ReviewHistoryCallbacks().forUndoReview(data, queue, uid);
		}).fail(function reviewUndoFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param queue
	 * @param uid
	 */
	this.cancelReview = function(queue, uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_cancel_review',
			method: 'GET',
			data:{ 'queue': queue, uid: uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewCancelDone(data) {
			new ReviewHistoryCallbacks().forUndoReview(data, queue, uid);
		}).fail(function reviewCancelFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
}
