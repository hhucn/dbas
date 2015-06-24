/*global $, jQuery, alert, GuiHandler, InteractionHandler */

function AjaxHandler() {
	'use strict';

	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 */
	this.getAllPositions = function () {
		$.ajax({
			url: 'ajax_all_positions',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetAllPositionsDone(data) {
			new InteractionHandler().callbackIfDoneForGetAllPositions(data);
		}).fail(function ajaxGetAllPositionsFail() {
			new GuiHandler().setErrorDescription('Internal Error :(');
			new GuiHandler().showDiscussionError('Internal failure in ajaxGetAllPositionsFail',
				'', false, 'getArgumentsForJustification', true);
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument has a connection to the
	 * position with given uid.
	 * @param pos_uid uid of clicked position
	 */
	this.getArgumentsForJustification = function (pos_uid) {
		$.ajax({
			url: 'ajax_arguments_connected_to_position_uid',
			method: 'POST',
			data: { uid : pos_uid},
			dataType: 'json',
			async: true
		}).done(function ajaxGetArgumentsForJustificationDone(data) {
			new InteractionHandler().callbackIfDoneForArgsForJustification(data);
		}).fail(function ajaxGetArgumentsForJustificationFail() {
			new GuiHandler().setErrorDescription('Internal Error :(');
			new GuiHandler().showDiscussionError('Internal failure in ajaxGetArgumentsForJustificationFail',
				pos_uid, false, 'getArgumentsForJustification', true);
		});
	};

	/**
	 * Requests data for a new argumentation round. This includes a statement, an confrontation and justifications
	 * @param currentStatementId uid of the current statement
	 */
	this.getNewArgumentationRound = function (currentStatementId) {
		$.ajax({
			url: 'ajax_args_for_new_discussion_round',
			method: 'POST',
			data: { uid: currentStatementId},
			dataType: 'json',
			async: true
		}).done(function ajaxGetNewArgumentationRoundDone(data) {
			new InteractionHandler().callbackIfDoneForGetNewArgumentationRound(data);
		}).fail(function ajaxGetNewArgumentationRoundFail() {
			alert("debug");
			new GuiHandler().showDiscussionError('Internal failure in ajaxGetNewArgumentationRound',
				currentStatementId, is_argument, 'getNewArgumentationRound');
		});
	};

	/**
	 * Request all users
	 */
	this.getAllUsersAndSetInGui = function () {
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetAllUsersDone(data) {
			new GuiHandler().setJsonDataToAdminContent($.parseJSON(data));
		}).fail(function ajaxGetAllUsersFail() {
			alert('internal failure while requesting all users');
		});
	};

	/**
	 * Request data for getting one step back
	 */
	this.getOneStepBack = function () {
		$.ajax({
			url: 'ajax_one_step_back',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetOneStepBackDone(data) {
			$('#' + stepBackButtonId).hide();
			$('#' + sendAnswerButtonId).show();
			new InteractionHandler().callbackGetOneStepBack(data);
		}).fail(function ajaxGetOneStepBackFail() {
			$('#' + stepBackButtonId).hide();
			$('#' + sendAnswerButtonId).show();
			new GuiHandler().setErrorDescription('Internal Error :(');
			new GuiHandler().showDiscussionError('Internal failure in ajaxGetAllPositionsFail',
				'', false, 'ajaxGetOneStepBackFail', true);
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param argument_dictionary for inserting
	 */
	this.sendNewArgument = function (argument_dictionary) {
		$.ajax({
			url: 'ajax_send_new_arguments',
			type: 'GET',
			data: argument_dictionary,
			dataType: 'json',
			async: true
		}).done(function ajaxSendNewArgumentDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewArguments(data);
		}).fail(function ajaxSendNewArgumentFail() {
			new GuiHandler().setErrorDescription('New arguments could not be sent. Sorry!')
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param position for sending
	 */
	this.sendNewPosition = function (position) {
		$.ajax({
			url: 'ajax_send_new_position',
			type: 'GET',
			data: { position : position},
			dataType: 'json',
			async: true
		}).done(function ajaxSendNewPositionDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewPosition(data);
		}).fail(function ajaxSendNewPositionFail() {
			new GuiHandler().setErrorDescription('New idea could not be sent. Sorry!')
		});
	};

	/**
	 * Request for all arguments, which have a relation to the last saved one
	 */
	this.getAllArgumentsForIslandView = function () {
		$.ajax({
			url: 'ajax_all_arguments_for_island',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetAllArgumentsForIslandViewDone(data) {
			new InteractionHandler().callbackIfDoneForGetAllArgumentsForIslandView(data);
		}).fail(function ajaxGetAllArgumentsForIslandViewFail() {
			new GuiHandler().setErrorDescription('Island view could not be displayed. Sorry!');
			new GuiHandler().setVisibilityOfDisplayStyleContainer(false, '');
		});
	};

	/***
	 * Requests the logfile for the given uid
	 * @param statement_uid current uid of the statement
	 * @param is_argument true, if it is an argument
	 */
	this.getLogfileForStatement = function (statement_uid, is_argument){
		$.ajax({
			url: 'ajax_get_logfile_for_statement',
			type: 'GET',
			data: { uid: statement_uid, is_argument: is_argument },
			dataType: 'json',
			async: true
		}).done(function ajaxGetLogfileForStatementDone(data) {
			new InteractionHandler().callbackIfDoneForGetLogfileForStatement(data);
		}).fail(function ajaxGetLogfileForStatementFail() {
			$('#' + popupErrorDescriptionId).text('Unfortunately, the log file could not be requested. Sorry!');
		});
	};

	/**
	 * Sends a correcture of a statement
	 * @param statement_uid current uid of the statement
	 * @param is_argument true, if it is an argument
	 * @param corrected_text the corrected text
	 */
	this.sendCorrectureOfStatement = function (statement_uid, is_argument, corrected_text){
		$.ajax({
			url: 'ajax_send_correcture_of_statement',
			type: 'GET',
			data: { uid: statement_uid, is_argument: is_argument, text: corrected_text},
			dataType: 'json',
			async: true
		}).done(function ajaxSendCorrectureOfStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data);
		}).fail(function ajaxSendCorrectureOfStatementFail() {
			new GuiHandler().setErrorDescription('Island view could not be displayed. Sorry!');
			$('#' + popupErrorDescriptionId).text('Unfortunately, the correcture could not be send.');
		});
	};

}