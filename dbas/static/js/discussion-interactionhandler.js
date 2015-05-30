/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */


function InteractionHandler() {
	'use strict';
	var guiHandler = new GuiHandler(), ajaxHandler = new AjaxHandler();
	/**
	 * Handler when an argument button was clicked
	 * @param value of the button
	 */
	this.argumentButtonWasClicked = function (id, value) {
		var pos, data;
		pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		guiHandler.setDiscussionsDescription(argumentSentencesOpeners[pos] + '<b>' + value + '</b> But why?');

		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		// add all positions
		ajaxHandler.getArgumentsConnectedToPositionUidAndSetInGui(id, true);

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
		ajaxHandler.getArgumentsForTheSamePositionByArgUidAndSetInGui(id, false, true, 1, value);
		ajaxHandler.getArgumentsConnectedToPositionUidAndSetInGui(id, true);
	};

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 */
	this.radioButtonChanged = function (buttonId) {
		if ($('#' + addStatementButtonId).is(':checked')) {
			guiHandler.displayStyleOfAddArgumentContiner(true);
			$('#' + sendAnswerButtonId).hide();

			// get the second child, which is the label
			if ($('#' + addStatementButtonId).parent().children().eq(1).text().indexOf('position') >= 0) {
				$('#' + addStatementContainerH2Id).text('Please insert a new position');
				$('#' + addStatementContainerMainInputId).show();
			} else {
				$('#' + addStatementContainerH2Id).text('Please insert new arguments');
				$('#' + addStatementContainerMainInputId).hide();
			}
		} else {
			guiHandler.displayStyleOfAddArgumentContiner(false);
			$('#' + sendAnswerButtonId).show();
		}

		// enable or disable the send button
		$('#' + sendAnswerButtonId).prop('disabled', ($('input[name=' + radioButtonGroup + ']:checked') === 'undefined' ? true : false));
	};

	/**
	 * Defines the action for the send button
	 */
	this.sendAnswerButtonClicked = function () {
		var radioButton, id, value;
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
}
