/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(function () {
	'use strict';

	var not = new Notifications();
	not.setPanelClickFunctions();
	not.setClickFunctionsForAnswerNotification();
	not.setClickFunctionsForNewNotification();
});

function Notifications() {

	this.setPanelClickFunctions = function(){
		$.each($('.panel-title-link'), function ajaxLinksRead() {
			$(this).click(function(){
				var id = $(this).parent().parent().parent().attr('id');
				if ($(this).html().indexOf('<strong') != -1) {
					new Notifications().sendAjaxForReadMessage(id, this);
				}
			});
		}) ;

		$.each($('.glyphicon-trash'), function ajaxLinksDelete() {
			$(this).off('click').click(function(){
				$(this).parent().parent().attr('href','');
				new Notifications().sendAjaxForDeleteMessage($(this).parent().parent().parent().attr('id'));
			});
		});
	};

	this.setClickFunctionsForNewNotification = function() {
		// send notification to users
		$('#new-notification').click(function () {
			$('#popup-writing-notification').modal('show');
			$('#popup-writing-notification-success').hide();
			$('#popup-writing-notification-failed').hide();
			$('#popup-writing-notification-recipient').show();
			$('#popup-writing-notification-send').click(function() {
				new Notifications().sendNotification($('#popup-writing-notification-recipient').val());
			});
		});
	};

	this.setClickFunctionsForAnswerNotification = function() {
		// send notification to users
		$('.answer-notification').each(function () {
			$(this).click(function(){
				var _this = $(this);
				alert(_this.prev().text().trim());
				$('#popup-writing-notification-recipient').show().val(_this.prev().text().trim());
				$('#popup-writing-notification').modal('show');
				$('#popup-writing-notification-success').hide();
				$('#popup-writing-notification-failed').hide();
				var panel = $(this).parent().parent().parent().parent(),
					title = panel.find('.notification-title').text(),
					content = panel.find('.notification-content').text();
				$('#popup-writing-notification-title').val(title);
				$('#popup-writing-notification-text').text(content);
				$('#popup-writing-notification-send').click(function() {
					new Notifications().sendNotification($('#popup-writing-notification-recipient').text());
				});
			});
		});

		$('.new-notification').each(function () {
			$(this).click(function(){
				var _this = $(this);
				$('#popup-writing-notification-recipient').hide();
				$('#popup-writing-notification').modal('show');
				$('#popup-writing-notification-success').hide();
				$('#popup-writing-notification-failed').hide();
				$('#popup-writing-notification-send').click(function(){
					var url = window.location.href,
						splitted = url.split('/'),
						recipient;
					if (url.indexOf('/user/') != -1){
						recipient = splitted[splitted.length - 1];
					} else {
						recipient = _this.prev().text();
					}
					new Notifications().sendNotification(recipient.trim());
				});
			});
		});
	};

	/**
    *
    */
	this.hideInfoSpaces = function() {
		$('#error-space').hide();
		$('#error-description').text('');
		$('#success-space').hide();
		$('#success-description').text('');
	};

	/**
    *
    * @param counter
    */
	this.setNewBadgeCounter = function(counter){
		if (counter == 0){
			$('#header_badge_count_notifications').remove();
		} else {
			$('#header_badge_count_notifications').text(counter);
		}
		$('#unread_counter').text(' ' + counter + ' ');
	};

	/**
    *
    * @param id
    * @param _this
    */
	this.sendAjaxForReadMessage = function(id, _this){
		new Notifications().hideInfoSpaces();
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
				new Notifications().setNewBadgeCounter(parsedData.unread_messages);
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
	this.sendAjaxForDeleteMessage = function(id) {
		new Notifications().hideInfoSpaces();
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
				new Notifications().setNewBadgeCounter(parsedData.unread_messages);
				$('#total_in_counter').text(parsedData.total_in_messages);
				$('#total_out_counter').text(parsedData.total_out_messages);
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
    * @param recipient
    * @param recipient_avatar
    * @param title
    * @param text
    * @param timestamp
    * @param uid
    */
	this.appendMessageInOutbox = function(recipient, recipient_avatar, title, text, timestamp, uid) {
		var panel_html = '' +
			'<div class="panel panel-default" style="margin-bottom: 1em;" id="' + uid + '">' +
				'<div class="panel-heading">' +
					'<h4 class="panel-title">' +
						'<a class="accordion-toggle panel-title-link" data-toggle="collapse" data-parent="#accordion" href="#collapse' + uid + '">' +
							'<span class="text-primary notification-title">' + title + '</span>' +
						'</a>' +
						'<span style="float: right; margin-left: 1.0em; cursor: pointer;" class="glyphicon center glyphicon-trash" data-toggle="tooltip" data-placement="bottom" title="Delete"></span>' +
						'<span style="float: right; padding-right: 1em;"><span>To:</span> ' + recipient + ', ' + timestamp + '</span>' +
					'</h4>' +
				'</div>' +
				'<div id="collapse' + uid + '" class="panel-collapse collapse">' +
					'<div class="panel-body">' +
						'<div class="notification-content">text</div>' +
						'<div style="float:right; padding: 0.2em;">' +
							'<span>' + _t(to) + ':</span> ' +
							'<a href="/user/' + recipient + '" target="_blank" class="to_author_value">' +
								recipient +
								'<img src="' + recipient_avatar + '" style="margin-left: 0.5em; margin-right: 0.5em">' +
							'</a>' +
							'<a href="#" class="btn btn-primary btn-xs answer-notification">' + _t(answer) + '</a>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>';
		$('#outbox').find('.panel-group').append(panel_html);

		$.each($('#message-space').find('.glyphicon-trash'), function ajaxLinksDelete() {
			$(this).off('click').click(function(){
				$(this).parent().parent().attr('href','');
				new Notifications().sendAjaxForDeleteMessage($(this).parent().parent().parent().attr('id'));
			});
		});
	};

	/**
    *
    * @param recipient
    */
	this.sendNotification = function(recipient){
		var title = $('#popup-writing-notification-title').val(),
			text = $('#popup-writing-notification-text').val();

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