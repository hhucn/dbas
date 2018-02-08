/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxNotificationHandler(){
	'use strict';

	/**
    *
    * @param id_list
    */
	this.sendAjaxForReadMessages = function(id_list){
		new Notifications().hideInfoSpaces();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_notifications_read',
			method: 'POST',
			contentType: 'application/json',
            data: JSON.stringify({
                ids: id_list
            }),
			dataType: 'json',
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function sendAjaxForReadMessagesDone(data) {
			$.each(id_list, function(key, uid){
				var el = $('#' + uid);
				el.find('.label-info').remove();
				var title = el.find('.panel-title-link').text().trim();
				var spanEl = $('<span>').addClass('text-primary').text(title);
				el.find('.panel-title-link').empty().append(spanEl);
			});
			new Notifications().setNewBadgeCounter(data.unread_messages);
			$('.msg-checkbox:checked').each(function(){
				$(this).prop('checked',false);
			});
		}).fail(function sendAjaxForReadMessagesFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
		});
	};

	/**
    *
    * @param id_list
    */
	this.sendAjaxForDeleteMessages = function(id_list) {
		new Notifications().hideInfoSpaces();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_notifications_delete',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				ids: id_list
			}),
			dataType: 'json',
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function sendAjaxForDeleteMessagesDone(data) {
			$.each( id_list, function( key, value ) {
				$('#' + value).remove();
			});
			new Notifications().setNewBadgeCounter(data.unread_messages);
			$('#total_in_counter').text(data.total_in_messages);
			$('#total_out_counter').text(data.total_out_messages);
			setGlobalSuccessHandler('', data.success);
			$('.msg-checkbox:checked').each(function(){
				$(this).prop('checked',false);
			});
		}).fail(function sendAjaxForDeleteMessagesFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
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

		$.ajax({
			url: 'ajax_send_notification',
			type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({title: title, text: text, recipient: recipient}),
			dataType: 'json',
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function ajaxSendNewsDone(data) {
			$('#popup-writing-notification-success').show();
			$('#popup-writing-notification-success-message').text(_t(notificationWasSend));
			var out_counter = $('#total_out_counter');
			out_counter.text(' ' + (parseInt(out_counter.text()) + 1) + ' ');
			location.reload(true);
		}).fail(function ajaxSendNewsFail() {
			$('#popup-writing-notification-failed').show();
			$('#popup-writing-notification-failed-message').html(data.responseJSON.errors[0].description);
		});
	};
}
