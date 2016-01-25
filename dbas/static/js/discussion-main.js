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
 */
setClickFunctions = function (guiHandler, ajaxHandler){
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

	// hiding the argument container, when the X button is clicked
	$('#' + closeStatementContainerId).click(function closeStatementContainerId() {
		$('#' + addStatementContainerId).hide();
		$('#' + addStatementErrorContainer).hide();
		$('#' + discussionSpaceId + ' li:last-child input').attr('checked', false).prop('checked', false).enable = true;
	});

	$('#' + closePremiseContainerId).click(function closeStatementContainerId() {
		$('#' + addPremiseContainerId).hide();
		$('#' + addPremiseErrorContainer).hide();
		$('#' + discussionSpaceId + ' li:last-child input').attr('checked', false).prop('checked', false).enable = true;
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
		var val = $('#' + popupUrlSharingInputId).val();
		new Sharing().facebookShare(val, "FB Sharing", _t(haveALookAt) + ' ' + val,
			mainpage + "static/images/logo.png");
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

	guiHandler.setImageInactive($('#' + displayStyleIconGuidedId));
	$('#' + displayStyleIconGuidedId).click(function displayStyleIconGuidedFct () { guiHandler.setDisplayStyleAsDiscussion(); });
	$('#' + displayStyleIconIslandId).click(function displayStyleIconIslandFct () { guiHandler.setDisplayStyleAsIsland(); });
	$('#' + displayStyleIconExpertId).click(function displayStyleIconExpertFct () { guiHandler.setDisplayStyleAsGraphView(); });

	/**
	 * Handling report button
	 */
	$('#' + reportButtonId).click(function reportFunction(){
		// jump to contact tab
		var line1 = 'Report ' + new Helper().getTodayAsDate(),
				line2 = 'URL: ' + window.location.href,
				line3 = _t(fillLine).toUpperCase(),
				params = {'content': line1 + '\n' + line2 + '\n' + line3,
					'name': $('#header_user').parent().text().replace(/\s/g,'')};

		new Helper().redirectInNewTabForContact(params);

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
	// gui for the fuzzy search (statements)
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

	// gui for the fuzzy search (premises)
	$('#' + addPremiseContainerMainInputId).keyup(function () {
		new Helper().delay(function() {
			var escapedText = new Helper().escapeHtml($('#' + addPremiseContainerMainInputId).val());
			ajaxHandler.fuzzySearch(escapedText, addPremiseContainerMainInputId, fuzzy_add_reason, '');
		},200);
	});

	// gui for editing statements
	$('#' + popupEditStatementTextareaId).keyup(function popupEditStatementTextareaKeyUp() {
		new Helper().delay(function() {
			ajaxHandler.fuzzySearch($('#' + popupEditStatementTextareaId).val(),
				popupEditStatementTextareaId,
				fuzzy_statement_popup,
				$('#' + popupEditStatementContentId + ' .text-hover').attr('id').substr(3));
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
	$('#' + addStatementContainerId).hide(); // hiding container for adding arguments
	$('#' + discussionFailureRowId).hide(); // hiding error message at start
	$('#' + islandViewContainerId).hide(); // hidding the islandView

	guiHandler.hideSuccessDescription();
	guiHandler.hideErrorDescription();

	// focus text of input elements
	$("input[type='text']").on("click", function () {
		$(this).select();
	});
};

/**
 *
 */
setWindowOptions = function(){
	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); },
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});

	// some hack
	$('#navbar-left').empty();

	$(window).load( function windowLoad () {
	});
};

setInputExtraOptions = function(guiHandler, ajaxHandler){
	var input = $('#' + discussionSpaceId + ' li:last-child input'), text, splits, conclusion, supportive, arg, relation;
	if (window.location.href.indexOf('/r/') != -1){
		$('#' + discussionSpaceId + ' label').each(function(){
			$(this).css('width', '95%');
		})
	}

	$('#' + discussionSpaceId + ' input').each(function() {
		$(this).attr('checked', false).prop('checked', false);
	});

	input.change(function () {
		if (input.prop('checked')){
			// new position at start
			if (input.attr('id').indexOf('start_statement') != -1){
				guiHandler.displayHowToWriteTextPopup();
				guiHandler.showAddPositionContainer();
				$('#' + sendNewStatementId).click(function(){
					text = $('#' + addStatementContainerMainInputId).val();
					if (text.length == 0){
						guiHandler.setErrorDescription(_t(inputEmpty));
					} else {
						ajaxHandler.sendNewStartStatement(text);
					}
				});
			}
			// new premise for the start
			else if (input.attr('id').indexOf('start_premise') != -1){
				guiHandler.displayHowToWriteTextPopup();
				guiHandler.showAddPremiseContainer();
				$('#' + sendNewPremiseId).click(function(){
					splits = window.location.href.split('/');
					conclusion = splits[splits.length - 2];
					supportive = splits[splits.length - 1] == 't';
					text = $('#' + addPremiseContainerMainInputId).val();
					if (text.length == 0){
						guiHandler.setErrorDescription(_t(inputEmpty));
					} else {
						ajaxHandler.sendNewStartPremise(text, conclusion, supportive)
					}
				});
			}
			// new premise while judging

			else if (input.attr('id').indexOf('justify_premise') != -1){
				guiHandler.displayHowToWriteTextPopup();
				guiHandler.showAddPremiseContainer();
				$('#' + sendNewPremiseId).click(function(){
					splits = window.location.href.split('/');
					text = $('#' + addPremiseContainerMainInputId).val();
					arg = splits[splits.length - 3];
					supportive = splits[splits.length - 2] == 't';
					relation = splits[splits.length - 1];
					ajaxHandler.sendNewPremiseForArgument(arg, relation, supportive, text)
				});
			}
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
	setClickFunctions(guiHandler, ajaxHandler);
	setKeyUpFunctions(guiHandler, ajaxHandler);
	setStyleOptions(guiHandler);
	setWindowOptions();
	setInputExtraOptions(guiHandler, ajaxHandler);

	// render html tags
	replaceHtmlTags($('#discussions-header'));
	$.each($('#discussions-space label'), function () {
		replaceHtmlTags($(this));
	});
	$.each($('.panel-heading h5'), function () {
		replaceHtmlTags($(this));
	});
});

// new
replaceHtmlTags = function(element){
	var text = element.text();
	text = text.replace('&lt;strong&gt;', '<strong>');
	text = text.replace('&lt;/strong&gt;', '</strong>');
	text = text.replace('&lt;a', '<a');
	text = text.replace('&lt;/a', '</a');
	text = text.replace('&lt;br&gt;', '<br>');
	element.html(text);
};