/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	// buttons
	var optimization_ack = $('#opti_ack');
	var optimization_nack = $('#opti_nack');
	var optimization_skip = $('#opti_skip');
	var delete_ack = $('#del_ack');
	var delete_nack = $('#del_nack');
	var delete_skip = $('#del_skip');
	var request_lock = $('#request_lock');
	var send_edit
	
	// text
	var more_about_reason = $('#more_about_reason');
	var less_about_reason = $('#less_about_reason');
	var more_about_reason_content = $('#more_about_reason_content');
	
	/**
	 * OPTIMIZATION
	 */
	
	optimization_ack.click(function(){
		var review_uid = $(this).data('id');
		new Review().doOptimizationAck(review_uid);
	});
	
	optimization_nack.click(function(){
		var review_uid = $(this).data('id');
		new AjaxReviewHandler().reviewOptimizationArgument(false, review_uid);
	});
	
	optimization_skip.click(function(){
		new Review().reloadPageAndUnlockData(false);
	});
	
	/**
	 * DELETE
	 */
	
	delete_ack.click(function(){
		var review_uid = $(this).data('id');
		new Review().doDeleteAck(review_uid);
	});
	
	delete_nack.click(function(){
		var review_uid = $(this).data('id');
		new AjaxReviewHandler().reviewDeleteArgument(false, review_uid);
	});
	
	delete_skip.click(function(){
		new Review().reloadPageAndUnlockData(false);
	});
	
	/**
	 * MORE
	 */
	
	more_about_reason.click(function() {
		$(this).hide();
		less_about_reason.show();
		more_about_reason_content.show();
	});
	
	less_about_reason.click(function() {
		$(this).hide();
		more_about_reason.show();
		more_about_reason_content.hide();
	});
	
	request_lock.click(function(){
		var review_uid = $(this).data('id');
		new Review().doOptimizationAck(review_uid);
	});
	
	// extra info when user has already seen the complete queue
	if ($('#stats-table').data('extra-info') == 'already_seen'){
		setGlobalInfoHandler('Info', _t(queueCompleteSeen));
	}
	
	// unlock data on tab close/reload/...
	$(window).bind('beforeunload',function(){
        new AjaxReviewHandler().un_lockOptimizationReview($('#review-id').text(), false, undefined);
	});
});



