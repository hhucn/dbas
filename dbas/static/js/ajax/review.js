/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxReviewHandler(){
	
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
			if (should_lock)
				new ReviewCallbacks().forReviewLock(data, review_instance);
			else
				new ReviewCallbacks().forReviewUnlock(data);
		}).fail(function reviewDeleteArgumentFail() {
			if (should_lock)
				setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
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
			new ReviewCallbacks().forReviewArgument(data);
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
			new ReviewCallbacks().forReviewArgument(data);
		}).fail(function reviewDeleteArgumentFail() {
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
			new ReviewCallbacks().forReviewArgument(data);
		}).fail(function reviewDeleteArgumentFail() {
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
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewHistoryCallbacks().forUndoReview(data, queue, uid);
		}).fail(function reviewDeleteArgumentFail() {
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
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewHistoryCallbacks().forUndoReview(data, queue, uid);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	}
	
}
