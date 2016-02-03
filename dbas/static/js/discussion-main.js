/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */


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
	$('#' + listAllUsersArgumentId).click(function listAllUsersAttacksId() {
		if ($(this).val() === _t(showAllAttacks)) {
			ajaxHandler.getArgumentOverview();
		} else {
			$('#' + adminsSpaceForArgumentsId).empty();
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

	// hiding the island view, when the X button is clicked
	$('#' + closeGraphViewContainerId).click(function () {
		$('#' + graphViewContainerId).hide();
		guiHandler.resetChangeDisplayStyleBox();
	});

	// open edit statement
	$('#' + editStatementButtonId).click(function(){
		guiHandler.showEditStatementsPopup();
	});

	// close popups
	$('#' + popupEditStatementCloseButtonXId).click(function popupEditStatementCloseButtonXId(){	guiHandler.hideandClearEditStatementsPopup(); });
	$('#' + popupEditStatementCloseButtonId).click(function popupEditStatementCloseButtonId(){		guiHandler.hideandClearEditStatementsPopup(); });
	$('#' + popupUrlSharingCloseButtonXId).click(function popupUrlSharingCloseButtonXId(){			guiHandler.hideAndClearUrlSharingPopup(); });
	$('#' + popupUrlSharingCloseButtonId).click(function popupUrlSharingCloseButtonId(){			guiHandler.hideAndClearUrlSharingPopup(); });

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

	guiHandler.setDisplayStyleAsDiscussion();
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

	$('#' + issueDropdownListID + ' .enabled').each(function() {
		if ($(this).children().length > 0){
			$(this).children().click(function() {
				var href = $(this).attr('href'),
					text = _t(switchDiscussionText1) + ' <strong>' + $(this).attr('value') + '</strong> ' + _t(switchDiscussionText2);
				$(this).attr('href','#');
				displayConfirmationDialogWithCheckbox(_t(switchDiscussion), text, _t.keepSetting, href, true);
			});
		}
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
				ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputId, fuzzy_start_statement, '');
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
	var tmp1, tmp2, w1, w2;

	guiHandler.hideSuccessDescription();
	guiHandler.hideErrorDescription();

	tmp1 = $('#discussion-restart-btn');
	tmp2 = $('#' + issueDropdownButtonID);
	w1 = tmp1.outerWidth();
	w2 = tmp2.outerWidth();
	tmp1.attr('style', w1<w2 ? 'width: ' + w2 + 'px;' : '');
	tmp2.attr('style', w1>w2 ? 'width: ' + w1 + 'px;' : '');

	// focus text of input elements
	$("input[type='text']").on("click", function () {
		$(this).select();
	});

	// render html tags
	replaceHtmlTags($('#discussions-header'));
	$.each($('#' + discussionSpaceId + ' label'), function () {
		replaceHtmlTags($(this));
	});
	$.each($('#' + islandViewContainerId + ' h5'), function () {
		replaceHtmlTags($(this));
	});
	replaceHtmlTags($('#' + issueInfoId));
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

/**
 *
 */
setGuiOptions = function(){
	if (window.location.href.indexOf('/reaction/') != -1){
		var cl = 'icon-badge',
			style = 'height: 30px; width:30px;',
			src = mainpage + 'static/images/icon_discussion_',
			item_undermine = $('#item_undermine'),
			item_support = $('#item_support'),
			item_undercut = $('#item_undercut'),
			item_overbid = $('#item_overbid'),
			item_rebut = $('#item_rebut'),
			item_no_opinion = $('#item_no_opinion'),
			undermine = $('<img>').addClass(cl).attr({'style': style, 'src': src + 'undermine.png', 'onclick': item_undermine.attr('onclick')}),
			support = $('<img>').addClass(cl).attr({'style': style, 'src': src + 'support.png', 'onclick': item_support.attr('onclick')}),
			undercut = $('<img>').addClass(cl).attr({'style': style, 'src': src + 'undercut.png', 'onclick': item_undercut.attr('onclick')}),
			overbid = $('<img>').addClass(cl).attr({'style': style, 'src': src + 'overbid.png', 'onclick': item_overbid.attr('onclick')}),
			rebut = $('<img>').addClass(cl).attr({'style': style, 'src': src + 'rebut.png', 'onclick': item_rebut.attr('onclick')}),
			no_opinion = $('<img>').addClass(cl).attr({'style': style, 'src': src + 'no_opinion.png', 'onclick': item_no_opinion.attr('onclick')});
		item_undermine.next().prepend(undermine ); item_undermine.hide();
		item_support.next().prepend(support ); item_support.hide();
		item_undercut.next().prepend(undercut ); item_undercut.hide();
		item_overbid.next().prepend(overbid ); item_overbid.hide();
		item_rebut.next().prepend(rebut ); item_rebut.hide();
		item_no_opinion.next().prepend(no_opinion); item_no_opinion.hide();
	}
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

	// default function
	$('#' + sendNewPremiseId).click(function(){
		splits = window.location.href.split('/');
		text = $('#' + addPremiseContainerMainInputId).val();
		arg = splits[splits.length - 3];
		supportive = splits[splits.length - 2] == 't';
		relation = splits[splits.length - 1];
		ajaxHandler.sendNewPremiseForArgument(arg, relation, supportive, text)
	});

	// options for the extra buttons, where the user can add input!
	input.change(function () {
		if (input.prop('checked')){
			// new position at start
			if (input.attr('id').indexOf('start_statement') != -1){
				guiHandler.showHowToWriteTextPopup();
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
				guiHandler.showHowToWriteTextPopup();
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
				guiHandler.showHowToWriteTextPopup();
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
		interactionHandler = new InteractionHandler(), tmp;

	guiHandler.setHandler(interactionHandler);
	setClickFunctions(guiHandler, ajaxHandler);
	setKeyUpFunctions(guiHandler, ajaxHandler);
	setStyleOptions(guiHandler);
	setWindowOptions();
	// setGuiOptions();
	setInputExtraOptions(guiHandler, ajaxHandler);

	// some extras
	// get restart url and cut the quotes
	tmp = $('#discussion-restart-btn').attr('onclick').substr('location.href='.length);
	tmp = tmp.substr(1, tmp.length-2);
	$('#' + discussionEndRestart).attr('href', tmp);
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