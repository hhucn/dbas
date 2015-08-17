/*global $, jQuery, alert, GuiHandler
*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

// TODO KICK ALL METHODS WHICH ARE NOT USED

function InteractionHandler() {
	'use strict';

	/**
	 * Handler when an start statement was clicked
	 * @param id of the button
	 */
	this.startStatementButtonWasClicked = function (id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		new AjaxHandler().getPremisseForStatement(id);
	};

	/**
	 * Handler when an start premisse was clicked
	 * @param id of the button
	 */
	this.startPremisseButtonWasClicked = function (id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		new AjaxHandler().getReplyForPremisseGroup(id);
	};

	/**
	 * Handler when an relation button was clicked
	 * @param id of the button
	 */
	this.startRelationButtonWasClicked = function (id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionsDescriptionId).empty();
		new AjaxHandler().handleReplyForResponseOfConfrontation(id);
	};

	/**
	 * Handler when an position button was clicked
	 * @param id of the button
	 */
	/*
	this.positionButtonWasClicked = function (id) {
		var ajaxHandler = new AjaxHandler();
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		ajaxHandler.getArgumentsForJustification(id);
	};
	*/

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 */
	this.radioButtonChanged = function () {
		var guiHandler = new GuiHandler(), text, isStart = $('#' + discussionSpaceId + ' ul li input').hasClass('start');
		if ($('#' + addReasonButtonId).is(':checked')) {
			$('#' + stepBackButtonId).hide();

			// get the second child, which is the label
			text = $('#' + addReasonButtonId).parent().children().eq(1).text();
			if (text.indexOf(newConclusionRadioButtonText) >= 0 || text.indexOf(firstConclusionRadioButtonText) >= 0) {
				// statement
				guiHandler.setDisplayStylesOfAddArgumentContainer(true, true, isStart, false);
			} else {
				// premisse
				guiHandler.setDisplayStylesOfAddArgumentContainer(true, false, isStart, true);
			}
		} else if ($('#' + goodPointTakeMeBackButtonId).is(':checked')) {
			$('#' + stepBackButtonId).show();
			guiHandler.setDisplayStylesOfAddArgumentContainer(false, true, isStart, false);
		} else {
			guiHandler.setDisplayStylesOfAddArgumentContainer(false, true, isStart, false);
			$('#' + stepBackButtonId).hide();

			this.radioButtonWasChoosen();
			guiHandler.setVisibilityOfDisplayStyleContainer(false, '');
			$('#' + islandViewContainerId).fadeOut('slow');
		}
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
	 * Fetches all premisses out of the textares and send them
	 */
	this.getPremissesAndSendThem = function (useIntro) {
		var i = 0, dict = {}, no, intro;
		$('#' + leftPositionTextareaId + ' div[id^="div-content-"]').children().each(function (){
		    if ($(this).prop("tagName").toLowerCase().indexOf('textarea') > -1 && $(this).val().length > 0) {
				// get current number and then the value of the dropdown
				no = $(this).prop('id').substr($(this).prop('id').length-1);
				intro = useIntro ? $('#left-dropdown-sentences-openers-' + no).text() : '';
				dict['pro_' + i] = intro + $(this).val();
				i = i + 1;
			}
		});
		i = 0;
		$('#' + rightPositionTextareaId + ' div[id^="div-content-"]').children().each(function (){
		    if ($(this).prop("tagName").toLowerCase().indexOf('textarea') > -1 && $(this).val().length > 0) {
				// get current number and then the value of the dropdown
				no = $(this).prop('id').substr($(this).prop('id').length-1);
				intro = useIntro ? $('#right-dropdown-sentences-openers-' + no).text() : '';
				dict['con_' + i] = intro + $(this).val();
				i = i + 1;
			}
		});
		new AjaxHandler().sendNewPremisses(dict);
	};

	/**
	 * Defines the action for the send button
	 */
	this.radioButtonWasChoosen = function () {
		var guiHandler = new GuiHandler(), radioButton, id, value;
		radioButton = $('input[name=' + radioButtonGroup + ']:checked');
		id = radioButton.attr('id');
		value = radioButton.val();
		if (typeof id === 'undefined' || typeof value === 'undefined') {
			guiHandler.setErrorDescription(selectStatement);
		} else {
			guiHandler.setErrorDescription('');
			guiHandler.setSuccessDescription('');
			if (radioButton.hasClass('start')) {
				this.startStatementButtonWasClicked(id, value);
			} else if (radioButton.hasClass('premisse')) {
				this.startPremisseButtonWasClicked(id, value);
			} else if (radioButton.hasClass('relation')) {
				this.startRelationButtonWasClicked(id, value);
			} else {
				alert('new class in InteractionHandler: radioButtonWasChoosen')
			}
		}

		// reset style box
		guiHandler.resetChangeDisplayStyleBox();
	};

	/**
	 * Callback for the ajax method getPremisseForStatement
	 * @param data returned json data
	 */
	this.callbackIfDoneForPremisseForStatement = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			gh.setJsonDataToContentAsStartPremisses(parsedData.premisses, parsedData.currentStatementText);
		} else {
			gh.setNewArgumentButtonOnly(addPremisseRadioButtonText, true);
		}
		gh.resetAndDisableEditButton();
	};

	/**
	 * Callback for the ajax method getPremisseForStatement
	 * @param data returned json data
	 */
	this.callbackIfDoneReplyForPremisse = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			gh.setJsonDataAsFirstConfrontation(parsedData);
		} else if (parsedData.status == '0') {
			alert('TODO: callbackIfDoneReplyForPremisse')
		} else {
			alert('error in callbackIfDoneReplyForPremisse');
		}
		gh.resetAndDisableEditButton();
	};

	/**
	 * Callback for the ajax method handleReplyForResponseOfConfrontation
	 * @param data
	 */
	this.callbackIfDoneHandleReplyForResponseOfConfrontation = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			gh.setJsonDataAsConfrontationReasoning(parsedData);
		} else if (parsedData.status == '0') {
			alert('ohh');
		} else {
			alert('error in callbackIfDoneHandleReplyForResponseOfConfrontation');
		}
		gh.resetAndDisableEditButton();
	};

	/**
	 * Callback for the ajax method getArgsForJustification
	 * @param data returned json data
	 */
	/*
	this.callbackIfDoneForArgsForJustification = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		gh.setDiscussionsDescription('Why do you think that: <b>' + parsedData.currentStatementText + '</b>');
		if (parsedData.status != '-1') {
			gh.setJsonDataToDiscussionContentAsArguments(parsedData.justification, true);
		} else {
			gh.setNewArgumentButtonOnly(addPremisseRadioButtonText, true);
		}
		gh.resetAndDisableEditButton();
	};
	*/

	/**
	 * Callback for the ajax method getGetNewArgumentationRound
	 * @param data returned json data
	 */
	/*
	this.callbackIfDoneForGetNewArgumentationRound = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		// -1 confrontation, but no justification
		//  0 no confrontation
		//  1 everything is fine
		switch(parsedData.status_con){
			case '-1':
				gh.setDiscussionsDescriptionForConfrontation(parsedData.currentStatementText, parsedData.confrontation);
				gh.setNewArgumentAndGoodPointButton(newPremisseRadioButtonText, true);
				break;
			case '0':
				gh.setDiscussionsDescriptionWithoutConfrontation(parsedData.currentStatementText);
				gh.setNewArgumentButtonOnly(newPremisseRadioButtonText, true);
				break;
			case '1':
				gh.setJsonDataToDiscussionContentAsArguments(parsedData.justifications, false, false);
				gh.setDiscussionsDescriptionForConfrontation(parsedData.currentStatementText, parsedData.confrontation);
				gh.setVisibilityOfDisplayStyleContainer(true, parsedData.currentStatementText);
				break;
		}

		//  0 no pro arguments
		//  1 everything is fine
		switch(parsedData.status_pro){
			case '0':
				gh.setDiscussionsAvoidanceDescription('');
				break;
			case '1':
				gh.setDiscussionsAvoidanceDescriptionForConfrontation(parsedData.currentStatementText);
				gh.setJsonDataToDiscussionContentAsArguments(parsedData.new_pros, false, true);
				break;
		}
		gh.resetAndDisableEditButton();
	};
	*/

	/**
	 * Callback for the ajax method getStartStatements
	 * @param data returned json data
	 */
	this.callbackIfDoneForGetStartStatements = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '-1') {
			gh.setDiscussionsDescription(firstPositionText);
			gh.resetAndDisableEditButton();
			gh.setNewArgumentButtonOnly(firstConclusionRadioButtonText, false);
		} else {
			gh.setJsonDataToContentAsStartStatement(parsedData.statements);
		}
	};

	/**
	 * Callback, when a new position was send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewStartStatement = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			alert('success -1 in callbackIfDoneForSendNewStartStatement');
		} else {
			new GuiHandler().setNewStatementAsLastChild(parsedData);
		}
	};

	/**
	 * Callback, when new premisses were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewPremisses = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			alert('success -1 in callbackIfDoneForSendNewPremisses');
		} else {
			new GuiHandler().setPremissesAsLastChild(parsedData);
		}
	};

	/**
	 * Callback, when a new arguments were send
	 * @param data returned data
	 */
	/*
	this.callbackIfDoneForSendNewArguments = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler;
		// -1 something went wrong
		//  1 everything is fine
		switch(parsedData.status){
			case '-1':
				gh.setErrorDescription(internalFailureWhileDeletingTrack);
				break;
			case '1':
				gh.setSuccessDescription(addedEverything);
				gh.addJsonDataToContentAsArguments(parsedData.arguments);
				gh.resetAddStatementContainer();
				break;
		}
	};
	*/

	/**
	 * Callback, when the user want to step back
	 * @param data returned data
	 */
	/*
	this.callbackGetOneStepBack = function (data) {
		var parsedData = $.parseJSON(data), ah = new AjaxHandler(), ih = new InteractionHandler();
		$('#' + discussionSpaceId).empty();
		// -1 user has no history/trace
		//  0 given data is for a positions callback
		//  1 given data is for an argument callback
		switch (parsedData.status){
			case '-1':
				ah.getStartStatements();
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
	*/

	/**
	 * Callback, when island data was fetched
	 * @param data of the ajax request
	 */
	/*
	this.callbackIfDoneForGetAllArgumentsForIslandView = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		// -1 no data
		// >0 island data
		switch(parsedData.status){
			case '-1':
				gh.setErrorDescription(noIslandView);
				gh.setVisibilityOfDisplayStyleContainer(false, '');
				$('#' + scStyle2Id).removeAttr('checked');
				break;
			default:
				gh.displayDataInIslandView(parsedData.arguments, true);
				break;
		}
	};
	*/

	/**
	 * Callback, when the logfile was fetched
	 * @param data of the ajax request
	 */
	this.callbackIfDoneForGetLogfileForStatement = function (data) {
		var parsedData = $.parseJSON(data);
		// status is the length of the content
		if (parsedData.status == '0'){
			$('#' + popupEditStatementLogfileSpaceId).text(noCorrections);
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
			$('#' + popupErrorDescriptionId).text(noCorrectionsSet);
		} else {
			new GuiHandler().updateOfStatementInDiscussion(parsedData);
			$('#' + popupErrorDescriptionId).text('');
			$('#' + popupSuccessDescriptionId).text(correctionsSet);
			$('#edit_statement_td_text_' + parsedData.uid).text(parsedData.text);
		}
	};
}