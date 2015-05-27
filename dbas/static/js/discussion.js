/*global $, jQuery, alert, AjaxHandler, GuiHandler, InteractionHandler */

var addStatementButtonId = 'add-statement';
var addPositionButtonId = 'add-position';
var startDiscussionButtonId = 'start-discussion';
var restartDiscussionButtonId = 'restart-discussion';
var discussionContainerId = 'discussion-container';
var addArgumentContainerId = 'add-argument-container';
var addProTextareaId = 'add-pro-textarea';
var addConTextareaId = 'add-con-textarea';
var closeArgumentContainerId = 'closeArgumentContainer';
var startDescriptionId = 'start-description';
var discussionsDescriptionId = 'discussions-description';
var sendAnswerButtonId = 'send-answer';
var discussionSpaceId = 'discussions-space';
var rightPositionColumnId = 'right-position-column';
var leftPositionColumnId = 'left-position-column';
var rightPositionTextareaId = 'right-textareas';
var leftPositionTextareaId = 'left-textareas';

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
	 * If fail: call setOnlyNewArgumentButton
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
			guiHandler.setOnlyNewArgumentButton();
		});
	};

	/**
	 * Send an ajax request for getting all pro arguments as dicitonary uid <-> value
	 * If done: call
	 * If fail: call
	 * @param ofPositionWithUid
	 */
	this.getAllProArgumentsAndSetInGui = function (ofPositionWithUid) {
		$.ajax({
			url: "ajax_all_pro_arguments_by_uid",
			method: "POST",
			data: { uid : ofPositionWithUid },
			dataType: "json"
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsArguments(data);
		}).fail(function () {
			alert('failed request');
			guiHandler.setOnlyNewArgumentButton();
		});
	};

	/**
	 * Send an ajax request for getting all contra arguments as dicitonary uid <-> value
	 * If done: call
	 * If fail: call
	 * @param ofPositionWithUid
	 */
	this.getAllConArgumentsAndSetInGui = function (ofPositionWithUid) {
		$.ajax({
			url: "ajax_all_con_arguments_by_uid",
			method: "POST",
			data: { uid : ofPositionWithUid },
			dataType: "json"
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsArguments(data);
		}).fail(function () {
			alert('failed request');
			guiHandler.setOnlyNewArgumentButton();
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
		//listitems.push(this.getKeyValAsInputButtonInLiWithType(addStatementButtonId, 'Adding a new statement.', true));
		listitems.push(this.getKeyValAsInputRadioInLiWithType(addStatementButtonId, 'Adding a new statement.', true));

		$('#' + discussionContainerId).show();
		this.addListItemsToDiscussionsSpace(listitems, 'position-list');
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
		//listitems.push(this.getKeyValAsInputButtonInLiWithType(addStatementButtonId, 'Adding a new position.', true));
		listitems.push(this.getKeyValAsInputRadioInLiWithType(addStatementButtonId, 'Adding a new position.', true));
		this.addListItemsToDiscussionsSpace(listitems, 'argument-list');

	};

	/**
	 * Sets an "add statement" button as content
	 */
	this.setOnlyNewArgumentButton = function () {
		alert('Todo 2');
		this.setDiscussionsDescription(firstOneText);
		var listitem = [];
		//listitem.push(this.getKeyValAsInputButtonInLiWithType(addStatementButtonId, 'Yeah, I will add a statement!', true));
		listitem.push(this.getKeyValAsInputRadioInLiWithType(addStatementButtonId, 'Yeah, I will add a statement!', true, true));
		this.addListItemsToDiscussionsSpace(listitem, 'statement-list');
	};

	/**
	 * Setting a description in some p-tag
	 * @param text to set
	 */
	this.setDiscussionsDescription = function (text) {
		$('#' + discussionsDescriptionId).text(text);
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
			inputElement.attr({name: 'radioGroup'});
			// adding label for the value
			labelElement = '<label for="' + key + '">&nbsp;&nbsp;' + val + '</label>';
		}

		if (key === addStatementButtonId) {
			//inputElement.setAttribute('onclick', "new GuiHandler().displayStyleOfAddArgumentConter(true)");
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

		ulElement = $('<ul>');
		ulElement.attr({id: id});

		for (i = 0, size = items.length; i < size; i += 1) {
			ulElement.append(items[i]);
		}

		$('#' + discussionSpaceId).append(ulElement);
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

	this.displayStyleOfAddArgumentConter = function (isVisible) {
		if (isVisible) {
			$('#' + addArgumentContainerId).show();
			$('#' + addStatementButtonId).disable = true;
		} else {
			$('#' + addArgumentContainerId).hide();
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
		ajaxHandler.getAllProArgumentsAndSetInGui(id);

	};

	/**
	 * Handler when an position button was clicked
	 * @param value of the button
	 */
	this.positionButtonWasClicked = function (id, value) {
		var pos, ajaxHandler;
		pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		guiHandler.setDiscussionsDescription(argumentSentencesOpeners[pos] + value + ' But an argument from the other side is:');

		// clear the discussion space
		$('#' + discussionSpaceId).empty();

		// add all positions from the other side
		alert('Todo 1: How to navigate here?');
	};

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 */
	this.radioButtonChanged = function (buttonId) {
		if ($('#' + addStatementButtonId).is(':checked')) {
			guiHandler.displayStyleOfAddArgumentConter(true);
			$('#' + sendAnswerButtonId).hide();
		} else {
			guiHandler.displayStyleOfAddArgumentConter(false);
			$('#' + sendAnswerButtonId).show();
		}
	};
}


/**
 * main function
 */
$(document).ready(function () {
	'use strict';
	var guiHandler = new GuiHandler(), ajaxHandler = new AjaxHandler();

	$('#' + discussionContainerId).hide(); // hiding discussions container
	$('#' + addArgumentContainerId).hide(); // hiding container for adding arguments

	// starts the discussion with getting all positions
	$('#' + startDiscussionButtonId).on('click', function () {
		$('#' + startDiscussionButtonId).hide(); // hides the start button
		$('#' + startDescriptionId).hide(); // hides the start description
		$('#' + restartDiscussionButtonId).show(); // show the restart button

		ajaxHandler.getAllPositionsAndSetInGui();
	});

	// handler for the send answer button
	$('#' + sendAnswerButtonId).on('click', function () {

	});

	// hover style element for the list elements
	$('#' + discussionSpaceId + ' ul li').hover(function(){
	    $(this).addClass('hover');
		alert('fufu');
	}, function(){
	    $(this).removeClass('hover');
	});

	// hide the restart button and add click function
	$('#' + restartDiscussionButtonId).hide(); // hides the restart button
	$('#' + restartDiscussionButtonId).on('click', function () {
		$('#' + startDiscussionButtonId).show(); // show the start description
		$('#' + restartDiscussionButtonId).hide(); // hide the restart button

		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionContainerId).hide();
	});
	
	// adding a textarea in the right column
	$('#' + addConTextareaId).on('click', function () {
		guiHandler.addTextareaAsChildIn(rightPositionTextareaId);
	});

	// adding a textarea in the left column
	$('#' + addProTextareaId).on('click', function () {

		guiHandler.addTextareaAsChildIn(leftPositionTextareaId);
	});

	// hiding the argument container, when the X button is clicked
	$('#' + closeArgumentContainerId).on('click', function () {
		$('#' + addArgumentContainerId).hide();
		$('#' + addStatementButtonId).enable = true;
		$('#' + addStatementButtonId).removeAttr('checked');
		$('#' + sendAnswerButtonId).hide();

	});

});