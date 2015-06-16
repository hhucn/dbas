/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

var addStatementButtonId = 'add-statement';
var addPositionButtonId = 'add-position';
var addStatementContainerId = 'add-statement-container';
var addStatementContainerH2Id = 'add-statement-container-h2';
var addStatementContainerMainInputId = 'add-statement-container-main-input';
var addProTextareaId = 'add-pro-textarea';
var addConTextareaId = 'add-con-textarea';
var adminsSpaceId = 'admins-space';
var argumentList = 'argument-list';
var closeStatementContainerId = 'closeStatementContainer';
var discussionsDescriptionId = 'discussions-description';
var discussionContainerId = 'discussion-container';
var discussionSpaceId = 'discussions-space';
var discussionFailureRowId = 'discussion-failure-row';
var discussionFailureMsgId = 'discussion-failure-msg';
var errorDescriptionId = 'error-description';
var leftPositionColumnId = 'left-position-column';
var leftPositionTextareaId = 'left-textareas';
var listAllUsersButtonId = 'list-all-users';
var insertStatementForm = 'insert_statement_form';
var restartDiscussionButtonId = 'restart-discussion';
var rightPositionColumnId = 'right-position-column';
var rightPositionTextareaId = 'right-textareas';
var radioButtonGroup = 'radioButtonGroup';
var scStyleGroupId = 'sc-display-style';
var newArgumentRadioButtonText = 'Let me state my own reason!';
var newPositionRadioButtonText = 'Neither of the above, I have a different idea!';
var scStyle1Id = 'sc-style-1';
var scStyle2Id = 'sc-style-2';
var scStyle3Id = 'sc-style-3';
var startDiscussionButtonId = 'start-discussion';
var startDescriptionId = 'start-description';
var statementContainerH2TextIfArgument = 'What are your arguments for and against?';
var statementContainerH2TextIfPosition = 'What is your idea?';
var sendAnswerButtonId = 'send-answer';
var sendNewStatementId = 'send-new-statement';
var statementListId = 'statement-list';
var tryAgainDiscussionButtonId = 'try-again-discussion';

var argumentSentencesOpeners = [
	'Okay, you have got the opinion: ',
	'Interesting, your opinion is: ',
	'So you meant: ',
	'You have said, that: ',
	'So your opinion is: '];
var startDiscussionText = 'How should we decide?';
var firstOneText = 'You are the first one, who said: ';


/**
 * main function
 */
$(function () {
	'use strict';
	var guiHandler = new GuiHandler(), ajaxHandler = new AjaxHandler(), interactionHandler = new InteractionHandler();

	guiHandler.setHandler(interactionHandler);
	interactionHandler.setHandler(guiHandler, ajaxHandler);

	$('#' + discussionContainerId).hide(); // hiding discussions container
	$('#' + addStatementContainerId).hide(); // hiding container for adding arguments
	$('#' + discussionFailureRowId).hide(); // hiding error message at start
	$('#' + tryAgainDiscussionButtonId).hide();

	// starts the discussion with getting all positions
	$('#' + startDiscussionButtonId).click(function () {
		$('#' + startDiscussionButtonId).hide(); // hides the start button
		$('#' + startDescriptionId).hide(); // hides the start description
		$('#' + restartDiscussionButtonId).show(); // show the restart button
		$('#' + discussionContainerId).fadeIn('fast'); // hiding retry button

		ajaxHandler.getAllPositions(interactionHandler.callbackAjaxGetAllPositions);
	});

	// handler for the send answer button
	$('#' + sendAnswerButtonId).click(function () {
		interactionHandler.sendAnswerButtonClicked();
	});

	// hide the restart button and add click function
		$('#' + restartDiscussionButtonId).hide(); // hides the restart button
		$('#' + restartDiscussionButtonId).click(function () {
		$('#' + startDiscussionButtonId).show(); // show the start description
		$('#' + restartDiscussionButtonId).hide(); // hide the restart button
		$('#' + addStatementContainerId).hide(); // hide add statement container
		$('#' + tryAgainDiscussionButtonId).hide(); // hiding retry button

		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionContainerId).hide();
	});

	// admin list all users button
	$('#' + listAllUsersButtonId).click(function () {
		if ($(this).val() === 'List all users') {
			ajaxHandler.getAllUsersAndSetInGui(guiHandler.setJsonDataToAdminContent, 'internal failure while requesting all users');
			$(this).val('Hide all users'); // will be done in the ajaxhandler
		} else {
			$('#' + adminsSpaceId).empty();
			$(this).val('List all users'); // will be done in the ajaxhandler
		}
	});

	// adding a textarea in the right column
	$('#' + addConTextareaId).click(function () {
		guiHandler.addTextareaAsChildInParent(rightPositionTextareaId);
	});

	// adding a textarea in the left column
	$('#' + addProTextareaId).click(function () {
		guiHandler.addTextareaAsChildInParent(leftPositionTextareaId);
	});

	// hiding the argument container, when the X button is clicked
	$('#' + closeStatementContainerId).click(function () {
		$('#' + addStatementContainerId).hide();
		$('#' + addStatementButtonId).enable = true;
		$('#' + addStatementButtonId).removeAttr('checked');
		$('#' + sendAnswerButtonId).hide();
	});
	
	// ajax loading animation
	$(document).on({
		ajaxStart: function () { setTimeout("$('body').addClass('loading')", 0); }, // delay, because we do not want a flickering screen
		ajaxStop: function () { setTimeout("$('body').removeClass('loading')", 0); }
	});

	/*
	// ask for refreshing
	$(window).bind('beforeunload', function(){
		return 'Every data in this documt will be lost during a reload of the page.';
	});

	// logout user on unload
	$(window).on('unload', function(){
		// todo:
		// set checkbox on login
		// new db field for "stay_logged_in"
		// send request on unload
	});
	*/

});