/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>S
 */

function AjaxDiscussionHandler() {
	'use strict';

	/**
	 * Sends new premises to the server. Answer will be given to a callback
	 * @param arg_uid
	 * @param relation
	 * @param premisegroups
	 */
	this.sendNewPremiseForArgument = function (arg_uid, relation, premisegroups) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_new_premises_for_argument',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				arg_uid: arg_uid,
				attack_type: relation,
				premisegroups: premisegroups
			}),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewPremisesForArgumentDone(data) {
			window.location.href = data.url;
		}).fail(function ajaxSendNewPremisesForArgumentFail(data) {
			$('#' + addPremiseErrorContainer).show();
			$('#' + addPremiseErrorMsg).text(data.responseJSON.errors[0].description);
		});
	};

	/**
	 *
	 * @param position
	 * @param reason
	 */
	this.sendNewStartArgument = function(position, reason){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_new_start_argument',
			method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
				position: position,
				reason: reason
			}),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewStartArgumentDone(data) {
			window.location.href = data.url;
		}).fail(function ajaxSendNewStartArgumentFail(data) {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(data.responseJSON.errors[0].description);
		});
	};

	/**
	 * Sends new premises to the server. Answer will be given to a callback
	 * @param premisegroups List of premisegroups
	 * @param conclusion_id id of the conclusion
	 * @param supportive boolean, whether it is supportive
	 */
	this.sendNewStartPremise = function (premisegroups, conclusion_id, supportive) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_new_start_premise',
			method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
	            premisegroups: premisegroups,
				conclusion_id: conclusion_id,
				supportive: supportive
            }),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewStartPremiseDone(data) {
			window.location.href = data.url;
		}).fail(function ajaxSendNewStartPremiseFail(data) {
			$('#' + addPremiseErrorContainer).show();
			$('#' + addPremiseErrorMsg).text(data.responseJSON.errors[0].description);
		});
	};

	/**
	 *
	 * @param info
	 * @param long_info
	 * @param title
	 * @param is_public
	 * @param is_read_only
	 * @param language
	 */
	this.sendNewIssue = function(info, long_info, title, is_public, is_read_only, language){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$('#add-topic-error').hide();
		$.ajax({
			url: 'ajax_set_new_issue',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				info: info,
				long_info: long_info,
				title: title,
				is_public: is_public,
				is_read_only: is_read_only,
				lang: language
			}),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendnewIssueDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewIssue(data);
		}).fail(function ajaxSendnewIssueFail(data) {
			$('#' + addTopicPopupError).removeClass('hidden');
			$('#' + addTopicPopupErrorText).text(data.responseJSON.errors[0].description);
			setTimeout(function(){
				$('#' + addTopicPopupError).addClass('hidden');
				$('#' + addTopicPopupErrorText).text('');
			}, 2500);
		});
	};

	/**
	 * Requests the logfile for the given uid
	 * @param statements_uids current uid of the statement
	 */
	this.getLogfileForStatements = function (statements_uids) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_logfile_for_statements',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				uids: statements_uids,
				issue: getCurrentIssueId()
			}),
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetLogfileForStatementsDone(data) {
			new InteractionHandler().callbackIfDoneForGettingLogfile(data);
		}).fail(function ajaxGetLogfileForStatementsFail() {
			var description = $('#' + popupEditStatementErrorDescriptionId);
			description.text(_t(requestFailed));
			description.addClass('text-danger');
			description.removeClass('text-info');
			$('#' + popupEditStatementLogfileSpaceId).prev().hide();
		});
	};

	/**
	 * Sends a correction of statements
	 * @param elements
	 * @param statements_uids
	 */
	this.sendCorrectionOfStatement = function (elements, statements_uids) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_correction_of_statement',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				'elements': elements
			}),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendCorrectureOfStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data, statements_uids);
		}).fail(function ajaxSendCorrectureOfStatementFail(data) {
			setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
		});
	};

	/**
	 * Shortens url
	 * @param long_url for shortening
	 */
	this.getShortenUrl = function (long_url) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_shortened_url',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				url: encodeURI(long_url),
				issue: getCurrentIssueId()
			}),
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetShortenUrlDone(data) {
			var service = '<a href="' + data.service_url + '" title="' + data.service + '" target="_blank">' + data.service_text + '</a>';
			$('#' + popupUrlSharingDescriptionPId).html(_t_discussion(feelFreeToShareUrl) + ' (' + _t_discussion(shortenedBy) + ' ' + service + '):');
			$('#' + popupUrlSharingInputId).val(data.url).data('short-url', data.url);
		}).fail(function ajaxGetShortenUrl(data) {
			setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
			new PopupHandler().hideAndClearUrlSharingPopup();
		});
	};

	/**
	 *
	 * @param uid
	 */
	this.getMoreInfosAboutArgument = function(uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_infos_about_argument',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				uid: uid,
				lang: getDiscussionLanguage()
			}),
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetMoreInfosAboutArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForGettingInfosAboutArgument(data);
		}).fail(function ajaxGetMoreInfosAboutArgumentFail(data) {
			var element = $('<p>').html(data.responseJSON.errors[0].description);
			displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(messageInfoTitle), element);
		});
	};

	/**
	 *
	 * @param type
	 * @param argument_uid
	 * @param statement_uid
	 */
	this.getMoreInfosAboutOpinion = function(type, argument_uid, statement_uid){
		var is_argument = type === 'argument';
		var is_position = type === 'position' || type === 'statement';
		var uid = argument_uid === 'None' ? statement_uid : argument_uid;
		var csrf_token = $('#' + hiddenCSRFTokenId).val();

		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				uid: uid,
				is_argument: is_argument,
				is_attitude: false,
				is_reaction: false,
				is_position: is_position,
				lang: getDiscussionLanguage()
			}),
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetMoreInfosAboutOpinionDone(data) {
			new InteractionHandler().callbackIfDoneForGettingMoreInfosAboutOpinion(data, is_argument);
		}).fail(function ajaxGetMoreInfosAboutOpinionFail(data) {
			setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
		});

	};

	/***
	 * Ajax request for the fuzzy search
	 * @param value
	 * @param callbackid
	 * @param type
	 * @param extra optional integer
	 * @param reason optional
	 */
	this.fuzzySearch = function (value, callbackid, type, extra, reason) {
		var callback = $('#' + callbackid);
		var pencil = ' <i class="fa fa-pencil" aria-hidden="true"></i>';
		var tmpid = callbackid.split('-').length === 6 ? callbackid.split('-')[5] : '0';
		var bubble_value = value;
		if (tmpid === 'reason' || tmpid === 'position'){
			var pos = escapeHtml($('#' + addStatementContainerMainInputPosId).val());
			var res = escapeHtml($('#' + addStatementContainerMainInputResId).val());
			pos = pos.length === 0 ? '...' : pos;
			res = res.length === 0 ? '...' : res;
			bubble_value = pos + ' ' + _t_discussion(because) +  ' ' + res;
			tmpid = 'reason_position';
		}
		var bubbleSpace = $('#' + discussionBubbleSpaceId);
		var csrf_token = $('#' + hiddenCSRFTokenId).val();

		// clear lists if input is empty
		if(callback.val().length === 0) {
			$('#' + proposalStatementListGroupId).empty();
			$('#' + proposalPremiseListGroupId).empty();
			$('#' + proposalEditListGroupId).empty();
			$('#' + proposalUserListGroupId).empty();
			$('#' + proposalStatementSearchGroupId).empty();
			$('#proposal-mergesplit-list-group-' + callbackid).empty();
			$('p[id^="current_"]').each(function() {
				$(this).parent().remove();
			});
			return;
		}

		if (!$.inArray(type, [fuzzy_find_user, fuzzy_find_statement, fuzzy_duplicate])) {
			var opener = $('#' + addPremiseContainerMainInputIntroId).text().replace('...', _t_discussion(because) + ' ' );
			// add or remove bubble only iff we are not in an popup
			if (type !== fuzzy_statement_popup) {
				if (bubbleSpace.find('#current_' + tmpid).length === 0) {
					var text = $('<p>').addClass('triangle-r').attr('id', 'current_' + tmpid).html(opener + bubble_value + '...' + pencil);
					var current = $('<div>').addClass('line-wrapper-r').append(text).hide().fadeIn();
					current.insertAfter(bubbleSpace.find('div:last-child'));
					setInterval(function () { // fading pencil
						bubbleSpace.find('.fa-pencil').fadeTo('slow', 0.2, function () {
							bubbleSpace.find('.fa-pencil').fadeTo('slow', 1.0, function () {
							});
						});
					}, 1000);
				} else {
					$('#current_' + tmpid).html(opener + ' ' + bubble_value + '...' + pencil);
				}
			}
			var gh = new GuiHandler();
			var resize = gh.setMaxHeightForBubbleSpace();
			gh.setMaxHeightForDiscussionContainer(resize);
		}

		$.ajax({
			url: 'ajax_fuzzy_search',
			method: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				value: value,
				type: type,
				extra: extra,
				issue: getCurrentIssueId()
			}),
			global: false,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxFuzzySearchDone(data) {
			new InteractionHandler().callbackIfDoneFuzzySearch(data, callbackid, type, reason);
		}).fail(function ajaxFuzzySearchFail() {
		});
		callback.focus();
	};

	/**
	 *
	 * @param uid
	 * @param is_argument
	 */
	this.revokeContent = function(uid, is_argument){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_revoke_content',
			method: 'GET',
			dataType: 'json',
			data: {
				uid: uid, is_argument: is_argument
			},
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxRevokeContentDone(data) {
			new InteractionHandler().callbackIfDoneRevokeContent(data);
		}).fail(function ajaxRevokeContentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			new PopupHandler().hideAndClearUrlSharingPopup();
			//$('#' + popupUrlSharingInputId).val(long_url);
		});
	};

	/**
	 * Marks given statements as read
	 *
	 * @param uids of the statements
	 */
	this.setSeenStatements = function(uids){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_seen_statements',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				uids: uids
			}),
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).fail(function () {
			$('#' + discussionSpaceShowItems).attr('data-send-request', 'true');
			$('#' + discussionSpaceHideItems).attr('data-send-request', 'true');
		});
	};

	/**
	 *
	 * @param uid
	 * @param is_argument
	 * @param is_supportive
	 * @param should_mark
	 * @param step
	 * @param history
	 * @param callback_id
	 */
	this.markStatementOrArgument = function(uid, is_argument, is_supportive, should_mark, step, history, callback_id){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_mark_statement_or_argument',
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({
				uid: uid,
				is_argument: is_argument,
				is_supportive: is_supportive,
				should_mark: should_mark,
				step: step,
				history: history
			}),
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxMarkStatementOrArgumentDone(data) {
			setGlobalSuccessHandler('Yeah!', data.success);
			var el = $('#' + callback_id);
			el.hide();
			if (data.text.length > 0) {
				el.parent().find('.triangle-content').html(data.text);
			}
			if (should_mark){
				el.prev().show();
			} else {
				el.next().show();
			}
		}).fail(function ajaxMarkStatementOrArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/*

	 */
	this.setDiscussionSettings = function(toggle_element){
		var checked = toggle_element.prop('checked');
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_discussion_properties',
			method: 'POST',
			data:{
				'checked': checked ? 'True': 'False',
				'uid': toggle_element.data('uid'),
				'key': toggle_element.data('keyword')},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function setEnOrDisableDiscussionDone(data) {
			new InteractionHandler().callbackForSetAvailabilityOfDiscussion(toggle_element, data);
		}).fail(function setEnOrDisableDiscussionFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
}
