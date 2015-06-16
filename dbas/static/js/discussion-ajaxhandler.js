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
			new InteractionHandler().callbackAjaxGetAllPositions(data);
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
	 *
	 * @param currentStatementId
	 * @param is_argument
	 */
	this.getNewArgumentationRound = function (currentStatementId, is_argument) {
		is_argument = is_argument ? 'argument' : 'position';
		$.ajax({
			url: 'ajax_args_for_new_discussion_round',
			method: 'POST',
			data: { is_argument : is_argument, uid : currentStatementId},
			dataType: 'json',
			async: true
		}).done(function ajaxGetNewArgumentationRoundDone(data) {
			new InteractionHandler().callbackIfDoneForGetNewArgumentationRound(data);
		}).fail(function ajaxGetNewArgumentationRoundFail() {
			alert("debug");
			new GuiHandler().showDiscussionError('Internal failure in ajaxGetNewArgumentationRound',
				currentStatementId, is_argument, 'getNewArgumentationRound', false);
		});
	};

	/**
	 * Request all users
	 * @param posCallbackFct callback if done
	 * @param negCallbackText for an alert if fail
	 */
	this.getAllUsersAndSetInGui = function (posCallbackFct, negCallbackText) {
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetAllUsersDone(data) {
			posCallbackFct(data);
		}).fail(function ajaxGetAllUsersFail() {
			alert(negCallbackText);
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
			new InteractionHandler().callbackGetOneStepBack(data);
		}).fail(function ajaxGetOneStepBackFail() {
			new GuiHandler().setErrorDescription('Internal Error :(');
			new GuiHandler().showDiscussionError('Internal failure in ajaxGetAllPositionsFail',
				'', false, 'ajaxGetOneStepBackFail', true);
		});
	};

	this.sendNewArgument = function () {
		alert('todo: sendNewArgument');
	};

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
}