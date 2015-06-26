/*global $, jQuery, alert, GuiHandler, firstOneText , addStatementButtonId , argumentList , adminsSpaceId , addStatementButtonId , statementList, argumentSentencesOpeners, addStatementButtonId, discussionFailureRowId, discussionFailureMsgId, tryAgainDiscussionButtonId, discussionsDescriptionId, errorDescriptionId, radioButtonGroup, discussionSpaceId, sendAnswerButtonId, addStatementContainerH2Id, AjaxHandler
*/

function InteractionHandler() {
	'use strict';
	var guiHandler, ajaxHandler;

	this.setHandler = function (externGuiHandler, externAjaxHandler) {
		guiHandler = externGuiHandler;
		ajaxHandler = externAjaxHandler;
	};
	/**
	 * Handler when an argument button was clicked
	 * @param id of the button
	 */
	this.argumentButtonWasClicked = function (id) {
		var ajaxHandler = new AjaxHandler();
		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		ajaxHandler.getNewArgumentationRound(id);
	};

	/**
	 * Handler when an position button was clicked
	 * @param id of the button
	 * @param value of the button
	 */
	this.positionButtonWasClicked = function (id, value) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		ajaxHandler.getArgumentsForJustification(id);
	};

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 * @param buttonId current id
	 */
	this.radioButtonChanged = function (buttonId) {
		var guiHandler = new GuiHandler();
		if ($('#' + addStatementButtonId).is(':checked')) {
			$('#' + stepBackButtonId).hide();
			$('#' + sendAnswerButtonId).hide();

			// get the second child, which is the label
			if ($('#' + addStatementButtonId).parent().children().eq(1).text().indexOf(newPositionRadioButtonText) >= 0) {
				// no argument -> position
				guiHandler.setDisplayStylesOfAddArgumentContainer(true, false);
			} else {
				// argument
				guiHandler.setDisplayStylesOfAddArgumentContainer(true, true);
			}
		} else if ($('#' + goodPointTakeMeBackButtonId).is(':checked')) {
			$('#' + stepBackButtonId).show();
			$('#' + sendAnswerButtonId).hide();
		} else {
			guiHandler.setDisplayStylesOfAddArgumentContainer(false, true);
			$('#' + sendAnswerButtonId).show();
			$('#' + stepBackButtonId).hide();
		}

		// enable or disable the send button
		$('#' + sendAnswerButtonId).prop('disabled', ($('input[name=' + radioButtonGroup + ']:checked') === 'undefined' ? true : false));
	};

	/**
	 * Segmented button for display style was pressed
	 * @param buttonId current id
	 */
	this.styleButtonChanged = function (buttonId) {
		var guiHandler = new GuiHandler();
		switch (buttonId){
			case scStyle1Id:
				guiHandler.setDisplayStyleAsDiscussion();
				break;
			case scStyle2Id:
				guiHandler.setDisplayStyleAsProContraList();
				break;
			case scStyle3Id:
				guiHandler.setDisplayStyleAsFullView();
				break;
			default: alert ('unknown id: ' + buttonId);
		}
	};

	/**
	 * Fetches all arguments out of the textares and send them
	 */
	this.getArgumentsAndSendThem = function () {
		var i = 0, dict = {};
		$('#' + leftPositionTextareaId + ' > div').children().each(function (){
		    if ($(this).prop("tagName").toLowerCase().indexOf('textarea') > -1 && $(this).val().length > 0) {
				dict['pro_' + i] = $(this).val();
				i = i + 1;
			}
		});
		i = 0;
		$('#' + rightPositionTextareaId + ' > div').children().each(function (){
		    if ($(this).prop("tagName").toLowerCase().indexOf('textarea') > -1 && $(this).val().length > 0) {
				dict['con_' + i] = $(this).val();
				i = i + 1;
			}
		});
		new AjaxHandler().sendNewArgument(dict);
	};

	/**
	 * Defines the action for the send button
	 */
	this.sendAnswerButtonClicked = function () {
		var guiHandler = new GuiHandler(), radioButton, id, value;
		radioButton = $('input[name=' + radioButtonGroup + ']:checked');
		id = radioButton.attr('id');
		value = radioButton.val();
		if (typeof id === 'undefined' || typeof value === 'undefined') {
			guiHandler.setErrorDescription('Please select a statement!');
		} else {
			guiHandler.setErrorDescription('');
			guiHandler.setSuccessDescription('');
			if (radioButton.hasClass('argument')) {
				this.argumentButtonWasClicked(id, value);
			} else {
				this.positionButtonWasClicked(id, value);
			}
		}
	};

	/**
	 * Callback for the ajax method getArgsForJustification
	 * @param data returned json data
	 */
	this.callbackIfDoneForArgsForJustification = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status != '-1') {
			gh.setDiscussionsDescription('Why do you think that: <b>' + parsedData.currentStatementText + '</b>');
			gh.setJsonDataToContentAsArguments(parsedData.justification, true);
		} else {
			gh.setNewArgumentButtonOnly();
		}
		gh.resetEnAndDisableOfEditButton();
	};

	/**
	 * Callback for the ajax method getGetNewArgumentationRound
	 * @param data returned json data
	 */
	this.callbackIfDoneForGetNewArgumentationRound = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		// -1 confrontation, but no justification
		//  0 no confrontation
		//  1 everything is fine
		switch(parsedData.status){
			case '-1':
				gh.setDiscussionsDescriptionForConfrontation(parsedData.currentStatementText, parsedData.confrontation);
				gh.setNewArgumentAndGoodPointButton(newArgumentRadioButtonText, true, 'radio');
				break;
			case '0':
				gh.setDiscussionsDescriptionWithoutConfrontation(parsedData.currentStatementText);
				gh.setNewArgumentButtonOnly(newArgumentRadioButtonText, true, 'radio');
				break;
			case '1':
				gh.setJsonDataToContentAsArguments(parsedData.justifications, false);
				gh.setDiscussionsDescriptionForConfrontation(parsedData.currentStatementText, parsedData.confrontation);
				gh.setVisibilityOfDisplayStyleContainer(true, parsedData.currentStatementText);
				break;
		}
		gh.resetEnAndDisableOfEditButton();
	};

	/**
	 * Callback for the ajax method getAllPositions
	 * @param data returned json data
	 */
	this.callbackIfDoneForGetAllPositions = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			new GuiHandler().setNewArgumentButtonOnly();
		} else {
			new GuiHandler().setJsonDataToContentAsPositions(parsedData.positions);
		}
	};

	/**
	 * Callback, when a new position was send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewPosition = function (data) {
		var parsedData = $.parseJSON(data);
		new GuiHandler().setNewPositionAsLastChild(parsedData);
	};

	/**
	 * Callback, when a new arguments were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewArguments = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler;
		// -1 something went wrong
		//  1 everything is fine
		switch(parsedData.status){
			case '-1':
				gh.setErrorDescription('Internal failure, please try again or did you have deleted your track recently?');
				break;
			case '1':
				gh.setSuccessDescription('Everything was added.');
				gh.addJsonDataToContentAsArguments(parsedData.arguments);
				gh.resetAddStatementContainer();
				break;
		}
	};

	/**
	 * Callback, when the user want to step back
	 * @param data returned data
	 */
	this.callbackGetOneStepBack = function (data) {
		var parsedData = $.parseJSON(data), ah = new AjaxHandler(), ih = new InteractionHandler();
		$('#' + discussionSpaceId).empty();
		// -1 user has no history/trace
		//  0 given data is for a positions callback
		//  1 given data is for an argument callback
		switch (parsedData.status){
			case '-1':
				ah.getAllPositions();
				break;
			case '0':
				new GuiHandler().setDiscussionsDescription('Why do you think that: <b>' + parsedData.currentStatementText + '</b>');
				ih.callbackIfDoneForArgsForJustification(data);
				break;
			case '1':
				ih.callbackIfDoneForGetNewArgumentationRound(data);
				break;
		}
	};

	/**
	 * Callback, when island data was fetched
	 * @param data of the ajax request
	 */
	this.callbackIfDoneForGetAllArgumentsForIslandView = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		// -1 no data
		// >0 island data
		switch(parsedData.status){
			case '-1':
				gh.setErrorDescription('Could not fetch data for the sialnd view. Sorry!');
				gh.setVisibilityOfDisplayStyleContainer(false, '');
				$('#' + scStyle2Id).removeAttr('checked');
				break;
			default:
				gh.displayDataInIslandView(parsedData.arguments, true);
				break;
		}
	};

	/**
	 * Callback, when the logfile was fetched
	 * @param data of the ajax request
	 */
	this.callbackIfDoneForGetLogfileForStatement = function (data) {
		var parsedData = $.parseJSON(data);
		// status is the length of the content
		if (parsedData.status == '0'){
			$('#' + popupEditStatementLogfileSpaceId).text('No corrections for the given statement.');
		} else {
			$('#' + popupEditStatementLogfileSpaceId).text('');
			new GuiHandler().displayStatementCorrectionsInPopup(parsedData.content);
		}
	};

	/**
	 * Callback, when a correcture could be send
	 * @param data of the ajax request
	 */
	this.callbackIfDoneForSendCorrectureOfStatement = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1'){
			$('#' + popupErrorDescriptionId).text('Correction could not be set, because your user was not fount in the database. Are you' +
				' currently logged in?');
		} else {
			new GuiHandler().updateOfStatementInDiscussion(parsedData);
			$('#' + popupErrorDescriptionId).text('');
			$('#' + popupSuccessDescriptionId).text('Your correction was set.');
		}
	};


}