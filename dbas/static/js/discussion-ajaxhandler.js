/*global $, jQuery, alert, GuiHandler, InteractionHandler, internal_error, popupErrorDescriptionId */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function AjaxHandler() {
	'use strict';

	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 */
	this.getStartStatements = function () {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_start_statements',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxGetAllPositionsDone(data) {
			// document.location.hash = '';
			history.pushState(data, '', document.location);
			new InteractionHandler().callbackIfDoneForGetStartStatements(data);
		}).fail(function ajaxGetAllPositionsFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure, could not find any start point.');
		});
	};

	/**
	 * Send an ajax request for getting all premisses for a givens tatement
	 * @param uid of clicked statement
	 */
	this.getPremisseForStatement = function (uid) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data;
		$.ajax({
			url: 'ajax_get_premisses_for_statement',
			method: 'POST',
			data: {
				uid: uid
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
			}
		}).done(function ajaxGetPremisseForStatementDone(data) {
			// document.location.hash = settings_data;
			history.pushState(data, '', document.location);
			new InteractionHandler().callbackIfDoneForPremisseForStatement(data);
		}).fail(function ajaxGetPremisseForStatementFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while requesting data for your statement.');
		});
	};

	/**
	 * Sends an ajax request for getting all premisses for a given statement
	 * @param uid of clicked statement
	 */
	this.getReplyForPremisseGroup = function (uid) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data;
		$.ajax({
			url: 'ajax_reply_for_premissegroup',
			method: 'POST',
			data: {
				uid: uid
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
			}
		}).done(function ajaxGetReplyForPremisseDone(data) {
			// document.location.hash = settings_data;
			history.pushState(data, '', document.location);
			new InteractionHandler().callbackIfDoneReplyForPremissegroup(data);
		}).fail(function ajaxGetReplyForPremisseFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while requesting another opininion.');
		});
	};

	/**
	 * Sends an ajax request for getting all confrotations for a given argument
	 * @param uid of the clicked premisse group
	 */
	this.getReplyForArgument = function (uid) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data;
		$.ajax({
			url: 'ajax_reply_for_argument',
			method: 'POST',
			data: {
				uid: uid
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
			}
		}).done(function ajaxGetReplyForArgumentDone(data) {
			// document.location.hash = settings_data;
			history.pushState(data, '', document.location);
			new InteractionHandler().callbackIfDoneReplyForArgument(data);
		}).fail(function ajaxGetReplyForArgumentFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while requesting another opininion.');
		});
	};

	/**
	 * Sends an ajax request for handle the reaction of a confrontation
	 * @param id of clicked relation and statement
	 */
	this.handleReplyForResponseOfConfrontation = function (id) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data;
		$.ajax({
			url: 'ajax_reply_for_response_of_confrontation',
			method: 'POST',
			data: {
				id: id
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
			}
		}).done(function ajaxHandleReplyForResponseOfConfrontationDone(data) {
			// document.location.hash = settings_data;
			history.pushState(data, '', document.location);
			new InteractionHandler().callbackIfDoneHandleReplyForResponseOfConfrontation(data);
		}).fail(function ajaxHandleReplyForResponseOfConfrontationFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while requesting another opininion.');
		});
	};

	/**
	 * Requests all users
	 */
	this.getUsersAndSetInGui = function () {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxGetAllUsersDone(data) {
			new InteractionHandler().callbackIfDoneGetUsersAndSetInGui(data);
		}).fail(function ajaxGetAllUsersFail() {
			new GuiHandler().setErrorDescription(internal_error);
		});
	};

	/**
	 * Sends new premisses to the server. Answer will be given to a callback
	 * @param argument_dictionary for inserting
	 */
	this.sendNewPremissesForArgument = function (argument_dictionary) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_new_premisses',
			type: 'POST',
			data: argument_dictionary,
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendNewPremissesDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewPremisses(data);
		}).fail(function ajaxSendNewPremissesFail() {
			new GuiHandler().setErrorDescription(internal_error);
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param statement for sending
	 */
	this.sendNewStartStatement = function (statement) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_new_start_statement',
			type: 'POST',
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
			new GuiHandler().setErrorDescription(internal_error);
		});
	};

	/**
	 * Requests the logfile for the given uid
	 * @param statement_uid current uid of the statement
	 */
	this.getLogfileForStatement = function (statement_uid) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_logfile_for_statement',
			type: 'POST',
			data: {
				uid: statement_uid
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxGetLogfileForStatementDone(data) {
			new InteractionHandler().callbackIfDoneForGetLogfileForStatement(data);
		}).fail(function ajaxGetLogfileForStatementFail() {
			$('#' + popupErrorDescriptionId).text('Unfortunately, the log file could not be requested (server offline or csrf check' +
				' failed. Sorry!');
		});
	};

	/**
	 * Sends a correcture of a statement
	 * @param uid
	 * @param edit_dialog_td_id
	 * @param corrected_text the corrected text
	 */
	this.sendCorrectureOfStatement = function (uid, edit_dialog_td_id, corrected_text) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_correcture_of_statement',
			type: 'POST',
			data: {
				uid: uid,
				text: corrected_text
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendCorrectureOfStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data, edit_dialog_td_id);
		}).fail(function ajaxSendCorrectureOfStatementFail() {
			$('#' + popupErrorDescriptionId).text('Unfortunately, the correcture could not be send (server offline or csrf check' +
				' failed. Sorry!');
		});
	};
}