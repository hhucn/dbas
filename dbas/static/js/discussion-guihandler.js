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
			onclick: 'this.parentNode.parentNode.removeChild(parentNode);'
		});

		// add everything
		// TODO insert dropdown menu
		// div_dropdown.attr('class', 'col-md-3');
		// div_content.attr('class', 'col-md-9');
		div_content.attr('title', textAreaReasonHintText);
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
		var newElement, helper = new Helper(), text, l, keyword;

		// are we positive or negateive?
		keyword = $('#' + discussionsDescriptionId).attr('attack').indexOf(attr_undermine) != -1
		|| $('#' + discussionsDescriptionId).attr('attack').indexOf(attr_undercut) != -1
		|| $('#' + discussionsDescriptionId).attr('attack').indexOf(attr_rebut) != -1 ? 'con' : 'pro';

		$.each(jsonData, function setPremissesAsLastChildEach(key, val) {

			if (key.substr(0, 3) == keyword) {
				text = 'Because ' + val.text;
				l = text.length - 1;
				if (text.substr(l) != '.' && text.substr(l) != '?' && text.substr(l) != '!') {
					text += '.';
				}
				newElement = helper.getKeyValAsInputInLiWithType(val.premissegroup_uid, text, false, true, false, val.text);
				newElement.children().hover(function () {
					$(this).toggleClass('table-hover');
				});
				$('#li_' + addReasonButtonId).before(newElement);
			} else if (key.substr(0, 3) == 'con') {
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
			relation = $('#' + discussionsDescriptionId).attr('attack'),
			last_relation = $('#' + discussionsDescriptionId).attr('last_relation'),
			confrontation = $('#' + discussionsDescriptionId).attr('confrontation_text'),
			guihandler = new GuiHandler(),
			ajaxhandler = new AjaxSiteHandler(),
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
		$('#' + addStatementErrorContainer).hide();
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
			$('#' + addStatementContainerMainInputId).hide().focus();

			// take a look, if we agree or disagree, and where we are
			alert('now: ' + relation + '\nlast: ' + last_relation);
			if (relation.indexOf(attr_undermine) != -1) {		this.showAddStatementsTextareasWithTitle(false, true, false, statement);
			} else if (relation.indexOf(attr_support) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, false, statement);
			} else if (relation.indexOf(attr_undercut) != -1) {	this.showAddStatementsTextareasWithTitle(false, true, true, statement);
			} else if (relation.indexOf(attr_overbid) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, true, statement);
			} else if (relation.indexOf(attr_rebut) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, false, statement);
			} else {
				alert("Something went wrong in 'setDisplayStylesOfAddStatementContainer'");
			}

			// does other users have an opinion?
			if (isArgument) {
				if ($('#' + discussionsDescriptionId).text().indexOf(otherParticipantsDontHave) == -1) {
					alert('Todo: How to insert something at this place?');
				} else {
					// other users have no opinion, so the participant can give pro and con
					this.showAddStatementsTextareasWithTitle(true, true, statement);
				}
			}

			$('#' + sendNewStatementId).off('click').click(function setDisplayStylesOfAddStatementContainerWhenArgument() {
				if (isPremisse) {
					interactionhandler.getPremissesAndSendThem(false, true);
				} else {
					alert("todo 424 in guihandler");
				}
				guihandler.setErrorDescription('');
				guihandler.setSuccessDescription('');
				$('#' + addStatementErrorContainer).hide();
				$('#' + addStatementErrorMsg).text('');
			});
		} else {
			alert('What now (II)? GuiHandler: setDisplayStylesOfAddStatementContainer');
		}

		guihandler.addTextareaAsChildInParent(proPositionTextareaId, id_pro, isStatement);
		guihandler.addTextareaAsChildInParent(conPositionTextareaId, id_con, isStatement);
	};

	/**
	 *
	 * @param isAgreeing
	 * @param isDisagreeing
	 * @param isAttackingRelation
	 * @param title
	 */
	this.showAddStatementsTextareasWithTitle = function (isAgreeing, isDisagreeing, isAttackingRelation, title) {
		var extra = isAttackingRelation ? (' ' + theCounterArgument) : '';
		if (isAgreeing) {
			$('#' + proPositionColumnId).show();
		} else {
			$('#' + proPositionColumnId).hide();
		}

		if (isDisagreeing) {
			$('#' + conPositionColumnId).show();
		} else {
			$('#' + conPositionColumnId).hide();
		}

		// given colors are the HHU colors. we could use bootstrap (text-success, text-danger) instead, but they are too dark
		$('#' + headingProPositionTextId).html(isAgreeing ? ' I <span class=\'green-bg\'>agree</span> with' + extra +
			': <b>' + title + '</b>, because...' : '');
		$('#' + headingConPositionTextId).html(isDisagreeing ? ' I <span class=\'red-bg\'>disagree</span> with' + extra +
			': <b>' + title + '</b>, because...' : '');
	};


	/**
	 *
	 * @param parsedData
	 * @param callbackid
	 */
	this.setStatementsAsProposal = function (parsedData, callbackid){
		if (Object.keys(parsedData).length == 0){
			$('#' + callbackid).next().empty();
			return;
		}

		var availableStrings = [], params, token, button, span_dist, span_text, statementListGroup;
		$('#' + callbackid).focus();
		statementListGroup = $('#' + callbackid).next();
		statementListGroup.empty(); // list with elements should be after the callbacker
		// $('#' + statementListGroupId).empty();

		$.each(parsedData, function (key, val) {
			params = key.split('_'); // distance = params[1], index = params[2]
			token = $('#' + callbackid).val();
			var pos = val.toLocaleLowerCase().indexOf(token.toLocaleLowerCase()), newpos = 0;
			var start = 0;

			// make all tokens bild
			while (token.length>0 && newpos != -1){//val.length) {
				val = val.substr(0, pos) + '<b>' + val.substr(pos, token.length) + '</b>' + val.substr(pos + token.length);
				start = pos + token.length + 7;
				newpos = val.toLocaleLowerCase().substr(start).indexOf(token.toLocaleLowerCase());
				pos = start + (newpos > -1 ? val.toLocaleLowerCase().substr(start).indexOf(token.toLocaleLowerCase()) : 0);

				// val = val.replace(token, '<b>' + token + '</b>');
			}

			if (parseInt(params[1]) < 500) { // TODO: Limit for Levenshtein
				button = $('<button>').attr({type : 'button',
					class : 'list-group-item',
					id : 'proposal_' + params[2]});
   				button.hover(function(){ $(this).addClass('active');
   				    	  }, function(){ $(this).removeClass('active');
   				});
				span_dist = $('<span>').attr({class : 'badge'}).text(levenshteinDistance + ' ' + params[1]);
				span_text = $('<span>').attr({id : 'proposal_' + params[2] + '_text'}).html(val);
				button.append(span_dist);
				button.append(span_text);

				statementListGroup.append(button);
				$('#proposal_' + params[2]).click(function(){
					$('#' + callbackid).val($('#proposal_' + params[2] + '_text').text());
					statementListGroup.empty(); // list with elements should be after the callbacker
					//$('#' + statementListGroupId).empty();
				});
				availableStrings.push(val);
			}
		});
		 // list with elements should be after the callbacker
		statementListGroup.prepend('<h4>' + didYouMean + '</h4>');
		//$('#' + statementListGroupId).prepend('<h4>' + didYouMean + '</h4>');
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
			uid = $(this).attr('id');
			is_premisse = $(this).hasClass('premisse');
			is_start = $(this).hasClass('start');
			// do we have a child with input or just the label?
			if ($(this).prop('tagName').toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid) || is_premisse || is_start) {
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
	this.showEditStatementsPopup = function () {
		var table, tr, td_text, td_buttons, statement, uid, type, is_start, is_premisse, tmp, text_count, statement_id, text, i, helper = new Helper(), is_final;
		$('#' + popupEditStatementId).modal('show');
		$('#' + popupEditStatementSubmitButtonId).hide();
		$('#' + popupEditStatementWarning).hide();

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
			uid = $(this).attr('id');
			type = $(this).attr('class');
			is_premisse = $(this).hasClass('premisse');
			is_start = $(this).hasClass('start');

			// TODO edit premisse groups
			if (typeof uid != 'undefined' && uid.indexOf('_') != -1){
				tmp = uid.split('_');
				uid = tmp[tmp.length -1];
			}

			// do we have a child with input or just the label?
			if ($(this).prop('tagName').toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid) || is_premisse || is_start) {

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
			is_final = $('#' + popupEditStatementWarning).is(':visible');
			//$('#edit_statement_td_text_' + $(this).attr('statement_id')).text(statement);
			new AjaxSiteHandler().sendCorrectureOfStatement($(this).attr('statement_id'), $(this).attr('callback_td'), statement, is_final);
		});

		// on click: do ajax
		// ajax done: refresh current statement with new text
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
	 *
	 */
	this.displayHowToWriteTextPopup = function(){
		var cookie_name = 'HOW_TO_WRITE_TEXT',
			userAcceptedCookies = false,
			cookies = document.cookie.split(";");

		// show popup, when the user does not accepted the cookie already
		for (var i = 0; i < cookies.length; i++) {
			var c = cookies[i].trim();
			if (c.indexOf(cookie_name) == 0) {
				userAcceptedCookies = c.substring(cookie_name.length + 1, c.length);
			}
		}
		if (!userAcceptedCookies) {
			$('#' + popupHowToWriteText).modal('show');
		}

		$('#' + popupHowToWriteTextCloseButton).click(function(){
			$('#' + popupHowToWriteText).modal('hide');
		});
		$('#' + popupHowToWriteTextClose).click(function(){
			$('#' + popupHowToWriteText).modal('hide');
		});

		// accept cookie
		$('#' + popupHowToWriteTextOkayButton).click(function(){
			$('#' + popupHowToWriteText).modal('hide');
			var d = new Date(), consent = true;
			var expiresInDays = 1 * 24 * 60 * 60 * 1000; // Todo
			d.setTime( d.getTime() + expiresInDays );
			var expires = 'expires=' + d.toGMTString();
			document.cookie = cookie_name + '=' + consent + '; ' + expires + ';path=/';

			$(document).trigger('user_cookie_consent_changed', {'consent' : consent});
		});

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
		new AjaxSiteHandler().getAllArgumentsForIslandView();
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