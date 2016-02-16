/**
 * Created by tobias on 15.02.16.
 */


$(function () {
	'use strict';

	$.each($('#message-space .panel-body'), function replaceHtmlTagsInMessages() {
		replaceHtmlTags($(this));
	});

	$.each($('#message-space .panel-heading a'), function replaceHtmlTagsInMessages() {
		$(this).click(function(){
			var id = $(this).parent().parent().parent().attr('id');
			if (new Helper().getFullHtmlTextOf($(this)).indexOf('<strong') != -1) {
				sendAjaxForReadMessage(id);
			}
		});
	});

	$.each($('#message-space .glyphicon-trash'), function replaceHtmlTagsInMessages() {
		$(this).off('click').click(function(){
			$(this).parent().parent().attr('href','');
			sendAjaxForDeleteMessage($(this).parent().parent().parent().attr('id'));
		});
	});
});

replaceHtmlTags = function(element){
	var text = element.text();
	text = text.replace('&lt;strong&gt;', '<strong>');
	text = text.replace('&lt;/strong&gt;', '</strong>');
	text = text.replace('&lt;a', '<a');
	text = text.replace('&lt;/a', '</a');
	text = text.replace('&lt;br&gt;', '<br>');
	element.html(text);
};

hideInfoSpaces = function() {
	$('#error-space').hide();
	$('#error-description').text('');
	$('#success-space').hide();
	$('#success-description').text('');
};

setNewBadgeCounter = function(counter){
	if (counter == 0){
		$('#header_user').next().remove();
		$('#header_messages').next().next().remove();
		$('#header_messages_new').next().next().remove();
	} else {
		$('#header_user').next().text(counter);
		$('#header_messages').next().next().text(counter);
		$('#header_messages_new').next().next().text(counter);
	}
	// $('#message-space > span:nth-child(1)').text(' ' + counter + ' ');
};

sendAjaxForReadMessage = function(id){
	hideInfoSpaces();
	$.ajax({
		url: 'ajax_notification_read',
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
			//var text = $('#' + id).find('.title-link').html();
			//text = text.replace('<span', '');
			//text = text.replace('</span', '');
			//text = text.replace('* ', '');
			//$('#' + id + ' .panel-title a:first-child').html(text);
			setNewBadgeCounter(parsedData.unread_messages);
		}
	}).fail(function sendAjaxForReadMessageFail() {
		$('#error-space').fadeIn();
		$('#error-description').text('Requested failed');
	});
};

sendAjaxForDeleteMessage = function(id) {
	alert(id);
	hideInfoSpaces();
	$.ajax({
		url: 'ajax_notification_delete',
		method: 'POST',
		data: {
			id: id
		},
		dataType: 'json'
	}).done(function sendAjaxForDeleteMessageDone(data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.success.length > 0) {
			$('#' + id).remove();
			setNewBadgeCounter(parsedData.unread_messages);
			$('#success-space').fadeIn();
			$('#success-description').text(parsedData.success);
		} else {
			$('#error-space').fadeIn();
			$('#error-description').text(parsedData.error);
		}
	}).fail(function sendAjaxForDeleteMessageFail() {
		$('#error-space').fadeIn();
		$('#error-description').text('Requested failed');
	});
};