/*global $, jQuery, alert */

function AjaxHandler () {
	'use strict';
	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 * @param posCallbackFunction callback if done
	 * @param negCallbackFunction callback if fail
	 */
	this.getAllPositions = function (posCallbackFunction, negCallbackFunction) {
		$.ajax({
			url: 'ajax_all_positions',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetAllPositionsDone (data) {
			posCallbackFunction(data);
		}).fail(function ajaxGetAllPositionsFail () {
			alert('failed request');
			negCallbackFunction();
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument has a connection to the
	 * position with given uid.
	 * @param ofPositionWithUid uid of clicked position
	 * @param shouldGetProArgument true, if the pro arguments should be fetched, false for the con
	 * @param numberOfReturnArguments number of arguments, which should be returned, -1 for all
	 * @param posCallbackFunction callback if done
	 * @param negCallbackFunction callback if fail
	 */
	this.getArgumentsConnectedToPositionUid = function (ofPositionWithUid, shouldGetProArgument, numberOfReturnArguments, posCallbackFunction, negCallbackFunction) {
		var type = shouldGetProArgument ? 'pro' : 'con';
		var no = typeof numberOfReturnArguments === 'undefined' || numberOfReturnArguments < -1 ? -1 : Math.round(numberOfReturnArguments);
		$.ajax({
			url: 'ajax_arguments_connected_to_position_uid',
			method: 'POST',
			data: { uid : ofPositionWithUid, returnCount : no, type: type },
			dataType: 'json',
			async: true
		}).done(function ajaxGetArgumentsConnectedToPositionUidDone (data) {
			posCallbackFunction(data);
		}).fail(function ajaxGetArgumentsConnectedToPositionUidFail () {
			alert('failed request');
			negCallbackFunction();
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument is for or against the
	 * the same position as the given argument uid.
	 * position with given uid
	 * @param ofPositionWithUid uid of clicked position
	 * @param shouldGetProArgument true, if the pro arguments should be fetched, false for the con
	 * @param setAsDescr true, if the pro arguments set as description
	 * @param numberOfReturnArguments number of arguments, which should be returned, -1 for all
	 */
	this.getArgumentsForTheSamePositionByArgUidAndSetInGui = function (ofArgumentWithUid, shouldGetProArgument, setAsDescr, numberOfReturnArguments, userArg) {
		var type = shouldGetProArgument ? 'pro' : 'con';
		var no = typeof numberOfReturnArguments === 'undefined' || numberOfReturnArguments < -1 ? -1 : Math.round(numberOfReturnArguments);
		$.ajax({
			url: 'ajax_arguments_against_same_positions_by_argument_uid',
			method: 'POST',
			data: { uid : ofArgumentWithUid, returnCount : no, type: type },
			dataType: 'json',
			async: true
		}).done(function ajaxGetArgumentsForTheSamePositionByArgUidAndSetInGuiDone (data) {
			var guiHandler = new GuiHandler();
			if (setAsDescr) {
				$.each($.parseJSON(data), function (key, val) {
					var pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
					var text = argumentSentencesOpeners[pos] + '<b>' + userArg + '</b> But an argument from the other side is: <b>'
						+ val + '</b> What\'s your opiniion?';
					guiHandler.setDiscussionsDescription(text);
				});
			} else {
				guiHandler.setJsonDataToContentAsArguments(data);
			}
		}).fail(function ajaxGetArgumentsForTheSamePositionByArgUidAndSetInGuiFail () {
			alert('failed request');
			var guiHandler = new GuiHandler();
			guiHandler.setNewArgumentButtonOnly();
		});
	};

	/**
	 * Request all users
	 * @param posCallbackFunction callback if done
	 * @param negCallbackText for an alert if fail
	 */
	this.getAllUsersAndSetInGui = function (posCallbackFunction, negCallbackText) {
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function ajaxGetAllUsersDone (data) {
			posCallbackFunction(data);
		}).fail(function ajaxGetAllUsersFail () {
			alert(negCallbackText);
		});
	};
};