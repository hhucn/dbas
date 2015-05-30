/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

function AjaxHandler() {
	'use strict';
	var guiHandler = new GuiHandler();
	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 * If done: call setJsonDataToContentAsPositions
	 * If fail: call setNewArgumentButtonOnly
	 */
	this.getAllPositionsAndSetInGui = function () {
		$.ajax({
			url: 'ajax_all_positions',
			type: 'GET',
			dataType: 'json'
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsPositions(data);
		}).fail(function () {
			alert('failed request');
			guiHandler.setNewArgumentButtonOnly();
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument has a connection to the
	 * position with given uid.
	 * @param ofPositionWithUid uid of clicked position
	 * @param shouldGetProArgument true, if the pro arguments should be fetched, false for the con
	 * @param numberOfReturnArguments number of arguments, which should be returned, -1 for all
	 */
	this.getArgumentsConnectedToPositionUidAndSetInGui = function (ofPositionWithUid, shouldGetProArgument, numberOfReturnArguments) {
		var type = shouldGetProArgument ? 'pro' : 'con';
		var no = typeof numberOfReturnArguments === 'undefined' || numberOfReturnArguments < -1 ? -1 : Math.round(numberOfReturnArguments);
		$.ajax({
			url: 'ajax_arguments_connected_to_position_uid',
			method: 'POST',
			data: { uid : ofPositionWithUid, returnCount : no, type: type },
			dataType: 'json'
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsArguments(data);
		}).fail(function () {
			alert('failed request');
			guiHandler.setNewArgumentButtonOnly();
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
			dataType: 'json'
		}).done(function (data) {
			if (setAsDescr){
				if (no != 1){
					alert('error with args in getArgumentsForTheSamePositionByArgUidAndSetInGui')
				} else {
					$.each(data, function (key, val) {
						var pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
						var text = argumentSentencesOpeners[pos] + '<b>' + userArg + '</b> But an argument from the other side is: <b>'
							+ val + '</b> What\'s your opiniion?';
						guiHandler.setDiscussionsDescription(text);
					});
				}
			} else {
				guiHandler.setJsonDataToContentAsArguments(data);
			}
		}).fail(function () {
			alert('failed request');
			guiHandler.setNewArgumentButtonOnly();
		});
	};

	/**
	 * Request all users
	 */
	this.getAllUsersAndSetInGui = function () {
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json'
		}).done(function (data) {
			guiHandler.setJsonDataToAdminContent(data);
		}).fail(function () {
			alert('internal failure');
		});
	};
}
