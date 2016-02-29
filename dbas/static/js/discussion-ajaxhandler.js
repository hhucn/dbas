/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxSiteHandler() {
	'use strict';

	/**
	 * Sends new premises to the server. Answer will be given to a callback
	 * @param arg_uid
	 * @param relation
	 * @param text
	 */
	this.sendNewPremiseForArgument = function (arg_uid, relation, text) {
		var csrfToken = $('#' + hiddenCSRFTokenId).val();
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
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendNewPremisesForArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewPremisesArgument(data);
		}).fail(function ajaxSendNewPremisesForArgumentFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 6). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Sends new premises to the server. Answer will be given to a callback
	 * @param text of the premise
	 * @param conclusion_id id of the conclusion
	 * @param supportive boolean, whether it is supportive
	 */
	this.sendNewStartPremise = function (text, conclusion_id, supportive) {
		var csrfToken = $('#' + hiddenCSRFTokenId).val();
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
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendNewStartPremiseDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewStartPremise(data, supportive);
		}).fail(function ajaxSendNewStartPremiseFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 7). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param statement for sending
	 */
	this.sendNewStartStatement = function (statement) {
		var csrfToken = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_set_new_start_statement',
			method: 'POST',
			data: {
				statement: statement
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendStartStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewStartStatement(data);
		}).fail(function ajaxSendStartStatementFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 8). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Requests the logfile for the given uid
	 * @param id_id current uid of the statement
	 */
	this.getLogfileForStatement = function (id_id) {
		var csrfToken = $('#' + hiddenCSRFTokenId).val(), settings_data, url;
		$.ajax({
			url: 'ajax_get_logfile_for_statement',
			method: 'GET',
			data: {
				uid: id_id
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetLogfileForStatementDone(data) {
			new InteractionHandler().callbackIfDoneForGettingLogfile(data);
		}).fail(function ajaxGetLogfileForStatementFail() {
			// $('#' + popupEditStatementErrorDescriptionId).html('Unfortunately, the log file could not be requested (server offline or csrf check' +
			// 	' failed. Sorry!');
			$('#' + popupEditStatementErrorDescriptionId).html(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 15). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Sends a correcture of a statement
	 * @param uid
	 * @param element
	 * @param corrected_text the corrected text
	 */
	this.sendCorrectureOfStatement = function (uid, corrected_text, element) {
		var csrfToken = $('#' + hiddenCSRFTokenId).val(),settings_data, url;
		$.ajax({
			url: 'ajax_set_correcture_of_statement',
			method: 'POST',
			data: {
				uid: uid,
				text: corrected_text
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxSendCorrectureOfStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data, element);
		}).fail(function ajaxSendCorrectureOfStatementFail() {
			// $('#' + popupEditStatementErrorDescriptionId).html('Unfortunately, the correcture could not be send (server offline or csrf check' +
			// 	' failed. Sorry!');
			$('#' + popupEditStatementErrorDescriptionId).html(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 13). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Shortens url
	 * @param long_url for shortening
	 */
	this.getShortenUrl = function (long_url) {
		var encoded_url = encodeURI(long_url), settings_data, url;
		$.ajax({
			url: 'ajax_get_shortened_url',
			method: 'GET',
			dataType: 'json',
			data: {
				url: encoded_url, issue: new Helper().getCurrentIssueId()
			},
			async: true,
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetShortenUrlDone(data) {
			new InteractionHandler().callbackIfDoneForShortenUrl(data);
		}).fail(function ajaxGetShortenUrl() {
			$('#' + popupUrlSharingInputId).val(long_url);
		});
	};

	this.getMoreInfosAboutArgument = function(uid, calledbButton){
		if (calledbButton){
			if (!$('#' + discussionsDescriptionBridgeInfoId).hasClass('in')){
				$('#' + discussionsDescriptionBridgeInfoId).collapse('show');
			} else {
				$('#' + discussionsDescriptionBridgeInfoId).collapse('hide');
			}
		} else {
			if ($('#' + discussionsDescriptionBridgeInfoId).hasClass('in')) {
				// $('#' + discussionsDescriptionBridgeInfoId).removeClass('in');
				return;
			}
		}


		var csrfToken = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_infos_about_argument',
			method: 'POST',
			data: {
				uid: uid
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxGetMoreInfosAboutArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForGettingInfosAboutArgument(data);
		}).fail(function ajaxGetMoreInfosAboutArgumentFail() {
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 8). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
			if ($('#' + discussionsDescriptionBridgeInfoId).hasClass('in')){
				$('#' + discussionsDescriptionBridgeInfoId).removeClass('in');
			}
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
		var settings_data, url, callback = $('#' + callbackid);

		if(callback.val().length==0) {
			$('#' + proposalStatementListGroupId).empty();
			$('#' + proposalPremiseListGroupId).empty();
			$('#' + proposalEditListGroupId).empty();
			return;
		}

		$.ajax({
			url: 'ajax_fuzzy_search',
			method: 'GET',
			dataType: 'json',
			data: { value: value, type:type, extra: extra, issue: new Helper().getCurrentIssueId() },
			async: true,
			global: false,
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetAllUsersDone(data) {
			new InteractionHandler().callbackIfDoneFuzzySearch(data, callbackid, type);
			new GuiHandler().hideDiscussionError();
		}).fail(function ajaxGetAllUsersFail() {
			new Helper().delay(function ajaxGetAllUsersFailDelay() {
				new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 11). '
						+ _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
			}, 350);
		});
		callback.focus();
	};
}
