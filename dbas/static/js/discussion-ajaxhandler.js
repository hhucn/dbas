/*global $, jQuery, alert */

function AjaxHandler () {
	'use strict';
	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 * @param posCallbackFct callback if done
	 * @param negCallbackFct callback if fail
	 */
	this.getAllPositions = function (posCallbackFct, negCallbackFct) {
		$.ajax({
			url: 'ajax_all_positions',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetAllPositionsDone (data) {
			posCallbackFct(data);
		}).fail(function ajaxGetAllPositionsFail () {
			alert('failed request');
			negCallbackFct();
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument has a connection to the
	 * position with given uid.
	 * @param ofPositionWithUid uid of clicked position
	 * @param getProArgument true, if the pro arguments should be fetched, false for the con
	 * @param noOfReturnArguments number of arguments, which should be returned, -1 for all
	 * @param posCallbackFct callback if done
	 * @param negCallbackFct callback if fail
	 */
	this.getArgsConnectedToPosUid = function (ofPositionWithUid, getProArgument, noOfReturnArguments, posCallbackFct, negCallbackFct) {
		var type = getProArgument ? 'pro' : 'con';
		var no = typeof noOfReturnArguments === 'undefined' || noOfReturnArguments < -1 ? -1 : Math.round(noOfReturnArguments);
		$.ajax({
			url: 'ajax_arguments_connected_to_position_uid',
			method: 'POST',
			data: { uid : ofPositionWithUid,
					returnCount : no,
					type: type },
			dataType: 'json',
			async: true
		}).done(function ajaxGetArgsConnectedToPosUidDone (data) {
			posCallbackFct(data);
		}).fail(function ajaxGetArgsConnectedToPosUidFail () {
			alert('failed request');
			negCallbackFct();
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument is for or against the
	 * the same position as the given argument uid.
	 * position with given uid
	 * @param ofArgumentWithUid uid of clicked position
	 * @param getProArgument true, if the pro arguments should be fetched, false for the con
	 * @param setAsDescr true, if the pro arguments set as description
	 * @param numberOfReturnArguments number of arguments, which should be returned, -1 for all
	 */
	this.getArgsForSamePosByArgUid = function (ofArgumentWithUid, getProArgument, setAsDescr, numberOfReturnArguments, userArg) {
		var type = getProArgument ? 'pro' : 'con';
		var no = typeof numberOfReturnArguments === 'undefined' || numberOfReturnArguments < -1 ? -1 : Math.round(numberOfReturnArguments);
		// todo: diese methode raus, sofern die anderen beiden stehen?
		$.ajax({
			url: 'ajax_arguments_against_same_positions_by_argument_uid',
			method: 'POST',
			data: { uid : ofArgumentWithUid,
					returnCount : no,
					type: type },
			dataType: 'json',
			async: true
		}).done(function ajaxGetArgsForSamePosByArgUidDone (data) {
			var guiHandler = new GuiHandler();
			if (setAsDescr) {
				$.each($.parseJSON(data), function ajaxGetArgsForSamePosByArgUidDoneEach (key, val) {
					var pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
					var text = argumentSentencesOpeners[pos] + '<b>' + userArg + '</b> But an argument from the other side is: <b>'
						+ val + '</b> What\'s your opinion?';
					guiHandler.setDiscussionsDescription(text);
				});
			} else {
				guiHandler.setJsonDataToContentAsArguments(data);
			}
		}).fail(function ajaxGetArgsForSamePosByArgUidFail () {
			alert('failed request');
			new GuiHandler().setNewArgumentButtonOnly();
		});
	};

	this.getNextArgumentForConfrontation = function (currentArgumentUid, currentArgumentText) {
		$.ajax({
			url: 'ajax_next_arg_for_confrontation',
			method: 'POST',
			data: { uid : currentArgumentUid },
			dataType: 'json',
			async: true
		}).done(function ajaxGetNextArgumentForConfrontation (data) {
			var obj = $.parseJSON(data);
			new GuiHandler().setDiscussionsDescriptionForConfrontation(currentArgumentText, obj['confrontation']);
		}).fail(function ajaxGetNextArgumentForConfrontation () {
			new GuiHandler().setDiscussionsDescriptionForConfrontation(currentArgumentText, 'nothing');
		});
	};

	this.getNextArgumentsForJustification = function (currentArgumentUid) {
		$.ajax({
			url: 'ajax_next_args_for_justification',
			method: 'POST',
			data: { uid : currentArgumentUid },
			dataType: 'json',
			async: true
		}).done(function ajaxGetNextArgumentForJustification (data) {
			new GuiHandler().setJsonDataToContentAsArguments(data);
		}).fail(function ajaxGetNextArgumentForJustification () {
			new GuiHandler().setNewArgumentButtonOnly();
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
		}).done(function ajaxGetAllUsersDone (data) {
			posCallbackFct(data);
		}).fail(function ajaxGetAllUsersFail () {
			alert(negCallbackText);
		});
	};
}