/*global $, jQuery, alert, startDiscussionText , addStatementButtonId , statementList , GuiHandler , firstOneText , addStatementButtonId , argumentList , adminsSpaceId , addStatementButtonId , statementList, argumentSentencesOpeners, addStatementContainerId, addStatementButtonId, discussionFailureRowId, discussionFailureMsgId, tryAgainDiscussionButtonId, discussionsDescriptionId, errorDescriptionId, radioButtonGroup, discussionSpaceId
*/

function GuiHandler() {
	'use strict';
	var interactionHandler;

	this.setHandler = function (externInteractionHandler) {
		interactionHandler = externInteractionHandler;
	};

	/**
	 * Sets given json content as position buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsPositions = function (jsonData) {
		var listitems = [], _this = new GuiHandler();
		this.setDiscussionsDescription(startDiscussionText);
		$.each($.parseJSON(jsonData), function setJsonDataToContentAsPositionsEach(key, val) {
			//listitems.push(_this.getKeyValAsInputButtonInLiWithType(key, val, false));
			listitems.push(_this.getKeyValAsInputInLiWithType(key, val, false, 'radio'));
		});

		// sanity check for an empty list
		if (listitems.length === 0) {
			this.setDiscussionsDescription(firstOneText + '<b>' + jsonData.currentStatementText + '</b>');
		}

		listitems.push(this.getKeyValAsInputInLiWithType(addStatementButtonId, newPositionRadioButtonText, false, 'radio'));

		this.addListItemsToDiscussionsSpace(listitems, statementListId);
	};

	/**
	 * Sets given json content as argument buttons in the discussions space
	 * @param jsonData data with json content
	 * @param isUserExplainingHisPosition true, when the prefix should be 'because', because user should explain his position
	 */
	this.setJsonDataToContentAsArguments = function (jsonData, isUserExplainingHisPosition) {
		var listitems = [], _this = new GuiHandler();

		$.each(jsonData, function setJsonDataToContentAsArgumentsEach(key, val) {
			// set text, if it not the current statement
			if (key !== 'currentStatementText') {
				// prefix, when it is the first justification
				var text = isUserExplainingHisPosition ? "Because " + val.text.substring(0, 1).toLowerCase() + val.text.substring(1, val.text.length) : val.text;
				listitems.push(_this.getKeyValAsInputInLiWithType(key, text, true, 'radio'));
			}
		});

		// button, when the users agree and want to step back
		if (!isUserExplainingHisPosition){
			listitems.push(_this.getKeyValAsInputInLiWithType(goodPointTakeMeBackButtonId, goodPointTakeMeBackButtonText, true, 'radio'));
		}
		// button for new statements
		listitems.push(_this.getKeyValAsInputInLiWithType(addStatementButtonId, newArgumentRadioButtonText, true, 'radio'));
		_this.addListItemsToDiscussionsSpace(listitems, argumentList);
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonDataToAdminContent = function (jsonData) {
		var ulElement, trElement, tdElement, spanElement, i;
		tdElement = ['', '', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', '', ''];
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
		spanElement[1].text('firstname');
		spanElement[2].text('surname');
		spanElement[3].text('nickname');
		spanElement[4].text('email');
		spanElement[5].text('group');
		spanElement[6].text('last_logged');
		spanElement[7].text('registered');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			ulElement.append(trElement);
		}

		// add each user element
		$.each($.parseJSON(jsonData), function setJsonDataToAdminContentEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}
			tdElement[0].text(value.uid);
			tdElement[1].text(value.firstname);
			tdElement[2].text(value.surname);
			tdElement[3].text(value.nickname);
			tdElement[4].text(value.email);
			tdElement[5].text(value.group);
			tdElement[6].text(value.last_logged);
			tdElement[7].text(value.registered);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('table-hover');
			});
			ulElement.append(trElement);
		});

		$('#' + adminsSpaceId).empty();
		$('#' + adminsSpaceId).append(ulElement);
	};

	/**
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 * @param btnType for the input element
	 */
	this.setNewArgumentButtonOnly = function (val, isArgument, btnType) {
		var listitem = [];
		listitem.push(new GuiHandler().getKeyValAsInputInLiWithType(addStatementButtonId, val, isArgument, btnType));
		new GuiHandler().addListItemsToDiscussionsSpace(listitem, statementListId);
	};

	/**
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 * @param btnType for the input element
	 */
	this.setNewArgumentAndGoodPointButton = function (val, isArgument, btnType) {
		var listitems = [], gh = new GuiHandler();
		listitems.push(gh.getKeyValAsInputInLiWithType(goodPointTakeMeBackButtonId, goodPointTakeMeBackButtonText, true, 'radio'));
		listitems.push(gh.getKeyValAsInputInLiWithType(addStatementButtonId, val, isArgument, btnType));
		new GuiHandler().addListItemsToDiscussionsSpace(listitems, statementListId);
	};

	/**
	 * Setting a description in some p-tag for confrontation
	 * @param currentUserArgument
	 * @param confrontationArgument
	 */
	this.setDiscussionsDescriptionForConfrontation = function (currentUserArgument, confrontationArgument) {
		var pos = Math.floor(Math.random() * argumentSentencesOpeners.length), text = argumentSentencesOpeners[pos] + '<b>' + currentUserArgument + '</b>'
			+ ' However, other users argued that: ' + '<b>' + confrontationArgument + '</b>' + ' What do you think about that?';
		new GuiHandler().setDiscussionsDescription(text);
	};

	/**
	 * Setting a description in some p-tag for confrontation, whereby we have no justifications
	 * @param currentUserArgument
	 */
	this.setDiscussionsDescriptionWithoutConfrontation = function (currentUserArgument) {
		var pos = Math.floor(Math.random() * argumentSentencesOpeners.length), text = argumentSentencesOpeners[pos] + '<b>' + currentUserArgument + '</b>'
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
	 * Setting an error description in some p-tag
	 * @param text to set
	 */
	this.setErrorDescription = function (text) {
		$('#' + errorDescriptionId).text(text);
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 * @param type for the input element
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getKeyValAsInputInLiWithType = function (key, val, isArgument, type) {
		var liElement, inputElement, labelElement;
		liElement = $('<li>');
		liElement.attr({id: 'li_' + key});

		inputElement = $('<input>');
		inputElement.attr({id: key, type: type, value: val});
		//inputElement.attr({data-dismiss: 'modal'});

		// additional attributes for a button
		if (type === 'button') {
			inputElement.attr({class: 'button button-block btn btn-primary btn-default btn-discussion'});
		}

		// additional attributes for a radio button
		if (type === 'radio') {
			inputElement.attr({name: radioButtonGroup});
			// adding label for the value
			labelElement = '<label for="' + key + '">' + val + '</label>';
		}

		if (key === addStatementButtonId) {
			//inputElement.setAttribute('onclick', "new GuiHandler().setDisplayStylesOfAddArgumentContainer(true)");
		}


		if (type === 'button') {
			alert('check code for completion');
			if (isArgument) {
				inputElement.attr({onclick: "new InteractionHandler().argumentButtonWasClicked(this.id);"});
			} else {
				inputElement.attr({onclick: "new InteractionHandler().positionButtonWasClicked(this.id);"});
			}
		} else if (type === 'radio') {
			inputElement.attr({onclick: "new InteractionHandler().radioButtonChanged(this.id);"});
			inputElement.addClass((isArgument ? 'argument' : 'position'));
		}

		liElement.html(this.getFullHtmlTextOf(inputElement) + labelElement);

		return liElement;
	};

	/**
	 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
	 * @param items list with al items
	 * @param id for the ul list, where all items are appended
	 */
	this.addListItemsToDiscussionsSpace = function (items, id) {
		var ulElement;

		// wrap all elements into a list
		ulElement = $('<ul>');
		ulElement.attr({id: id});
		ulElement.append(items);

		// append them to the space
		$('#' + discussionSpaceId).append(ulElement);

		// hover style element for the list elements
		ulElement.children().hover(function () {
			$(this).toggleClass('table-hover');
		});
	};

	/**
	 * Adds a textarea with a little close button (both in a div tag) to a parend tag
	 * @param parentid id-tag of the parent element, where a textare should be added
	 */
	this.addTextareaAsChildInParent = function (parentid) {
		/**
		 * The structure is like:
		 * <div><textarea .../><button...></button></div>
		 */
		var area, parent, div, button, span, childCount;
		parent = $('#' + parentid);
		childCount = parent.children().length;

		div = $('<div>');
		div.attr({id: 'div' + childCount.toString()});

		button = $('<button>');
		button.attr({type: 'button',
			class: 'close',
			id: 'button' + childCount.toString()});

		span = $('<span>');
		//span.setAttribute('aria-hidden', 'true');
		span.html('&times;');

		area = $('<textarea>');
		area.attr({type: 'text',
			class: '',
			name: '',
			autocomplete: 'off',
			placeholder: 'example: I am the area number ' + (childCount).toString() + '.',
			value: '',
			id: 'area' + childCount.toString()});

		button.append(span);
		div.append(area);
		div.append(button);

		// remove everything on click
		button.attr({onclick: "this.parentNode.parentNode.removeChild(parentNode);"});

		// add everything
		parent.append(div);
	};

	/**
	 * Sets the new position as lsat child in discussion space or displays an error
	 * @param jsonData returned data
	 */
	this.setNewPositionAsLastChild = function (jsonData) {
		if (jsonData.result === 'failed') {
			if (jsonData.reason === 'empty text') {
				this.setErrorDescription('Your idea was not inserted, because your input text is empty.');
			} else if (jsonData.reason === 'duplicate'){
				this.setErrorDescription('Your idea was not inserted, because your idea is a duplicate.');
			} else {
				this.setErrorDescription('Your idea was not inserted due to an unkown error.');
			}
		} else {
			var newElement = this.getKeyValAsInputInLiWithType(jsonData.position.uid, jsonData.position.text, false, 'radio');
			$('#li_' + addStatementButtonId).before(newElement);
		}
	};

	/**
	 * Set some style attributes,
	 * @param isVisible
	 */
	this.setDisplayStylesOfAddArgumentContainer = function (isVisible, is_argument) {
		if (isVisible) {
			$('#' + addStatementContainerId).fadeIn('slow');
			$('#' + addStatementButtonId).disable = true;
			if (is_argument){
				$('#' + addStatementContainerH2Id).text(statementContainerH2TextIfArgument);
				$('#' + addStatementContainerMainInputId).hide();
				$('#' + leftPositionColumnId).show();
				$('#' + rightPositionColumnId).show();
				$('#' + sendNewStatementId).off("click");
				$('#' + sendNewStatementId).click(function () {
					new AjaxHandler().sendNewArgument();
				});
			} else {
				$('#' + addStatementContainerH2Id).text(statementContainerH2TextIfPosition);
				$('#' + addStatementContainerMainInputId).show();
				$('#' + leftPositionColumnId).hide();
				$('#' + rightPositionColumnId).hide();
				$('#' + sendNewStatementId).off("click");
				$('#' + sendNewStatementId).click(function () {
					new AjaxHandler().sendNewPosition($('#' + addStatementContainerMainInputId).val());
				});
			}
		} else {
			$('#' + addStatementContainerId).fadeOut('slow');
			$('#' + addStatementButtonId).disable = false;
		}
	};

	/**
	 * Shows an error on discussion space as well as a retry button
	 * @param error_msg message of the error
	 * @param id of the last choosen statement
	 * @param is_argument, if it was an argument
	 * @param try_again_fct the function, which should be called
	 */
	this.showDiscussionError = function (error_msg, id, is_argument, try_again_fct, is_only_justification) {
		$('#' + discussionFailureRowId).fadeIn('slow');
		$('#' + discussionFailureMsgId).text(error_msg);
		$('#' + tryAgainDiscussionButtonId).fadeIn('slow');

		var fct1, fct2;
		fct1 = 'new AjaxHandler().' + try_again_fct;
		fct1 += is_argument !== '' ? '(' + id : '(';
		fct1 += !is_only_justification ? ', ' + is_argument + '); ' : '); ';
		fct2 = '$(#' + tryAgainDiscussionButtonId + ').hide();';

		$('#' + tryAgainDiscussionButtonId).attr({onclick: fct1 + fct2});
	};

	/**
	 * Return the full HTML text of an given element
	 * @param element which should be translated
	 */
	this.getFullHtmlTextOf = function (element) {
		return $('<div>').append(element).html();
	};


	/**
	 * Dialog based discussion modi
	 */
	this.setDisplayStyleAsDiscussion  = function () {
		// todo setDisplayStyleAsDiscussion
	};

	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsProContraList  = function () {
		alert('todo: pro con');
		// todo setDisplayStyleAsProContraList
	};

	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsFullView  = function () {
		alert('todo: full view');
		// todo setDisplayStyleAsFullView
	};
}