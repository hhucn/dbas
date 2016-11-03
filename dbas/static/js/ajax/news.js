/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxNewsHandler(){
	/**
	 *
	 */
	this.ajaxGetNews = function () {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_news',
			type: 'POST',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetNewsDone(data) {
			new News().callbackIfDoneForGettingNews(data);
		}).fail(function ajaxGetNewsFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 */
	this.ajaxSendNews = function () {
		var title = $('#' + writingNewNewsTitleId).val();
		var text = $('#' + writingNewNewsTextId).val();

		if (title.length == 0 || text.length < 10) {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).text(_t(empty_news_input));
			delay(function(){
				$('#' + writingNewsFailedId).fadeOut();
				delay(function(){
					$('#' + writingNewsFailedMessageId).text('');
				}, 2000);
			}, 2000);
			return;
		} else {
			$('#' + writingNewsFailedId).hide();
			$('#' + writingNewsSuccessId).hide();
		}

		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_send_news',
			type: 'POST',
			data: {title: title, text: text},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewsDone(data) {
			new News().callbackIfDoneForSendingNews(data);
		}).fail(function ajaxSendNewsFail() {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).html(_t(internalError));
		});
	};
}
