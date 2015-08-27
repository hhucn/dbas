/*global $, jQuery, discussionsDescriptionId, discussionContainerId, discussionSpaceId, discussionAvoidanceSpaceId */

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
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 *
	this.setNewArgumentButtonOnly = function (val, isArgument) {
		var listitem = [], gh = new GuiHandler();
		listitem.push(gh.getKeyValAsInputInLiWithType(addReasonButtonId, val, isArgument, false, false, ''));
		gh.addListItemsToDiscussionsSpace(listitem);
	};
	*/

	/**
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 *
	this.setNewArgumentAndGoodPointButton = function (val, isArgument) {
		var listitems = [], gh = new GuiHandler();
		listitems.push(gh.getKeyValAsInputInLiWithType(goodPointTakeMeBackButtonId, goodPointTakeMeBackButtonText, true, false, false, ''));
		listitems.push(gh.getKeyValAsInputInLiWithType(addReasonButtonId, val, isArgument, false, false, ''));
		new GuiHandler().addListItemsToDiscussionsSpace(listitems);
	};
	*/

	/**
	 * Setting a description in some p-tag for confrontation
	 * @param currentUserArgument
	 * @param confrontationArgument
	 *
	this.setDiscussionsDescriptionForConfrontation = function (currentUserArgument, confrontationArgument) {
		var pos = Math.floor(Math.random() * sentencesOpenersForArguments.length), text = sentencesOpenersForArguments[pos] + '<b>' + currentUserArgument + '</b>'
			+ '<br>' + otherParticipantsThinkThat + ': ' + '<b>' + confrontationArgument + '</b>' + '<br><br>What do you think about that?';
		new GuiHandler().setDiscussionsDescription(text);
	};
	*/

	/**
	 * Setting a description in some p-tag for confrontation
	 * @param currentUserArgument
	 *
	this.setDiscussionsAvoidanceDescriptionForConfrontation = function (currentUserArgument) {
		var text = 'Or do you have a better argument for: ' + '<b>' + currentUserArgument + '</b>';
		new GuiHandler().setDiscussionsAvoidanceDescription(text);
	};
	*/

	/**
	 * Setting a description in some p-tag for confrontation, whereby we have no justifications
	 * @param currentUserArgument
	 *
	this.setDiscussionsDescriptionWithoutConfrontation = function (currentUserArgument) {
		var pos = Math.floor(Math.random() * sentencesOpenersForArguments.length), text = sentencesOpenersForArguments[pos] + '<b>' + currentUserArgument + '</b>'
			+ ' However, other users argued nothing yet:';
		new GuiHandler().setDiscussionsDescription(text);
	};
	*/

	/**
	 * Setting a description in some p-tag without mouse over
	 * @param text to set
	 */
	this.setDiscussionsDescription = function (text) {
		this.setDiscussionsDescription(text, text, {title: '', text: ''});
	};

	/**
	 * Setting a description in some p-tag with mouse over
	 * @param text to set
	 * @param mouseover hover-text
	 * @param additionalAttributesAsDict additional attribute
	 */
	this.setDiscussionsDescription = function (text, mouseover, additionalAttributesAsDict) {
		$('#' + discussionsDescriptionId).html(text).attr('title', mouseover);
		if (additionalAttributesAsDict !== null)
			$.each(additionalAttributesAsDict, function setDiscussionsDescriptionEach(key, val) {
				$('#' + discussionsDescriptionId).attr(key, val);
			});
	};

	/**
	 * Setting a description in some p-tag
	 * @param text to set
	 */
	this.setDiscussionsAvoidanceDescription = function (text) {
		$('#' + discussionsAvoidanceDescriptionId).html(text);
	};

	/**
	 * Setting an error description in some p-tag
	 * @param text to set
	 */
	this.setErrorDescription = function (text) {
		$('#' + discussionErrorDescriptionId).text(text);
	};

	/**
	 * Setting a success description in some p-tag
	 * @param text to set
	 */
	this.setSuccessDescription = function (text) {
		$('#' + discussionSuccessDescriptionId).text(text);
	};

	/**
	 * Sets the visibility of the island view conainter
	 * @param shouldBeVisibile true, when it should be visible
	 * @param currentStatementText current user statement
	 */
	this.setVisibilityOfDisplayStyleContainer = function (shouldBeVisibile, currentStatementText) {
		if (shouldBeVisibile) {
			$('#' + displayControlContainerId).fadeIn('slow');
			$('#' + islandViewContainerH4Id).html(islandViewHeaderText + ' <b>' + currentStatementText + '</b>');
		} else {
			$('#' + displayControlContainerId).hide();
		}
	};

	/**
	 * Displays given data in the island view
	 * @param jsonData json encoded dictionary
	 */
	this.displayDataInIslandView = function (jsonData) {
		var liElement, ulProElement, ulConElement;
		ulProElement = $('<ul>');
		ulConElement = $('<ul>');

		// get all values as text in list
		$.each(jsonData, function displayDataInIslandViewEach(key, val) {
			// is there a con or pro element?
			if (key.indexOf('pro') == 0) {
				liElement = $('<li>');
				liElement.text(val.text);
				ulProElement.append(liElement);
			} else if (key.indexOf('con') == 0) {
				liElement = $('<li>');
				liElement.text(val.text);
				ulConElement.append(liElement);
			}
		});

		// append in divs
		$('#' + proIslandId).empty().append(ulProElement);
		$('#' + conIslandId).empty().append(ulConElement);

	};

	/**
	 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
	 * @param items list with al items
	 * @param isAvoidance true, when the given data should be used as avoidance
	 */
	this.addListItemsToDiscussionsSpace = function (items, isAvoidance) {
		var ulElement;

		// wrap all elements into a list
		ulElement = $('<ul>');
		ulElement.append(items);

		// append them to the space
		if (isAvoidance)
			$('#' + discussionAvoidanceSpaceId).append(ulElement);
		else
			$('#' + discussionSpaceId).append(ulElement);

		// hover style element for the list elements
		ulElement.children().hover(function () {
			$(this).toggleClass('table-hover');
		});
	};

	/**
	 * Adds a textarea with a little close button (both in a div tag) to a parend tag
	 * @param parentid id-tag of the parent element, where a textare should be added
	 * @param identifier additional id
	 * @param is_statement
	 */
	this.addTextareaAsChildInParent = function (parentid, identifier, is_statement) {
		/**
		 * The structure is like:
		 * <div><textarea .../><button...></button></div>
		 */
		var area, parent, div, div_content, button, span, childCount, div_dropdown;
		parent = $('#' + parentid);
		childCount = parent.children().length;

		div = $('<div>');
		div.attr({
			class: 'row',
			id: 'div' + childCount.toString()
		});

		div_content = $('<div>');
		div_content.attr({
			id: 'div-content-' + childCount.toString()
		});

		button = $('<button>');
		button.attr({
			type: 'button',
			class: 'close',
			id: 'button_' + identifier + childCount.toString()
		});

		span = $('<span>');
		span.html('&times;');

		area = $('<textarea>');
		area.attr({
			type: 'text',
			class: '',
			name: '',
			autocomplete: 'off',
			value: '',
			id: 'textarea_' + identifier + childCount.toString()
		});

		button.append(span);
		div_dropdown = this.getDropdownWithSentencesOpeners(identifier, childCount.toString());
		div_content.append(area);
		div_content.append(button);

		// remove everything on click
		button.attr({
			onclick: "this.parentNode.parentNode.removeChild(parentNode);"
		});

		// add everything
		div_dropdown.attr('class', 'col-md-3');
		div_content.attr('class', 'col-md-9');
		div.append(div_dropdown);
		div.append(div_content);
		parent.append(div);

		if (is_statement) {
			div_dropdown.show();
		} else {
			div_dropdown.hide();
		}

		this.setDropdownClickListener(identifier, childCount.toString());
	};

	/**
	 * Creates dropdown button
	 * @param identifier
	 * @param number
	 * @returns {jQuery|HTMLElement|*}
	 */
	this.getDropdownWithSentencesOpeners = function (identifier, number) {
		var dropdown, button, span, ul, li_content, li_header, i, a, btn_id, a_id, h = new Helper(),
			sentencesOpeners;
		sentencesOpeners = identifier == id_pro ? sentencesOpenersArguingWithAgreeing : sentencesOpenersArguingWithDisagreeing;

		// div tag for the dropdown
		dropdown = $('<div>');
		dropdown.attr('id', 'div-' + identifier + '-dropdown-' + number);
		dropdown.attr('class', 'dropdown');

		// button with span element
		span = $('<span>');
		span.attr('class', 'caret');
		button = $('<button>');
		button.attr('class', 'btn btn-default dropdown-toggle ' + (identifier.toLowerCase() == 'left' ? 'btn-success' : 'btn-danger'));
		button.attr('type', 'button');
		btn_id = identifier + '-dropdown-sentences-openers-' + number;
		button.attr('id', btn_id);
		button.attr('data-toggle', 'dropdown');
		button.text(identifier.toLowerCase() == 'left' ? agreeBecause : disagreeBecause);
		button.append(span);
		dropdown.append(button);

		ul = $('<ul>');
		ul.attr('class', 'dropdown-menu');
		ul.attr('role', 'menu');

		// first categorie
		li_header = $('<li>');
		li_header.attr('class', 'dropdown-header');
		li_header.text('Argue');
		ul.append(li_header);
		for (i = 0; i < sentencesOpeners.length; i++) {
			li_content = $('<li>');
			a_id = identifier + '-sentence-opener-' + i;
			a = h.getATagForDropDown(a_id, clickToChoose + ': ' + sentencesOpeners[i], sentencesOpeners[i]);
			li_content.append(a);
			ul.append(li_content);
		}

		// second categorie
		li_header = $('<li>');
		li_header.attr('class', 'dropdown-header');
		li_header.text('Inform');
		ul.append(li_header);
		for (i = 0; i < sentencesOpenersInforming.length; i++) {
			li_content = $('<li>');
			a_id = identifier + '-sentence-opener-' + (sentencesOpeners.length + i);
			a = h.getATagForDropDown(a_id, clickToChoose + ': ' + sentencesOpenersInforming[i], sentencesOpenersInforming[i]);
			li_content.append(a);
			ul.append(li_content);
		}

		// append everything
		dropdown.append(ul);

		return dropdown;
	};

	/**
	 *
	 * @param identifier
	 * @param number
	 */
	this.setDropdownClickListener = function (identifier, number) {
		var a_id, i, sentencesOpeners;
		sentencesOpeners = identifier == id_pro ? sentencesOpenersArguingWithAgreeing : sentencesOpenersArguingWithDisagreeing;

		// add clicks
		for (i = 0; i < sentencesOpenersInforming.length + sentencesOpeners.length; i++) {
			a_id = identifier + '-sentence-opener-' + i;
			$('#' + a_id).click(function () {
				$('#' + identifier + '-dropdown-sentences-openers-' + number).html($(this).text() + '<span class="caret"></span>');
			});
		}
	};

	/**
	 * Sets the new position as list child in discussion space or displays an error
	 * @param jsonData returned data
	 */
	this.setNewStatementAsLastChild = function (jsonData) {
		if (jsonData.result === 'failed') {
			if (jsonData.reason === 'empty text') {
				this.setErrorDescription(notInsertedErrorBecauseEmpty);
			} else if (jsonData.reason === 'duplicate') {
				this.setErrorDescription(notInsertedErrorBecauseDuplicate);
			} else {
				this.setErrorDescription(notInsertedErrorBecauseUnknown);
			}
		} else {
			var newElement = new Helper().getKeyValAsInputInLiWithType(jsonData.statement.uid, jsonData.statement.text, true, false, false, '');
			newElement.children().hover(function () {
				$(this).toggleClass('table-hover');
			});
			$('#li_' + addReasonButtonId).before(newElement);
			new GuiHandler().setSuccessDescription(addedEverything);
		}
	};

	/**
	 * Sets the new premisses as list child in discussion space or displays an error
	 * @param jsonData returned data
	 */
	this.setPremissesAsLastChild = function (jsonData) {
		var newElement, helper = new Helper();
		$.each(jsonData, function setPremissesAsLastChildEach(key, val) {
			if (key.substr(0, 3) == "pro") {
				newElement = helper.getKeyValAsInputInLiWithType(val.premissegroup_uid, val.text + '.', false, true, false, val.text);
				newElement.children().hover(function () {
					$(this).toggleClass('table-hover');
				});
				$('#li_' + addReasonButtonId).before(newElement);
			} else if (key.substr(0, 3) == "con") {
				// todo setPremissesAsLastChild contra premisses
			}
		});
		this.setDisplayStylesOfAddStatementContainer(false, false, false, false, false);
		$('#' + addReasonButtonId).attr('checked', false);

	};

	/**
	 * Set some style attributes,
	 * @param isVisible true, if the container should be displayed
	 * @param isStatement true, if we have an argument
	 * @param isStart
	 * @param isPremisse
	 * @param isArgument
	 */
	this.setDisplayStylesOfAddStatementContainer = function (isVisible, isStart, isPremisse, isStatement, isArgument) {
		var statement, attack, argument, conclusion,
			guihandler = new GuiHandler(),
			ajaxhandler = new AjaxHandler(),
			interactionhandler = new InteractionHandler();
		if (!isVisible) {
			$('#' + addStatementContainerId).fadeOut('slow');
			$('#' + addStatementContainerMainInputId).val('');
			$('#' + addReasonButtonId).disable = false;
			return;
		}

		// isVisible == true:
		$('#' + proPositionTextareaId).empty();
		$('#' + conPositionTextareaId).empty();
		$('#' + addStatementContainerId).fadeIn('slow');
		$('#' + addReasonButtonId).disable = true;

		if (isStatement) {
			$('#' + addStatementContainerH4Id).text(argumentContainerH4TextIfConclusion);
			$('#' + addStatementContainerMainInputId).show();
			$('#' + proPositionColumnId).hide();
			$('#' + conPositionColumnId).hide();
			$('#' + sendNewStatementId).off('click').click(function setDisplayStylesOfAddStatementContainerWhenStatement() {
				if (isStart) {
					ajaxhandler.sendNewStartStatement($('#' + addStatementContainerMainInputId).val());
				} else {
					alert('What now (I)? GuiHandler: setDisplayStylesOfAddStatementContainer');
				}
				guihandler.setErrorDescription('');
				guihandler.setSuccessDescription('');
			});

		} else if (isPremisse || isArgument) {
			statement = $('#' + discussionsDescriptionId).attr('text');
			$('#' + addStatementContainerH4Id).text(isPremisse ? argumentContainerH4TextIfPremisse : argumentContainerH4TextIfArgument);
			// given colors are the HHU colors. we could use bootstrap (text-success, text-danger) instead, but they are too dark
			$('#' + headingProPositionTextId).html(' I <span class=\'green-bg\'>agree</span> with: <b>' + statement + '</b>, because ...');
			$('#' + headingConPositionTextId).html(' I <span class=\'red-bg\'>disagree</span> with: <b>' + statement + '</b>, because ...');
			$('#' + addStatementContainerMainInputId).hide().focus();
			$('#' + proPositionColumnId).show();
			$('#' + conPositionColumnId).show();
			if (isPremisse)
				$('#' + sendNewStatementId).off('click').click(function setDisplayStylesOfAddStatementContainerWhenPremisse() {
					// conclusion = $('#' + discussionsDescriptionId).attr('conclusion_id');
					// attack = $('#' + discussionsDescriptionId).attr('attack');
					// argument = $('#' + discussionsDescriptionId).attr('related_argument');
					// conclusion = typeof conclusion === 'undefined' ? '' : conclusion;
					// attack = typeof attack === 'undefined' ? '' : attack;
					// argument = typeof argument === 'undefined' ? '' : argument;
					interactionhandler.getPremissesAndSendThem(false);
					guihandler.setErrorDescription('');
					guihandler.setSuccessDescription('');
				});
			else
				alert('Todo: How to insert something at this place?');
		} else {
			alert('What now (II)? GuiHandler: setDisplayStylesOfAddStatementContainer');
		}

		guihandler.addTextareaAsChildInParent(proPositionTextareaId, id_pro, isStatement);
		guihandler.addTextareaAsChildInParent(conPositionTextareaId, id_con, isStatement);
	};

	/**
	 * Restets the values of the add statement container to default.
	 */
	this.resetAddStatementContainer = function () {
		$('#' + proPositionTextareaId).empty();
		$('#' + conPositionTextareaId).empty();
	};

	/**
	 * Shows an error on discussion space as well as a retry button
	 * @param error_msg message of the error
	 */
	this.showDiscussionError = function (error_msg) {
		$('#' + discussionFailureRowId).fadeIn('slow');
		$('#' + discussionFailureMsgId).text(error_msg);
	};

	/**
	 * Check whether the edit button should be visible or not
	 */
	this.resetEditButton = function () {
		var is_editable = false, statement, uid, is_premisse, is_start;
		$('#' + discussionSpaceId + ' ul > li').children().each(function () {
			statement = $(this).val();
			uid = $(this).attr("id");
			is_premisse = $(this).hasClass('premisse');
			is_start = $(this).hasClass('start');
			// do we have a child with input or just the label?
			if ($(this).prop("tagName").toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid) || is_premisse || is_start) {
				is_editable = true;
				return false; // break
			}
		});

		// do we have an statement there?
		if (is_editable) {
			$('#' + editStatementButtonId).fadeIn('slow');
		} else {
			$('#' + editStatementButtonId).fadeOut('slow');
		}
	};

	/**
	 * Opens the edit statements popup
	 */
	this.displayEditStatementsPopup = function () {
		var table, tr, td_text, td_buttons, statement, uid, type, is_start, is_premisse, tmp, text_count, statement_id, text, i, helper = new Helper();
		$('#' + popupEditStatementId).modal('show');
		$('#' + popupEditStatementSubmitButtonId).hide();

		// each statement will be in a table with row: index, text, button for editing
		// more action will happen, if the button is pressed

		// top row
		table = $('<table>');
		table.attr({
			id: 'edit_statement_table',
			class: 'table table-condensed',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 5px 5px;'
		});
		tr = $('<tr>');
		td_text = $('<td>');
		td_buttons = $('<td>');
		td_text.html('<b>Text</b>').css('text-align', 'center');
		td_buttons.html('<b>Options</b>').css('text-align', 'center');
		tr.append(td_text);
		tr.append(td_buttons);
		table.append(tr);

		uid = 0;
		// append a row for each statement
		$('#' + discussionSpaceId + ' ul > li').children().each(function () {
			statement = $(this).val();
			if (statement.toLocaleLowerCase().indexOf('because ') == 0){
				statement = new Helper().startWithUpperCase(statement.substring(8));
			}
			uid = $(this).attr("id");
			type = $(this).attr("class");
			is_premisse = $(this).hasClass('premisse');
			is_start = $(this).hasClass('start');

			// TODO edit premisse groups
			if (typeof uid != 'undefined' && uid.indexOf('_') != -1){
				tmp = uid.split('_');
				uid = tmp[tmp.length -1];
			}

			// do we have a child with input or just the label?
			if ($(this).prop("tagName").toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid) || is_premisse || is_start) {

				// is this a premisse group with more than one text?
				if (typeof $(this).attr('text_count') !== typeof undefined && $(this).attr('text_count') !== false){
					text_count = $(this).attr('text_count');
					type = 'premissesgroup';

					for (i=1; i<=parseInt(text_count); i++) {
						statement_id = $(this).attr('text_' + i + '_statement_id');
						text = $(this).attr('text_' + i);
						tr = helper.createRowInEditDialog(statement_id, text, type);
						table.append(tr);
					}
				} else {
					tr = helper.createRowInEditDialog(uid, statement, type);
					table.append(tr);
				}
			}
		});

		$('#' + popupEditStatementContentId).empty().append(table);
		$('#' + popupEditStatementTextareaId).hide();
		$('#' + popupEditStatementDescriptionId).hide();
		$('#' + popupEditStatementSubmitButtonId).hide().click(function edit_statement_click() {
			statement = $('#' + popupEditStatementTextareaId).val();
			//$('#edit_statement_td_text_' + $(this).attr('statement_id')).text(statement);
			alert($(this).attr('statement_id') + "\n" + $(this).attr('callback_td'));
			new AjaxHandler().sendCorrectureOfStatement($(this).attr('statement_id'), $(this).attr('callback_td'), statement);
		});

		// on click: do ajax
		// ajax done: refresh current statement with new text
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
	 * Hides the edit text field
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
	this.closeEditStatementsPopup = function () {
		$('#' + popupEditStatementId).modal('hide');
		$('#' + popupEditStatementContentId).empty();
		$('#' + popupEditStatementLogfileSpaceId).text('');
		$('#' + popupEditStatementLogfileHeaderId).text('');
		$('#' + popupEditStatementTextareaId).text('');
		$('#' + popupErrorDescriptionId).text('');
		$('#' + popupSuccessDescriptionId).text('');
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
	 * Updates an statement in the discussions list
	 * @param jsonData
	 */
	this.updateOfStatementInDiscussion = function (jsonData) {
		// append a row for each statement
		$('#li_' + jsonData.uid + ' input').val(jsonData.text);
		$('#li_' + jsonData.uid + ' label').text(jsonData.text);
	};

	/**
	 * Dialog based discussion modi
	 */
	this.setDisplayStyleAsDiscussion = function () {
		$('#' + islandViewContainerId).hide();
	};

	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsProContraList = function () {
		$('#' + islandViewContainerId).fadeIn('slow');
		new AjaxHandler().getAllArgumentsForIslandView();
	};

	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsFullView = function () {
		$('#' + islandViewContainerId).hide();
	};

	/**
	 * Sets style attributes to default
	 */
	this.resetChangeDisplayStyleBox = function () {
		$('#' + scStyle1Id).attr('checked', true);
		$('#' + scStyle2Id).attr('checked', false);
		$('#' + scStyle3Id).attr('checked', false);
	};
}