/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxNotificationHandler(){
	/**
    *
    * @param id
    * @param _this
    */
	this.sendAjaxForReadMessage = function(id, _this){
		new Notifications().hideInfoSpaces();
		const csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_notification_read',
			method: 'POST',
			data: {
				id: id
			},
			dataType: 'json',
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function sendAjaxForReadMessageDone(data) {
			const parsedData = $.parseJSON(data);
			if (parsedData.error.length > 0) {
				setGlobalErrorHandler(_t_discussion(ohsnap), parsedData.error);
			} else {
				const titletext = $(_this).text().replace(_t(neww).toLocaleUpperCase(), '').trim();
				const spanEl = $('<span>').addClass('text-primary').text(titletext);
				$(_this).empty().html(spanEl);
				$('#collapse' + id).addClass('in');
				new Notifications().setNewBadgeCounter(parsedData.unread_messages);
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
		const csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_notification_delete',
			method: 'POST',
			data: {
				id: id
			},
			dataType: 'json',
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function sendAjaxForDeleteMessageDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData.success.length > 0) {
				$('#' + id).remove();
				new Notifications().setNewBadgeCounter(parsedData.unread_messages);
				$('#total_in_counter').text(parsedData.total_in_messages);
				$('#total_out_counter').text(parsedData.total_out_messages);
				setGlobalSuccessHandler('', parsedData.success);
			} else {
				setGlobalErrorHandler(_t_discussion(ohsnap), parsedData.error);
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
		const csrf_token = $('#' + hiddenCSRFTokenId).val();

		$('#popup-writing-notification-success').hide();
		$('#popup-writing-notification-failed').hide();

		$.ajax({
			url: 'ajax_send_notification',
			type: 'POST',
			data: {title: title, text: text, recipient: recipient},
			dataType: 'json',
			async: true,
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function ajaxSendNewsDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData.error.length == 0) {
				$('#popup-writing-notification-success').show();
				$('#popup-writing-notification-success-message').text(_t(notificationWasSend));
				var out_counter = $('#total_out_counter');
				out_counter.text(' ' + (parseInt(out_counter.text()) + 1) + ' ');
				new Notifications().appendMessageInOutbox(recipient, parsedData.recipient_avatar, title, text, parsedData.timestamp, parsedData.uid)
			} else {
				$('#popup-writing-notification-failed').show();
				$('#popup-writing-notification-failed-message').html(parsedData.error);
			}
		}).fail(function ajaxSendNewsFail() {
			$('#popup-writing-notification-failed').show();
			$('#popup-writing-notification-failed-message').html(_t(internalError));
		});
	};
}
