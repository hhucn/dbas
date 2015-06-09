/*global $, jQuery, alert, GuiHandler, firstOneText , addStatementButtonId , argumentList , adminsSpaceId , addStatementButtonId , statementList, argumentSentencesOpeners, addStatementContainerId, addStatementButtonId, discussionFailureRowId, discussionFailureMsgId, tryAgainDiscussionButtonId, discussionsDescriptionId, errorDescriptionId, radioButtonGroup, discussionSpaceId, sendAnswerButtonId, addStatementContainerH2Id, AjaxHandler
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
	 * @param value of the button
	 */
	this.argumentButtonWasClicked = function (id, value) {
		var guiHandler = new GuiHandler(), ajaxHandler = new AjaxHandler(), pos;
		pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		guiHandler.setDiscussionsDescription(argumentSentencesOpeners[pos] + '<b>' + value + '</b> But why?');

		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		ajaxHandler.getNewArgumentationRound(id, true);
	};

	/**
	 * Handler when an position button was clicked
	 * @param value of the button
	 */
	this.positionButtonWasClicked = function (id, value) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		ajaxHandler.getArgumentsForJustification(id);
	};

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 */
	this.radioButtonChanged = function (buttonId) {
		var guiHandler = new GuiHandler();
		if ($('#' + addStatementButtonId).is(':checked')) {
			guiHandler.setDisplayStylesOfAddArgumentContainer(true);
			$('#' + sendAnswerButtonId).hide();

			// get the second child, which is the label
			if ($('#' + addStatementButtonId).parent().children().eq(1).text().indexOf('position') >= 0) {
				$('#' + addStatementContainerH2Id).text('Please insert a new position');
				//$('#' + addStatementContainerMainInputId).show();
			} else {
				$('#' + addStatementContainerH2Id).text('Please insert new arguments');
				//$('#' + addStatementContainerMainInputId).hide();
			}
		} else {
			guiHandler.setDisplayStylesOfAddArgumentContainer(false);
			$('#' + sendAnswerButtonId).show();
		}

		// enable or disable the send button
		$('#' + sendAnswerButtonId).prop('disabled', ($('input[name=' + radioButtonGroup + ']:checked') === 'undefined' ? true : false));
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
		if (data.length > 0) {
			var parsedData = $.parseJSON(data);
			new GuiHandler().setJsonDataToContentAsArguments(parsedData);
		} else {
			new GuiHandler().setNewArgumentButtonOnly();
		}
	};


	/**
	 * Callback for the ajax method getGetNewArgumentationRound
	 * @param data returned json data
	 */
	this.callbackIfDoneForGetNewArgumentationRound = function (data) {
		var parsedData = $.parseJSON(data);
		// justification
		new GuiHandler().setJsonDataToContentAsArguments(parsedData.justifications);
		// confrontation
		new GuiHandler().setDiscussionsDescriptionForConfrontation(parsedData.currentStatementText, parsedData.confrontation);
	};

	/**
	 * Callback for the ajax method getAllPositions
	 * @param data returned json data
	 */
	this.callbackAjaxGetAllPositions = function (data) {
		if (typeof data === 'undefined') {
			new GuiHandler().setNewArgumentButtonOnly();
		} else {
			new GuiHandler().setJsonDataToContentAsPositions(data);
		}
	};
}