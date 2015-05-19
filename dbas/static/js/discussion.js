/*global $, jQuery, alert, addListItemsToDiscussionsSpace, getAllPositions, getKeyValAsInputBtnInLiElement,
 setDiscussionsDescription, addTextareaAsChildIn, argumentButtonWasClicked, positionButtonWasClicked*/

var addStatementButtonid = 'add-statement';

/*
var Testclass(position, argment){
   this.position = position;
   this.argment = argment;
}
*/

/**
 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
 * @param items list with al items
 * @param id for the ul list, where all items are appended
 */
function addListItemsToDiscussionsSpace(items, id) {
	'use strict';
	var i, size, newList, discussionsSpace, ulElement;
	
	discussionsSpace = document.getElementById("discussions-space");
	ulElement = document.createElement('ul');
	ulElement.setAttribute('id', id);
	
	for (i = 0, size = items.length; i < size; i += 1) {
		ulElement.appendChild(items[i]);
	}
	
	discussionsSpace.appendChild(ulElement);
}

/**
 * Creates an input element tih key as id and val as value. This is embedded in an li element
 * @param key
 * @param val
 * @param isAddArgumentButton true, if if is the addArgumentButton
 * @returns {Element|*} an li tag with embedded input element
 */
function getKeyValAsInputBtnInLiElement(key, val, isArgument, isAddArgumentButton) {
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
	if (isAddArgumentButton) {
		inputElement.setAttribute('onclick', "$('#add-argument-container').show();$('#'+addStatementButtonid).disable = true;");
	} else {
		if (isArgument) {
			inputElement.setAttribute('onclick', "argumentButtonWasClicked(this.value);");
		} else {
			inputElement.setAttribute('onclick', "positionButtonWasClicked(this.value);");
		}
	}
	
	liElement.appendChild(inputElement);
	return liElement;
}

/**
 * Handler when an argument button was clicked
 * @param value of the button
 */
function argumentButtonWasClicked(value) {
	'use strict';
	setDiscussionsDescription('Okay, you have got the opinion: ' + value + ' Can you choose a position therefore?');
}

/**
 * Handler when an position button was clicked
 * @param value of the button
 */
function positionButtonWasClicked(value) {
	setDiscussionsDescription('So, your position is: ' + value + '. But ...');
	'use strict';
}

/**
 * Setting a description in some p-tag
 * @param text to set
 */
function setDiscussionsDescription(text) {
	'use strict';
	$('#discussions-description').text(text);
}

/**
 * Send a json-request to ajax_positions for getting all positions in the database.
 * The response is given to getKeyValAsInputBtnInLiElement(...) and this list
 * is given to addListItemsToDiscussionsSpace(...)
 */
function getAllPositions() {
	'use strict';
	var listitems = [];
	jQuery.ajax({
		url: 'ajax_positions',
		type: 'POST',
		dataType: 'json',
		success: function (data) {
			var posCount = data.countPos;
			// case 1: we have positions
			if (posCount !== 'undefined') {
				// list iterator
				$.each(data, function (key, val) {
					// adding positions only
					if (key.indexOf('pos') === 0) {
						listitems.push(getKeyValAsInputBtnInLiElement(key, val, true, false));
					}
				});
				setDiscussionsDescription('These are the current statements, given by users input. You can choose a position, which is next to your own intention or add a new one.');
				$('#discussion-container').show();
				listitems.push(getKeyValAsInputBtnInLiElement(addStatementButtonid, 'Adding a new statement.', true, true));
			// case 2: we have no positions
			} else {
				setDiscussionsDescription('You are the first one. Please add a new statement:');
				$('#discussion-container').show();
				listitems.push(getKeyValAsInputBtnInLiElement(addStatementButtonid, 'Yeah, I will add a statement!', true, true));
			}
			// call handle items
			addListItemsToDiscussionsSpace(listitems, 'position-list');
		}
	});
}

/**
 * Adds a textarea with a little close button (both in a div tag) to a parend tag
 * @param parentid id-tag of the parent element, where a textare should be added
 */
function addTextareaAsChildIn(parentid) {
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
}

/**
 * main function
 */
$(document).ready(function () {
	'use strict';

	$('#discussion-container').hide(); // hiding discussions container
	$('#add-argument-container').hide(); // hiding container for adding arguments

	// jump to chapter-function
	$('#get-positions').on('click', function (e) {
		getAllPositions();
		$('#get-positions').hide(); // hides the start button
		$('#start-description').hide(); // hides the start description
	});
	
	// adding a textarea in the right column 
	$('#add-con-textarea').on('click', function (e) {
		addTextareaAsChildIn('right-position-column');
	});
	
	// adding a textarea in the left column 
	$('#add-pro-textarea').on('click', function (e) {
		addTextareaAsChildIn('left-position-column');
	});
	
	// hiding the argument container, when the X button is clicked
	$('#closeArgumentContainer').on('click', function (e) {
		$('#add-argument-container').hide();
		$('#' + addStatementButtonid).enable = true;
	});
	
});