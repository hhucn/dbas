/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

startDiscussion = function () {
	//$('#' + startDiscussionButtonId).hide(); // hides the start button
	//$('#' + startDescriptionId).hide(); // hides the start description
	$('#' + restartDiscussionButtonId).show(); // show the restart button
	$('#' + discussionContainerId).fadeIn('fast'); // hiding retry button

	new AjaxHandler().getStartStatements();
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

	$('#' + discussionContainerId).hide(); // hiding discussions container
	$('#' + addStatementContainerId).hide(); // hiding container for adding arguments
	$('#' + discussionFailureRowId).hide(); // hiding error message at start
	$('#' + stepBackButtonId).hide(); // hiding the step one round back button
	$('#' + islandViewContainerId).hide(); // hidding the islandView
	$('#' + displayControlContainerId).hide(); // hidding the control container
	$('#sc-style-3').hide();
	$('#label-sc-style-3').hide();
	$('#' + minimapId).hide();
	// handler for the step back button
	$('#' + stepBackButtonId).click(function () {
		ajaxHandler.getOneStepBack();
		guiHandler.resetChangeDisplayStyleBox();
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
			ajaxHandler.getUsersAndSetInGui();
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
		guiHandler.setDisplayStylesOfAddStatementContainer(true,  true);
	});

	// adding a textarea in the right column
	$('#' + addConTextareaId).click(function () {
		guiHandler.addTextareaAsChildInParent(conPositionTextareaId, 'right', $('#' + discussionSpaceId + ' ul li input').hasClass('statement'));
	});

	// adding a textarea in the left column
	$('#' + addProTextareaId).click(function () {
		guiHandler.addTextareaAsChildInParent(proPositionTextareaId, 'left', $('#' + discussionSpaceId + ' ul li input').hasClass('statement'));
	});

	// hiding the argument container, when the X button is clicked
	$('#' + closeStatementContainerId).click(function () {
		$('#' + addStatementContainerId).hide();
		$('#' + addReasonButtonId).enable = true;
		$('#' + addReasonButtonId).attr('checked', false);
	});

	// hiding the island view, when the X button is clicked
	$('#' + closeIslandViewContainerId).click(function () {
		$('#' + islandViewContainerId).hide();
		guiHandler.resetChangeDisplayStyleBox();
		$('#li_' + addReasonButtonId).attr('checked', true);
	});

	// open edit statement
	$('#' + editStatementButtonId).click(function(){
		guiHandler.displayEditStatementsPopup();
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
		return 'If you refresh this page, your progress will be lost.';
	});

	// asks for go back
	$(window).bind('statechange', function(){
		return 'If you refresh this page, your progress will be lost.';
	});
	*/

	// logout user on unload
	$(window).on('unload', function(){
		// todo:
		// set checkbox on login
		// new db field for "stay_logged_in"
		// send request on unload
	});


	startDiscussion();

});