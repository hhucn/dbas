/*global $, jQuery */

function InteractionHandler () {
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
		var guiHandler = new GuiHandler(), pos;
		pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		guiHandler.setDiscussionsDescription(argumentSentencesOpeners[pos] + '<b>' + value + '</b> But why?');

		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		// add all positions
		ajaxHandler.getArgsConnectedToPosUid(id, true, -1, guiHandler.setJsonDataToContentAsArguments, guiHandler.setNewArgumentButtonOnly);
	};

	/**
	 * Handler when an position button was clicked
	 * @param value of the button
	 */
	this.positionButtonWasClicked = function (id, value) {
		//var pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		//guiHandler.setDiscussionsDescription(argumentSentencesOpeners[pos] + '<b>' + value + '</b> But an argument from the other side' +
		//	' is:');

		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		// add all positions from the other side
		ajaxHandler.getArgsForSamePosByArgUid(id, false, true, 1, value);
		ajaxHandler.getArgsConnectedToPosUid(id, true, -1, guiHandler.setJsonDataToContentAsArguments, guiHandler.setNewArgumentButtonOnly);
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
	 * Callback for the ajax method getAllPositions
	 * @param data returned json data
	 */
	this.callbackAjaxGetAllPositions = function (data) {
		if (typeof data === 'undefined') {
			guiHandler.setNewArgumentButtonOnly();
		} else {
			guiHandler.setJsonDataToContentAsPositions(data);
		}
	};
}