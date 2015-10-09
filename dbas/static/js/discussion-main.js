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

	window.location.href = mainpage + 'discussion/start';
};


/**
 * main function
 */
$(function () {
	'use strict';
	var guiHandler = new GuiHandler(),
		ajaxHandler = new AjaxSiteHandler(),
		interactionHandler = new InteractionHandler(),
		hidden_service, hidden_params,
		delay = (function(){
			var timer = 0;
			return function(callback, ms){
				clearTimeout (timer);
				timer = setTimeout(callback, ms);
			};
		})();

	guiHandler.setHandler(interactionHandler);

	$('#' + addStatementContainerMainInputId).keyup(function () {
		delay(function() {
			ajaxHandler.fuzzySearch($('#' + addStatementContainerMainInputId).val(), addStatementContainerMainInputId, 0, '');
		},200);
	});

	$('#' + popupEditStatementTextareaId).keyup(function () {
		delay(function() {
			ajaxHandler.fuzzySearch($('#' + popupEditStatementTextareaId).val(), popupEditStatementTextareaId, 1,
			$('#' + popupEditStatementTextareaId).attr('statement_id'));
			$('#' + popupEditStatementWarning).hide();
			$('#' + popupEditStatementWarningMessage).text('');
		},200);
	});

	$('#' + discussionContainerId).hide(); // hiding discussions container
	$('#' + addStatementContainerId).hide(); // hiding container for adding arguments
	$('#' + discussionFailureRowId).hide(); // hiding error message at start
	$('#' + islandViewContainerId).hide(); // hidding the islandView
	$('#' + displayControlContainerId).hide(); // hidding the control container
	$('#' + scStyle3Id).hide();
	$('#label-' + scStyle3Id).hide();
	$('#' + minimapId).hide();

	// hide the restart button and add click function
	$('#' + restartDiscussionButtonId).hide(); // hides the restart button
	$('#' + restartDiscussionButtonId).click(function restartDiscussionButtonId() {
		restartDiscussion();
	});

	// admin list all users button
	$('#' + listAllUsersButtonId).click(function listAllUsersButtonId() {
		if ($(this).val() === showAllUsers) {
			ajaxHandler.getUsersOverview();
			$(this).val(hideAllUsers);
		} else {
			$('#' + adminsSpaceForUsersId).empty();
			$(this).val(showAllUsers);
		}
	});

	// admin list all attacks button
	$('#' + listAllUsersAttacksId).click(function listAllUsersAttacksId() {
		if ($(this).val() === showAllAttacks) {
			ajaxHandler.getAttackOverview();
			$(this).val(hideAllAttacks);
		} else {
			$('#' + adminsSpaceForAttacksId).empty();
			$(this).val(showAllAttacks);
		}
	});

	// add argument button in the island view
	$('#' + islandViewAddArgumentsBtnid).click(function islandViewAddArgumentsBtnid() {
		$('#' + scStyle2Id).attr('checked', true);
		$('#' + scStyle1Id).attr('checked', false);
		$('#' + scStyle3Id).attr('checked', false);
		guiHandler.setDisplayStylesOfAddStatementContainer(true, true, false, false);
	});

	// adding a textarea in the right column
	$('#' + addConTextareaId).click(function addConTextareaId() {
		guiHandler.addTextareaAsChildInParent(conPositionTextareaId, 'right', $('#' + discussionSpaceId + ' ul li input').hasClass('statement'));
	});

	// adding a textarea in the left column
	$('#' + addProTextareaId).click(function addProTextareaId() {
		guiHandler.addTextareaAsChildInParent(proPositionTextareaId, 'left', $('#' + discussionSpaceId + ' ul li input').hasClass('statement'));
	});

	// hiding the argument container, when the X button is clicked
	$('#' + closeStatementContainerId).click(function closeStatementContainerId() {
		$('#' + addStatementContainerId).hide();
		$('#' + addStatementErrorContainer).hide();
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
	$('#' + popupEditStatementCloseButtonXId).click(function popupEditStatementCloseButtonXId(){	guiHandler.hideEditStatementsPopup();	});
	$('#' + popupEditStatementCloseButtonId).click(function popupEditStatementCloseButtonId(){	guiHandler.hideEditStatementsPopup();	});
	$('#' + popupUrlSharingCloseButtonXId).click(function popupUrlSharingCloseButtonXId(){	guiHandler.hideUrlSharingPopup();	});
	$('#' + popupUrlSharingCloseButtonId).click(function popupUrlSharingCloseButtonId(){		guiHandler.hideUrlSharingPopup();	});

	// share url for argument blogging
	$('#' + shareUrlId).click(function shareurlClick (){
		guiHandler.showUrlSharingPopup();
	});

	/**
	 * Switch between shortened and long url
	 */
	$('#' + popupUrlSharingLongUrlButtonID).click(function (){

		if ($(this).attr('short_url') == '0'){
			new AjaxSiteHandler().getShortenUrl(window.location);
			$(this).attr('short_url', '1').text(fetchLongUrl);
		} else {
			$('#' + popupUrlSharingInputId).val(window.location);
			$(this).attr('short_url', '0').text(fetchShortUrl);
		}
	});

	/**
	 * Sharing shortened url with mail
	 */
	$('#' + shareUrlButtonMail).click(function shareUrlButtonMail(){
		mailShare('user@example.com', interestingOnDBAS, haveALookAt + ' ' + $('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on twitter
	 */
	$('#' + shareUrlButtonTwitter).click(function shareUrlButtonTwitter(){
		tweetShare($('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on google
	 */
	$('#' + shareUrlButtonGoogle).click(function shareUrlButtonGoogle(){
		alert($('#' + popupUrlSharingInputId).val());
		googleShare($('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on facebook
	 */
	$('#' + shareUrlButtonFacebook).click(function shareUrlButtonFacebook(){
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
    	if (window.location == mainpage + 'discussion/start') {
			startDiscussion();
		} else {
			$('#' + discussionContainerId).fadeIn('fast');
			$('#' + restartDiscussionButtonId).show(); // show the restart button

			hidden_service = $('#' + hiddenDiscussionInformationServiceId).text();
			hidden_params = $('#' + hiddenDiscussionInformationParametersId).text();

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