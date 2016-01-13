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
	 * Setting a description in some p-tag without mouse over
	 * @param text to set
	 */
	this.setDiscussionsDescription = function (text) {
		this.setDiscussionsDescription(text, text, null);
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
	this.setDiscussionAttackDescription = function (text) {
		$('#' + discussionAttackDescriptionId).html(text);
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
	 * Setting a success description in some p-tag
	 * @param text to set
	 */
	this.setSuccessDescription = function (text) {
		$('#' + discussionSuccessDescriptionId).text(text);
		$('#' + discussionSuccessDescriptionSpaceId).show();
	};

	/**
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgumentOrStart if true, argumentButtonWasClicked is used, otherwise
	 */
	this.setNewArgumentButtonOnly = function (val, isArgumentOrStart) {
		var listitem = [];
		listitem.push(new Helper().getKeyValAsInputInLiWithType(addReasonButtonId, val, isArgumentOrStart, false, false, ''));
		new GuiHandler().addListItemsToDiscussionsSpace(listitem);
	};

	/**
	 * Checks and hides the new argument button
	 */
	this.checkAndHideNewArgumentButton = function(){
		$('#' + addReasonButtonId).attr('checked', true).prop('checked', true).parent().hide();
	};

	/**
	 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
	 * @param items list with al items
	 */
	this.addListItemsToDiscussionsSpace = function (items) {
		var ulElement;

		// wrap all elements into a list
		ulElement = $('<ul>');
		ulElement.append(items);

		// append them to the space
		$('#' + discussionSpaceId).append(ulElement);

		// hover style element for the list elements
		ulElement.children().hover(function () {
			$(this).toggleClass('text-hover');
		});
	};

	/**
	 * Adds a textarea with a little close button (both in a div tag) to a parend tag
	 * @param parentid id-tag of the parent element, where a textare should be added
	 * @param identifier additional id
	 * @param is_statement
	 * @param type
	 */
	this.addTextareaOrInputAsChildInParent = function (parentid, identifier, is_statement, type) {
		/**
		 * The structure is like:
		 * <div><textarea .../><button...></button></div>
		 */
		var area, parent, div, div_content, button, span, childCount, div_dropdown, id, span_because;
		parent = $('#' + parentid);
		childCount = parent.children().length;
		id = 'textarea_' + identifier + childCount.toString();

		div = $('<div>').attr({
			class: 'row',
			id: 'div' + childCount.toString()
		});
		div_content = $('<div>').attr({
			id: 'div-content-' + childCount.toString()
		});
		button = $('<button>').attr({
			type: 'button',
			class: 'close',
			id: 'button_' + identifier + childCount.toString()
		});
		span = $('<span>').html('&times;');
		span_because = $('<span>').attr('style', 'float:left; line-height:60px; text-align:center;').html('<h5>' + _t(because) + '...' + '</h5>');

		area = $('<' + type + '>').attr({
			type: 'text',
			class: 'form-control',
			name: '',
			autocomplete: 'off',
			value: '',
			id: id,
			style: 'padding: 12px 10px 12px 50px; ' +
			'-webkit-border-radius: 3px; ' +
			'-moz-border-radius: 5px; ' +
			'-o-border-radius: 5px; ' +
			'margin: 0px 0px 10px 0px; ' +
			'-webkit-appearance: none;'
		}).click(function(){ // new fuzzy search, when the text field changes
			new Helper().delay(function() {
				new AjaxSiteHandler().fuzzySearch($('#' + id).val(), id, fuzzy_add_reason, '');
			},200);
		});

		button.append(span);
		div_dropdown = this.getDropdownWithSentencesOpeners(identifier, childCount.toString());
		div_content.append(span_because);
		div_content.append(area);
		// div_content.append(button); // TODO "add a textfield" is currently hidden

		// remove everything on click
		button.attr({
			onclick: 'this.parentNode.parentNode.removeChild(parentNode);'
		});

		// add everything
		// TODO insert dropdown menu for sentences openers
		// div_dropdown.attr('class', 'col-md-3');
		// div_content.attr('class', 'col-md-9');
		div_content.attr('title', _t(textAreaReasonHintText));
		div.append(div_dropdown);
		div.append(div_content);
		parent.append(div);

		if (is_statement) {
			div_dropdown.show();
		} else {
			div_dropdown.hide();
		}

		// dropdown listener with sentence openers
		this.setDropdownClickListener(identifier, childCount.toString());
		// fuzzy search
		$('#' + id).keyup(function () {
			new Helper().delay(function() {
				new AjaxSiteHandler().fuzzySearch($('#' + id).val(), id, fuzzy_add_reason, '');
			},200);
		});
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
		sentencesOpeners = identifier == id_pro ? _t(sentencesOpenersArguingWithAgreeing) : _t(sentencesOpenersArguingWithDisagreeing);

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
		button.text(identifier.toLowerCase() == 'left' ? _t(agreeBecause) : _t(disagreeBecause));
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
			a = h.getATagForDropDown(a_id, _t(clickToChoose) + ': ' + _t(sentencesOpeners[i]), _t(sentencesOpeners[i]));
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
			a = h.getATagForDropDown(a_id, _t(clickToChoose) + ': ' + _t(sentencesOpenersInforming[i]), _t(sentencesOpenersInforming[i]));
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
		sentencesOpeners = identifier == id_pro ? _t(sentencesOpenersArguingWithAgreeing) : _t(sentencesOpenersArguingWithDisagreeing);

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
				this.setErrorDescription(_t(notInsertedErrorBecauseEmpty));
			} else if (jsonData.reason === 'duplicate') {
				this.setErrorDescription(_t(notInsertedErrorBecauseDuplicate));
			} else {
				this.setErrorDescription(_t(notInsertedErrorBecauseUnknown));
			}
		} else {
			var newElement = new Helper().getKeyValAsInputInLiWithType(jsonData.statement.uid, jsonData.statement.text, true, false, false, '');
			newElement.children().hover(function () {
				$(this).toggleClass('text-hover');
			});
			$('#li_' + addReasonButtonId).before(newElement); // TODO.slideDown('slow').attr('checked', false).prop('checked', false);
			$('#' + jsonData.statement.uid).attr('checked', true).prop('checked', true);
			new InteractionHandler().radioButtonChanged();
			new GuiHandler().setSuccessDescription(_t(addedEverything));
		}
	};

	/**
	 * Sets the new premises as list child in discussion space or displays an error
	 * @param jsonData returned data
	 * @param isStart is at the beginning with a premise. at the start we need a reply for an premisegroup, otherwise for an argument
	 */
	this.setPremisesAsLastChild = function (jsonData, isStart) {
		var newElement = '', helper = new Helper(), text, tmp='', l, keyword, attack, same_group,
				premisegroup_uid = '0', countSg = 0, countPl = 0, long_id, last_id = 0, current_id, is_duplicate = false;

		// premise group?
		same_group = jsonData.same_group == '1';
		// are we positive or negative?
		attack = $('#' + discussionsDescriptionId).attr('attack');
		if (typeof attack !== typeof undefined && attack !== false){
			keyword = attack.indexOf(attr_undermine) != -1 || attack.indexOf(attr_undercut) != -1 ? 'con' : 'pro';
		} else {
			keyword = 'pro';
		}

		$.each(jsonData, function setPremisesAsLastChildEach(key, val) {
			if (key.substr(0, 3) == keyword) {

				if (!same_group) {
					countSg += 1;
					text = _t(because) + ' ' + new Helper().startWithLowerCase(val.text);
					l = text.length - 1;
					if (text.substr(l) != '.' && text.substr(l) != '?' && text.substr(l) != '!') {
						text += '.';
					}

					last_id = isStart ? val.premisegroup_uid : val.uid;
					if (!isStart) {
						long_id = attack + '_premisegroup_' + val.premisegroup_uid;
						is_duplicate = jsonData.duplicates['arg_' + val.premisegroup_uid] == 'true';
					}

					// add only, if it is now duplicate
					if (!is_duplicate) {
						current_id = isStart ? val.premisegroup_uid : val.uid;
						newElement = helper.getKeyValAsInputInLiWithType(current_id, text, false, true, !isStart, val.text, isStart? {} : {'long_id': long_id});
						newElement.children().hover(function () {
							$(this).toggleClass('text-hover');
						});
						$('#li_' + addReasonButtonId).before(newElement);
					}
				} else {
					countPl += 1;
					alert("How to handle pgroups? Look at 'changelog and edit'");
					// TODO how to handle inserting pgroups? Look at 'changelog and edit'
					// TODO how to handle duplicates
					text = val.text;
					l = text.length - 1;
					if (text.substr(l) == '.' || text.substr(l) == '?' || text.substr(l) == '!') {
							text = text.substr(0,l);
						}

					if (tmp == ''){
						tmp = _t(because) + ' ' + text;
						premisegroup_uid = val.premisegroup_uid;
					} else {
						tmp += ' ' + _t(and) + ' ' + text
					}
				}
			} else if (key.substr(0, 3) == 'con') {
				// todo setPremisesAsLastChild contra premises
			}
		});
		// add the group element, because we have not done this
		if (same_group){
			tmp += '.';
			newElement = helper.getKeyValAsInputInLiWithType(premisegroup_uid, tmp, isStart, true, false, tmp);
			newElement.children().hover(function () {
				$(this).toggleClass('text-hover');
			});
			$('#li_' + addReasonButtonId).before(newElement);
		}

		this.hideAddStatementContainer();
		//this.setDisplayStylesOfAddStatementContainer(false, false, false, false, false);
		$('#' + addReasonButtonId).attr('checked', false).prop('checked', false);

		// todo chose the only element, which was given
		if (countSg == 1){
			$('#li_' + last_id + ' input').attr('checked', true).prop('checked', true);
			new InteractionHandler().radioButtonChanged();
		}
	};

	/**
	 * Hides the add statement/premise/argument container
	 */
	this.hideAddStatementContainer = function () {
		$('#' + addStatementContainerId).fadeOut('slow');
		$('#' + addStatementContainerMainInputId).val('');
		$('#' + addReasonButtonId).disable = false;
	};

	/**
	 *
	 */
	this.prepareAddStatementContainer = function() {
		$('#' + proPositionTextareaId).empty();
		$('#' + conPositionTextareaId).empty();
		$('#' + addStatementContainerMainInputIntroId).text('');
		$('#' + addStatementContainerId).fadeIn('slow');
		$('#' + addStatementErrorContainer).hide();
		$('#' + addReasonButtonId).disable = true;
	};

	/**
	 * Shows an container for adding arguments
	 * @param isArgument boolean
	 * @param isStart boolean
	 */
	this.showAddPremiseOrArgumentContainer = function (isArgument, isStart){
		// method is called while justifying arguments
		var	discussionsDescription = $('#' + discussionsDescriptionId),
			confrontation = discussionsDescription.attr('confrontation_text'),
			conclusion = discussionsDescription.attr('conclusion'),
			premise = discussionsDescription.attr('premise'),
			argument =  conclusion + ' ' + _t(because).toLocaleLowerCase() + ' ' + premise,
			relation = discussionsDescription.attr('attack'),
			guihandler = new GuiHandler(),
			interactionhandler = new InteractionHandler();
		this.prepareAddStatementContainer();

		// special case
		if (typeof relation == 'undefined'){
			this.showAddStatementContainer(isStart);
			return;
		}
		alert("showAddPremiseOrArgumentContainer");

		// $('#' + addStatementContainerTitleId).text(isPremise ? _t(argumentContainerH4TextIfPremise) :
		// _t(argumentContainerH4TextIfArgument));
		// pretty print, whether above are more than one lititems
		if($('#' + discussionSpaceId + ' ul li').length == 1) {
			$('#' + addStatementContainerTitleId).text(_t(addPremiseRadioButtonText));
		} else {
			$('#' + addStatementContainerTitleId).text(_t(argumentContainerH4TextIfPremise));
		}
		$('#' + addStatementContainerMainInputId).hide().focus();

		// take a look, if we agree or disagree, and where we are
		if (relation.indexOf(attr_undermine) != -1) {		this.showAddStatementsTextareasWithTitle(false, true, confrontation, '', false);
		} else if (relation.indexOf(attr_support) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, confrontation, '', false);
		} else if (relation.indexOf(attr_undercut) != -1) {	this.showAddStatementsTextareasWithTitle(false, true, confrontation, conclusion, true);
		} else if (relation.indexOf(attr_overbid) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, confrontation, conclusion, true);
		} else if (relation.indexOf(attr_rebut) != -1) { // special case, when we are in the attack branch
			var supportive = discussionsDescription.attr('supportive') == 'true';
			if (supportive)									this.showAddStatementsTextareasWithTitle(true, false, argument, '', false);
			else											this.showAddStatementsTextareasWithTitle(false, true, conclusion, '', false);
		} else {
			alert("Something went wrong in 'setDisplayStylesOfAddStatementContainer'");
		}

		// does other users have an opinion?
		if (isArgument) {
			if (discussionsDescription.text().indexOf(_t(otherParticipantsDontHaveCounter)) != -1) {
				// other users have no opinion, so the participant can give pro and con
				this.showAddStatementsTextareasWithTitle(true, true, statement);
			} else {
				// alert('Todo: How to insert something at this place?');
			}
		}

		$('#' + sendNewStatementId).off('click').click(function setDisplayStylesOfAddStatementContainerWhenArgument() {
			if (interactionhandler.getPremisesAndSendThem(false)) {
				guihandler.hideErrorDescription();
				guihandler.hideSuccessDescription();
				$('#' + addStatementErrorContainer).hide();
				$('#' + addStatementErrorMsg).text('');
			} else {
				guihandler.setErrorDescription(_t(inputEmpty));
			}
		});

		guihandler.addTextareaOrInputAsChildInParent(proPositionTextareaId, id_pro, false, 'input');
		guihandler.addTextareaOrInputAsChildInParent(conPositionTextareaId, id_con, false, 'input');
	};

	/**
	 * Shows an container for adding statement
	 * @param isStart boolean
	 */
	this.showAddStatementContainer = function (isStart){
		// method is called for the first position and the first premise
		var	discussionsDescription = $('#' + discussionsDescriptionId),
			conclusion = discussionsDescription.attr('conclusion'),
			premise = discussionsDescription.attr('premise'),
			header, escapedText, titleText,
			addStatementContainerMainInputIntro = $('#' + addStatementContainerMainInputIntroId),
			guihandler = new GuiHandler(),
			ajaxhandler = new AjaxSiteHandler(),
			html = discussionsDescription.html();
		this.prepareAddStatementContainer();
		alert("showAddStatementContainer");
		// TODO NARRATION FIELD FOR POSITION AND FIRST PREMISE

		// some pretty print options
		if (isStart) {
			titleText = _t(argumentContainerH4TextIfConclusion);
		} else {
			if (html.indexOf(_t(firstPremiseText1)) != -1){
				titleText = _t(whyDoYouThinkThat) + ' <b>' + discussionsDescription.attr('text') + '<b>?';
			} else if (html.indexOf(_t(otherParticipantsDontHaveCounter)) != -1) {
				header = html.substr(html.indexOf('<b>'), html.indexOf('</b>')-html.indexOf('<b>')+5);
				titleText = _t(whyDoYouThinkThat) + ' <b>' + header + '</b>';
			} else {
				titleText = _t(argumentContainerH4TextIfPremise) + '<br><br>' + html;
			}
			addStatementContainerMainInputIntro.text(_t(because) + '...');
		}
		$('#' + addStatementContainerTitleId).html(titleText);

		// gui modifications
		$('#' + addStatementContainerMainInputId).show();
		$('#' + proPositionColumnId).hide();
		$('#' + conPositionColumnId).hide();
		// at the beginning we differentiate between statement and statements
		$('#' + sendNewStatementId).off('click').click(function setDisplayStylesOfAddStatementContainerWhenStatement() {
			escapedText = new Helper().escapeHtml($('#' + addStatementContainerMainInputId).val());
			if (escapedText.length == 0){
				guihandler.setErrorDescription(_t(inputEmpty));
				return;
			}
			if (isStart) {
				if ($('#' + addReasonButtonId).hasClass(attr_attack)){
					alert("handle this case in guiHandler");
					return;
				}
				ajaxhandler.sendNewStartStatement(escapedText);
			} else {
				ajaxhandler.sendNewStartPremise(escapedText, discussionsDescription.attr('conclusion_id'), (discussionsDescription.attr('supportive')=='true'));
			}
			guihandler.hideErrorDescription();
			guihandler.hideSuccessDescription();
		});

		guihandler.addTextareaOrInputAsChildInParent(proPositionTextareaId, id_pro, true, 'input');
		guihandler.addTextareaOrInputAsChildInParent(conPositionTextareaId, id_con, true, 'input');
	};

	/**
	 *
	 * @param isAgreeing
	 * @param isDisagreeing
	 * @param text1
	 * @param text2
	 * @param isAttackingRelation
	 */
	this.showAddStatementsTextareasWithTitle = function (isAgreeing, isDisagreeing, text1, text2, isAttackingRelation) {
		if (isAgreeing) {	 $('#' + proPositionColumnId).show(); } else { $('#' + proPositionColumnId).hide(); }
		if (isDisagreeing) { $('#' + conPositionColumnId).show(); } else { $('#' + conPositionColumnId).hide(); }

		var suffix;
		if (isAttackingRelation)
			suffix = ': <b>' + text1 + ' ' + _t(asReasonFor) + ' ' + text2 + '</b>.';
		else
			suffix = ': <b>' + text1 + '</b>.' ;
		$('#' + headingProPositionTextId).html(_t(iAgreeWithInColor) + suffix);
		$('#' + headingConPositionTextId).html(_t(iDisagreeWithInColor) + suffix);
	};

	/**
	 *
	 * @param parsedData
	 * @param callbackid
	 */
	this.setStatementsAsProposal = function (parsedData, callbackid){
		var callback = $('#' + callbackid), uneditted_value;
		// is there any value ?
		if (Object.keys(parsedData).length == 0){
			callback.next().empty();
			return;
		}

		var params, token, button, span_dist, span_text, distance, index;
		callback.focus();
		//statementListGroup = callback.next();
		//statementListGroup.empty(); // list with elements should be after the callbacker
		$('#' + proposalListGroupId).empty();//.prepend('<h4>' + _t(didYouMean) + '</h4>');

		$.each(parsedData, function (key, val) {
			params = key.split('_');
			distance = parseInt(params[0]);
			index = params[1];

			token = callback.val();
			//var pos = val.toLocaleLowerCase().indexOf(token.toLocaleLowerCase()), newpos = 0, start = 0;

			// make all tokens bold
			uneditted_value = val;
			val = '<b>' + val.replace(token, '</b>' + token + '<b>').replace(token.toLocaleLowerCase(), '</b>' + token.toLocaleLowerCase() + '<b>') + '</b>';

			//while (token.length>0 && newpos != -1){//val.length) {
			//	val = val.substr(0, pos) + '<b>' + val.substr(pos, token.length) + '</b>' + val.substr(pos + token.length);
			//	start = pos + token.length + 7;
			//	newpos = val.toLocaleLowerCase().substr(start).indexOf(token.toLocaleLowerCase());
			//	pos = start + (newpos > -1 ? val.toLocaleLowerCase().substr(start).indexOf(token.toLocaleLowerCase()) : 0);
			//	// val = val.replace(token, '<b>' + token + '</b>');
			//}

			button = $('<button>').attr({type : 'button',
				class : 'list-group-item',
				id : 'proposal_' + index,
				text: uneditted_value});
   			button.hover(function(){ $(this).addClass('active');
   			    	  }, function(){ $(this).removeClass('active');
   			});
			span_dist = $('<span>').attr({class : 'badge'}).text(_t(levenshteinDistance) + ' ' + distance);
			span_text = $('<span>').attr({id : 'proposal_' + index + '_text'}).html(val);
			button.append(span_dist).append(span_text).click(function(){
				callback.val($(this).attr('text'));
				$('#' + proposalListGroupId).empty(); // list with elements should be after the callbacker
			});
			$('#' + proposalListGroupId).append(button);
		});
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
		var table, tr, td_text, td_buttons, statement, uid, type, is_start, is_premise, tmp, text_count, statement_id, text, i,
			helper = new Helper(), is_final, popupEditStatementSubmitButton = $('#' + popupEditStatementSubmitButtonId);
		$('#' + popupEditStatementId).modal('show');
		popupEditStatementSubmitButton.hide();
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
			if (statement.toLocaleLowerCase().indexOf(_t(because)) == 0){
				statement = new Helper().startWithUpperCase(statement.substring(8));
			}
			uid = $(this).attr('id');
			type = $(this).attr('class');
			is_premise = $(this).hasClass('premise');
			is_start = $(this).hasClass('start');

			// TODO edit premise groups
			if (typeof uid != 'undefined' && uid.indexOf('_') != -1){
				tmp = uid.split('_');
				uid = tmp[tmp.length -1];
			}

			// do we have a child with input or just the label?
			if ($(this).prop('tagName').toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid) || is_premise || is_start) {

				// is this a premise group with more than one text?
				if (typeof $(this).attr('text_count') !== typeof undefined && $(this).attr('text_count') !== false){
					text_count = $(this).attr('text_count');
					type = 'premisesgroup';

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
		popupEditStatementSubmitButton.hide().click(function edit_statement_click() {
			statement = $('#' + popupEditStatementTextareaId).val();
			if (statement.toLocaleLowerCase().indexOf(_t(because).toLocaleLowerCase()) == 0){
				statement = statement.substr(_t(because.length() + 1));
			}
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
	 * Shows the display style container
	 */
	this.showDisplayControlContainer = function(){
		$('#' + displayControlContainerId).show();
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
	 * Hides the display style container
	 */
	this.hideDisplayControlContainer = function(){
		$('#' + displayControlContainerId).hide();
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
	 * Dispalys the 'how to write text '-popup, when the setting is not in the cookies
	 */
	this.displayPremiseGroupPopup = function(){
		var cookie_name = 'HOW_TO_SET_PremiseGROUPS',
			// show popup, when the user does not accepted the cookie already
			userAcceptedCookies = new Helper().isCookieSet(cookie_name);

		if (!userAcceptedCookies) {
			$('#' + popupHowToSetPremiseGroups).modal('show');
		}

		$('#' + popupHowToSetPremiseGroupsCloseButton).click(function(){
			$('#' + proTextareaPremisegroupCheckboxId).attr('checked', false).prop('checked', false);
			$('#' + conTextareaPremisegroupCheckboxId).attr('checked', false).prop('checked', false);
		});

		$('#' + popupHowToSetPremiseGroupsClose).click(function(){
			$('#' + proTextareaPremisegroupCheckboxId).attr('checked', false).prop('checked', false);
			$('#' + conTextareaPremisegroupCheckboxId).attr('checked', false).prop('checked', false);
		});

		// accept cookie
		$('#' + popupHowToSetPremiseGroupsOkayButton).click(function(){
			$('#' + popupHowToSetPremiseGroups).modal('hide');
			new Helper().setCookie(cookie_name);
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
		$('#' + graphViewContainerId).hide();
		$('#' + discussionContainerId).show();
	};

	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsIsland = function () {
		$('#' + islandViewContainerId).fadeIn('slow');
		$('#' + graphViewContainerId).hide();
		new DiscussionIsland().showIsland($('#' + discussionsDescriptionId).attr(attr_argument_uid));
	};

	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsGraphView = function () {
		$('#' + islandViewContainerId).hide();
		$('#' + discussionContainerId).hide();
		new GuiHandler().hideDiscussionError();
		new DiscussionGraph().showGraph();
	};

	/**
	 * Sets style attributes to default
	 */
	this.resetChangeDisplayStyleBox = function () {
		$('#' + scStyleDialogId).attr('checked', true).prop('checked', true);
		$('#' + scStyleIslandId).attr('checked', false).prop('checked', false);
		$('#' + scStyleCompleteId).attr('checked', false).prop('checked', false);
	};

	/**
	 * Sets given data as list to the issue dropdown.
	 * Also the onclick function is set
	 */
	this.setIssueList = function (jsonData){
		var li, a, current_id = '', issue, topic, issueDropdownButton = $('#' + issueDropdownButtonID), issue_curr,
				text, i, helper = new Helper(), count, span;

		li = $('<li>');
		li.addClass('dropdown-header').text(_t(issueList));
		$('#' + issueDropdownListID).empty().append(li);

		// create an issue for each entry
		count = jsonData.current_issue_arg_count;
		$.each(jsonData, function setIssueListEach(key, val) {
			if (key == 'current_issue') {
				current_id = val;
			} else if (typeof val.text !== 'undefined'){
				li = $('<li>');
				li.attr({id: 'issue_' + val.uid, 'issue': val.uid, 'date': val.date, 'count': count});
				span = $('<span>').addClass('badge').attr({'id':'issue_args' + val.uid,
					'style':'float: right',
					'title': _t(countOfArguments)}).text(val.arguments);
				a = $('<a>');
				a.text(val.text);
				a.attr({'style':'cursor:pointer', 'text':val.text});
				a.append(span);
				li.append(a);
				a.click(function () {
					issue = $(this).parent().attr('issue');
					topic = $('#issue_' + issue + ' a').text();

					// parameter func will be used as a string to go to the new issue page
					displayConfirmationDialogWithCheckbox(_t(switchDiscussion), _t(switchDiscussionText1) + ': <i>\'' + topic
						+ '\'</i> ' + _t(switchDiscussionText2), _t(keepSetting), issue, true);
				});
				$('#' + issueDropdownListID).append(li);
			}
		});

		// set the main issue text for the button
		if (issueDropdownButton.text().length == 0 || issueDropdownButton.text().length == 15) {
			issue_curr = $('#issue_' + current_id);
			$('#' + issueDateId).text(issue_curr.attr('date'));
			$('#' + issueCountId).text(issue_curr.attr('count'));
			text = $('#issue_' + current_id + ' a').attr('text');
			issueDropdownButton.attr('value', text);
			text = helper.resizeIssueText(text);
			this.setIssueDropDownText(text);
			issue_curr.addClass('disabled').children().eq(0).removeAttr('style');
		}

		// some helper
		issueDropdownButton.attr('issue', current_id);
	};

	/**
	 * Sets text for the issue dropdown
	 * @param text string
	 */
	this.setIssueDropDownText = function(text) {
		$('#' + issueDropdownButtonID).html(text + '&#160;&#160;&#160;<span class="caret"></span>');
	};
}