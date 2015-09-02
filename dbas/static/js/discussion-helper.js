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
	 * @param premisse current premisses
	 * @param conclusion current conclusion
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param endWithDot, true, when each sentences should end with a dot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createRelationsText = function(premisse, conclusion, startLowerCase, endWithDot){
		if (premisse.substr(premisse.length-1) == ".")
			premisse = premisse.substr(0, premisse.length-1);

		if (conclusion.substr(conclusion.length-1) == ".")
			conclusion = conclusion.substr(0, conclusion.length-1);

		var w = startLowerCase ? 'wrong' : 'Wrong',
			r = startLowerCase ? 'right' : 'Right',
			enddot = endWithDot ? '.' : '',
			belCounterJusti = 'believe that this is a good counter-argument for my justification',
			undermine = '<b>' + w + ', it is not true that ' + premisse + '</b>' + enddot,
			support	  = '<b>' + r + ', it is true that ' + premisse + '</b>' + enddot,
			undercut  = '<b>' + r + ', ' + premisse + '</b>, but I do not ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			overbid	  = '<b>' + r + ', ' + premisse + '</b>, and I do ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			rebut	  = '<b>' + r + ', ' + premisse + '</b> and I do accept that this is an counter-argument for <b>' + conclusion
				+ '</b>. However, I have a much stronger argument for accepting that <b>' + conclusion + '</b>' + enddot,
			dontknow   = r + ' I do not know whether <b>' + premisse + '</b> is right or wrong. Let me give another support for my opinion.',
			irrelevant = r + ' I do not care about: <b>' + premisse + '</b>. Let me give another support for my opinion.';
		return [undermine, support, undercut, overbid, rebut, dontknow, irrelevant];
	};

	/**
	 * Returns all kinds of attacks for the given confrontation and conclusion
	 * @param confrontation current confrontation
	 * @param conclusion current conclusion
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param endWithDot, true, when each sentences should end with a dot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createConfrontationsRelationsText = function(confrontation, conclusion, startLowerCase, endWithDot){

		if (conclusion.substr(conclusion.length-1) == ".")
			conclusion = conclusion.substr(0, conclusion.length-1);

		var w = startLowerCase ? 'wrong' : 'Wrong',
			r = startLowerCase ? 'right' : 'Right',
			i = startLowerCase ? 'irrelevant' : 'Irrelevant',
			enddot = endWithDot ? '.' : '',
			belCounterJusti = 'believe that this is a good counter-argument for my justification',
			undermine = w + ', it is not true that <b>' + confrontation + '</b>' + enddot,
			support	  = r + ', it is true that <b>' + confrontation + '</b>' + enddot,
			undercut  = r + ', <b>' + confrontation + '</b>, but				 I do not ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			overbid	  = r + ', <b>' + confrontation + '</b>, and I do ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			rebut	  = r + ', <b>' + confrontation + '</b> and I do accept that this is an counter-argument for <b>' + conclusion
				+ '</b>. However, I have a much stronger argument for accepting that <b>' + conclusion + '</b>' + enddot,
			dontknow   = i + ', I do not know whether <b>' + confrontation + '</b> is right or wrong. Let me give another support for my opinion.',
			irrelevant = i + ', I do not care about: <b>' + confrontation + '</b>.  Let me give another support for my opinion.';
		return [undermine, support, undercut, overbid, rebut, dontknow, irrelevant];
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

		inputElement.attr({onclick: "new InteractionHandler().radioButtonChanged(this.id);"});
		if (isStartStatement){ inputElement.addClass('start'); }
		if (isPremisse){ inputElement.addClass('premisse'); }
		if (isRelation){ inputElement.addClass('relation'); }
		if (!isStartStatement && !isPremisse && !isRelation){ inputElement.addClass('add'); }

		tmp = new Helper().getFullHtmlTextOf(inputElement);
		tmp = tmp.substr(0,tmp.length-1) + extras + ">";
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
			$('#' + popupEditStatementTextareaId).text($(this).attr('statement_text'));
			$('#' + popupEditStatementSubmitButtonId).attr({
				statement_type: $(this).attr('statement_type'),
				statement_text: $(this).attr('statement_text'),
				statement_id: $(this).attr('statement_id'),
				callback_td: 'edit_' + type + '_td_text_' + uid
			});
			$('#edit_statement_table td').removeClass('table-hover');
			$('#edit_' + type + '_td_index_' + uid).addClass('table-hover');
			$('#edit_' + type + '_td_text_' + uid).addClass('table-hover');
			$('#' + popupErrorDescriptionId).text('');
			$('#' + popupSuccessDescriptionId).text('');
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
			$('#' + popupErrorDescriptionId).text('');
			$('#' + popupSuccessDescriptionId).text('');
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