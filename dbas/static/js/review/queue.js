/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	// buttons
	const optimization_ack = $('#opti_ack');
	const optimization_nack = $('#opti_nack');
	const optimization_skip = $('#opti_skip');
	const delete_ack = $('#del_ack');
	const delete_nack = $('#del_nack');
	const delete_skip = $('#del_skip');
	const edit_ack = $('#edit_ack');
	const edit_nack = $('#edit_nack');
	const edit_skip = $('#edit_skip');
	const request_lock = $('#request-lock');
	const send_edit  = $('#send_edit');
	
	// text
	const more_about_reason = $('#more_about_reason');
	const less_about_reason = $('#less_about_reason');
	const more_about_reason_content = $('#more_about_reason_content');
	
	/**
	 * OPTIMIZATION
	 */
	optimization_ack.click(function(){
		new Review().doOptimizationAck($(this).data('id'));
	});
	
	optimization_nack.click(function(){
		new AjaxReviewHandler().reviewOptimizationArgument(false, $(this).data('id'), '');
	});
	
	optimization_skip.click(function(){
		new Review().reloadPageAndUnlockData(false);
	});
	
	send_edit.click(function(){
		new Review().sendOptimization();
	});
	
	/**
	 * DELETE
	 */
	delete_ack.click(function(){
		new Review().doDeleteAck($(this).data('id'));
	});
	
	delete_nack.click(function(){
		new Review().doDeleteNack($(this).data('id'));
	});
	
	delete_skip.click(function(){
		new Review().reloadPageAndUnlockData(false);
	});
	
	/**
	 * Edit
	 */
	edit_ack.click(function(){
		new Review().doEditAck($(this).data('id'));
	});
	
	edit_nack.click(function(){
		new Review().doEditNack($(this).data('id'));
	});
	
	edit_skip.click(function(){
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
		new Review().doOptimizationAck($(this).data('id'));
	});
	
	// align buttons
	let max = 0;
	let elements = $("*[class^='review-btn-']");
	elements.each(function(){
		max = $(this).outerWidth() > max ? $(this).outerWidth() : max;
	});
	elements.each(function(){
		$(this).css('width', max + 'px');
	});
	
	// extra info when user has already seen the complete queue
	if ($('#stats-table').data('extra-info') == 'already_seen'){
		setGlobalInfoHandler('Info', _t(queueCompleteSeen));
	}
	
	// unlock data on tab close/reload/...
	$(window).bind('beforeunload',function(){
		if (window.location.href.indexOf('review/optimiz') != -1)
			new Review().reloadPageAndUnlockData(true);
	});
});



