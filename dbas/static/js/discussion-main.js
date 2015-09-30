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

	new AjaxSiteHandler().getStartStatements();
};

restartDiscussion = function () {
	// $('#' + startDiscussionButtonId).show(); // show the start description
	/*
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
	guiHandler.resetEditButton();

	startDiscussion();
	*/

	window.location.href = mainpage + "discussion/start";
};


/**
 * main function
 */
$(function () {
	'use strict';
	var guiHandler = new GuiHandler(),
		ajaxHandler = new AjaxSiteHandler(),
		interactionHandler = new InteractionHandler(),
		hidden_service, hidden_params;

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
		if ($(this).val() === showAllUsers) {
			ajaxHandler.getUsersOverview();
			$(this).val(hideAllUsers);
		} else {
			$('#' + adminsSpaceForUsersId).empty();
			$(this).val(showAllUsers);
		}
	});

	// admin list all attacks button
	$('#' + listAllUsersAttacksId).click(function () {
		if ($(this).val() === showAllAttacks) {
			ajaxHandler.getAttackOverview();
			$(this).val(hideAllAttacks);
		} else {
			$('#' + adminsSpaceForAttacksId).empty();
			$(this).val(showAllAttacks);
		}
	});

	// add argument button in the island view
	$('#' + islandViewAddArgumentsBtnid).click(function () {
		$('#' + scStyle2Id).attr('checked', true);
		$('#' + scStyle1Id).attr('checked', false);
		$('#' + scStyle3Id).attr('checked', false);
		guiHandler.setDisplayStylesOfAddStatementContainer(true, true, false, false);
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
		guiHandler.showEditStatementsPopup();
	}).hover(function () {
		$(this).toggleClass('btn-primary', 400);
	});

	// close popups
	$('#' + popupEditStatementCloseButtonXId).click(function(){	guiHandler.hideEditStatementsPopup();	});
	$('#' + popupEditStatementCloseButtonId).click(function(){	guiHandler.hideEditStatementsPopup();	});
	$('#' + popupUrlSharingCloseButtonXId).click(function(){	guiHandler.hideUrlSharingPopup();	});
	$('#' + popupUrlSharingCloseButtonId).click(function(){		guiHandler.hideUrlSharingPopup();	});

	// share url for argument blogging
	$('#' + shareUrlId).click(function shareurlClick (){
		guiHandler.showUrlSharingPopup();
	});

	/**
	 * Switch between shortened and long url
	 */
	$('#' + popupUrlSharingLongUrlButtonID).click(function(){
		if ($('#' + popupUrlSharingLongUrlButtonID).attr('short_url') == '0'){
			new AjaxSiteHandler().getShortenUrl(window.location);
			$('#' + popupUrlSharingLongUrlButtonID).attr('short_url', '1').text(fetchLongUrl);
		} else {
			$('#' + popupUrlSharingInputId).val(window.location);
			$('#' + popupUrlSharingLongUrlButtonID).attr('short_url', '0').text(fetchShortUrl);
		}
	});

	/**
	 * Sharing shortened url with mail
	 */
	$('#' + shareUrlButtonMail).click(function(){
		mailShare('user@example.com', interestingOnDBAS, haveALookAt + ' ' + $('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on twitter
	 */
	$('#' + shareUrlButtonTwitter).click(function(){
		tweetShare($('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on google
	 */
	$('#' + shareUrlButtonGoogle).click(function(){
		alert($('#' + popupUrlSharingInputId).val());
		googleShare($('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on facebook
	 */
	$('#' + shareUrlButtonFacebook).click(function(){
		fbShare($('#' + popupUrlSharingInputId).val(), "FB Sharing", haveALookAt + ' ' + $('#' + popupUrlSharingInputId).val(), "https://dbas.cs.uni-duesseldorf.de/static/images/logo.png");
	});

	// focos text of input elements
	$("input[type='text']").on("click", function () {
		$(this).select();
	});

	/*
	// managed in the html file
	$('#' + scStyle1Id).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	$('#' + scStyle2Id).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	$('#' + scStyle3Id).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	*/

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});

	/*
	// ask for refreshing
	$(window).bind('beforeunload', function(){	return 'If you refresh this page, your progress will be lost.';	});

	// asks for go back
	$(window).bind('statechange', function(){	return 'If you refresh this page, your progress will be lost.';	});
	*/

	// logout user on unload
	$(window).on('unload', function windowUnload(){
		// todo:
		// set checkbox on login
		// new db field for "stay_logged_in"
		// send request on unload
	});

	$(window).load( function windowLoad () {
    	if (window.location == mainpage + 'discussion/' + 'start') {
			startDiscussion();
		} else {
			$('#' + discussionContainerId).fadeIn('fast');
			$('#' + restartDiscussionButtonId).show(); // show the restart button

			hidden_service = $('#' + hiddenDiscussionInformationServiceId).text();
			hidden_params = $('#' + hiddenDiscussionInformationParametersId).text();
			// alert("params: "	+ hidden_params + "\n\n" + "service: "	+ hidden_service);

			if (hidden_service == 'ajax_get_start_statements'){
				ajaxHandler.getStartStatements();
			} else if (hidden_service == 'ajax_get_premisses_for_statement'){
				ajaxHandler.getPremisseForStatement(hidden_params);
			} else if (hidden_service == 'ajax_reply_for_premissegroup'){
				ajaxHandler.getReplyForPremisseGroup(hidden_params);
			} else if (hidden_service == 'ajax_reply_for_response_of_confrontation'){
				ajaxHandler.handleReplyForResponseOfConfrontation(hidden_params);
			} else if (hidden_service == 'ajax_reply_for_argument'){
				ajaxHandler.getReplyForArgument(hidden_params);	}
		}
	});

});