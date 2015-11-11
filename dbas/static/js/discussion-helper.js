/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function Helper() {

	/**
	 * For debugging: Displays an alert with entries of the json data
	 * @param jsonData data for displaying
	 */
	this.alertWithJsonData = function (jsonData){
		var txt = '';
		$.each(jsonData, function(k,v){
			txt += k+": " + v + "\n";
		});
		alert(txt);
	};

	/**
	 * Cuts off each punctuation at the end
	 * @param text
	 * @returns {*} text without {.,?,!} at the end
	 */
	this.cutOffPunctiation = function (text){
		if (text.indexOf('.') == text.length-1
				|| text.indexOf('?') == text.length-1
				|| text.indexOf('!') == text.length-1){
			text = text.substr(0, text.length-1);
		}
		return text;
	};

	/**
	 * Use the browser's built-in functionality to quickly and safely escape the string
	 * Based on http://shebang.brandonmintern.com/foolproof-html-escaping-in-javascript/
	 * @param text to escape
	 * @returns {*} escaped string
	 */
	this.escapeHtml = function(text) {
		var div = document.createElement('div');
    	div.appendChild(document.createTextNode(text));
    	return div.innerHTML;
	};

	/**
	 * Checks if the string contains one of the keyword undercut, rebut or undermine
	 * @param text to check
	 * @returns {boolean} if the string contains a keyword
	 */
	this.stringContainsAnAttack = function (text){
		return (text.indexOf('undermine') != -1
				|| text.indexOf('rebut') != -1
				|| text.indexOf('undercut') != -1);
	};

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
	 * Returns all kinds of attacks for the given premise and conclusion
	 * @param confrontation current confrontation
	 * @param premise current premises
	 * @param attackType current type of the attack
	 * @param lastAttack last attack
	 * @param conclusion current conclusion
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @returns {string} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createRelationsText = function(confrontation, premise, attackType, lastAttack, conclusion, startLowerCase){
		if (premise.substr(premise.length-1) == '.')
			premise = premise.substr(0, premise.length-1);

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		var rebutConclusion, w,  r;

		if (lastAttack == attr_undermine){			rebutConclusion = premise;
		} else if (lastAttack == attr_rebut){		rebutConclusion = conclusion;
		} else if (lastAttack == attr_undercut){	rebutConclusion = conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise;
		}

		// pretty print
		w = '<b>' + (startLowerCase ? this.startWithLowerCase(_t(wrong)) : this.startWithUpperCase(_t(wrong))) + ', ';
		r = '<b>' + (startLowerCase ? this.startWithLowerCase(_t(right)) : this.startWithUpperCase(_t(right))) + ', ';
		// counterJusti = ' <b>' + conclusion + ', </b>' + _t(because).toLocaleLowerCase() + '<b> ' + premise + '</b>';

		// different cases
		if (attackType === attr_undermine)	return w + _t(itIsFalse) + ' ' + confrontation + '</b>.';
		if (attackType === attr_support)	return r + _t(itIsTrue) + ' ' + confrontation + '</b>.';
		if (attackType === attr_undercut)	return r + confrontation + '</b>, ' + _t(butIDoNotBelieve) + ' <b>' + conclusion + '</b>.';
		if (attackType === attr_overbid)	return r + confrontation + '</b>, ' + _t(andIDoBelieve) + ' <b>' + conclusion + '</b>.';
		if (attackType === attr_rebut)		return r + confrontation + '</b> ' + _t(iAcceptCounter) + ' <b>' + conclusion + '</b>.<br><br>'
												+ _t(iHaveMuchStrongerArgument) + ' <b>' + rebutConclusion + '</b>.';
	};

	/**
	 * Returns all kinds of attacks for the given confrontation and conclusion
	 * @param confrontation current confrontation
	 * @param conclusion current conclusion
	 * @param premise current premise
	 * @param attackType current type of the attack
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createConfrontationsRelationsText = function(confrontation, conclusion, premise, attackType, startLowerCase){
		var rebutConclusion, w, r, counterJusti, undermine, support, undercut, overbid, rebut, noopinion;
		if (attackType == attr_undermine){			rebutConclusion = premise;
		} else if (attackType == attr_rebut){		rebutConclusion = conclusion;
		} else if (attackType == attr_undercut){	rebutConclusion = conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise;
		}

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		w = startLowerCase ? this.startWithLowerCase(_t(wrong)) : this.startWithUpperCase(_t(wrong));
		r = startLowerCase ? this.startWithLowerCase(_t(right)) : this.startWithUpperCase(_t(right));
		counterJusti = ' <b>' + conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise + '</b>';
		undermine = w + ', ' + _t(itIsFalse) + ' <b>' + confrontation + '</b>.';
		support	  = r + ', ' + _t(itIsTrue) + ' <b>' + confrontation + '</b>.';
		undercut  = r + ', <b>' + confrontation + '</b>, ' + _t(butIDoNotBelieve) + ' ' + counterJusti + '.';
		overbid	  = r + ', <b>' + confrontation + '</b>, ' + _t(andIDoBelieve) + ' ' + counterJusti + '.' + _t(iHaveEvenStrongerArgument) + ' ' + counterJusti + '.';
		rebut	  = r + ', <b>' + confrontation + '</b> ' + _t(iAcceptCounter) + ' <b>' + conclusion + '</b>. '
			+ _t(iHaveMuchStrongerArgument) + ' <b>' + rebutConclusion + '</b>.';
		noopinion  = _t(iNoOpinion) + ': <b>' + confrontation + '</b>. ' + _t(goStepBack) + '.';
		return [undermine, support, undercut, overbid, rebut, noopinion];
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isStartStatement if true, argumentButtonWasClicked is used, otherwise
	 * @param isPremise
	 * @param isRelation
	 * @param mouseover
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getKeyValAsInputInLiWithType = function (key, val, isStartStatement, isPremise, isRelation, mouseover) {
		return this.getKeyValAsInputInLiWithType(key, val, isStartStatement, isPremise, isRelation, mouseover, {'text_count':'0'});
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isStartStatement if true, argumentButtonWasClicked is used, otherwise
	 * @param isPremise
	 * @param isRelation
	 * @param mouseover
	 * @param additionalAttributesAsDict
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getKeyValAsInputInLiWithType = function (key, val, isStartStatement, isPremise, isRelation, mouseover, additionalAttributesAsDict) {
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
		if (isPremise){ inputElement.addClass('premise'); }
		if (isRelation){ inputElement.addClass('relation'); }
		if (!isStartStatement && !isPremise && !isRelation){ inputElement.addClass('add'); }

		tmp = new Helper().getFullHtmlTextOf(inputElement);
		tmp = tmp.substr(0,tmp.length-1) + extras + '>';
		liElement.html(tmp + labelElement);

		return liElement;
	};

	this.createRowInEditDialog = function(uid, statement, type){
		var edit_button, log_button, guiHandler = new GuiHandler(), ajaxHandler = new AjaxSiteHandler(), tr, td_text, td_buttons, tmp;

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
			tmp = $(this).attr('statement_text');
			if (tmp.indexOf(_t(because)) == 0){
				tmp = new Helper().startWithUpperCase(tmp.substr(_t(because).length+1));
			}
			$('#' + popupEditStatementTextareaId).text(tmp).attr({'statement_id': uid});
			$('#' + popupEditStatementSubmitButtonId).attr({
				statement_type: $(this).attr('statement_type'),
				statement_text: $(this).attr('statement_text'),
				statement_id: $(this).attr('statement_id'),
				callback_td: 'edit_' + type + '_td_text_' + uid
			});
			$('#' + popupEditStatementTableId + ' td').removeClass('text-hover');
			$('#edit_' + type + '_td_index_' + uid).addClass('text-hover');
			$('#edit_' + type + '_td_text_' + uid).addClass('text-hover');
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');
			guiHandler.showEditFieldsInEditPopup();
			guiHandler.hideLogfileInEditPopup();
		}).hover(function edit_button_hover() {
			$(this).toggleClass('btn-primary', 400);
		});

		// show logfile
		log_button.attr({
			id: popupEditStatementShowLogButtonId,
			type: 'button',
			value: 'changelog',
			class: 'btn-sm btn button-primary',
			statement_type: type,
			statement_text: statement,
			statement_id: uid
		}).click(function log_button_click() {
			$('#' + popupEditStatementLogfileHeaderId).html(_t(logfile) + ': <b>' + $(this).attr('statement_text') + '</b>');
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');
			$('#edit_statement_table td').removeClass('text-hover');
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
	};

	/**
	 *
	 * @returns {number}
	 */
	this.getCurrentIssueId = function(){
		return $('#' + issueDropdownButtonID).attr('issue');
	};

	/**
	 *
	 * @param cookie_name
	 */
	this.setCookie = function(cookie_name){
		this.setCookieForDays(cookie_name, 7);
	};

	/**
	 *
	 * @param cookie_name
	 * @param days
	 */
	this.setCookieForDays = function(cookie_name, days){
		var d = new Date(), consent = true;
		var expiresInDays = days * 24 * 60 * 60 * 1000; // Todo expiresInDays for how to write cookie
		d.setTime( d.getTime() + expiresInDays );
		var expires = 'expires=' + d.toGMTString();
		document.cookie = cookie_name + '=' + consent + '; ' + expires + ';path=/';

		$(document).trigger('user_cookie_consent_changed', {'consent' : consent});
	};

	/**
	 *
	 * @param cookie_name
	 * @returns {boolean}
	 */
	this.isCookieSet = function(cookie_name){
		var cookies = document.cookie.split(";"), userAcceptedCookies = false;
		for (var i = 0; i < cookies.length; i++) {
			var c = cookies[i].trim();
			if (c.indexOf(cookie_name) == 0) {
				userAcceptedCookies = c.substring(cookie_name.length + 1, c.length);
			}
		}
		return userAcceptedCookies;
	};

	/**
	 *
	 * @param string
	 * @param index
	 * @param character
	 * @param replacedCharacter
	 * @returns {string}
	 */
	this.replaceAt = function(string, index, character, replacedCharacter) {
    	return string.substr(0, index) + character + string.substr(index + replacedCharacter.length);
	};

	this.delay = (function(){
			var timer = 0;
			return function(callback, ms){
				clearTimeout (timer);
				timer = setTimeout(callback, ms);
			};
		})();
}