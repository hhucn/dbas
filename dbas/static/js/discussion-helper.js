/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function Helper() {

	/**
	 *
	 * @param id
	 * @param title
	 * @param text
	 * @returns {jQuery|HTMLElement}
	 */
	this.getATagForDropDown = function (id, title, text) {
		var a = $('<a>');
		a.attr('id', id);
		a.attr('role', 'menuitem');
		a.attr('tabindex', '-1');
		a.attr('data-toggle', 'modal');
		a.attr('title', title);
		a.attr('href', '#');
		a.text(text);
		return a
	};

	/**
	 * Return the full HTML text of an given element
	 * @param element which should be translated
	 */
	this.getFullHtmlTextOf = function (element) {
		return $('<div>').append(element).html();
	};

	/**
	 *
	 * @param text
	 * @returns {string}
	 */
	this.startWithLowerCase = function (text){
		return text.substr(0, 1).toLowerCase() + text.substr(1);
	};

	/**
	 *
	 * @param text
	 * @returns {string}
	 */
	this.startWithUpperCase = function (text){
		return text.substr(0, 1).toLocaleUpperCase() + text.substr(1);
	};

	/**
	 * Returns all kinds of attacks for the given premisse and conclusion
	 * @param confrontation current confrontation
	 * @param premisse current premisses
	 * @param conclusion current conclusion
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param endWithDot, true, when each sentences should end with a dot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createRelationsText = function(confrontation, premisse, conclusion, startLowerCase, endWithDot){
		if (premisse.substr(premisse.length-1) == '.')
			premisse = premisse.substr(0, premisse.length-1);

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		var w = startLowerCase ? this.startWithLowerCase(wrong) : this.startWithUpperCase(wrong),
			r = startLowerCase ? this.startWithLowerCase(right) : this.startWithUpperCase(right),
			enddot = endWithDot ? '.' : '',
			belCounterJusti = believeThatGoodCounter + ' <b>' + conclusion + '</b>',
			undermine = '<b>' + w + ', ' + itIsFalse + " " + premisse + '</b>' + enddot,
			support	  = '<b>' + r + ', ' + itIsTrue + " " + premisse + '</b>' + enddot,
			undercut  = '<b>' + r + ', ' + premisse + '</b>, ' + butIDoNot + ' ' + belCounterJusti + enddot,
			overbid	  = '<b>' + r + ', ' + premisse + '</b>, ' + andIDo + ' ' + belCounterJusti + enddot,
			rebut	  = '<b>' + r + ', ' + confrontation + '</b> ' + iAcceptCounter + ' <b>' + conclusion
				+ '</b>.<br><br>' + iHaveStrongerArgument + ' <b>' + premisse + '</b>' + enddot,
			noopinion  = 'I have no opinion regarding <b>' + conclusion + '</b>. ' + goStepBack + '.';
		return [undermine, support, undercut, overbid, rebut, noopinion];
	};

	/**
	 * Returns all kinds of attacks for the given confrontation and conclusion
	 * @param confrontation current confrontation
	 * @param conclusion current conclusion
	 * @param premisse current premisse
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param endWithDot, true, when each sentences should end with a dot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createConfrontationsRelationsText = function(confrontation, conclusion, premisse, startLowerCase, endWithDot){

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		var w = startLowerCase ? this.startWithLowerCase(wrong) : this.startWithUpperCase(wrong),
			r = startLowerCase ? this.startWithLowerCase(right) : this.startWithUpperCase(right),
			i = startLowerCase ? this.startWithLowerCase(irrelevant) : this.startWithUpperCase(irrelevant),
			enddot = endWithDot ? '.' : '',
			belCounterJusti = believeThatGoodCounter + ' <b>' + conclusion + '</b>',
			undermine = w + ', ' + itIsFalse + ' <b>' + confrontation + '</b>' + enddot,
			support	  = r + ', ' + itIsTrue + ' <b>' + confrontation + '</b>' + enddot,
			undercut  = r + ', <b>' + confrontation + '</b>, ' + butIDoNot + ' ' + belCounterJusti + enddot,
			overbid	  = r + ', <b>' + confrontation + '</b>, ' + andIDo + ' ' + belCounterJusti + enddot,
			rebut	  = r + ', <b>' + confrontation + '</b> ' + iAcceptCounter + ' <b>' + premisse
				+ '</b>. ' + iHaveStrongerArgument + ' <b>' + premisse + '</b>' + enddot,
			noopinion  = iNoOpinion + ': <b>' + confrontation + '</b>. ' + goStepBack + '.';
		return [undermine, support, undercut, overbid, rebut, noopinion];
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isStartStatement if true, argumentButtonWasClicked is used, otherwise
	 * @param isPremisse
	 * @param isRelation
	 * @param mouseover
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getKeyValAsInputInLiWithType = function (key, val, isStartStatement, isPremisse, isRelation, mouseover) {
		return this.getKeyValAsInputInLiWithType(key, val, isStartStatement, isPremisse, isRelation, mouseover, {'text_count':'0'});
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isStartStatement if true, argumentButtonWasClicked is used, otherwise
	 * @param isPremisse
	 * @param isRelation
	 * @param mouseover
	 * @param additionalAttributesAsDict
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getKeyValAsInputInLiWithType = function (key, val, isStartStatement, isPremisse, isRelation, mouseover, additionalAttributesAsDict) {
		var liElement, inputElement, labelElement, extras = '', tmp;
		liElement = $('<li>');
		liElement.attr({id: 'li_' + key});

		inputElement = $('<input>');
		inputElement.attr({id: key, type: 'radio', value: val});
		//inputElement.attr({data-dismiss: 'modal'});

		if (typeof additionalAttributesAsDict !== 'undefined')
			$.each(additionalAttributesAsDict, function getKeyValAsInputInLiWithTypeEach(key, val) {
				extras += ' ' + key + '="' + val + '"';
			});

		inputElement.attr({name: radioButtonGroup});
		// adding label for the value
		labelElement = '<label title="' + mouseover + '" for="' + key + '">' + val + '</label>';

		inputElement.attr({onclick: 'new InteractionHandler().radioButtonChanged();'});
		if (isStartStatement){ inputElement.addClass('start'); }
		if (isPremisse){ inputElement.addClass('premisse'); }
		if (isRelation){ inputElement.addClass('relation'); }
		if (!isStartStatement && !isPremisse && !isRelation){ inputElement.addClass('add'); }

		tmp = new Helper().getFullHtmlTextOf(inputElement);
		tmp = tmp.substr(0,tmp.length-1) + extras + '>';
		liElement.html(tmp + labelElement);

		return liElement;
	};

	this.createRowInEditDialog = function(uid, statement, type){
		var edit_button, log_button, guiHandler = new GuiHandler(), ajaxHandler = new AjaxSiteHandler(), tr, td_text, td_buttons;

		// create new items
		tr = $('<tr>');
		td_text = $('<td>').attr({
			id: 'edit_' + type + '_td_text_' + uid
		});
		td_buttons = $('<td>').css('text-align', 'center');
		edit_button = $('<input>').css('margin', '2px');
		log_button = $('<input>').css('margin', '2px');

		// set attributes, text, ...
		td_text.text(statement);

		// some attributes and functions for the edit button
		edit_button.attr({
			id: 'edit-statement',
			type: 'button',
			value: 'edit',
			class: 'btn-sm btn button-primary',
			statement_type: type,
			statement_text: statement,
			statement_id: uid
		}).click(function edit_button_click() {
			$('#' + popupEditStatementTextareaId).text($(this).attr('statement_text')).attr({'statement_id': uid});
			$('#' + popupEditStatementSubmitButtonId).attr({
				statement_type: $(this).attr('statement_type'),
				statement_text: $(this).attr('statement_text'),
				statement_id: $(this).attr('statement_id'),
				callback_td: 'edit_' + type + '_td_text_' + uid
			});
			$('#edit_statement_table td').removeClass('table-hover');
			$('#edit_' + type + '_td_index_' + uid).addClass('table-hover');
			$('#edit_' + type + '_td_text_' + uid).addClass('table-hover');
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');
			guiHandler.showEditFieldsInEditPopup();
			guiHandler.hideLogfileInEditPopup();
		}).hover(function edit_button_hover() {
			$(this).toggleClass('btn-primary', 400);
		});

		// show logfile
		log_button.attr({
			id: 'show_log_of_statement',
			type: 'button',
			value: 'changelog',
			class: 'btn-sm btn button-primary',
			statement_type: type,
			statement_text: statement,
			statement_id: uid
		}).click(function log_button_click() {
			$('#' + popupEditStatementLogfileHeaderId).html('Logfile for: <b>' + $(this).attr('statement_text') + '</b>');
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');
			$('#edit_statement_table td').removeClass('table-hover');
			ajaxHandler.getLogfileForStatement($(this).attr('statement_id'));
			guiHandler.hideEditFieldsInEditPopup();
		}).hover(function log_button_hover() {
			$(this).toggleClass('btn-primary', 400);
		});

		// append everything
		td_buttons.append(edit_button);
		td_buttons.append(log_button);
		tr.append(td_text);
		tr.append(td_buttons);

		return tr;
	}
}