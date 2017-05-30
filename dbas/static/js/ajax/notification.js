/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxNotificationHandler(){
	'use strict';
	
	/**
    *
    * @param id
    * @param _this
    */
	this.sendAjaxForReadMessage = function(id, _this){
		new Notifications().hideInfoSpaces();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_notification_read',
			method: 'POST',
			data: {
				id: id
			},
			dataType: 'json',
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function sendAjaxForReadMessageDone(data) {
			if (data.error.length > 0) {
				setGlobalErrorHandler(_t_discussion(ohsnap), data.error);
			} else {
				var titletext = $(_this).text().replace(_t(neww).toLocaleUpperCase(), '').trim();
				var spanEl = $('<span>').addClass('text-primary').text(titletext);
				$(_this).empty().html(spanEl);
				$('#collapse' + id).addClass('in');
				new Notifications().setNewBadgeCounter(data.unread_messages);
			}
		}).fail(function sendAjaxForReadMessageFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
    *
    * @param id
    */
	this.sendAjaxForDeleteMessage = function(id) {
		new Notifications().hideInfoSpaces();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_notification_delete',
			method: 'POST',
			data: {
				id: id
			},
			dataType: 'json',
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function sendAjaxForDeleteMessageDone(data) {
			if (data.success.length > 0) {
				$('#' + id).remove();
				new Notifications().setNewBadgeCounter(data.unread_messages);
				$('#total_in_counter').text(data.total_in_messages);
				$('#total_out_counter').text(data.total_out_messages);
				setGlobalSuccessHandler('', data.success);
			} else {
				setGlobalErrorHandler(_t_discussion(ohsnap), data.error);
			}
		}).fail(function sendAjaxForDeleteMessageFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
    *
    * @param recipient
    */
	this.sendNotification = function(recipient){
		var title = $('#popup-writing-notification-title').val(),
			text = $('#popup-writing-notification-text').val();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();

		$('#popup-writing-notification-success').hide();
		$('#popup-writing-notification-failed').hide();
		var data = {title: title, text: text, recipient: recipient};
		
		$.ajax({
			url: 'ajax_send_notification',
			type: 'POST',
			data: data,
			dataType: 'json',
			async: true,
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function ajaxSendNewsDone(data) {
			if (data.error.length === 0) {
				$('#popup-writing-notification-success').show();
				$('#popup-writing-notification-success-message').text(_t(notificationWasSend));
				var out_counter = $('#total_out_counter');
				out_counter.text(' ' + (parseInt(out_counter.text()) + 1) + ' ');
				location.reload();
				// new Notifications().appendMessageInOutbox(recipient, data.recipient_avatar, title, text, data.timestamp, data.uid)
			} else {
				$('#popup-writing-notification-failed').show();
				$('#popup-writing-notification-failed-message').html(data.error);
			}
		}).fail(function ajaxSendNewsFail() {
			$('#popup-writing-notification-failed').show();
			$('#popup-writing-notification-failed-message').html(_t(internalError));
		});
	};
}
