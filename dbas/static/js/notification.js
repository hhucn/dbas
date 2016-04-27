/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(function () {
	'use strict';

	$.each($('#message-space .panel-title-link'), function ajaxLinksRead() {
		$(this).click(function(){
			var id = $(this).parent().parent().parent().attr('id');
			if ($(this).html().indexOf('<strong') != -1) {
				sendAjaxForReadMessage(id, this);
			}
		});
	});

	$.each($('#message-space .glyphicon-trash'), function ajaxLinksDelete() {
		$(this).off('click').click(function(){
			$(this).parent().parent().attr('href','');
			sendAjaxForDeleteMessage($(this).parent().parent().parent().attr('id'));
		});
	});

	// send notification to users
	$('#send-notification').click(function () {
		$('#popup-writing-notification').modal('show');
		$('#popup-writing-notification-success').hide();
		$('#popup-writing-notification-failed').hide();
		$('#popup-writing-notification-send').click(function(){
			sendNotification();
		});
	});
});

/**
 *
 */
hideInfoSpaces = function() {
	$('#error-space').hide();
	$('#error-description').text('');
	$('#success-space').hide();
	$('#success-description').text('');
};

/**
 *
 * @param counter
 */
setNewBadgeCounter = function(counter){
	if (counter == 0){
		$('#header_user').next().remove();
		$('#header_notifications').next().next().remove();
		$('#header_notifications_new').next().next().remove();
	} else {
		$('#header_user').next().text(counter);
		$('#header_notifications').next().next().text(counter);
		$('#header_notifications_new').next().next().text(counter);
	}
	$('#unread_counter').text(' ' + counter + ' ');
};

/**
 *
 * @param id
 * @param _this
 */
sendAjaxForReadMessage = function(id, _this){
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
			var text = $(_this).text().replace('* ', ''),
				spanEl = $('<span>').addClass('text-primary').text($(_this).text().replace('* ', ''));
			$(_this).empty().html(spanEl);
			$('#collapse' + id).addClass('in');
			setNewBadgeCounter(parsedData.unread_messages);
		}
	}).fail(function sendAjaxForReadMessageFail() {
		$('#error-space').fadeIn();
		$('#error-description').text('Requested failed');
	});
};

/**
 *
 * @param id
 */
sendAjaxForDeleteMessage = function(id) {
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
			$('#total_counter').text(parsedData.total_messages);
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

/**
 *
 */
sendNotification = function(){
	var url = window.location.href,
		splitted = url.split('/'),
		title = $('#popup-writing-notification-title').val(),
		text = $('#popup-writing-notification-text').val(),
		recipient;
	if (url.indexOf('/user/') != -1){
		recipient = splitted[splitted.length - 1];
	} else {
		recipient = $('#from_author_value').text();
	}

	$('#popup-writing-notification-success').hide();
	$('#popup-writing-notification-failed').hide();

	$.ajax({
		url: 'ajax_send_notification',
		type: 'POST',
		data: {title: title, text: text, recipient: recipient},
		dataType: 'json',
		async: true
	}).done(function ajaxSendNewsDone(data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length == 0) {
			$('#popup-writing-notification-success').show();
			$('#popup-writing-notification-success-message').text(_t(notificationWasSend));
		} else {
			$('#popup-writing-notification-failed').show();
			$('#popup-writing-notification-failed-message').html(parsedData.error);
		}
	}).fail(function ajaxSendNewsFail() {
		$('#popup-writing-notification-failed').show();
		$('#popup-writing-notification-failed-message').html(_t(internalError));
	});
};