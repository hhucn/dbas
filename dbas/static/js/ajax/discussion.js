/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxDiscussionHandler() {
	'use strict';
	/**
	 * Sends new premises to the server. Answer will be given to a callback
	 * @param arg_uid
	 * @param relation
	 * @param text
	 */
	this.sendNewPremiseForArgument = function (arg_uid, relation, text) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_new_premises_for_argument',
			method: 'POST',
			data: {
				arg_uid: arg_uid,
				attack_type: relation,
				premisegroups: JSON.stringify(text)
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewPremisesForArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewPremisesArgument(data);
		}).fail(function ajaxSendNewPremisesForArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			//new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + _t(errorCode) + ' 6). '
			//	 + _t(doNotHesitateToContact) + '. ');
		});
	};

	/**
	 * Sends new premises to the server. Answer will be given to a callback
	 * @param text of the premise
	 * @param conclusion_id id of the conclusion
	 * @param supportive boolean, whether it is supportive
	 */
	this.sendNewStartPremise = function (text, conclusion_id, supportive) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_new_start_premise',
			method: 'POST',
			data: {
				premisegroups: JSON.stringify(text),
				conclusion_id: conclusion_id,
				supportive: supportive
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewStartPremiseDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewStartPremise(data);
		}).fail(function ajaxSendNewStartPremiseFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			//new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + _t(errorCode) + ' 7). '
			//	 + _t(doNotHesitateToContact) + '. ');
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param statement for sending
	 */
	this.sendNewStartStatement = function (statement) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_new_start_statement',
			method: 'POST',
			data: {
				statement: statement
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendStartStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewStartStatement(data);
		}).fail(function ajaxSendStartStatementFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			//new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + _t(errorCode) + ' 2). '
			//	 + _t(doNotHesitateToContact) + '. ');
		});
	};

	/**
	 * Sends a new topic
	 *
	 * @param info
	 * @param long_info
	 * @param title
	 * @param language
	 */
	this.sendNewIssue = function(info, long_info, title, language){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$('#add-topic-error').hide();
		$.ajax({
			url: 'ajax_set_new_issue',
			method: 'POST',
			data: {
				info: info,
				long_info: long_info,
				title: title,
				lang: language
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendStartStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewIssue(data);
		}).fail(function ajaxSendStartStatementFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			$('#' + addTopicPopupErrorText).text(_t(requestFailed) + ' (' + _t(errorCode) + ' 9). '
				 + _t(doNotHesitateToContact) + '. ');
			$('#' + addTopicPopupContainer).show();
			setTimeout(function(){
				$('#' + addTopicPopupContainer).hide();
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
			method: 'GET',
			data: {
				uids: JSON.stringify(statements_uids),
				issue: getCurrentIssueId()
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetLogfileForPremisegroupDone(data) {
			new InteractionHandler().callbackIfDoneForGettingLogfile(data);
		}).fail(function ajaxGetLogfileForPremisegroupFail() {
			// $('#' + popupEditStatementErrorDescriptionId).html('Unfortunately, the log file could not be requested (server offline or csrf check' +
			// 	' failed. Sorry!');
			$('#' + popupEditStatementErrorDescriptionId).html(_t(requestFailed) + ' (' + _t(errorCode) + ' 15). '
				 + _t(doNotHesitateToContact) + '. ');
		});
	};

	/**
	 * Sends a correction of statements
	 * @param elements
	 */
	this.sendCorrectionOfStatement = function (elements) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_correction_of_statement',
			method: 'POST',
			data: {
				'elements': JSON.stringify(elements)
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendCorrectureOfStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data);
		}).fail(function ajaxSendCorrectureOfStatementFail() {
			// $('#' + popupEditStatementErrorDescriptionId).html('Unfortunately, the correcture could not be send (server offline or csrf check' +
			// 	' failed. Sorry!');
			$('#' + popupEditStatementErrorDescriptionId).html(_t(requestFailed) + ' (' + _t(errorCode) + ' 13). '
				 + _t(doNotHesitateToContact) + '. ');
		});
	};

	/**
	 * Shortens url
	 * @param long_url for shortening
	 */
	this.getShortenUrl = function (long_url) {
		var encoded_url = encodeURI(long_url);
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_shortened_url',
			method: 'GET',
			dataType: 'json',
			data: {
				url: encoded_url, issue: getCurrentIssueId()
			},
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetShortenUrlDone(data) {
			new InteractionHandler().callbackIfDoneForShortenUrl(data, long_url);
		}).fail(function ajaxGetShortenUrl() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			new PopupHandler().hideAndClearUrlSharingPopup();
			//$('#' + popupUrlSharingInputId).val(long_url);
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
			data: {
				uid: uid,
				lang: $('#issue-info').data('discussion-language')
			},
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetMoreInfosAboutArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForGettingInfosAboutArgument(data);
		}).fail(function ajaxGetMoreInfosAboutArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			//new GuiHandler().showDiscussionError(_t_discussion(requestFailed) + ' (' + _t_discussion(errorCode) + ' 8). '
			//	 + _t_discussion(doNotHesitateToContact) + '. ');
		});
	};

	/**
	 *
	 * @param type
	 * @param argument_uid
	 * @param statement_uid
	 * @param is_supportive
	 */
	this.getMoreInfosAboutOpinion = function(type, argument_uid, statement_uid, is_supportive){
		var is_argument = type == 'argument';
		var is_position = type == 'position' || type == 'statement';
		var uid = argument_uid == 'None' ? statement_uid : argument_uid;
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		
		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			method: 'GET',
			data: {
				is_argument: is_argument,
				uids: uid,
				is_position: is_position,
				is_supporti: is_supportive,
				lang: $('#issue_info').data('discussion-language')
			},
			dataType: 'json',
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetMoreInfosAboutArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForGettingMoreInfosAboutOpinion(data, is_argument);
		}).fail(function ajaxGetMoreInfosAboutArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			//new GuiHandler().showDiscussionError(_t_discussion(requestFailed) + ' (' + _t_discussion(errorCode) + ' 10). '
			//	 + _t_discussion(doNotHesitateToContact) + '. ');
		});

	};

	/***
	 * Ajax request for the fuzzy search
	 * @param value
	 * @param type
	 */
	this.fuzzySearchForDuplicate = function (value, type) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_fuzzy_search',
			method: 'GET',
			dataType: 'json',
			data: { value: value, type:type, extra: 'all', issue: getCurrentIssueId() },
			async: true,
			global: false,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetAllUsersDone(data) {
			new InteractionHandler().callbackIfDoneFuzzySearchForDuplicate(data);
		}).fail(function ajaxGetAllUsersFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
		
	};

	/***
	 * Ajax request for the fuzzy search
	 * @param value
	 * @param callbackid
	 * @param type
	 * @param extra optional
	 */
	this.fuzzySearch = function (value, callbackid, type, extra) {
		var callback = $('#' + callbackid);
		var pencil = '<i class="fa fa-pencil" aria-hidden="true"></i>';
		var tmpid = callbackid.split('-').length == 6 ? callbackid.split('-')[5] : '0';
		var bubbleSpace = $('#' + discussionBubbleSpaceId);
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		// clear lists if input is empty
		if(callback.val().length==0) {
			$('#' + proposalStatementListGroupId).empty();
			$('#' + proposalPremiseListGroupId).empty();
			$('#' + proposalEditListGroupId).empty();
			$('#' + proposalUserListGroupId).empty();
			$('p[id^="current_"]').each(function() {
				$(this).parent().remove();
			});
			return;
		}

		if (type != fuzzy_find_user) {
			// add or remove bubble only iff we are not in an popup
			if (type != fuzzy_statement_popup) {
				if (bubbleSpace.find('#current_' + tmpid).length == 0) {
					var text = $('<p>').addClass('triangle-r').attr('id', 'current_' + tmpid).html(value + '...' + pencil);
					var current = $('<div>').addClass('line-wrapper-r').append(text).hide().fadeIn();
					current.insertAfter(bubbleSpace.find('div:last-child'));
					setInterval(function () { // fading pencil
						bubbleSpace.find('.fa-pencil').fadeTo('slow', 0.2, function () {
							bubbleSpace.find('.fa-pencil').fadeTo('slow', 1.0, function () {
							});
						});
					}, 1000);
				} else {
					$('#current_' + tmpid).html(value + '...' + pencil);
				}
			}
			var gh = new GuiHandler();
			var resize = gh.setMaxHeightForBubbleSpace();
			gh.setMaxHeightForDiscussionContainer(resize);
		}

		$.ajax({
			url: 'ajax_fuzzy_search',
			method: 'GET',
			dataType: 'json',
			data: { value: value, type:type, extra: extra, issue: getCurrentIssueId() },
			async: true,
			global: false,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetAllUsersDone(data) {
			new InteractionHandler().callbackIfDoneFuzzySearch(data, callbackid, type);
		}).fail(function ajaxGetAllUsersFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			//setTimout(function ajaxGetAllUsersFailDelay() {
			//	new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + _t(errorCode) + ' 11). '
			//			+ _t(doNotHesitateToContact) + '. ');
			//}, 350);
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
			data: {
				uids: JSON.stringify(uids),
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function (data) {
			var parsedData = $.parseJSON(data);
			// note that we already send data
			if (parsedData.error.length == 0){
				$('#' + discussionSpaceShowItems).attr('data-send-request', 'true');
				$('#' + discussionSpaceHideItems).attr('data-send-request', 'true');
			}
		}).fail(function () {
		});
	};
}
