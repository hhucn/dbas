/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

/**
 *
 */
startDiscussion = function () {
	//$('#' + startDiscussionButtonId).hide(); // hides the start button
	//$('#' + startDescriptionId).hide(); // hides the start description
	$('#' + restartDiscussionButtonId).show(); // show the restart button
	$('#' + discussionContainerId).fadeIn('fast'); // hiding retry button

	// on success we will get the start statements
	new AjaxSiteHandler().getIssueList();
};

/**
 *
 */
resetDiscussion = function () {
	var issue_id = new Helper().getCurrentIssueId();
	window.location.href = mainpage + 'discussion/start/issue=' + issue_id;
};


/**
 * main function
 */
$(function () {
	'use strict';
	var guiHandler = new GuiHandler(),
		ajaxHandler = new AjaxSiteHandler(),
		interactionHandler = new InteractionHandler(),
		hidden_service, params,
		delay = (function(){
			var timer = 0;
			return function(callback, ms){
				clearTimeout (timer);
				timer = setTimeout(callback, ms);
			};
		})();

	guiHandler.setHandler(interactionHandler);

	// gui for the fuzzy search
	$('#' + addStatementContainerMainInputId).keyup(function () {
		delay(function() {
			if($('#' + addStatementContainerMainInputId).val().length==0){
				$('#' + addStatementContainerMainInputId).next().empty();
			} else {
				if ($('#' + discussionsDescriptionId).text().indexOf(_t(startDiscussionText)) != -1) {
					// here we have our start statement
					ajaxHandler.fuzzySearch($('#' + addStatementContainerMainInputId).val(), addStatementContainerMainInputId, 0, '');
				} else {
					// some trick: here we have a premisse for our start statement
					ajaxHandler.fuzzySearch($('#' + addStatementContainerMainInputId).val(), addStatementContainerMainInputId, 2, '');
				}
			}
		},200);
	});

	// gui for editing statements
	$('#' + popupEditStatementTextareaId).keyup(function () {
		delay(function() {
			if($('#' + popupEditStatementTextareaId).val().length==0){
				$('#' + popupEditStatementTextareaId).next().empty();
			} else {
				ajaxHandler.fuzzySearch($('#' + popupEditStatementTextareaId).val(), popupEditStatementTextareaId, 1,
					$('#' + popupEditStatementTextareaId).attr('statement_id'));
				$('#' + popupEditStatementWarning).hide();
				$('#' + popupEditStatementWarningMessage).text('');
			}
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
		resetDiscussion();
	});

	// admin list all users button
	$('#' + listAllUsersButtonId).click(function listAllUsersButtonId() {
		if ($(this).val() === _t(showAllUsers)) {
			ajaxHandler.getUsersOverview();
			$(this).val(_t(hideAllUsers));
		} else {
			$('#' + adminsSpaceForUsersId).empty();
			$(this).val(_t(showAllUsers));
		}
	});

	// admin list all attacks button
	$('#' + listAllUsersAttacksId).click(function listAllUsersAttacksId() {
		if ($(this).val() === _t(showAllAttacks)) {
			ajaxHandler.getAttackOverview();
		} else {
			$('#' + adminsSpaceForAttacksId).empty();
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
			$(this).attr('short_url', '1').text(_t(fetchLongUrl));
		} else {
			$('#' + popupUrlSharingInputId).val(window.location);
			$(this).attr('short_url', '0').text(_t(fetchShortUrl));
		}
	});

	/**
	 * Sharing shortened url with mail
	 */
	$('#' + shareUrlButtonMail).click(function shareUrlButtonMail(){
		mailShare('user@example.com', _t(interestingOnDBAS), _t(haveALookAt) + ' ' + $('#' + popupUrlSharingInputId).val());
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
		googleShare($('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on facebook
	 */
	$('#' + shareUrlButtonFacebook).click(function shareUrlButtonFacebook(){
		fbShare($('#' + popupUrlSharingInputId).val(), "FB Sharing", _t(haveALookAt) + ' ' + $('#' + popupUrlSharingInputId).val(),
			mainpage + "static/images/logo.png");
	});

	// focus text of input elements
	$("input[type='text']").on("click", function () {
		$(this).select();
	});

	/*
	 * Display message on premisse group checkbox
	 */
	$('#' + proTextareaPremissegroupCheckboxId).click(function (){
		if ($('#' + proTextareaPremissegroupCheckboxId).prop('checked')){
			guiHandler.displayPremisseGroupPopup();
		}
	});
	$('#' + conTextareaPremissegroupCheckboxId).click(function (){
		if ($('#' + conTextareaPremissegroupCheckboxId).prop('checked')){
			guiHandler.displayPremisseGroupPopup();
		}
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

	// some hack
	$('#navbar-left').empty();

	$(window).load( function windowLoad () {
		var url = window.location.href;
    	if (url.indexOf(mainpage + 'discussion/start') != -1) {
			startDiscussion();
		} else {
			$('#' + discussionContainerId).fadeIn('fast');
			$('#' + restartDiscussionButtonId).show(); // show the restart button

			params = window.location.href.substr(window.location.href.indexOf('discussion/') + 'discussion/'.length);
			params = params.substr(0,params.indexOf('/'));
			// get issue list
			ajaxHandler.getIssueList();

			if (url.indexOf('start') != -1){
				ajaxHandler.getStartStatements();
			} else if (url.indexOf(attrGetPremissesForStatement) != -1){
				ajaxHandler.getPremisseForStatement(params);
			} else if (url.indexOf(attrReplyForPremissegroup) != -1){
				ajaxHandler.getReplyForPremisseGroup(params);
			} else if (url.indexOf(attrReplyForResponseOfConfrontation) != -1){
				ajaxHandler.handleReplyForResponseOfConfrontation(params);
			} else if (url.indexOf(attrReplyForArgument) != -1){
				ajaxHandler.getReplyForArgument(params);	}
		}
	});

});