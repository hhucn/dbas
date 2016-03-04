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
});

hideInfoSpaces = function() {
	$('#error-space').hide();
	$('#error-description').text('');
	$('#success-space').hide();
	$('#success-description').text('');
};

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