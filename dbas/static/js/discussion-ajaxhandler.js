/*global $, jQuery, alert, GuiHandler, InteractionHandler */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

// TODO KICK ALL METHODS WHICH ARE NOT USED

function AjaxHandler() {
	'use strict';
	var internal_error = 'Internal Error: Maybe the server is offline or your data was not valid due to a CSRF check.';

	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 */
	this.getStartStatements = function () {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_start_statements',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetAllPositionsDone(data) {
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
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_premisses_for_statement',
			method: 'POST',
			data: { uid : uid},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetPremisseForStatementDone(data) {
			new InteractionHandler().callbackIfDoneForPremisseForStatement(data);
		}).fail(function ajaxGetPremisseForStatementFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while requesting data for your statement.');
		});
	};

	/**
	 * Request all users
	 */
	this.getUsersAndSetInGui = function () {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetAllUsersDone(data) {
			new GuiHandler().setJsonDataToAdminContent($.parseJSON(data));
		}).fail(function ajaxGetAllUsersFail() {
			new GuiHandler().setErrorDescription(internal_error);
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument has a connection to the
	 * position with given uid.
	 * @param pos_uid uid of clicked position
	 *
	this.getArgumentsForJustification = function (pos_uid) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_arguments_connected_to_position_uid',
			method: 'POST',
			data: { uid : pos_uid},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetArgumentsForJustificationDone(data) {
			new InteractionHandler().callbackIfDoneForArgsForJustification(data);
		}).fail(function ajaxGetArgumentsForJustificationFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while requesting data for the next argumentation.');
		});
	};

	/**
	 * Requests data for a new argumentation round. This includes a statement, an confrontation and justifications
	 * @param currentStatementId uid of the current statement
	 *
	this.getNewArgumentationRound = function (currentStatementId) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_args_for_new_discussion_round',
			method: 'POST',
			data: { uid: currentStatementId},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetNewArgumentationRoundDone(data) {
			new InteractionHandler().callbackIfDoneForGetNewArgumentationRound(data);
		}).fail(function ajaxGetNewArgumentationRoundFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while requesting data for the next argumentation.');
		});
	};

	/**
	 * Request data for getting one step back
	 *
	this.getOneStepBack = function () {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_one_step_back',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetOneStepBackDone(data) {
			$('#' + stepBackButtonId).hide();
			new InteractionHandler().callbackGetOneStepBack(data);
		}).fail(function ajaxGetOneStepBackFail() {
			$('#' + stepBackButtonId).hide();
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().showDiscussionError('Internal failure while stepping back');
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param argument_dictionary for inserting
	 *
	this.sendNewArgument = function (argument_dictionary) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_send_new_arguments',
			type: 'POST',
			data: argument_dictionary,
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxSendNewArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewArguments(data);
		}).fail(function ajaxSendNewArgumentFail() {
			new GuiHandler().setErrorDescription(internal_error);
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param position for sending
	 *
	this.sendNewPosition = function (position) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_send_new_position',
			type: 'POST',
			data: { position : position},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxSendNewPositionDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewPosition(data);
		}).fail(function ajaxSendNewPositionFail() {
			new GuiHandler().setErrorDescription(internal_error);
		});
	};

	/**
	 * Request for all arguments, which have a relation to the last saved one
	 *
	this.getAllArgumentsForIslandView = function () {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_all_arguments_for_island',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetAllArgumentsForIslandViewDone(data) {
			new InteractionHandler().callbackIfDoneForGetAllArgumentsForIslandView(data);
		}).fail(function ajaxGetAllArgumentsForIslandViewFail() {
			new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().setVisibilityOfDisplayStyleContainer(false, '');
		});
	};

	/**
	 * Requests the logfile for the given uid
	 * @param statement_uid current uid of the statement
	 */
	this.getLogfileForStatement = function (statement_uid){
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_logfile_for_statement',
			type: 'POST',
			data: { uid: statement_uid},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetLogfileForStatementDone(data) {
			new InteractionHandler().callbackIfDoneForGetLogfileForStatement(data);
		}).fail(function ajaxGetLogfileForStatementFail() {
			$('#' + popupErrorDescriptionId).text('Unfortunately, the log file could not be requested (server offline or csrf check' +
				' failed. Sorry!');
		});
	};

	/**
	 * Sends a correcture of a statement
	 * @param statement_uid current uid of the statement
	 * @param is_argument true, if it is an argument
	 * @param corrected_text the corrected text
	 */
	this.sendCorrectureOfStatement = function (statement_uid, corrected_text){
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_correcture_of_statement',
			type: 'POST',
			data: { uid: statement_uid, text: corrected_text},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxSendCorrectureOfStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data, statement_uid);
		}).fail(function ajaxSendCorrectureOfStatementFail() {
			$('#' + popupErrorDescriptionId).text('Unfortunately, the correcture could not be send (server offline or csrf check' +
				' failed. Sorry!');
		});
	};
}