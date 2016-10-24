/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxMainHandler(){
	/**
	 * Sends a request for language change
	 * @param new_lang is the shortcut for the language
	 */
	this.ajaxSwitchDisplayLanguage = function (new_lang){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_switch_language',
			type: 'POST',
			data: { lang: new_lang},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSwitchDisplayLanguageDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData.error.length != 0) {
				setGlobalErrorHandler(_t(ohsnap), parsedData.error);
			} else {
				location.reload(true);
				setPiwikOptOutLink(new_lang);
			}
		}).fail(function ajaxSwitchDisplayLanguageFail(xhr) {
			if (xhr.status == 400) {
				setGlobalErrorHandler(_t(ohsnap), _t(requestFailedBadToken));
			} else if (xhr.status == 500) {
				setGlobalErrorHandler(_t(ohsnap), _t(requestFailedInternalError));
			} else {
				setGlobalErrorHandler(_t(ohsnap), _t(languageCouldNotBeSwitched));
			}
		});
	};

	/**
	 *
	 */
	this.ajaxLogin = function(user, password, showGlobalError){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var url = window.location.href;
		var keep_login = $('#keep-login-box').prop('checked') ? 'true' : 'false';

		$.ajax({
			url: mainpage + 'ajax_user_login',
			type: 'POST',
			data: {
				user: user,
				password: password,
				url: url,
				keep_login: keep_login
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxLoginDone(data) {
			callbackIfDoneForLogin(data, showGlobalError);
		}).fail(function ajaxLoginFail(xhr) {
			console.log('FAIL ' + xhr.status);
			var showError = false;
			var errorMsg = '';
			
			if (xhr.status == 200) {			location.reload(true);
			} else if (xhr.status == 302) {		location.href = xhr.getResponseHeader('Location');
			} else if (xhr.status == 400) {		errorMsg = _t(requestFailedBadToken);
			} else if (xhr.status == 500) {		errorMsg = _t(requestFailedInternalError);
			} else {            				errorMsg = _t(requestFailed);
			}
			
			if (showError){
				if (showGlobalError) {
					setGlobalErrorHandler('Ohh!', errorMsg);
				} else {
					$('#' + popupLoginFailed).show();
					$('#' + popupLoginFailed + '-message').text(errorMsg);
				}
			}
		}).always(function ajaxLoginAlways(){
			$('#' + loginPwId).val('');
		});
	};

	/**
	 *
	 */
	this.ajaxLogout = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: mainpage + 'ajax_user_logout',
			type: 'POST',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxLogoutDone(data) {
			location.reload();
		}).fail(function ajaxLogoutFail(xhr) {
			if (xhr.status == 200) {
				if (window.location.href.indexOf('settings') != 0){
					window.location.href = mainpage;
				} else {
					location.reload();
				}
			} else if (xhr.status == 403) {
				window.location.href = mainpage;
			} else {
				location.reload();
			}
		});
	};

	/**
	 *
	 */
	this.ajaxRegistration = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var firstname = $('#userfirstname-input').val(),
			lastname = $('#userlastname-input').val(),
			nickname = $('#nick-input').val(),
			email = $('#email-input').val(),
			password = $('#' + popupLoginPasswordInputId).val(),
			passwordconfirm = $('#' + popupLoginPasswordconfirmInputId).val(),
			spamanswer = $('#popup-login-spamanswer-input').val(),
			gender = '';

		if ($('#' + popupLoginInlineRadioGenderN).is(':checked')) gender = 'n';
		if ($('#' + popupLoginInlineRadioGenderM).is(':checked')) gender = 'm';
		if ($('#' + popupLoginInlineRadioGenderF).is(':checked')) gender = 'f';

		$.ajax({
			url: 'ajax_user_registration',
			type: 'POST',
			data: { firstname: firstname,
					lastname: lastname,
					nickname: nickname,
					gender: gender,
					email: email,
					password: password,
					passwordconfirm: passwordconfirm,
					spamanswer: spamanswer,
					lang: getLanguage()},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxRegistrationDone(data) {
			callbackIfDoneForRegistration(data);
		}).fail(function ajaxRegistrationFail(xhr) {
			$('#' + popupLoginRegistrationFailed).show();
			if (xhr.status == 400) {		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedBadToken));
			} else if (xhr.status == 500) {	$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedInternalError));
			} else {                		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
			}
		}).always(function ajaxLoginAlways(){
			$('#' + popupLoginPasswordInputId).val('');
			$('#' + popupLoginPasswordconfirmInputId).val('');
		});
	};

	/**
	 *
	 */
	this.ajaxPasswordRequest = function(){
		var email = $('#password-request-email-input').val();
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_user_password_request',
			type: 'POST',
			data: { email: email, lang: getLanguage()},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxPasswordRequestDone(data) {
			callbackIfDoneForPasswordRequest(data);
		}).fail(function ajaxPasswordRequestFail(xhr) {
			$('#' + popupLoginRegistrationFailed).show();
			if (xhr.status == 400) {		$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedBadToken));
			} else if (xhr.status == 500) {	$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailedInternalError));
			} else {            			$('#' + popupLoginRegistrationFailed + '-message').text(_t(requestFailed));
			}
		});
	};

	/**
	 * Get-Request for an roundhouse kick
	 */
	this.ajaxRoundhouseKick = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'additional_service',
			type: 'POST',
			data: {type:'chuck'},
			global: false,
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxRoundhouseKickDone(data) {
			if (data.type == 'success'){
				displayConfirmationDialogWithoutCancelAndFunction('Chuck Norris Fact #' + data.value.id,
					'<h5>' + data.value.joke + '</h5>\n\n' +
					'<span style="float:right;">powered by <a href="http://www.icndb.com/" target="_blank">http://www.icndb.com/</a></span>');

			}
		});
	};

	/**
	 * Get your mama
	 */
	this.ajaxMama = function(){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'additional_service',
			type: 'POST',
			data: {type:'mama'},
			global: false,
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxMamaDone(data) {
			displayConfirmationDialogWithoutCancelAndFunction('Yo Mamma',  '<h4>' + data.joke + '</h4>\n\n<span' +
					' style="float:right;">powered by <a href="http://yomomma.info/">http://yomomma.info/</a></span>');
		});
	};
	
	/**
	 *
	 * @param uid
	 * @param reason
	 * @param is_argument
	 */
	this.ajaxFlagArgumentOrStatement = function(uid, reason, is_argument){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_flag_argument_or_statement',
			method: 'POST',
			data: {
				uid: uid,
				reason: reason,
				is_argument: is_argument
			},
			global: false,
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxFlagArgumentDone(data) {
			var parsedData = $.parseJSON(data);
			if (parsedData['error'].length != 0){
				setGlobalErrorHandler('', parsedData['error']);
			} else if (parsedData['info'].length != 0) {
				setGlobalInfoHandler('', parsedData['info'])
			} else {
				setGlobalSuccessHandler('', parsedData['success'])
			}
			
		}).fail(function ajaxFlagArgumentFail() {
			setGlobalErrorHandler('', _t_discussion(requestFailed));
		});
	}
}

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
	 * @param info
	 * @param title
	 * @param language
	 * @param callbackFunctionOnDone
	 */
	this.sendNewIssue = function(info, title, language, callbackFunctionOnDone){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$('#add-topic-error').hide();
		$.ajax({
			url: 'ajax_set_new_issue',
			method: 'POST',
			data: {
				info: info, title: title, lang: language
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendStartStatementDone(data) {
			callbackFunctionOnDone(data);
		}).fail(function ajaxSendStartStatementFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			$('#' + addTopicPopupErrorText).text(_t(requestFailed) + ' (' + _t(errorCode) + ' 9). '
				 + _t(doNotHesitateToContact) + '. ');
			$('#' + addTopicPopupContainer).show();
			new Helper().delay(function(){
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
				issue: new Helper().getCurrentIssueId()
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
				url: encoded_url, issue: new Helper().getCurrentIssueId()
			},
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetShortenUrlDone(data) {
			new InteractionHandler().callbackIfDoneForShortenUrl(data, long_url);
		}).fail(function ajaxGetShortenUrl() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			new GuiHandler().hideAndClearUrlSharingPopup();
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
		var attack = '';
		var splitted = window.location.href.split('?')[0].split('/');
		if (splitted.indexOf('reaction') != -1)
			attack = splitted[splitted.indexOf('reaction') + 2];
		
		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			method: 'GET',
			data: {
				is_argument: is_argument,
				uids: uid,
				is_position: is_position,
				is_supporti: is_supportive,
				lang: $('#issue_info').data('discussion-language'),
				attack: attack
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
	 * @param callbackid
	 * @param type 0 for statements, 1 for edit-popup
	 * @param extra optional
	 */
	this.fuzzySearch = function (value, callbackid, type, extra) {
		var callback = $('#' + callbackid),
			pencil = '<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>',
			tmpid = callbackid.split('-').length == 6 ? callbackid.split('-')[5] : '0',
			bubbleSpace = $('#' + discussionBubbleSpaceId),
			csrf_token = $('#' + hiddenCSRFTokenId).val();
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
					var text = $('<p>').addClass('triangle-r').attr('id', 'current_' + tmpid).html(value + '...' + pencil),
						current = $('<div>').addClass('line-wrapper-r').append(text).hide().fadeIn();
					current.insertAfter(bubbleSpace.find('div:last-child'));
					setInterval(function () { // fading pencil
						$('.glyphicon-pencil').fadeTo('slow', 0.2, function () {
							$('.glyphicon-pencil').fadeTo('slow', 1.0, function () {
							});
						});
					}, 1000);
				} else {
					$('#current_' + tmpid).html(value + '...' + pencil);
				}
			}
			new GuiHandler().setMaxHeightForBubbleSpace();
		}

		$.ajax({
			url: 'ajax_fuzzy_search',
			method: 'GET',
			dataType: 'json',
			data: { value: value, type:type, extra: extra, issue: new Helper().getCurrentIssueId() },
			async: true,
			global: false,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetAllUsersDone(data) {
			new InteractionHandler().callbackIfDoneFuzzySearch(data, callbackid, type);
		}).fail(function ajaxGetAllUsersFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			//new Helper().delay(function ajaxGetAllUsersFailDelay() {
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
			new InteractionHandler().callbackIfDoneRevokeContent(data, is_argument);
		}).fail(function ajaxRevokeContentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
			new GuiHandler().hideAndClearUrlSharingPopup();
			//$('#' + popupUrlSharingInputId).val(long_url);
		});
	}
}

function AjaxUserHandler(){

	/**
	 * Ajax call for user data
	 */
	this.getPublicUserData = function () {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_public_user_data',
			method: 'GET',
			data:{ 'nickname': $('#public_nick').text() },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getPublicUserDataDone(data) {
			new User().callbackDone(data);
		}).fail(function getPublicUserDataFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
}

function AjaxNewsHandler(){
	/**
	 *
	 */
	this.ajaxGetNews = function () {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_news',
			type: 'POST',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxGetNewsDone(data) {
			new News().callbackIfDoneForGettingNews(data);
		}).fail(function ajaxGetNewsFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 */
	this.ajaxSendNews = function () {
		var title = $('#' + writingNewNewsTitleId).val();
		var text = $('#' + writingNewNewsTextId).val();

		if (title.length == 0 || text.length < 10) {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).text(_t(empty_news_input));
			new Helper().delay(function(){
				$('#' + writingNewsFailedId).fadeOut();
				new Helper().delay(function(){
					$('#' + writingNewsFailedMessageId).text('');
				}, 2000);
			}, 2000);
			return;
		} else {
			$('#' + writingNewsFailedId).hide();
			$('#' + writingNewsSuccessId).hide();
		}

		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_send_news',
			type: 'POST',
			data: {title: title, text: text},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrf_token
			}
		}).done(function ajaxSendNewsDone(data) {
			new News().callbackIfDoneForSendingNews(data);
		}).fail(function ajaxSendNewsFail() {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).html(_t(internalError));
		});
	};
}

function AjaxSettingsHandler(){
	/**
	 * Ajax request for getting the users history
	 */
	this.getUserHistoryData = function(){
		'use strict';
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_user_history',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().getUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail(xhr) {
			new HistoryHandler().getDataFail(xhr.status);
		});
	};

	/**
	 * Ajax request for deleting the users history
	 */
	this.deleteUserHistoryData = function(){
		'use strict';
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_user_history',
			method: 'POST',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().removeUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail(xhr) {
			new HistoryHandler().getDataFail(xhr.status);
		});
	};

	/**
	 *
	 * @param toggle_element
	 * @param service
	 */
	this.setUserSetting = function(toggle_element, service) {
		var settings_value = toggle_element.prop('checked');
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_setting',
			method: 'POST',
			data:{'settings_value': settings_value ? 'True': 'False', 'service': service},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function setUserSettingDone(data) {
			new SettingsHandler().callbackDone(data, toggle_element, settings_value, service);
		}).fail(function setUserSettingFail() {
			new SettingsHandler().callbackFail(toggle_element, settings_value, service);
		});
	};

	/**
	 *
	 * @param ui_locales
	 */
	this.setNotifcationLanguage = function(ui_locales){
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_language',
			method: 'POST',
			data:{'ui_locales': ui_locales},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function setUserSettingDone(data) {
			var parsedData = $.parseJSON(data);

			if (parsedData.error.length == 0){
				$('#' + settingsSuccessDialog).fadeIn();
				new Helper().delay(function() { $('#' + settingsSuccessDialog).fadeOut(); }, 3000);
				$.each($('#settings-language-dropdown').find('li'), function(){ $(this).removeClass('active');});
				$.each($('#current-lang-images').find('img'), function(){ $(this).hide()});
				$('#link-settings-' + parsedData.ui_locales).addClass('active');
				$('#indicator-' + parsedData.ui_locales).show();
				$('#current-lang-images span').eq(0).text(parsedData.current_lang);
			} else {
				$('#' + settingsAlertDialog).fadeIn();
				new Helper().delay(function() { $('#' + settingsAlertDialog).fadeOut(); }, 3000);
			}
		}).fail(function setUserSettingFail() {
			$('#' + settingsAlertDialog).fadeIn();
			new Helper().delay(function() { $('#' + settingsAlertDialog).fadeOut(); }, 3000);
		});
	};

	/**
	 *
	 */
	this.getEditsDone = function() {
		if ($('#' + editsDoneCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_edits',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allEditsDone), false);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 *
	 */
	this.getStatementsSend = function() {
		if ($('#' + statementsDoneCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_posted_statements',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allStatementsPosted), false);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 *
	 */
	this.getArgumentVotes = function(){
		if ($('#' + discussionArgVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_argument_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});

	};

	/**
	 *
	 */
	this.getStatementVotes = function(){
		if ($('#' + discussionStatVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_statement_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});

	};

	/**
	 *
	 */
	this.deleteStatisticsRequest = function() {
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_statistics',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackDeleteStatisticsDone(data);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail();
		});
	};
}

function AjaxNotificationHandler(){
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
			var parsedData = $.parseJSON(data);
			if (parsedData.error.length > 0) {
				setGlobalErrorHandler(_t_discussion(ohsnap), parsedData.error);
			} else {
				var titletext = $(_this).text().replace(_t(neww).toLocaleUpperCase(), '').trim();
				var spanEl = $('<span>').addClass('text-primary').text(titletext);
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
		var csrf_token = $('#' + hiddenCSRFTokenId).val();

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

function AjaxGraphHandler(){
	
	/**
	 * Requests JSON-Object
	 * @param uid: current id in url
	 * @param adress: keyword in url
	 */
	this.getUserGraphData = function(uid, adress){
		var dataString;
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var attack = '';
		var splitted = window.location.href.split('?')[0].split('/');
		if (splitted.indexOf('reaction') != -1)
			attack = splitted[splitted.indexOf('reaction') + 2];
		
		switch(adress){
			case 'attitude':
				dataString = {is_argument: 'false', is_attitude: 'true', is_reaction: 'false', is_position: 'false', uids: uid};
				break;
			case 'justify':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'false', uids: JSON.stringify(uid)};
				break;
			case 'argument':
				dataString = {is_argument: 'true', is_attitude: 'false', is_reaction: 'true', is_position: 'false', uids: JSON.stringify(uid)};
				break;
			case 'position':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'true', uids: JSON.stringify(uid)};
		}
		dataString['lang'] = $('#issue_info').data('discussion-language');
		dataString['attack'] = attack;
		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			type: 'POST',
			dataType: 'json',
			data: dataString,
			async: true,
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function (data) {
			new DiscussionBarometer().callbackIfDoneForGetDictionary(data, adress);
		}).fail(function () {
			new DiscussionBarometer().callbackIfFailForGetDictionary();
		});
	};

	/**
	 * Displays a graph of current discussion
	 */
	this.getDiscussionGraphData = function (url) {
		// TODO FIX CSRF
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			data: {issue: new Helper().getCurrentIssueId()}
		}).done(function (data) {
			new DiscussionGraph().callbackIfDoneForDiscussionGraph(data);
		}).fail(function () {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param uid
     */
	this.getJumpDataForGraph = function (uid) {
		$.ajax({
			url: '/ajax_get_arguments_by_statement/' + uid,
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function (data) {
			new DiscussionGraph().callbackIfDoneForGetJumpDataForGraph(data);
		}).fail(function () {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
}

function AjaxReviewHandler(){
	
	/**
	 *
	 * @param review_uid
	 * @param should_lock is true, when the review should be locked and false otherwise
	 * @param review_instance
	 */
	this.un_lockOptimizationReview = function (review_uid, should_lock, review_instance) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_lock',
			method: 'POST',
			data:{ 'review_uid': review_uid, 'lock': should_lock },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			if (should_lock)
				new ReviewCallbacks().forReviewLock(data, review_instance);
			else
				new ReviewCallbacks().forReviewUnlock(data);
		}).fail(function reviewDeleteArgumentFail() {
			if (should_lock)
				setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
	
	/**
	 *
	 * @param should_delete
	 * @param review_uid
	 */
	this.reviewDeleteArgument = function(should_delete, review_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_delete_argument',
			method: 'POST',
			data:{ 'should_delete': should_delete, 'review_uid': review_uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewCallbacks().forReviewArgument(data);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
	
	/**
	 *
	 * @param is_edit_okay
	 * @param review_uid
	 */
	this.reviewEditArgument = function(is_edit_okay, review_uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_edit_argument',
			method: 'POST',
			data:{ 'is_edit_okay': is_edit_okay, 'review_uid': review_uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewCallbacks().forReviewArgument(data);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
	
	/**
	 *
	 * @param should_optimized
	 * @param review_uid
	 * @param new_data (Important: must be JSON.stringify(...))
	 */
	this.reviewOptimizationArgument = function(should_optimized, review_uid, new_data){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_review_optimization_argument',
			type: 'POST',
			data:{
				'should_optimized': should_optimized,
				'review_uid': review_uid,
				'new_data': JSON.stringify(new_data) },
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewCallbacks().forReviewArgument(data);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
	
	/**
	 *
	 * @param queue
	 * @param uid
	 */
	this.undoReview = function(queue, uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_undo_review',
			method: 'GET',
			data:{ 'queue': queue, uid: uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewHistoryCallbacks().forUndoReview(data, queue, uid);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
	
	/**
	 *
	 * @param queue
	 * @param uid
	 */
	this.cancelReview = function(queue, uid){
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_cancel_review',
			method: 'GET',
			data:{ 'queue': queue, uid: uid },
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function reviewDeleteArgumentDone(data) {
			new ReviewHistoryCallbacks().forUndoReview(data, queue, uid);
		}).fail(function reviewDeleteArgumentFail() {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	}
	
}