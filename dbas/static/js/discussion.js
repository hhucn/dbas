/*global $, jQuery, alert, addListItemsToDiscussionsSpace, getAllPositions, getKeyValAsInputBtnInLiElement,
 setDiscussionsDescription, addTextareaAsChildIn, argumentButtonWasClicked, positionButtonWasClicked*/

var addStatementButtonId = 'add-statement';
var discussionSpaceId = 'discussions-space';
var argumentSentencesOpeners = [
	'Okay, you have got the opinion: ',
	'Interesting, your opinition is: ',
	'So you meant: ',
	'You have said, that: ',
	'So your opinion is: '];
var startDiscussionText = 'These are the current statements, given by users input. You can choose a' +
		' position, which is next to your own intention or add a new one.';
var firstOneText = 'You are the first one. Please add a new statement:';

function DiscussionHandler() {
	var guiHandler = new GuiHandler();

	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 * If done: call setJsonDataToContentAsPositions
	 * If fail: call setOnlyNewArgumentButton
	 */
	this.getAndSetAllPositions = function () {
		$.ajax({
			url: 'ajax_all_positions',
			type: 'GET',
			dataType: 'json'
		}).done(function (data) {
			guiHandler.setJsonDataToContentAsPositions(data);
		}).fail(function () {
			guiHandler.setOnlyNewArgumentButton();
		});
	};

	/**
	 * Send an ajax request for getting all pro arguments as dicitonary uid <-> value
	 * If done: call
	 * If fail: call
	 * @param ofPositionWithUid
	 */
	this.getAllProArguments = function (ofPositionWithUid) {
		var request = $.ajax({
			url: "ajax_all_pro_arguments_by_uid",
			method: "POST",
			data: { uid : ofPositionWithUid },
			dataType: "json"
		}).done(function (data) {
			return data;
		}).fail(function () {
			return 0;
		});
	};

	/**
	 * Send an ajax request for getting all contra arguments as dicitonary uid <-> value
	 * If done: call
	 * If fail: call
	 * @param ofPositionWithUid
	 */
	this.getAllConArguments = function (ofPositionWithUid) {
		var request = $.ajax({
			url: "ajax_all_con_arguments_by_uid",
			method: "POST",
			data: { uid : ofPositionWithUid },
			dataType: "json"
		}).done(function (data) {
			return data;
		}).fail(function () {
			return 0;
		});
	};
}

function GuiHandler() {

	/**
	 * Sets given json content as position buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsPositions = function (jsonData) {
		var listitems = [], _this = this;
		this.setDiscussionsDescription(startDiscussionText);
		$.each(jsonData, function (key, val) {
			listitems.push(_this.getKeyValAsInputBtnInLiElement(key, val, true));
		});
		listitems.push(this.getKeyValAsInputBtnInLiElement(addStatementButtonId, 'Adding a new statement.', true));

		$('#discussion-container').show();
		this.addListItemsToDiscussionsSpace(listitems, 'position-list');
	};

	/**
	 * Sets given json content as argumen buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsArguments = function (jsonData) {

	};

	this.setOnlyNewArgumentButton = function() {
		this.setDiscussionsDescription(firstOneText);
		listitems.push(this.getKeyValAsInputBtnInLiElement(addStatementButtonId, 'Yeah, I will add a statement!', true));
	};

	/**
	 * Setting a description in some p-tag
	 * @param text to set
	 */
	this.setDiscussionsDescription = function (text) {
		'use strict';
		$('#discussions-description').text(text);
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key
	 * @param val
	 * @returns {Element|*} an li tag with embedded input element
	 */
	this.getKeyValAsInputBtnInLiElement = function(key, val, isArgument) {
		'use strict';

		var liElement, inputElement;
		liElement = document.createElement('li');
		liElement.setAttribute('id', 'li_' + key);

		inputElement = document.createElement('input');
		inputElement.setAttribute('id', key);
		inputElement.setAttribute('type', 'button');
		inputElement.setAttribute('value', val);
		inputElement.setAttribute('class', 'button button-block btn btn-primary btn-default');
		inputElement.setAttribute('data-dismiss', 'modal');
		if (key === addStatementButtonId) {
			inputElement.setAttribute('onclick', "$('#add-argument-container').show();$('#'+addStatementButtonId).disable = true;");
		} else {
			if (isArgument) {
				inputElement.setAttribute('onclick', "new GuiHandler().argumentButtonWasClicked(this.value);");
			} else {
				inputElement.setAttribute('onclick', "new GuiHandler().positionButtonWasClicked(this.value);");
			}
		}

		liElement.appendChild(inputElement);
		return liElement;
	};

	/**
	 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
	 * @param items list with al items
	 * @param id for the ul list, where all items are appended
	 */
	this.addListItemsToDiscussionsSpace = function(items, id) {
		'use strict';
		var i, size, discussionsSpace, ulElement;

		discussionsSpace = document.getElementById(discussionSpaceId);
		ulElement = document.createElement('ul');
		ulElement.setAttribute('id', id);

		for (i = 0, size = items.length; i < size; i += 1) {
			ulElement.appendChild(items[i]);
		}

		discussionsSpace.appendChild(ulElement);
	};

	/**
	 * Adds a textarea with a little close button (both in a div tag) to a parend tag
	 * @param parentid id-tag of the parent element, where a textare should be added
	 */
	this.addTextareaAsChildIn = function(parentid) {
		'use strict';
		/**
		 * The structure is like:
		 * <div><textarea .../><button...></button></div>
		 */
		var area, parent, div, button, span, childCount;
		parent = document.getElementById(parentid);
		childCount = parent.childElementCount;

		div = document.createElement('div');
		div.setAttribute('id', 'div' + childCount.toString());

		button = document.createElement('button');
		button.setAttribute('type', 'button');
		button.setAttribute('class', 'close');
		button.setAttribute('data-dismiss', 'modal');
		button.setAttribute('aria-label', 'Close');
		button.setAttribute('id', 'button' + childCount.toString());

		span = document.createElement('span');
		span.setAttribute('aria-hidden', 'true');
		span.innerHTML = '&times;';

		area = document.createElement('textarea');
		area.setAttribute('type', 'text');
		area.setAttribute('class', '');
		area.setAttribute('name', '');
		area.setAttribute('autocomplete', 'off');
		area.setAttribute('placeholder', 'example: I am the area number ' + (childCount - 2).toString() + '.');
		area.setAttribute('value', '');
		area.setAttribute('id', 'area' + childCount.toString());

		button.appendChild(span);
		div.appendChild(area);
		div.appendChild(button);

		// remove everything on click
		button.setAttribute('onclick', "var parentNode = this.parentNode;var grandParentNode = parentNode.parentNode;grandParentNode.removeChild(parentNode);");

		// add everything
		parent.insertBefore(div, parent.childNodes[childCount + 1]);
	};

	/**
	 * Handler when an argument button was clicked
	 * @param value of the button
	 */
	this.argumentButtonWasClicked = function(value) {
		'use strict';
		var pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		setDiscussionsDescription(argumentSentencesOpeners[pos] + value + ' Can you choose a position therefore?');
	};

	/**
	 * Handler when an position button was clicked
	 * @param value of the button
	 */
	this.positionButtonWasClicked = function(value) {
		'use strict';
		var pos = Math.floor(Math.random() * argumentSentencesOpeners.length);
		setDiscussionsDescription(argumentSentencesOpeners[pos] + value + '. But ...');
	}
}


/**
 * main function
 */
$(document).ready(function () {
	'use strict';

	$('#discussion-container').hide(); // hiding discussions container
	$('#add-argument-container').hide(); // hiding container for adding arguments

	// starts the discussion with getting all positions
	$('#get-positions').on('click', function () {
		$('#get-positions').hide(); // hides the start button
		$('#start-description').hide(); // hides the start description

		var discussionHandler;
		discussionHandler = new DiscussionHandler();
		discussionHandler.getAndSetAllPositions();

	});

	// adding a textarea in the right column
	$('#add-con-textarea').on('click', function () {
		var guiHandler = new GuiHandler();
		guiHandler.addTextareaAsChildIn('right-position-column');
	});

	// adding a textarea in the left column
	$('#add-pro-textarea').on('click', function () {
		var guiHandler = new GuiHandler();
		guiHandler.addTextareaAsChildIn('left-position-column');
	});

	// hiding the argument container, when the X button is clicked
	$('#closeArgumentContainer').on('click', function () {
		$('#add-argument-container').hide();
		$('#' + addStatementButtonId).enable = true;
	});

});

/**
 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
 * @param items list with al items
 * @param id for the ul list, where all items are appended
 */
function addListItemsToDiscussionsSpace(items, id) {
	'use strict';
	var i, size, discussionsSpace, ulElement;

	discussionsSpace = document.getElementById(discussionSpaceId);
	ulElement = document.createElement('ul');
	ulElement.setAttribute('id', id);

	for (i = 0, size = items.length; i < size; i += 1) {
		ulElement.appendChild(items[i]);
	}

	discussionsSpace.appendChild(ulElement);
}

/**
 * Setting a description in some p-tag
 * @param text to set
 */
function setDiscussionsDescription(text) {
	'use strict';
	$('#discussions-description').text(text);
}