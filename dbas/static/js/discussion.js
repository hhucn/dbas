/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

var addStatementButtonId = 'add-statement';
var addPositionButtonId = 'add-position';
var addStatementContainerId = 'add-statement-container';
var addStatementContainerH2Id = 'add-statement-container-h2';
var addStatementContainerMainInputId = 'add-statement-container-main-input';
var addProTextareaId = 'add-pro-textarea';
var addConTextareaId = 'add-con-textarea';
var adminsSpaceId = 'admins-space';
var argumentList = 'argument-list';
var closeStatementContainerId = 'closeStatementContainer';
var discussionsDescriptionId = 'discussions-description';
var discussionContainerId = 'discussion-container';
var discussionSpaceId = 'discussions-space';
var errorDescriptionId = 'error-description';
var leftPositionColumnId = 'left-position-column';
var leftPositionTextareaId = 'left-textareas';
var listAllUsersButtonId = 'list-all-users';
var insertStatementForm = 'insert_statement_form';
var restartDiscussionButtonId = 'restart-discussion';
var rightPositionColumnId = 'right-position-column';
var rightPositionTextareaId = 'right-textareas';
var radioButtonGroup = 'radioButtonGroup';
var startDiscussionButtonId = 'start-discussion';
var startDescriptionId = 'start-description';
var sendAnswerButtonId = 'send-answer';
var statementList = 'statement-list';

var argumentSentencesOpeners = [
	'Okay, you have got the opinion: ',
	'Interesting, your opinion is: ',
	'So you meant: ',
	'You have said, that: ',
	'So your opinion is: '];
var startDiscussionText = 'These are the current statements, given by users input. You can choose a' +
		' position, which is next to your own intention or add a new one.';
var firstOneText = 'You are the first one. Please add a new statement:';


function AjaxHandler() {
	'use strict';
	var guiHandler = new GuiHandler();
	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 * If done: call setJsonDataToContentAsPositions
	 * If fail: call setNewArgumentButtonOnly
	 */
	this.getAllPositionsAndSetInGui = function () {
		$.ajax({
			url: 'ajax_all_positions',
			type: 'GET',
			dataType: 'json'
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsPositions(data);
		}).fail(function () {
			alert('failed request');
			guiHandler.setNewArgumentButtonOnly();
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument has a connection to the
	 * position with given uid.
	 * @param ofPositionWithUid uid of clicked position
	 * @param shouldGetProArgument true, if the pro arguments should be fetched, false for the con
	 * @param numberOfReturnArguments number of arguments, which should be returned, -1 for all
	 */
	this.getProOrConArgumentsConnectedToPositionUidAndSetInGui = function (ofPositionWithUid, shouldGetProArgument, numberOfReturnArguments) {
		var url = shouldGetProArgument ? "ajax_pro_arguments_connected_to_position_uid" : "ajax_con_arguments_connected_to_position_uid";
		var no = typeof numberOfReturnArguments === 'undefined' || numberOfReturnArguments < -1 ? -1 : Math.round(numberOfReturnArguments);
		$.ajax({
			url: url,
			method: "POST",
			data: { uid : ofPositionWithUid, returnCount : no },
			dataType: "json"
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsArguments(data);
		}).fail(function () {
			alert('failed request');
			guiHandler.setNewArgumentButtonOnly();
		});
	};

	/**
	 * Send an ajax request for getting all pro or contra arguments as dicitonary uid <-> value. Every argument is for or against the
	 * the same position as the given argument uid.
	 * position with given uid
	 * @param ofPositionWithUid uid of clicked position
	 * @param shouldGetProArgument true, if the pro arguments should be fetched, false for the con
	 * @param numberOfReturnArguments number of arguments, which should be returned, -1 for all
	 */
	this.getProOrConArgumentsWhichAreAgainstOrForTheSamePositionForArgumentUidAndSetInGui = function (ofArgumentWithUid, shouldGetProArgument, numberOfReturnArguments) {
		var url = shouldGetProArgument ? "ajax_pro_arguments_against_same_positions_by_argument_uid" : "ajax_con_arguments_against_same_positions_by_argument_uid";
		var no = typeof numberOfReturnArguments === 'undefined' || numberOfReturnArguments < -1 ? -1 : Math.round(numberOfReturnArguments);
		$.ajax({
			url: url,
			method: "POST",
			data: { uid : ofArgumentWithUid, returnCount : no },
			dataType: "json"
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsArguments(data);
		}).fail(function () {
			alert('failed request');
			guiHandler.setNewArgumentButtonOnly();
		});
	};

	/**
	 * Request all users
	 */
	this.getAllUsersAndSetInGui = function () {
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json'
		}).done(function (data) {
			guiHandler.setJsonDataToAdminContent(data);
		}).fail(function () {
			alert('internal failure');
		});
	};
}


function GuiHandler() {
	'use strict';
	/**
	 * Sets given json content as position buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsPositions = function (jsonData) {
		var listitems = [], _this = this;
		this.setDiscussionsDescription(startDiscussionText);
		$.each(jsonData, function (key, val) {
			//listitems.push(_this.getKeyValAsInputButtonInLiWithType(key, val, true));
			listitems.push(_this.getKeyValAsInputRadioInLiWithType(key, val, true));
		});

		// sanity check for an empty list
		if (listitems.length === 0) {
			this.setDiscussionsDescription(firstOneText);
		}

		//listitems.push(this.getKeyValAsInputButtonInLiWithType(addStatementButtonId, 'Adding a new statement.', true));
		listitems.push(this.getKeyValAsInputRadioInLiWithType(addStatementButtonId, 'Adding a new position.', true));

		$('#' + discussionContainerId).show();
		this.addListItemsToDiscussionsSpace(listitems, statementList);
	};

	/**
	 * Sets given json content as argumen buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsArguments = function (jsonData) {
		var listitems = [], _this = this;
		$.each(jsonData, function (key, val) {
			//listitems.push(_this.getKeyValAsInputButtonInLiWithType(key, val, false));
			listitems.push(_this.getKeyValAsInputRadioInLiWithType(key, val, false));
		});

		// sanity check for an empty list
		if (listitems.length === 0) {
			this.setDiscussionsDescription(firstOneText);
		}

		//listitems.push(this.getKeyValAsInputButtonInLiWithType(addStatementButtonId, 'Adding a new position.', true));
		listitems.push(this.getKeyValAsInputRadioInLiWithType(addStatementButtonId, 'Adding a new argument.', true));
		this.addListItemsToDiscussionsSpace(listitems, argumentList);
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
						style: 'border-collapse: separate; border-spacing: 5px 5px;'});

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({class: 'font-semi-bold'});
		}

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

		$.each(jsonData, function (key, val) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}
			tdElement[0].text(val.uid);
			tdElement[1].text(val.firstname);
			tdElement[2].text(val.surname);
			tdElement[3].text(val.nickname);
			tdElement[4].text(val.email);
			tdElement[5].text(val.group);
			tdElement[6].text(val.last_logged);
			tdElement[7].text(val.registered);

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
	 */
	this.setNewArgumentButtonOnly = function () {
		alert('Todo 2');
		this.setDiscussionsDescription(firstOneText);
		var listitem = [];
		//listitem.push(this.getKeyValAsInputButtonInLiWithType(addStatementButtonId, 'Yeah, I will add a statement!', true));
		listitem.push(this.getKeyValAsInputRadioInLiWithType(addStatementButtonId, 'Yeah, I will add a statement!', true, true));
		this.addListItemsToDiscussionsSpace(listitem, statementList);
	};

	/**
	 * Setting a description in some p-tag
	 * @param text to set
	 */
	this.setDiscussionsDescription = function (text) {
		$('#' + discussionsDescriptionId).text(text);
	};

	/**
	 * Setting an error description in some p-tag
	 * @param text to set
	 */
	this.setErrorDescription = function (text) {
		$('#' + errorDescriptionId).text(text);
	};

	/**
	 * Wrapper for getKeyValAsInputInLiWithType
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 * @returns {*} a button in li element
	 */
	this.getKeyValAsInputButtonInLiWithType = function (key, val, isArgument) {
		return this.getKeyValAsInputInLiWithType(key, val, isArgument, 'button');
	};

	/**
	 * Wrapper for getKeyValAsInputInLiWithType
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 * @returns {*} a radio button in li element
	 */
	this.getKeyValAsInputRadioInLiWithType = function (key, val, isArgument) {
		return this.getKeyValAsInputInLiWithType(key, val, isArgument, 'radio');
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
			labelElement = '<label for="' + key + '">&nbsp;&nbsp;' + val + '</label>';
		}

		if (key === addStatementButtonId) {
			//inputElement.setAttribute('onclick', "new GuiHandler().displayStyleOfAddArgumentContiner(true)");
		}
		if (type === 'button') {
			alert('check code for completion');
			if (isArgument) {
				inputElement.attr({onclick: "new InteractionHandler().argumentButtonWasClicked(this.id, this.value);"});
			} else {
				inputElement.attr({onclick: "new InteractionHandler().positionButtonWasClicked(this.id, this.value);"});
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
		var i, size, ulElement;

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
	this.addTextareaAsChildIn = function (parentid) {
		/**
		 * The structure is like:
		 * <div><textarea .../><button...></button></div>
		 */
		var area, parent, div, button, span, childCount;
		parent = $('#' + parentid);
		childCount = parent.children().length;
		//alert('TOD-O');

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
		button.attr({onclick: "var parentNode = this.parentNode;var grandParentNode = parentNode.parentNode;grandParentNode.removeChild(parentNode);"});

		// add everything
		parent.append(div);
	};

	/**
	 * Set some style attributes, 
	 * @param isVisible
	 */
	this.displayStyleOfAddArgumentContiner = function (isVisible) {
		if (isVisible) {
			$('#' + addStatementContainerId).show();
			$('#' + addStatementButtonId).disable = true;
		} else {
			$('#' + addStatementContainerId).hide();
			$('#' + addStatementButtonId).disable = false;
		}
	};

	/**
	 * Return the full HTML text of an given element
	 * @param element which should be translated
	 */
	this.getFullHtmlTextOf = function (element) {
		return $('<div>').append(element).html();
	};
}


function InteractionHandler() {
	'use strict';
	var guiHandler = new GuiHandler(), ajaxHandler = new AjaxHandler();
	/**
	 * Handler when an argument button was clicked
	 * @param value of the button
	 */
	this.argumentButtonWasClicked = function (id, value) {
		var pos, data;
		pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		guiHandler.setDiscussionsDescription(argumentSentencesOpeners[pos] + value + ' But why?');

		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		// add all positions
		ajaxHandler.getProOrConArgumentsConnectedToPositionUidAndSetInGui(id, true);

	};

	/**
	 * Handler when an position button was clicked
	 * @param value of the button
	 */
	this.positionButtonWasClicked = function (id, value) {
		var pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		guiHandler.setDiscussionsDescription(argumentSentencesOpeners[pos] + value + ' But an argument from the other side is:');

		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		// add all positions from the other side
		ajaxHandler.getProOrConArgumentsWhichAreAgainstOrForTheSamePositionForArgumentUidAndSetInGui(id, false);
	};

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 */
	this.radioButtonChanged = function (buttonId) {
		if ($('#' + addStatementButtonId).is(':checked')) {
			guiHandler.displayStyleOfAddArgumentContiner(true);
			$('#' + sendAnswerButtonId).hide();

			// get the second child, which is the label
			if ($('#' + addStatementButtonId).parent().children().eq(1).text().indexOf('position') >= 0) {
				$('#' + addStatementContainerH2Id).text('Please insert a new position');
				$('#' + addStatementContainerMainInputId).show();
			} else {
				$('#' + addStatementContainerH2Id).text('Please insert new arguments');
				$('#' + addStatementContainerMainInputId).hide();
			}
		} else {
			guiHandler.displayStyleOfAddArgumentContiner(false);
			$('#' + sendAnswerButtonId).show();
		}

		// enable or disable the send button
		$('#' + sendAnswerButtonId).prop('disabled', ($('input[name=' + radioButtonGroup + ']:checked') === 'undefined' ? true : false));
	};

	/**
	 * Defines the action for the send button
	 */
	this.sendAnswerButtonClicked = function () {
		var radioButton, id, value;
		radioButton = $('input[name=' + radioButtonGroup + ']:checked');
		id = radioButton.attr('id');
		value = radioButton.val();

		if (typeof id === 'undefined' || typeof value === 'undefined') {
			guiHandler.setErrorDescription('Please select a statement!');
		} else {
			guiHandler.setErrorDescription('');
			if (radioButton.hasClass('argument')) {
				this.argumentButtonWasClicked(id, value);
			} else {
				this.positionButtonWasClicked(id, value);
			}
		}
	};
}


/**
 * main function
 */
$(document).ready(function () {
	'use strict';
	var guiHandler = new GuiHandler(), ajaxHandler = new AjaxHandler(), interactionHandler = new InteractionHandler();

	$('#' + discussionContainerId).hide(); // hiding discussions container
	$('#' + addStatementContainerId).hide(); // hiding container for adding arguments

	// starts the discussion with getting all positions
	$('#' + startDiscussionButtonId).click(function () {
		$('#' + startDiscussionButtonId).hide(); // hides the start button
		$('#' + startDescriptionId).hide(); // hides the start description
		$('#' + restartDiscussionButtonId).show(); // show the restart button

		ajaxHandler.getAllPositionsAndSetInGui();
	});

	// handler for the send answer button
	$('#' + sendAnswerButtonId).click(function () {
		interactionHandler.sendAnswerButtonClicked();
	});

	// hide the restart button and add click function
	$('#' + restartDiscussionButtonId).hide(); // hides the restart button
	$('#' + restartDiscussionButtonId).click(function () {
		$('#' + startDiscussionButtonId).show(); // show the start description
		$('#' + restartDiscussionButtonId).hide(); // hide the restart button

		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionContainerId).hide();
	});

	// admin list all users button
	$('#' + listAllUsersButtonId).click(function () {
		if ($(this).val() === 'List all users') {
			ajaxHandler.getAllUsersAndSetInGui();
			$(this).val('Hide all users');
		} else {
			$('#' + adminsSpaceId).empty();
			$(this).val('List all users');
		}
	});

	// adding a textarea in the right column
	$('#' + addConTextareaId).click(function () {
		guiHandler.addTextareaAsChildIn(rightPositionTextareaId);
	});

	// adding a textarea in the left column
	$('#' + addProTextareaId).click(function () {

		guiHandler.addTextareaAsChildIn(leftPositionTextareaId);
	});

	// hiding the argument container, when the X button is clicked
	$('#' + closeStatementContainerId).click(function () {
		$('#' + addStatementContainerId).hide();
		$('#' + addStatementButtonId).enable = true;
		$('#' + addStatementButtonId).removeAttr('checked');
		$('#' + sendAnswerButtonId).hide();
	});
	
	// ajax loading animation
	$(document).on({
		ajaxStart: function() { $('body').addClass('loading'); },
		ajaxStop: function() { $('body').removeClass('loading'); }    
	});

});