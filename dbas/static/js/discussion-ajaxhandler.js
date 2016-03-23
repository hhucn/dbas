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
			new InteractionHandler().callbackIfDoneForSendNewStartPremise(data);
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

	/**
	 *
	 * @param uid
	 */
	this.getMoreInfosAboutArgument = function(uid){
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
		var settings_data, url, callback = $('#' + callbackid),
			pencil = '<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>',
			tmpid = callbackid.split('-').length == 6 ? callbackid.split('-')[5] : '0',
			bubbleSpace = $('#' + discussionBubbleSpaceId);

		// clear lists if input is empty
		if(callback.val().length==0) {
			$('#' + proposalStatementListGroupId).empty();
			$('#' + proposalPremiseListGroupId).empty();
			$('#' + proposalEditListGroupId).empty();
			$('p[id^="current_"]').each(function() {
				$(this).parent().remove();
			});
			return;
		}

		// add or remove bubble only iff we are not in an popp
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
