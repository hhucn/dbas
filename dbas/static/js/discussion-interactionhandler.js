/*global $, jQuery, alert, GuiHandler
*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

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
				guiHandler.setDisplayStylesOfAddStatementContainer(true, true, isStart, false);
			} else {
				// premisse
				guiHandler.setDisplayStylesOfAddStatementContainer(true, false, isStart, true);
			}
		} else if ($('#' + goodPointTakeMeBackButtonId).is(':checked')) {
			$('#' + stepBackButtonId).show();
			guiHandler.setDisplayStylesOfAddStatementContainer(false, true, isStart, false);
		} else {
			guiHandler.setDisplayStylesOfAddStatementContainer(false, true, isStart, false);
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
	this.callbackIfDoneReplyForPremissegroup = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			gh.setJsonDataAsConfrontation(parsedData);
		} else if (parsedData.status == '0') {
			alert('TODO: callbackIfDoneReplyForPremissegroup')
		} else {
			alert('error in callbackIfDoneReplyForPremissegroup');
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