/*global $, jQuery, alert, addListItemsToDiscussionsSpace, getAllPositions, getKeyValAsInputBtnInLiElement, setDiscussionsDescription, addTextareaAsChildIn*/

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

function getKeyValAsInputBtnInLiElement(key, val, isAddArgumentButton) {
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
		inputElement.setAttribute('onclick', "$('#add-argument-container').show();");
	} else {
		inputElement.setAttribute('onclick', "alert('todo');");
	}
	
	liElement.appendChild(inputElement);
	return liElement;
}

function setDiscussionsDescription(text) {
	'use strict';
	$('#discussions-description').text(text);
}

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
						listitems.push(getKeyValAsInputBtnInLiElement(key, val, false));
					}
				});
				setDiscussionsDescription('These are the current statements, given by users input. You can choose a position, which is next to your own intention or add a new one.');
				$('#discussion-container').show();
				listitems.push(getKeyValAsInputBtnInLiElement('add-position', 'Adding a new statement.', true));
			// case 2: we have no positions
			} else {
				setDiscussionsDescription('You are the first one. Please add a new statement:');
				$('#discussion-container').show();
				listitems.push(getKeyValAsInputBtnInLiElement('add-position', 'Yeah, I will add a statement!', true));
			}
			// call handle items
			addListItemsToDiscussionsSpace(listitems, 'position-list');
		}
	});
}

function addTextareaAsChildIn(parentid) {
	'use strict';
	var area, parent, div, button, span, childCount;
	parent = document.getElementById(parentid);
	childCount = parent.childElementCount;
	
	div = document.createElement('div');
	
	button = document.createElement('button');
	button.setAttribute('type', 'button');
	button.setAttribute('class', 'close');
	button.setAttribute('data-dismiss', 'modal');
	button.setAttribute('aria-label', 'Close');
	button.setAttribute('id', childCount.toString());

	span = document.createElement('span');
	span.setAttribute('aria-hidden', 'true');
	span.innerHTML = '&times;';
	
	button.appendChild(span);
	
	area = document.createElement('textarea');
	area.setAttribute('type', 'text');
	area.setAttribute('class', '');
	area.setAttribute('name', '');
	area.setAttribute('autocomplete', 'off');
	area.setAttribute('placeholder', 'I am new.');
	area.setAttribute('value', '');
	
	div.appendChild(area);
	div.appendChild(button);

	button.setAttribute('onclick', "button.parentNode.removeChild(button);area.parentNode.removeChild(area);alert('todo');");
	
	parent.insertBefore(div, parent.childNodes[childCount + 1]);
}

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
	});
	
});