/*global $, jQuery, alert, startDiscussionText , addStatementButtonId , statementList , GuiHandler , firstOneText , addStatementButtonId , adminsSpaceId , addStatementButtonId , statementList, argumentSentencesOpeners, addStatementContainerId, addStatementButtonId, discussionFailureRowId, discussionFailureMsgId, tryAgainDiscussionButtonId, discussionsDescriptionId, errorDescriptionId, radioButtonGroup, discussionSpaceId
*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

// TODO KICK ALL METHODS WHICH ARE NOT USED

function GuiHandler() {
	'use strict';
	var interactionHandler;

	this.setHandler = function (externInteractionHandler) {
		interactionHandler = externInteractionHandler;
	};

	/**
	 * Sets given json content as start statement buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsStartStatement = function (jsonData) {
		var listitems = [], _this = new GuiHandler();
		this.setDiscussionsDescription(startDiscussionText);
		$.each(jsonData, function setJsonDataToContentAsConclusionEach(key, val) {
			listitems.push(_this.getKeyValAsInputInLiWithType(val.uid, val.text, true, false));
		});

		// sanity check for an empty list
		if (listitems.length === 0) {
			// todo: is this even used?
			alert('discussion-guihandler: setJsonDataToContentAsStartStatement');
			this.setDiscussionsDescription(firstOneText + '<b>' + jsonData.currentStatementText + '</b>');
		}

		listitems.push(this.getKeyValAsInputInLiWithType(addStatementButtonId, newConclusionRadioButtonText, true));

		this.addListItemsToDiscussionsSpace(listitems, statementListId);
	};

	/**
	 * Sets given json content as start premisses buttons in the discussions space
	 * @param jsonData data with json content
	 * @param currentStatementText
	 */
	this.setJsonDataToContentAsStartPremisses = function (jsonData, currentStatementText) {
		var listitems = [], _this = new GuiHandler(), text;
		text = currentStatementText.text.substring(0, 1).toLowerCase() + currentStatementText.text.substring(1, currentStatementText.text.length);
		this.setDiscussionsDescription(sentencesOpenersRequesting[0] + ' <b>' + text + '</b>');
		$.each(jsonData, function setJsonDataToContentAsConclusionEach(key, val) {
			listitems.push(_this.getKeyValAsInputInLiWithType(val.uid, val.text, false, true));
		});

		listitems.push(this.getKeyValAsInputInLiWithType(addStatementButtonId, newPremisseRadioButtonText, true)); // TODO change button id

		this.addListItemsToDiscussionsSpace(listitems, statementListId);
	};

	/**
	 * Sets given json content as argument buttons in the discussions space
	 * @param jsonData data with json content
	 * @param isUserExplainingHisPosition true, when the prefix should be 'because', because user should explain his position
	 * @param isAvoidance true, when the given data should be used as avoidance
	 */
	this.setJsonDataToDiscussionContentAsArguments = function (jsonData, isUserExplainingHisPosition, isAvoidance) {
		var listitems = [], _this = new GuiHandler();

		$.each(jsonData, function setJsonDataToContentAsArgumentsEach(key, val) {
			// set text, if it not the current statement
			if (key !== 'currentStatementText') {
				// prefix, when it is the first justification
				var text = isUserExplainingHisPosition ? "Because " + val.text.substring(0, 1).toLowerCase() + val.text.substring(1, val.text.length) : val.text;
				listitems.push(_this.getKeyValAsInputInLiWithType(key, text, true));
			}
		});

		// button, when the users agree and want to step back
		if (!isUserExplainingHisPosition && !isAvoidance){
			listitems.push(_this.getKeyValAsInputInLiWithType(goodPointTakeMeBackButtonId, goodPointTakeMeBackButtonText, true));
		}

		// button for new statements
		if (!isAvoidance)
			listitems.push(_this.getKeyValAsInputInLiWithType(addStatementButtonId, newPremisseRadioButtonText, true));
		_this.addListItemsToDiscussionsSpace(listitems, argumentListId, isAvoidance);
	};

	/**
	 * Adds given json content as argument buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.addJsonDataToContentAsArguments = function (jsonData) {
		var _this = new GuiHandler(), text;
		$.each(jsonData, function addJsonDataToContentAsArgumentsEach(key, val) {
			// we only want attacking arguments
			if (val.is_supportive === '0') {
				if (val.text.toLowerCase() !== 'because') {
					text = "Because " + val.text.substring(0, 1).toLowerCase() + val.text.substring(1, val.text.length);
				} else {
					text = val.text;
				}
				$('#li_' + addStatementButtonId).before(_this.getKeyValAsInputInLiWithType(val.uid, text, true));
			}
		});

		// hover style element for the list elements
		$('#' + argumentListId).children().hover(function () {
			$(this).toggleClass('table-hover');
		});
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonDataToAdminContent = function (jsonData) {
		var ulElement, trElement, tdElement, spanElement, i;
		tdElement = ['', '', '', '', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', '', '', '', ''];
		ulElement = $('<table>');
		ulElement.attr({class: 'table table-condensed',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({class: 'font-semi-bold'});
		}

		// add header row
		spanElement[0].text('uid');
		spanElement[1].text('Firstname');
		spanElement[2].text('Surname');
		spanElement[3].text('Nickname');
		spanElement[4].text('E-Mail');
		spanElement[5].text('Group');
		spanElement[6].text('Last Action');
		spanElement[7].text('Last Login');
		spanElement[8].text('Registered');
		spanElement[9].text('Gender');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			ulElement.append(trElement);
		}

		// add each user element
		$.each(jsonData, function setJsonDataToAdminContentEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}

			tdElement[0].text(value.uid);
			tdElement[1].text(value.firstname);
			tdElement[2].text(value.surname);
			tdElement[3].text(value.nickname);
			tdElement[4].text(value.email);
			tdElement[5].text(value.group_uid);
			tdElement[6].text(value.last_action);
			tdElement[7].text(value.last_login);
			tdElement[8].text(value.registered);
			tdElement[9].text(value.gender);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('table-hover');
			});
			ulElement.append(trElement);
		});

		$('#' + adminsSpaceId).empty().append(ulElement);
	};

	/**
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 */
	this.setNewArgumentButtonOnly = function (val, isArgument) {
		var listitem = [], gh = new GuiHandler();
		listitem.push(gh.getKeyValAsInputInLiWithType(addStatementButtonId, val, isArgument));
		gh.addListItemsToDiscussionsSpace(listitem, statementListId);
	};

	/**
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 */
	this.setNewArgumentAndGoodPointButton = function (val, isArgument) {
		var listitems = [], gh = new GuiHandler();
		listitems.push(gh.getKeyValAsInputInLiWithType(goodPointTakeMeBackButtonId, goodPointTakeMeBackButtonText, true));
		listitems.push(gh.getKeyValAsInputInLiWithType(addStatementButtonId, val, isArgument));
		new GuiHandler().addListItemsToDiscussionsSpace(listitems, statementListId);
	};

	/**
	 * Setting a description in some p-tag for confrontation
	 * @param currentUserArgument
	 * @param confrontationArgument
	 */
	this.setDiscussionsDescriptionForConfrontation = function (currentUserArgument, confrontationArgument) {
		var pos = Math.floor(Math.random() * sentencesOpenersForArguments.length), text = sentencesOpenersForArguments[pos] + '<b>' + currentUserArgument + '</b>'
			+ '<br>However, other users argued that: ' + '<b>' + confrontationArgument + '</b>' + '<br><br>What do you think about that?';
		new GuiHandler().setDiscussionsDescription(text);
	};

	/**
	 * Setting a description in some p-tag for confrontation
	 * @param currentUserArgument
	 */
	this.setDiscussionsAvoidanceDescriptionForConfrontation = function (currentUserArgument) {
		var text = 'Or do you have a better argument for: ' + '<b>' + currentUserArgument + '</b>';
		new GuiHandler().setDiscussionsAvoidanceDescription(text);
	};

	/**
	 * Setting a description in some p-tag for confrontation, whereby we have no justifications
	 * @param currentUserArgument
	 */
	this.setDiscussionsDescriptionWithoutConfrontation = function (currentUserArgument) {
		var pos = Math.floor(Math.random() * sentencesOpenersForArguments.length), text = sentencesOpenersForArguments[pos] + '<b>' + currentUserArgument + '</b>'
			+ ' However, other users argued nothing yet:';
		new GuiHandler().setDiscussionsDescription(text);
	};

	/**
	 * Setting a description in some p-tag
	 * @param text to set
	 */
	this.setDiscussionsDescription = function (text) {
		$('#' + discussionsDescriptionId).html(text);
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
	this.setVisibilityOfDisplayStyleContainer = function (shouldBeVisibile, currentStatementText){
		if (shouldBeVisibile){
			$('#' + displayControlContainerId).fadeIn('slow');
			$('#' + islandViewContainerH4Id).html(islandViewHeaderText + ' <b>' + currentStatementText + '</b>');
		} else {
			$('#' + displayControlContainerId).hide();
		}
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isStartStatement if true, argumentButtonWasClicked is used, otherwise
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getKeyValAsInputInLiWithType = function (key, val, isStartStatement, isPremisse) {
		var liElement, inputElement, labelElement;
		liElement = $('<li>');
		liElement.attr({id: 'li_' + key});

		inputElement = $('<input>');
		inputElement.attr({id: key, type: 'radio', value: val});
		//inputElement.attr({data-dismiss: 'modal'});

		inputElement.attr({name: radioButtonGroup});
		// adding label for the value
		labelElement = '<label for="' + key + '">' + val + '</label>';

		inputElement.attr({onclick: "new InteractionHandler().radioButtonChanged(this.id);"});
		if (isStartStatement){ inputElement.addClass('start'); }
		if (isPremisse){ inputElement.addClass('premisse'); }

		liElement.html(this.getFullHtmlTextOf(inputElement) + labelElement);

		return liElement;
	};

	/**
	 * Displays given data in the island view
	 * @param jsonData json encoded dictionary
	 */
	this.displayDataInIslandView = function (jsonData){
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
		$('#' + leftIslandId).empty().append(ulProElement);
		$('#' + rightIslandId).empty().append(ulConElement);

	};

	/**
	 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
	 * @param items list with al items
	 * @param id for the ul list, where all items are appended
	 * @param isAvoidance true, when the given data should be used as avoidance
	 */
	this.addListItemsToDiscussionsSpace = function (items, id, isAvoidance) {
		var ulElement;

		// wrap all elements into a list
		ulElement = $('<ul>');
		ulElement.attr({id: id});
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
	 */
	this.addTextareaAsChildInParent = function (parentid, identifier) {
		/**
		 * The structure is like:
		 * <div><textarea .../><button...></button></div>
		 */
		var area, parent, div, div_content, button, span, childCount, div_dropdown;
		parent = $('#' + parentid);
		childCount = parent.children().length;

		div = $('<div>');
		div.attr({class: 'row', id: 'div' + childCount.toString()});

		div_content = $('<div>');
		div_content.attr({id: 'div-content-' + childCount.toString()});

		button = $('<button>');
		button.attr({type: 'button',
			class: 'close',
			id: 'button_' + identifier + childCount.toString()});

		span = $('<span>');
		span.html('&times;');

		area = $('<textarea>');
		area.attr({type: 'text',
			class: '',
			name: '',
			autocomplete: 'off',
			value: '',
			id: 'textarea_' + identifier + childCount.toString()});

		button.append(span);
		div_dropdown = this.getDropdownWithSentencesOpeners(identifier, childCount.toString());
		div_content.append(area);
		div_content.append(button);

		// remove everything on click
		button.attr({onclick: "this.parentNode.parentNode.removeChild(parentNode);"});

		// add everything
		div_dropdown.attr('class', 'col-md-3');
		div_content.attr('class', 'col-md-9');
		div.append(div_dropdown);
		div.append(div_content);
		parent.append(div);

		this.setDropdownClickListener(identifier, childCount.toString());
	};

	/**
	 * Creates dropdown button
	 * @param identifier
	 * @param number
	 * @returns {jQuery|HTMLElement|*}
	 */
	this.getDropdownWithSentencesOpeners = function (identifier, number) {
		var dropdown, button, span, ul, li_content, li_header, i, a, btn_id, a_id, h = new Helper(), sentencesOpeners;
		sentencesOpeners = identifier == id_left ? sentencesOpenersArguingWithAgreeing : sentencesOpenersArguingWithDisagreeing;

		// div tag for the dropdown
		dropdown = $('<div>');
		dropdown.attr('id', 'div-' + identifier + '-dropdown-' + number);
		dropdown.attr('class', 'dropdown');

		// button with span element
		span = $('<span>');
		span.attr('class', 'caret');
		button = $('<button>');
		button.attr('class', 'btn btn-default dropdown-toggle ' + (identifier.toLowerCase()  == 'left' ? 'btn-success' : 'btn-danger'));
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
		for (i=0; i < sentencesOpenersInforming.length; i++) {
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
		sentencesOpeners = identifier == id_left ? sentencesOpenersArguingWithAgreeing : sentencesOpenersArguingWithDisagreeing;

		// add clicks
		for (i = 0; i < sentencesOpenersInforming.length + sentencesOpeners.length; i++) {
			a_id = identifier + '-sentence-opener-' + i;
			$('#' + a_id).click(function () {
				$('#' + identifier + '-dropdown-sentences-openers-' + number).html($(this).text() + '<span class="caret"></span>');
			});
		}
	};

	/**
	 * Sets the new position as lsat child in discussion space or displays an error
	 * @param jsonData returned data
	 */
	this.setNewPositionAsLastChild = function (jsonData) {
		if (jsonData.result === 'failed') {
			if (jsonData.reason === 'empty text') {			this.setErrorDescription(notInsertedErrorBecauseEmpty);
			} else if (jsonData.reason === 'duplicate'){	this.setErrorDescription(notInsertedErrorBecauseDuplicate);
			} else {										this.setErrorDescription(notInsertedErrorBecauseUnknown);
			}
		} else {
			var newElement = this.getKeyValAsInputInLiWithType(jsonData.position.uid, jsonData.position.text, false);
			$('#li_' + addStatementButtonId).before(newElement);
			new GuiHandler().setSuccessDescription(addedEverything);
		}
	};

	/**
	 * Set some style attributes,
	 * @param isVisible true, if the container should be displayed
	 * @param is_argument true, if we have an argument
	 */
	this.setDisplayStylesOfAddArgumentContainer = function (isVisible, is_argument) {
		if (isVisible) {
			$('#' + leftPositionTextareaId).empty();
			$('#' + rightPositionTextareaId).empty();
			$('#' + addStatementContainerId).fadeIn('slow');
			$('#' + addStatementButtonId).disable = true;
			if (is_argument){
				var statement = $('#' + discussionsDescriptionId + ' b:last-child').text();
				$('#' + addStatementContainerH4Id).text(argumentContainerH4TextIfPremisse + ' ' + statement);
				// given colors are the HHU colors. we could use bootstrap (text-success, text-danger) instead, but they are too dark
				$('#' + headingProPositionTextId).html(' I <span class=\'green-bg\'>agree</span> with <b>\'' + statement + '</b>\':');
				$('#' + headingConPositionTextId).html(' I <span class=\'red-bg\'>disagree</span> with <b>\'' + statement + '</b>\':');
				$('#' + addStatementContainerMainInputId).hide().focus();
				$('#' + leftPositionColumnId).show();
				$('#' + rightPositionColumnId).show();
				$('#' + sendNewStatementId).off('click').click(function () {
					new InteractionHandler().getArgumentsAndSendThem();
					var gh = new GuiHandler();
					gh.setErrorDescription('');
					gh.setSuccessDescription('');
				});
			} else {
				$('#' + addStatementContainerH4Id).text(argumentContainerH4TextIfConclusion);
				$('#' + addStatementContainerMainInputId).show();
				$('#' + leftPositionColumnId).hide();
				$('#' + rightPositionColumnId).hide();
				$('#' + sendNewStatementId).off('click').click(function () {
					new AjaxHandler().sendNewPosition($('#' + addStatementContainerMainInputId).val());
					var gh = new GuiHandler();
					gh.setErrorDescription('');
					gh.setSuccessDescription('');
				});
			}
			var gh = new GuiHandler();
			gh.addTextareaAsChildInParent(leftPositionTextareaId, id_left);
			gh.addTextareaAsChildInParent(rightPositionTextareaId, id_right);
		} else {
			$('#' + addStatementContainerId).fadeOut('slow');
			$('#' + addStatementButtonId).disable = false;
		}
	};

	/**
	 * Restets the values of the add statement container to default.
	 */
	this.resetAddStatementContainer = function () {
		$('#' + leftPositionTextareaId).empty();
		$('#' + rightPositionTextareaId).empty();
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
	 * Return the full HTML text of an given element
	 * @param element which should be translated
	 */
	this.getFullHtmlTextOf = function (element) {
		return $('<div>').append(element).html();
	};

	/**
	 * Check whether the edit button should be visible or not
	 */
	this.resetAndDisableEditButton = function() {
		var list_id, count, statement, uid;
		count = 0;
		list_id = $('#' + statementListId + ' > li').children().length > 0 ? statementListId : argumentListId;
		$('#' + list_id + ' > li').children().each(function () {
			statement = $(this).val();
			uid = $(this).attr("id");
			// do we have a child with input or just the label?
			if ($(this).prop("tagName").toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid)) {
				count += 1;
			}
		});

		// do we have an statement there?
		if (count==0){
			$('#' + editStatementButtonId).fadeOut('slow');
		} else {
			$('#' + editStatementButtonId).fadeIn('slow');
		}
	};

	/**
	 * Opens the edit statements popup
	 */
	this.displayEditStatementsPopup = function(){
		var table, tr, td_text, td_buttons, list_id, i, edit_button, log_button, statement, uid, type;
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
			style: 'border-collapse: separate; border-spacing: 5px 5px;'});
		tr = $('<tr>');
		td_text = $('<td>');
		td_buttons = $('<td>');
		td_text.html('<b>Text</b>').css('text-align','center');
		td_buttons.html('<b>Options</b>').css('text-align','center');
		tr.append(td_text);
		tr.append(td_buttons);
		table.append(tr);

		// do we have an argument or a position?
		list_id = $('#' + statementListId + ' > li').children().length > 0 ? statementListId : argumentListId;
		i = 1;
		uid = 0;
		// append a row for each statement
		$('#' + list_id + ' > li').children().each(function (){
			statement = $(this).val();
			uid = $(this).attr("id");
			type = $(this).attr("class");
			// do we have a child with input or just the label?
		    if ($(this).prop("tagName").toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid)) {
				// create new items
				tr = $('<tr>');
				td_text = $('<td>').attr({id: 'edit_statement_td_text_' + i});
				td_buttons = $('<td>').css('text-align','center');
				edit_button = $('<input>');
				log_button = $('<input>');
				edit_button.css('margin', '2px');
				log_button.css('margin', '2px');

				// set attributes, text, ...
				td_text.text(statement);

				// some attributes and functions for the edit button
				edit_button.attr({id:'edit-statement',
					type: 'button',
					value: 'edit',
					class: 'btn-sm btn button-primary',
					statement_type: type,
					statement_text: statement,
					statement_id: uid,
					index: i
				}).click(function edit_button_click () {
					$('#' + popupEditStatementTextareaId).text($(this).attr('statement_text')).prop('disabled', false);
					$('#' + popupEditStatementSubmitButtonId).attr({
						statement_type: $(this).attr('statement_type'),
						statement_text: $(this).attr('statement_text'),
						statement_id: $(this).attr('statement_id')
					});
					$('#edit_statement_table td').removeClass('table-hover');
					$('#edit_statement_td_index_' + $(this).attr('index')).addClass('table-hover');
					$('#edit_statement_td_text_' + $(this).attr('index')).addClass('table-hover');
					$('#' + popupErrorDescriptionId).text('');
					$('#' + popupSuccessDescriptionId).text('');
					new GuiHandler().shouldHideEditFieldsinEditPopup(true);
				}).hover(function edit_button_hover () {
					$(this).toggleClass('btn-primary', 400);
				});

				// show logfile
				log_button.attr({id:'show_log_of_statement',
					type: 'button',
					value: 'changelog',
					class: 'btn-sm btn button-primary',
					statement_type: type,
					statement_text: statement,
					statement_id: uid,
					index: i
				}).click(function log_button_click () {
					$('#' + popupEditStatementLogfileHeaderId).html('Logfile for: <b>' + $(this).attr('statement_text') + '</b>');
					$('#' + popupErrorDescriptionId).text('');
					$('#' + popupSuccessDescriptionId).text('');
					new AjaxHandler().getLogfileForStatement($(this).attr('statement_id'), $(this).attr('statement_type') == 'argument');
					new GuiHandler().shouldHideEditFieldsinEditPopup(false);
				}).hover(function log_button_hover () {
					$(this).toggleClass('btn-primary', 400);
				});

				// append everything
				td_buttons.append(edit_button);
				td_buttons.append(log_button);
				tr.append(td_text);
				tr.append(td_buttons);
				table.append(tr);
				i = i + 1; // increasing index
			}
		});

		$('#' + popupEditStatementContentId).empty().append(table);
		$('#' + popupEditStatementTextareaId).hide();
		$('#' + popupEditStatementDescriptionId).hide();
		$('#' + popupEditStatementSubmitButtonId).hide().click(function edit_statement_click () {
			statement = $('#' + popupEditStatementTextareaId).val();
			$('#edit_statement_td_text_' + $(this).attr('statement_id')).text(statement);
			new AjaxHandler().sendCorrectureOfStatement($(this).attr('statement_id'), $(this).attr('statement_type') == 'argument', statement);
		});

		// on click: do ajax
		// ajax done: refresh current statement with new text
	};

	/**
	 * Displays or hide the edit text field
	 * @param isVisible
	 */
	this.shouldHideEditFieldsinEditPopup = function (isVisible){
		if (isVisible){
			$('#' + popupEditStatementSubmitButtonId).fadeIn('slow');
			$('#' + popupEditStatementTextareaId).fadeIn('slow');
			$('#' + popupEditStatementDescriptionId).fadeIn('slow');
		} else {
			$('#' + popupEditStatementSubmitButtonId).hide();
			$('#' + popupEditStatementTextareaId).hide();
			$('#' + popupEditStatementDescriptionId).hide();
		}
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
			style: 'border-collapse: separate; border-spacing: 5px 5px;'});
		tr = $('<tr>');
		td_date = $('<td>');
		td_text = $('<td>');
		td_author = $('<td>');
		td_date.html('<b>Date</b>').css('text-align','center');
		td_text.html('<b>Text</b>').css('text-align','center');
		td_author.html('<b>Author</b>').css('text-align','center');
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
		var is_argument = jsonData.is_argument == '1', list_id;

		// do we have an argument or a position?
		list_id = is_argument ? statementListId : argumentListId;
		// append a row for each statement
		$('#li_' + jsonData.uid + ' input').val(jsonData.text);
		$('#li_' + jsonData.uid + ' label').text(jsonData.text);
	};

	/**
	 * Dialog based discussion modi
	 */
	this.setDisplayStyleAsDiscussion  = function () {
		$('#' + islandViewContainerId).hide();
	};

	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsProContraList  = function () {
		$('#' + islandViewContainerId).fadeIn('slow');
		new AjaxHandler().getAllArgumentsForIslandView();
	};

	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsFullView  = function () {
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