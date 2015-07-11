/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

/**
 * ID's
 * @type {string[]}
 */
var addStatementButtonId = 'add-statement';
var addPositionButtonId = 'add-position';
var addStatementContainerId = 'add-statement-container';
var addStatementContainerH4Id = 'add-statement-container-h4';
var addStatementContainerMainInputId = 'add-statement-container-main-input';
var addProTextareaId = 'add-pro-textarea';
var addConTextareaId = 'add-con-textarea';
var adminsSpaceId = 'admins-space';
var argumentListId = 'argument-list';
var closeStatementContainerId = 'close-statement-container';
var closeIslandViewContainerId = 'close-island-view-container';
var discussionsDescriptionId = 'discussions-description';
var discussionsAvoidanceDescriptionId = 'discussions-avoidance-description';
var discussionContainerId = 'discussion-container';
var discussionSpaceId = 'discussions-space';
var discussionAvoidanceSpaceId = 'discussions-avoidance-space';
var discussionFailureRowId = 'discussion-failure-row';
var discussionFailureMsgId = 'discussion-failure-msg';
var displayControlContainerId = 'display-control-container';
var discussionErrorDescriptionId = 'discussion-error-description';
var discussionSuccessDescriptionId = 'discussion-success-description';
var editStatementButtonId = 'edit-statement';
var headingProPositionTextId = 'heading-pro-positions';
var headingConPositionTextId = 'heading-contra-positions';
var leftPositionColumnId = 'left-position-column';
var leftPositionTextareaId = 'pro-textareas';
var leftIslandId = 'left-island';
var listAllUsersButtonId = 'list-all-users';
var goodPointTakeMeBackButtonId = 'good-point-of-the-others';
var insertStatementForm = 'insert_statement_form';
var islandViewContainerId = 'island-view-container';
var islandViewContainerH4Id = 'island-view-container-h4';
var islandViewAddArgumentsBtnid = 'island-view-add-arguments';
var restartDiscussionButtonId = 'restart-discussion';
var rightPositionColumnId = 'right-position-column';
var rightPositionTextareaId = 'con-textareas';
var rightIslandId = 'right-island';
var radioButtonGroup = 'radioButtonGroup';
var minimapId = 'navigation-minimap-container';
var popupEditStatementId = 'popup_edit_statement';
var popupEditStatementCloseButtonXId = 'popup_edit_statement_close';
var popupEditStatementCloseButtonId = 'popup_edit_statement_close_button';
var popupEditStatementTextareaId = 'popup_edit_statement_textarea';
var popupEditStatementContentId = 'popup_edit_statement_content';
var popupEditStatementLogfileHeaderId = 'popup_edit_statement_logfile_header';
var popupEditStatementLogfileSpaceId = 'popup_edit_statement_logfile';
var popupEditStatementSubmitButtonId = "popup_edit_statement_submit";
var popupEditStatementDescriptionId = "popup-edit-statement-description-p";
var popupErrorDescriptionId = 'popup-edit-error-description';
var popupSuccessDescriptionId = 'popup-edit-success-description';
var scStyleGroupId = 'sc-display-style';
var scStyle1Id = 'sc-style-1';
var scStyle2Id = 'sc-style-2';
var scStyle3Id = 'sc-style-3';
// var startDiscussionButtonId = 'start-discussion';
// var startDescriptionId = 'start-description';
var stepBackButtonId = 'step-back';
var sendAnswerButtonId = 'send-answer';
var sendNewStatementId = 'send-new-statement';
var statementListId = 'statement-list';

/**
 * TEXT
 * @type {string[]}
 */
var argumentSentencesOpeners = [
	'Okay, you have got the opinion: ',
	'Interesting, your opinion is: ',
	'You have said, that: ',
	'So your opinion is: '];
var firstOneText = 'You are the first one, who said: ';
var firstPositionText = 'You are the first one in this discussion!';
var goodPointTakeMeBackButtonText = 'I agree, that is a good argument! Take me one step back.';
var islandViewHeaderText = 'These are all arguments for: ';
var newArgumentRadioButtonText = 'I disagree! Let me state my own reason(s)!';
var newPositionRadioButtonText = 'Neither of the above, I have a different idea!';
var firstArgumentRadioButtonText = 'Let me insert my reasons!';
var firstPositionRadioButtonText = 'Let me insert my ideas!';
var statementContainerH4TextIfArgument = 'You want to state your own reason(s)?';
var statementContainerH4TextIfPosition = 'What is your idea?';
var startDiscussionText = 'How should we decide?';


startDiscussion = function () {
	//$('#' + startDiscussionButtonId).hide(); // hides the start button
	//$('#' + startDescriptionId).hide(); // hides the start description
	$('#' + restartDiscussionButtonId).show(); // show the restart button
	$('#' + discussionContainerId).fadeIn('fast'); // hiding retry button

	new AjaxHandler().getAllPositions(new InteractionHandler().callbackIfDoneForGetAllPositions);
};

restartDiscussion = function () {
	// $('#' + startDiscussionButtonId).show(); // show the start description
	$('#' + restartDiscussionButtonId).hide(); // hide the restart button
	$('#' + addStatementContainerId).hide(); // hide add statement container
	$('#' + islandViewContainerId).hide(); // hidding the islandView
	$('#' + displayControlContainerId).hide(); // hidding the control container

	// clear the discussions spaces
	$('#' + discussionSpaceId).empty();
	$('#' + discussionAvoidanceSpaceId).empty();
	$('#' + discussionContainerId).hide();
	$('#' + discussionFailureRowId).hide();
	$('#' + stepBackButtonId).hide();

	var guiHandler = new GuiHandler();
	guiHandler.setErrorDescription('');
	guiHandler.setSuccessDescription('');
	guiHandler.setDiscussionsAvoidanceDescription('');
	guiHandler.resetChangeDisplayStyleBox();

	startDiscussion();
};


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
	$('#sc-style-3').hide();
	$('#label-sc-style-3').hide();
	$('#' + minimapId).hide();

	// handler for the send answer button
	$('#' + sendAnswerButtonId).click(function () {
		interactionHandler.sendAnswerButtonClicked();
		guiHandler.setVisibilityOfDisplayStyleContainer(false, '');
		$('#' + islandViewContainerId).fadeOut('slow');
	});

	// handler for the step back button
	$('#' + stepBackButtonId).click(function () {
		new AjaxHandler().getOneStepBack();
		new GuiHandler().resetChangeDisplayStyleBox();
		$('#' + islandViewContainerId).fadeOut('slow');
	});

	// hide the restart button and add click function
	$('#' + restartDiscussionButtonId).hide(); // hides the restart button
	$('#' + restartDiscussionButtonId).click(function () {
		restartDiscussion();
	});

	// admin list all users button
	$('#' + listAllUsersButtonId).click(function () {
		if ($(this).val() === 'List all users') {
			ajaxHandler.getAllUsersAndSetInGui();
			$(this).val('Hide all users'); // will be done in the ajaxhandler
		} else {
			$('#' + adminsSpaceId).empty();
			$(this).val('List all users'); // will be done in the ajaxhandler
		}
	});

	// add argument button in the island view
	$('#' + islandViewAddArgumentsBtnid).click(function () {
		$('#' + scStyle2Id).attr('checked', true);
		$('#' + scStyle1Id).attr('checked', false);
		$('#' + scStyle3Id).attr('checked', false);
		guiHandler.setDisplayStylesOfAddArgumentContainer(true,  true);
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
		$('#' + addStatementButtonId).attr('checked', false);
		$('#' + sendAnswerButtonId).hide();
	});

	// hiding the island view, when the X button is clicked
	$('#' + closeIslandViewContainerId).click(function () {
		$('#' + islandViewContainerId).hide();
		guiHandler.resetChangeDisplayStyleBox();
		$('#li_' + addStatementButtonId).attr('checked', true);
	});

	// open edit statement
	$('#' + editStatementButtonId).click(function(){
		guiHandler.openEditStatementsPopup();
	}).hover(function () {
		$(this).toggleClass('btn-primary', 400);
	});

	// close edit statement
	$('#' + popupEditStatementCloseButtonXId).click(function(){
		guiHandler.closeEditStatementsPopup();
	});
	$('#' + popupEditStatementCloseButtonId).click(function(){
		guiHandler.closeEditStatementsPopup();
	});

	// managed in the html file
	// $('#' + scSty$('#' + editStatementButtonId)le1Id).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
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

	// starts the discussion with getting all positions
	//$('#' + startDiscussionButtonId).click(function () {
	startDiscussion();
	//});

});