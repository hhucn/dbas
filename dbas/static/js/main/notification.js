/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

$(function () {
	'use strict';

	var not = new Notifications();
	not.setPanelClickFunctions();
	not.setClickFunctionsForAnswerNotification();
	not.setClickFunctionsForNewNotification();
	not.setClickFunctionsForRead();
	not.setClickFunctionsForDelete();
	not.setClickFunctionsForCheckboxes();

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

	if (parseInt($('#total_in_counter').text()) > 0){
		$('#read-inbox').removeClass('hidden');
		$('#delete-inbox').removeClass('hidden');
	}

	if (parseInt($('#total_out_counter').text()) > 0){
		$('#delete-outbox').removeClass('hidden');
	}
});

function Notifications() {
    'use strict';

	/**
	 *
	 */
	this.setPanelClickFunctions = function(){
		$.each($('.panel-title-link'), function ajaxLinksRead() {
			$(this).click(function(){
				var id = $(this).parent().parent().parent().attr('id');
				if ($(this).html().indexOf('<strong') !== -1) {
					new AjaxNotificationHandler().sendAjaxForReadMessages([id]);
				}
			});
		}) ;

		$.each($('.fa-trash'), function ajaxLinksDelete() {
			$(this).off('click').click(function(){
				$(this).parent().parent().attr('href','');
				new AjaxNotificationHandler().sendAjaxForDeleteMessages([$(this).data('id')]);
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
					if (url.indexOf('/user/') !== -1){
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
	this.setClickFunctionsForRead = function(){
		$('#read-inbox').click(function(){
			var uids = [];
			var inbox = $('#inbox');
			inbox.find('.msg-checkbox:checked').each(function(){
				uids.push($(this).data('id'));
			});
			if (uids.length === 0){
				inbox.find('.msg-checkbox').each(function(){
					uids.push($(this).data('id'));
				});
			}
			new AjaxNotificationHandler().sendAjaxForReadMessages(uids);
		});
	};

	/**
	 *
	 */
	this.setClickFunctionsForDelete = function(){
		$('#delete-inbox').click(function(){
			var uids = [];
			var inbox = $('#inbox');
			inbox.find('.msg-checkbox:checked').each(function(){
				uids.push($(this).data('id'));
			});
			if (uids.length === 0){
				inbox.find('.msg-checkbox').each(function(){
					uids.push($(this).data('id'));
				});
			}
			new AjaxNotificationHandler().sendAjaxForDeleteMessages(uids);
		});

		$('#delete-outbox').click(function(){
			var uids = [];
			var outbox = $('#outbox');
			outbox.find('.msg-checkbox:checked').each(function(){
				uids.push($(this).data('id'));
			});
			if (uids.length === 0){
				outbox.find('.msg-checkbox').each(function(){
					uids.push($(this).data('id'));
				});
			}
			new AjaxNotificationHandler().sendAjaxForDeleteMessages(uids);
		});
	};

	/**
	 *
	 */
	this.setClickFunctionsForCheckboxes = function(){
		$('.msg-checkbox').each(function () {
			$(this).change(function(){
				var count = $('.msg-checkbox:checked').length;
				if (count === 0){
					if ($('#inbox-link').attr('aria-expanded') === 'true'){
						$('#' + deleteInboxTxt).text(_t(deleteEverything));
						$('#' + readInboxTxt).text(_t(readEverything));
					} else {
						$('#' + deleteOutboxTxt).text(_t(deleteEverything));
					}
				} else {
					if ($('#inbox-link').attr('aria-expanded') === 'true'){
						$('#' + deleteInboxTxt).text(_t(deleteMarked));
						$('#' + readInboxTxt).text(_t(readMarked));
					} else {
						$('#' + deleteOutboxTxt).text(_t(deleteMarked));
					}
				}
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
		if (counter === 0){
			$('#header_badge_count_notifications').remove();
		} else {
			$('#header_badge_count_notifications').text(counter);
		}
		$('#unread_counter').text(' ' + counter + ' ');
	};
}
