/**
 * Created by tobias on 15.02.16.
 */


$(function () {
	'use strict';

	$.each($('#message-space .panel-body'), function replaceHtmlTagsInMessages() {
		replaceHtmlTags($(this));
	});

	$.each($('#message-space .panel-heading > a'), function replaceHtmlTagsInMessages() {
		$(this).click(function(){
			sendAjaxForReadMessage($(this).parent().parent().attr('id'));
		});
	});
});

// new
replaceHtmlTags = function(element){
	var text = element.text();
	text = text.replace('&lt;strong&gt;', '<strong>');
	text = text.replace('&lt;/strong&gt;', '</strong>');
	text = text.replace('&lt;a', '<a');
	text = text.replace('&lt;/a', '</a');
	text = text.replace('&lt;br&gt;', '<br>');
	element.html(text);
};

sendAjaxForReadMessage = function(id){
	$('#error-space').hide();
	$('#error-description').text('');
	$.ajax({
		url: 'ajax_message_read',
		method: 'POST',
		data: {
			id: id
		},
		dataType: 'json'
	}).done(function sendAjaxForReadMessageDone(data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length > 0) {
		$('#error-space').fadeIn();
		$('#error-description').text(parsedData.error);
		} else {
			var text = $('#' + id + ' .panel-title').html();
			text = text.replace('<strong>', '');
			text = text.replace('</strong>', '');
			text = text.replace('* ', '');
			$('#' + id + ' .panel-title').html(text);
			if (parsedData.unread_messages == 0){
				$('#header_user').next().remove();
				$('#header_messages').next().next().remove();
				$('#header_messages_new').next().next().remove();
			} else {
				$('#header_user').next().text(parsedData.unread_messages);
				$('#header_messages').next().next().text(parsedData.unread_messages);
				$('#header_messages_new').next().next().text(parsedData.unread_messages);
			}
		}
	}).fail(function sendAjaxForReadMessageFail() {
		$('#error-space').fadeIn();
		$('#error-description').text('Requested failed');
	});
};