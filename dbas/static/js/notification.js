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

	$('#popup-writing-notification-recipient').keyup(function () {
		setTimeout(function () {
			var escapedText = escapeHtml($('#popup-writing-notification-recipient').val());
			new AjaxDiscussionHandler().fuzzySearch(escapedText, 'popup-writing-notification-recipient', fuzzy_find_user, '');
		}, 200);
	});
	$('#popup-writing-notification-title').focusin(function(){
		$('#proposal-user-list-group').empty();
	});
	$('#popup-writing-notification-text').focusin(function(){
		$('#proposal-user-list-group').empty();
	});
});

function Notifications() {

	/**
	 *
	 */
	this.setPanelClickFunctions = function(){
		$.each($('.panel-title-link'), function ajaxLinksRead() {
			$(this).click(function(){
				var id = $(this).parent().parent().parent().attr('id');
				if ($(this).html().indexOf('<strong') != -1) {
					new AjaxNotificationHandler().sendAjaxForReadMessage(id, this);
				}
			});
		}) ;

		$.each($('.fa-trash'), function ajaxLinksDelete() {
			$(this).off('click').click(function(){
				$(this).parent().parent().attr('href','');
				new AjaxNotificationHandler().sendAjaxForDeleteMessage($(this).parent().parent().parent().attr('id'));
			});
		});
	};

	/**
	 *
	 */
	this.setClickFunctionsForNewNotification = function() {
		// send notification to users
		$('#new-notification').click(function () {
			$('#popup-writing-notification').modal('show');
			$('#popup-writing-notification-success').hide();
			$('#popup-writing-notification-failed').hide();
			$('#popup-writing-notification-recipient').show();
			$('#popup-writing-notification-send').click(function() {
				new AjaxNotificationHandler().sendNotification($('#popup-writing-notification-recipient').val());
			});
		});
	};

	/**
	 *
	 */
	this.setClickFunctionsForAnswerNotification = function() {
		// send notification to users
		$('.answer-notification').each(function () {
			$(this).click(function(){
				var _this = $(this);
				$('#popup-writing-notification-recipient').show().val(_this.prev().text().trim());
				$('#popup-writing-notification').modal('show');
				$('#popup-writing-notification-success').hide();
				$('#popup-writing-notification-failed').hide();
				var panel = $(this).parent().parent().parent().parent();
				var title = panel.find('.notification-title').text();
				var content = panel.find('.notification-content').text();
				$('#popup-writing-notification-title').val(title);
				$('#popup-writing-notification-text').text(content);
				$('#popup-writing-notification-send').click(function() {
					new AjaxNotificationHandler().sendNotification($('#popup-writing-notification-recipient').val());
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
					var url = window.location.href;
					var splitted = url.split('/');
					var recipient;
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
						'<i style="float: right; margin-left: 1.0em; cursor: pointer;" class="fa center fa-trash"></i>' +
						'<span style="float: right; padding-right: 1em;"><span>' + _t(to) + ':</span> ' + recipient + ', ' + timestamp + '</span>' +
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

		$.each($('#message-space').find('.fa-trash'), function ajaxLinksDelete() {
			$(this).off('click').click(function(){
				$(this).parent().parent().attr('href','');
				new Notifications().sendAjaxForDeleteMessage($(this).parent().parent().parent().attr('id'));
			});
		});
	};
}