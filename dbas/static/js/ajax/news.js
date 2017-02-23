/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxNewsHandler(){
	/**
	 *
	 */
	this.ajaxSendNews = function () {
		var title = $('#' + writingNewNewsTitleId).val();
		var text = $('#' + writingNewNewsTextId).val();

		if (title.length === 0 || text.length < 10) {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).text(_t(empty_news_input));
			setTimeout(function(){
				$('#' + writingNewsFailedId).fadeOut();
				setTimeout(function(){
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
