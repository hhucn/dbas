/*global $, jQuery, discussionsDescriptionId, discussionContainerId, discussionSpaceId, discussionAvoidanceSpaceId, _t */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function GuiHandler() {
	'use strict';
	var interactionHandler;

	this.setHandler = function (externInteractionHandler) {
		interactionHandler = externInteractionHandler;
	};

	/**
	 * Setting an error description in some p-tag
	 * @param text to set
	 */
	this.setErrorDescription = function (text) {
		$('#' + discussionErrorDescriptionId).html(text);
		$('#' + discussionErrorDescriptionSpaceId).show();
	};

	/**
	 *
	 */
	this.showAddPositionContainer = function(){
		$('#' + addStatementContainerId).show();
	};

	/**
	 *
	 */
	this.showAddPremiseContainer = function(){
		$('#' + addPremiseContainerId).show();
	};

	/**
	 *
	 * @param parsedData
	 * @param callbackid
	 */
	this.setStatementsAsProposal = function (parsedData, callbackid, type){
		var callback = $('#' + callbackid), uneditted_value;
		if (type == fuzzy_start_premise)        $('#' + proposalPremiseListGroupId).empty();
		else if (type == fuzzy_start_statement) $('#' + proposalStatementListGroupId).empty();
		else if (type == fuzzy_add_reason)      $('#' + proposalPremiseListGroupId).empty();
		else if (type == fuzzy_statement_popup) $('#' + proposalEditListGroupId).empty();

		// is there any value ?
		if (Object.keys(parsedData).length == 0){
			return;
		}

		var params, token, button, span_dist, span_text, distance, index;
		callback.focus();

		$.each(parsedData.values, function (key, val) {
			params = key.split('_');
			distance = parseInt(params[0]);
			index = params[1];

			token = callback.val();
			//var pos = val.toLocaleLowerCase().indexOf(token.toLocaleLowerCase()), newpos = 0, start = 0;

			// make all tokens bold
			uneditted_value = val;
			val = '<b>' + val.replace(token, '</b>' + token + '<b>').replace(token.toLocaleLowerCase(), '</b>' + token.toLocaleLowerCase() + '<b>') + '</b>';

			button = $('<button>').attr({type : 'button',
				class : 'list-group-item',
				id : 'proposal_' + index,
				text: uneditted_value})
				.hover(function(){$(this).addClass('active');},
					   function(){ $(this).removeClass('active');});
			span_dist = $('<span>').attr({class : 'badge'}).text(parsedData.distance_name + ' ' + distance);
			span_text = $('<span>').attr({id : 'proposal_' + index + '_text'}).html(val);
			button.append(span_dist).append(span_text).click(function(){
				callback.val($(this).attr('text'));
				$('#' + proposalStatementListGroupId).empty();
				$('#' + proposalPremiseListGroupId).empty();
				$('#' + proposalEditListGroupId).empty(); // list with elements should be after the callbacker
			});

			if (type == fuzzy_start_premise)        $('#' + proposalPremiseListGroupId).append(button);
			else if (type == fuzzy_start_statement) $('#' + proposalStatementListGroupId).append(button);
			else if (type == fuzzy_add_reason)      $('#' + proposalPremiseListGroupId).append(button);
			else if (type == fuzzy_statement_popup) $('#' + proposalEditListGroupId).append(button);
		});
		//$('#' + statementListGroupId).prepend('<h4>' + didYouMean + '</h4>');
	};

	/**
	 * Shows an error on discussion space as well as a retry button and sets a link for the contact page
	 * @param error_msg message of the error
	 */
	this.showDiscussionError = function (error_msg) {
		$('#' + discussionFailureRowId).fadeIn('slow');
		$('#' + discussionFailureMsgId).html(error_msg);
		$('#' + contactOnErrorId).click(function(){
			var line1 = 'Report ' + new Helper().getTodayAsDate(),
				line2 = 'URL: ' + window.location.href,
				line3 = _t(fillLine).toUpperCase(),
				params = {'content': line1 + '\n' + line2 + '\n' + line3,
				'name': $('#header_user').parent().text().replace(/\s/g,'')};
			new Helper().redirectInNewTabForContact(params);
		})
	};

	/**
	 * Hides the error field
	 */
	this.hideDiscussionError = function () {
		$('#' + discussionFailureRowId).hide();
	};

	/**
	 * Check whether the edit button should be visible or not
	 */
	this.resetEditAndRefactorButton = function (optionalEditable) {
		if (typeof optionalEditable === 'undefined') { optionalEditable = true; }

		var is_editable = false, statement, uid, is_premise, is_start;
		$('#' + discussionSpaceId + ' ul > li').children().each(function () {
			statement = $(this).val();
			uid = $(this).attr('id');
			is_premise = $(this).hasClass('premise');
			is_start = $(this).hasClass('start');
			// do we have a child with input or just the label?
			if (optionalEditable) {
				if ($(this).prop('tagName').toLowerCase().indexOf('input') > -1
						&& statement.length > 0
						&& $.isNumeric(uid)
						|| is_premise
						|| is_start) {
					is_editable = true;
					return false; // break
				}
			}
		});

		// do we have an statement there?
		if (is_editable) {
			$('#' + editStatementButtonId).show();
			$('#' + reportButtonId).show();
		} else {
			$('#' + editStatementButtonId).hide();
			$('#' + reportButtonId).hide();
		}
	};

	/**
	 * Opens the edit statements popup
	 */
	this.showEditStatementsPopup = function () {
		var table, tr, td_text, td_buttons, helper = new Helper();
		$('#' + popupEditStatementId).modal('show');
		$('#' + popupEditStatementWarning).hide();

		// top row
		table = $('<table>').attr({
			class: 'table table-condensed',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 5px 5px;'
		});
		td_text = $('<td>').html('<strong>' + _t(text) + '</strong>').css('text-align', 'center');
		td_buttons = $('<td>').html('<strong>' + _t(options) + '</strong>').css('text-align', 'center');
		table.append($('<tr>').append(td_text).append(td_buttons));

		// append a row for each statement
		$('#' + discussionSpaceId + ' li:not(:last-child) label:nth-child(odd)').each(function () {
			tr = helper.createRowInEditDialog($(this).text(), $(this).attr('for'), $(this).attr('id'));
			table.append(tr);

		});

		$('#' + popupEditStatementContentId).empty().append(table);
		$('#' + popupEditStatementTextareaId).hide();
		$('#' + popupEditStatementDescriptionId).hide();
		$('#' + popupEditStatementSubmitButtonId).hide();
		$('#' + proposalEditListGroupId).empty();
	};

	/**
	 * Display url sharing popup
	 */
	this.showUrlSharingPopup = function () {
		$('#' + popupUrlSharingId).modal('show');
		new AjaxSiteHandler().getShortenUrl(window.location);
		//$('#' + popupUrlSharingInputId).val(window.location);
	};

	/**
	 * Display url sharing popup
	 */
	this.showGeneratePasswordPopup = function () {
		$('#' + popupGeneratePasswordId).modal('show');
		$('#' + popupGeneratePasswordCloseButtonId).click(function(){
			$('#' + popupGeneratePasswordId).modal('hide');
		});
		$('#' + popupLoginCloseButton).click(function(){
			$('#' + popupGeneratePasswordId).modal('hide');
		});
	};

	/**
	 * Displays the edit text field
	 */
	this.showEditFieldsInEditPopup = function () {
		$('#' + popupEditStatementSubmitButtonId).fadeIn('slow');
		$('#' + popupEditStatementTextareaId).fadeIn('slow');
		$('#' + popupEditStatementDescriptionId).fadeIn('slow');
	};

	/**
	 * Hides the url sharing text field
	 */
	this.hideEditFieldsInEditPopup = function () {
		$('#' + popupEditStatementSubmitButtonId).hide();
		$('#' + popupEditStatementTextareaId).hide();
		$('#' + popupEditStatementDescriptionId).hide();
	};

	/**
	 * Hides the logfiles
	 */
	this.hideLogfileInEditPopup = function () {
		$('#' + popupEditStatementLogfileSpaceId).empty();
		$('#' + popupEditStatementLogfileHeaderId).html('');
	};

	/**
	 * Closes the popup and deletes all of its content
	 */
	this.hideEditStatementsPopup = function () {
		$('#' + popupEditStatementId).modal('hide');
		$('#' + popupEditStatementContentId).empty();
		$('#' + popupEditStatementLogfileSpaceId).text('');
		$('#' + popupEditStatementLogfileHeaderId).text('');
		$('#' + popupEditStatementTextareaId).text('');
		$('#' + popupEditStatementErrorDescriptionId).text('');
		$('#' + popupEditStatementSuccessDescriptionId).text('');
	};

	/**
	 * Closes the popup and deletes all of its content
	 */
	this.hideUrlSharingPopup = function () {
		$('#' + popupUrlSharingId).modal('hide');
		$('#' + popupUrlSharingInputId).val('');
	};

	/**
	 * Hides error description
	 */
	this.hideErrorDescription = function(){
		$('#' + discussionErrorDescriptionId).html('');
		$('#' + discussionErrorDescriptionSpaceId).hide();
	};

	/**
	 * Hides success description
	 */
	this.hideSuccessDescription = function(){
		$('#' + discussionSuccessDescriptionId).html('');
		$('#' + discussionSuccessDescriptionSpaceId).hide();
	};

	/**
	 * Hide some element for getting more space (hides last col-md-2)
	 */
	this.hideDiscussionDescriptionsNextElement = function() {
		$('#' + discussionsDescriptionId).attr('style', 'margin-bottom: 0px;').parent().parent().next().hide();
	};

	/**
	 * Displays all corrections in the popup
	 * @param jsonData json encoded return data
	 */
	this.displayStatementCorrectionsInPopup = function (jsonData) {
		var table, tr, td_text, td_date, td_author;

		// top row
		table = $('<table>');
		table.attr({
			id: 'edit_statement_table',
			class: 'table table-condensed',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 5px 5px;'
		});
		tr = $('<tr>');
		td_date = $('<td>');
		td_text = $('<td>');
		td_author = $('<td>');
		td_date.html('<b>Date</b>').css('text-align', 'center');
		td_text.html('<b>Text</b>').css('text-align', 'center');
		td_author.html('<b>Author</b>').css('text-align', 'center');
		tr.append(td_date);
		tr.append(td_text);
		tr.append(td_author);
		table.append(tr);

		$.each(jsonData, function displayStatementCorrectionsInPopupEach(key, val) {
			tr = $('<tr>');
			td_date = $('<td>');
			td_text = $('<td>');
			td_author = $('<td>');

			td_date.text(val.date);
			td_text.text(val.text);
			td_author.text(val.author);

			// append everything
			tr.append(td_date);
			tr.append(td_text);
			tr.append(td_author);
			table.append(tr);
		});

		$('#' + popupEditStatementLogfileSpaceId).empty().append(table);
	};

	/**
	 * Dispalys the 'how to write text '-popup, when the setting is not in the cookies
	 */
	this.displayHowToWriteTextPopup = function(){
		var cookie_name = 'HOW_TO_WRITE_TEXT',
			// show popup, when the user does not accepted the cookie already
			userAcceptedCookies = new Helper().isCookieSet(cookie_name);
		if (!userAcceptedCookies) {
			$('#' + popupHowToWriteText).modal('show');
		}

		// accept cookie
		$('#' + popupHowToWriteTextOkayButton).click(function(){
			$('#' + popupHowToWriteText).modal('hide');
			new Helper().setCookie(cookie_name);
		});
	};

	/**
	 * Updates an statement in the discussions list
	 * @param jsonData
	 */
	this.updateOfStatementInDiscussion = function (jsonData) {
		$('#td_' + jsonData.uid).text(jsonData.text);
		$('#' + jsonData.uid).text(jsonData.text);
	};

	/**
	 * Dialog based discussion modi
	 */
	this.setDisplayStyleAsDiscussion = function () {
		this.setImageInactive($('#' + displayStyleIconGuidedId));
		this.setImageActive($('#' + displayStyleIconIslandId));
		this.setImageActive($('#' + displayStyleIconExpertId));
		$('#' + islandViewContainerId).hide();
		$('#' + graphViewContainerId).hide();
		$('#' + discussionContainerId).show();
	};

	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsIsland = function () {
		this.setImageActive($('#' + displayStyleIconGuidedId));
		this.setImageInactive($('#' + displayStyleIconIslandId));
		this.setImageActive($('#' + displayStyleIconExpertId));
		$('#' + islandViewContainerId).fadeIn('slow');
		$('#' + graphViewContainerId).hide();
	};

	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsGraphView = function () {
		this.setImageActive($('#' + displayStyleIconGuidedId));
		this.setImageActive($('#' + displayStyleIconIslandId));
		this.setImageInactive($('#' + displayStyleIconExpertId));
		$('#' + islandViewContainerId).hide();
		$('#' + discussionContainerId).hide();
		new GuiHandler().hideDiscussionError();
		new DiscussionGraph().showGraph();
	};

	/**
	 * Sets style attributes to default
	 */
	this.resetChangeDisplayStyleBox = function () {
		this.setDisplayStyleAsDiscussion();
	};

	/**
	 * Adds the inactive-image-class, which includes a grayfilter and blur
	 * @param imageElement <img>-Element
	 */
	this.setImageInactive = function(imageElement){
		imageElement.addClass('inactive-image');
	};

	/**
	 * Removes the inactive-image-class, which includes a grayfilter and blur
	 * @param imageElement <img>-Element
	 */
	this.setImageActive = function(imageElement){
		imageElement.removeClass('inactive-image');
	};
}