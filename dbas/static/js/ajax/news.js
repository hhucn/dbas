/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxNewsHandler(){
	'use strict';

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
			url: 'send_news',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
					title: title,
					text: text
				}),
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewsDone() {
			location.reload(true);
		}).fail(function ajaxSendNewsFail(data) {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).html(data.responseJSON.errors[0].description);
		});
	};
}
