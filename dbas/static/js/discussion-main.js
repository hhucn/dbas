/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

/**
 * Discussion will be started: Resstart button and discussion container are visible, issue list will be fetched
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
 * Restarts discussion by redirecting to "mainpage + 'discussion/start/issue=' + issue_id"
 */
resetDiscussion = function () {
	var issue_id = new Helper().getCurrentIssueId();
	window.location.href = mainpage + 'discussion/start/issue=' + issue_id;
};

/**
 * Sets all click functions
 * @param guiHandler
 * @param ajaxHandler
 * @param interactionHandler
 */
setClickFunctions = function (guiHandler, ajaxHandler, interactionHandler){
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

	// adding a textarea in the right column
	$('#' + addConTextareaId).hide().click(function addConTextareaId() {
		guiHandler.addTextareaOrInputAsChildInParent(conPositionTextareaId, 'right', $('#' + discussionSpaceId + ' ul li input').hasClass('statement'), 'input');
		$('#' + proposalListGroupId).empty();
	});

	// adding a textarea in the left column
	$('#' + addProTextareaId).hide().click(function addProTextareaId() {
		guiHandler.addTextareaOrInputAsChildInParent(proPositionTextareaId, 'left', $('#' + discussionSpaceId + ' ul li input').hasClass('statement'), 'input');
		$('#' + proposalListGroupId).empty();
	});

	// hiding the argument container, when the X button is clicked
	$('#' + closeStatementContainerId).click(function closeStatementContainerId() {
		$('#' + addStatementContainerId).hide();
		$('#' + addStatementErrorContainer).hide();
		$('#' + addReasonButtonId).attr('checked', false).prop('checked', false).enable = true;
	});

	// hiding the island view, when the X button is clicked
	$('#' + closeIslandViewContainerId).click(function () {
		$('#' + islandViewContainerId).hide();
		guiHandler.resetChangeDisplayStyleBox();
		$('#li_' + addReasonButtonId).attr('checked', true).prop('checked', true);
	});

	// open edit statement
	$('#' + editStatementButtonId).click(function(){
		guiHandler.showEditStatementsPopup();
	}).hover(function () {
		$(this).toggleClass('btn-primary', 400);
	});

	// close popups
	$('#' + popupEditStatementCloseButtonXId).click(function popupEditStatementCloseButtonXId(){	guiHandler.hideEditStatementsPopup(); });
	$('#' + popupEditStatementCloseButtonId).click(function popupEditStatementCloseButtonId(){		guiHandler.hideEditStatementsPopup(); });
	$('#' + popupUrlSharingCloseButtonXId).click(function popupUrlSharingCloseButtonXId(){			guiHandler.hideUrlSharingPopup(); });
	$('#' + popupUrlSharingCloseButtonId).click(function popupUrlSharingCloseButtonId(){			guiHandler.hideUrlSharingPopup(); });

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

	/*
	// managed in the html file
	$('#' + scStyleDialogId).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	$('#' + scStyleIslandId).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	$('#' + scStyleCompleteId).click(function () {	interactionHandler.styleButtonChanged(this.id);	});
	*/

	/**
	 * Sharing shortened url with mail
	 */
	$('#' + shareUrlButtonMail).click(function shareUrlButtonMail(){
		new Sharing().emailShare('user@example.com', _t(interestingOnDBAS), _t(haveALookAt) + ' ' + $('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on twitter
	 */
	$('#' + shareUrlButtonTwitter).click(function shareUrlButtonTwitter(){
		new Sharing().twitterShare($('#' + popupUrlSharingInputId).val(), '');
	});

	/**
	 * Sharing shortened url on google
	 */
	$('#' + shareUrlButtonGoogle).click(function shareUrlButtonGoogle(){
		new Sharing().googlePlusShare($('#' + popupUrlSharingInputId).val());
	});

	/**
	 * Sharing shortened url on facebook
	 */
	$('#' + shareUrlButtonFacebook).click(function shareUrlButtonFacebook(){
		new Sharing().facebookShare($('#' + popupUrlSharingInputId).val(), "FB Sharing", _t(haveALookAt) + ' ' + $('#' + popupUrlSharingInputId).val(),
			mainpage + "static/images/logo.png");
	});
	// hide the restart button and add click function
	$('#' + restartDiscussionButtonId).hide().click(function restartDiscussionButtonId() {
		resetDiscussion();
	});

	/*
	 * Display message on premise group checkbox
	 */
	$('#' + proTextareaPremisegroupCheckboxId).click(function (){
		if ($('#' + proTextareaPremisegroupCheckboxId).prop('checked')){
			guiHandler.displayPremiseGroupPopup();
		}
	});

	$('#' + conTextareaPremisegroupCheckboxId).click(function (){
		if ($('#' + conTextareaPremisegroupCheckboxId).prop('checked')){
			guiHandler.displayPremiseGroupPopup();
		}
	});

	$('#' + scStyleDialogId).click(function scStyle1Function () { interactionHandler.styleButtonChanged($(this).attr('id'))});
	$('#' + scStyleIslandId).click(function scStyle2Function () { interactionHandler.styleButtonChanged($(this).attr('id'))});
	$('#' + scStyleCompleteId).click(function scStyle3Function () { interactionHandler.styleButtonChanged($(this).attr('id'))});

	/**
	 * Handling report button
	 */
	$('#' + reportButtonId).click(function reportFunction(){
		/*
		var mailto = 'dbas.hhu@gmail.com',
				cc = 'krauthoff@cs.uni-duesseldorf.de',
				subject = 'Report ' + new Helper().getTodayAsDate(),
				body = 'URL: ' + window.location.href + '%0A%0AReport:%0A' + _t(fillLine).toUpperCase();
		// open new email tab
		window.location.href = 'mailto:' + mailto
				+ '?cc=' + cc
				+ '&subject=' + subject
				+ '&body=' + body;
		window.open(mainpage + 'contact', '_blank');
		*/

		// jump to contact tab
		var line1 = 'Report ' + new Helper().getTodayAsDate(),
				line2 = 'URL: ' + window.location.href,
				line3 = _t(fillLine).toUpperCase(),
				params = {'content': line1 + '\n' + line2 + '\n' + line3,
					'name': $('#header_user').parent().text().replace(/\s/g,'')};

		new Helper().redirectInNewTabForContact(params);

	}).hover(function () {
		$(this).toggleClass('btn-primary', 400);
	});

	// opinion barometer
	$('#' + opinionBarometerImageId).show().click(function opinionBarometerFunction() {
		new DiscussionBarometer().showBarometer()
	});

};

/**
 * Sets all keyUp functions
 * @param guiHandler
 * @param ajaxHandler
 */
setKeyUpFunctions = function (guiHandler, ajaxHandler){
	// gui for the fuzzy search
	$('#' + addStatementContainerMainInputId).keyup(function () {
		new Helper().delay(function() {
			var escapedText = new Helper().escapeHtml($('#' + addStatementContainerMainInputId).val());
			if ($('#' + discussionsDescriptionId).text().indexOf(_t(initialPositionInterest)) != -1) {
				// here we have our start statement
				// todo: currently not needed
				// ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputId, fuzzy_start_statement, '');
			} else {
				// some trick: here we have a premise for our start statement
				ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputId, fuzzy_start_premise, '');
			}
		},200);
	});

	// gui for editing statements
	$('#' + popupEditStatementTextareaId).keyup(function () {
		new Helper.delay(function() {
			ajaxHandler.fuzzySearch($('#' + popupEditStatementTextareaId).val(), popupEditStatementTextareaId, fuzzy_statement_popup,
				$('#' + popupEditStatementTextareaId).attr('statement_id'));
			$('#' + popupEditStatementWarning).hide();
			$('#' + popupEditStatementWarningMessage).text('');
		},200);
	});
};

/**
 *
 * @param guiHandler
 */
setStyleOptions = function (guiHandler){
	$('#' + discussionContainerId).hide(); // hiding discussions container
	$('#' + addStatementContainerId).hide(); // hiding container for adding arguments
	$('#' + discussionFailureRowId).hide(); // hiding error message at start
	$('#' + islandViewContainerId).hide(); // hidding the islandView
	//$('#' + scStyleIslandId).hide();
	//$('#' + scStyle2LabelId).hide();
	//$('#' + scStyle1LabelId).next().hide();
	$('#' + displayControlContainerIconGuidedId).click(function displayControlContainerIconGuidedClick(){
		var f = function dialogStyle () { $('#' + scStyleDialogId).attr('checked', true).prop('checked', true);
			new InteractionHandler().styleButtonChanged($('#' + scStyleDialogId).attr('id'))};
		displayConfirmationDialog(_t(displayControlDialogGuidedTitle), '<h4>' + _t(displayControlDialogGuidedBody) + '</h4>', f, false);
	});
	$('#' + displayControlContainerIconIslandId).click(function displayControlContainerIconIslandClick(){
		var f = function islandStyle () { $('#' + scStyleIslandId).attr('checked', true).prop('checked', true);
			new InteractionHandler().styleButtonChanged($('#' + scStyleIslandId).attr('id'))};
		displayConfirmationDialog(_t(displayControlDialogIslandTitle), '<h4>' + _t(displayControlDialogIslandBody) + '</h4>', f, false);
	});
	$('#' + displayControlContainerIconExpertId).click(function displayControlContainerIconExpertClick(){
		var f = function completeStyle () { $('#' + scStyleCompleteId).attr('checked', true).prop('checked', true);
			new InteractionHandler().styleButtonChanged($('#' + scStyleCompleteId).attr('id'))};
		displayConfirmationDialog(_t(displayControlDialogExpertTitle), '<h4>' + _t(displayControlDialogExpertBody) + '</h4>', f, false);
	});
	//$('#' + scStyleDialogId).click(function scStyle1Function () { interactionHandler.styleButtonChanged($(this).attr('id'))});
	//$('#' + scStyleIslandId).click(function scStyle2Function () { interactionHandler.styleButtonChanged($(this).attr('id'))});
	//$('#' + scStyleCompleteId).click(function scStyle3Function () { interactionHandler.styleButtonChanged($(this).attr('id'))});

	guiHandler.hideSuccessDescription();
	guiHandler.hideErrorDescription();

	// focus text of input elements
	$("input[type='text']").on("click", function () {
		$(this).select();
	});
};

/**
 *
 * @param guiHandler
 * @param ajaxHandler
 */
setWindowOptions = function(guiHandler, ajaxHandler){
	var params;
	/**
	 * handle toggle button
	 */
	if (window.location.href.indexOf('start') != -1){
		$('#' + discussionAttackSpaceId).show();
	} else {
		$('#' + discussionAttackSpaceId).hide();
	}

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});

	// logout user on unload
	$(window).on('unload', function windowUnload(){
		// set checkbox on login
		// new db field for "stay_logged_in"
		// send request on unload
	});

	$(window).on('resize', function resizeWindow(){
		// make some things pretty
		new GuiHandler().setIssueDropDownText(new Helper().resizeIssueText($('#' + issueDropdownButtonID).attr('value')));
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

			if (url.indexOf(attrStart) != -1) {										ajaxHandler.getStartStatements();
			} else if (url.indexOf(attrChooseActionForStatement) != -1){ 			ajaxHandler.getTextForStatement(params);
			} else if (url.indexOf(attrGetPremisesForStatement) != -1){				ajaxHandler.getPremiseForStatement(params, id_premisses);
			} else if (url.indexOf(attrMoreAboutArgument) != -1){ 					ajaxHandler.getPremiseForStatement(params, id_premisse);
			} else if (url.indexOf(attrReplyForPremisegroup) != -1){				ajaxHandler.getReplyForPremiseGroup(params);
			} else if (url.indexOf(attrReplyForResponseOfConfrontation) != -1){		ajaxHandler.handleReplyForResponseOfConfrontation(params);
			} else if (url.indexOf(attrReplyForArgument) != -1){					ajaxHandler.getReplyForArgument(params);	}
		}
	});
};

/**
 * main function
 */
$(function () {
	'use strict';
	var guiHandler = new GuiHandler(),
		ajaxHandler = new AjaxSiteHandler(),
		interactionHandler = new InteractionHandler();

	guiHandler.setHandler(interactionHandler);

	setClickFunctions(guiHandler, ajaxHandler, interactionHandler);
	setKeyUpFunctions(guiHandler, ajaxHandler);
	setStyleOptions(guiHandler);
	setWindowOptions(guiHandler, ajaxHandler);
});