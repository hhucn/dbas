/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

var addStatementButtonId = 'add-statement';
var addPositionButtonId = 'add-position';
var addStatementContainerId = 'add-statement-container';
var addStatementContainerH3Id = 'add-statement-container-h3';
var addStatementContainerMainInputId = 'add-statement-container-main-input';
var addProTextareaId = 'add-pro-textarea';
var addConTextareaId = 'add-con-textarea';
var adminsSpaceId = 'admins-space';
var argumentListId = 'argument-list';
var closeStatementContainerId = 'closeStatementContainer';
var closeIslandViewContainerId = 'closeIslandViewContainer';
var discussionsDescriptionId = 'discussions-description';
var discussionContainerId = 'discussion-container';
var discussionSpaceId = 'discussions-space';
var discussionFailureRowId = 'discussion-failure-row';
var discussionFailureMsgId = 'discussion-failure-msg';
var displayControlContainerId = 'display-control-container';
var errorDescriptionId = 'error-description';
var leftPositionColumnId = 'left-position-column';
var leftPositionTextareaId = 'left-textareas';
var leftIslandId = 'left-island';
var listAllUsersButtonId = 'list-all-users';
var goodPointTakeMeBackButtonId = 'good-point-of-the-others';
var goodPointTakeMeBackButtonText = 'I agree, that is a good argument! Take me one step back.';
var insertStatementForm = 'insert_statement_form';
var islandViewContainerId = 'island-view-container';
var islandViewHeaderText = 'These are all arguments for';
var islandViewContainerH3Id = 'island-view-container-h3';
var restartDiscussionButtonId = 'restart-discussion';
var rightPositionColumnId = 'right-position-column';
var rightPositionTextareaId = 'right-textareas';
var rightIslandId = 'right-island';
var radioButtonGroup = 'radioButtonGroup';
var newArgumentRadioButtonText = 'Let me state my own reason(s)!';
var newPositionRadioButtonText = 'Neither of the above, I have a different idea!';
var scStyleGroupId = 'sc-display-style';
var scStyle1Id = 'sc-style-1';
var scStyle2Id = 'sc-style-2';
var scStyle3Id = 'sc-style-3';
var startDiscussionButtonId = 'start-discussion';
var startDescriptionId = 'start-description';
var statementContainerH3TextIfArgument = 'What are your arguments for and against: ';
var statementContainerH3TextIfPosition = 'What is your idea?';
var stepBackButtonId = 'step-back';
var sendAnswerButtonId = 'send-answer';
var sendNewStatementId = 'send-new-statement';
var statementListId = 'statement-list';
var successDescriptionId = 'success-description';



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
	$('#' + stepBackButtonId).hide(); // hiding the step one round back button
	$('#' + islandViewContainerId).hide(); // hidding the islandView
	$('#' + displayControlContainerId).hide(); // hidding the control container

	// starts the discussion with getting all positions
	$('#' + startDiscussionButtonId).click(function () {
		$('#' + startDiscussionButtonId).hide(); // hides the start button
		$('#' + startDescriptionId).hide(); // hides the start description
		$('#' + restartDiscussionButtonId).show(); // show the restart button
		$('#' + discussionContainerId).fadeIn('fast'); // hiding retry button

		ajaxHandler.getAllPositions(interactionHandler.callbackIfDoneForGetAllPositions);
	});

	// handler for the send answer button
	$('#' + sendAnswerButtonId).click(function () {
		interactionHandler.sendAnswerButtonClicked();
	});

	// handler for the step back button
	$('#' + stepBackButtonId).click(function () {
		new AjaxHandler().getOneStepBack();
	});

	// hide the restart button and add click function
	$('#' + restartDiscussionButtonId).hide(); // hides the restart button
	$('#' + restartDiscussionButtonId).click(function () {
		$('#' + startDiscussionButtonId).show(); // show the start description
		$('#' + restartDiscussionButtonId).hide(); // hide the restart button
		$('#' + addStatementContainerId).hide(); // hide add statement container
		$('#' + islandViewContainerId).hide(); // hidding the islandView
		$('#' + displayControlContainerId).hide(); // hidding the control container

		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionContainerId).hide();
		$('#' + discussionFailureRowId).hide();
		$('#' + stepBackButtonId).hide();
		guiHandler.setErrorDescription('');
		guiHandler.setSuccessDescription('');

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
		guiHandler.addTextareaAsChildInParent(rightPositionTextareaId, 'right');
	});

	// adding a textarea in the left column
	$('#' + addProTextareaId).click(function () {
		guiHandler.addTextareaAsChildInParent(leftPositionTextareaId, 'left');
	});

	// hiding the argument container, when the X button is clicked
	$('#' + closeStatementContainerId).click(function () {
		$('#' + addStatementContainerId).hide();
		$('#' + addStatementButtonId).enable = true;
		$('#' + addStatementButtonId).removeAttr('checked');
		$('#' + sendAnswerButtonId).hide();
	});

	// hiding the island view, when the X button is clicked
	$('#' + closeIslandViewContainerId).click(function () {
		$('#' + islandViewContainerId).hide();
		$('#' + scStyle1Id).attr('checked');
		$('#' + scStyle2Id).removeAttr('checked');
	});

	// managed in the html file
	// $('#' + scStyle1Id).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	// $('#' + scStyle2Id).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	// $('#' + scStyle3Id).click(function () {	interactionHandler.styleButtonChanged(this.id);	});

	
	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); }, // delay, because we do not want a
		// flickering screen
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
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