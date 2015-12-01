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
	this.alertWithJsonData = function (jsonData) {
		var txt = '';
		$.each(jsonData, function (k, v) {
			txt += k + ": " + v + "\n";
		});
		alert(txt);
	};

	/**
	 *
	 * @param text
	 * @param maxTextWidth
	 * @param char
	 * @returns {*}
	 */
	this.cutTextOnChar = function (text, maxTextWidth, char) {
		var i, pos, l;
			i = 1;
			l = text.length;
		while (i * maxTextWidth < l) {
			pos = text.indexOf(char, i * maxTextWidth);
			text = this.replaceAt(text, pos, '<br>', char);
			i = i + 1;
		}
		return text;
	};

	/**
	 *
	 * @param text
	 */
	this.resizeIssueText = function (text) {
		if ($(window).width() < 500) {
			text = this.cutTextOnChar(text, 30, ' ');
		} else if ($(window).width() < 1200) {
			text = this.cutTextOnChar(text, 50, ' ');
		}
		return text;
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
	 * Returns today as date
	 * @returns {string} date as dd.mm.yyy
	 */
	this.getTodayAsDate = function(){
		var d = new Date(),
				month = d.getMonth()+ 1,
				day = d.getDate();
		return ((day<10 ? '0' : '') + day + '.' +
		(month<10 ? '0' : '') + month + '.' +
		d.getFullYear());
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
	 * Removes all HTML-Signs
	 * @param text to escape
	 * @returns {*} cleared string
	 */
	this.clearHtml = function(text) {
		var p = $('<p>');
    	p.html(text);
    	return p.text();
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
	 * @param isAttacking
	 * @param isSupportive, true, if it should be supportive
	 * @returns {string} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createRelationsTextWithConfrontation = function(confrontation, premise, attackType, lastAttack, conclusion, startLowerCase, isAttacking, isSupportive){
		if (premise.substr(premise.length-1) == '.')
			premise = premise.substr(0, premise.length-1);

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		var longConclusion, w, r, text;

		//if (lastAttack == attr_undermine){			longConclusion = premise;
		//} else if (lastAttack == attr_rebut){		longConclusion = conclusion;
		//} else if (lastAttack == attr_undercut){	longConclusion = conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise;
		//}

		if (attackType === attr_overbid){
			if (isSupportive) 	longConclusion = conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise;
			else				longConclusion = premise + ', ' + _t(doesNotJustify).toLocaleLowerCase() + ' ' + conclusion;
		}
		// pretty print
		w = '<b>' + (startLowerCase ? this.startWithLowerCase(_t(wrong)) : this.startWithUpperCase(_t(wrong))) + ', ';
		r = '<b>' + (startLowerCase ? this.startWithLowerCase(_t(right)) : this.startWithUpperCase(_t(right))) + ', ';

		// different cases
		if (attackType === attr_undermine)	return w + _t(itIsFalse) + ' ' + confrontation + '</b>.';
		if (attackType === attr_support)	return r + _t(itIsTrue) + ' ' + confrontation + '</b>.';
		if (attackType === attr_undercut)	return r + confrontation + '</b>, ' + _t(butIDoNotBelieveCounter) + ' <b>' + conclusion + '</b>.';
		if (attackType === attr_overbid)	return r + confrontation + '</b>, ' + _t(andIDoBelieve) + ' <b>' + conclusion + '</b>.<br><br>'
												+ _t(howeverIHaveEvenStrongerArgumentAccepting) + ' <b>' + longConclusion + '</b>.';
		if (attackType === attr_rebut) {	text = r + confrontation + '</b> ' + _t(iAcceptCounter) + ' <b>' + conclusion + '</b>.<br><br>';
			if (isSupportive)               text += _t(howeverIHaveMuchStrongerArgumentAccepting) + ' <b>' + conclusion + '</b>.';
			else                            text += _t(howeverIHaveMuchStrongerArgumentRejecting) + ' <b>' + conclusion + '</b>.';
											return text;
		}
	};

	/**
	 * Returns all kinds of attacks for the given confrontation and conclusion
	 * @param confrontation current confrontation
	 * @param conclusion current conclusion
	 * @param premise current premise
	 * @param attackType current type of the attack
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param isSupportive, true, if it should be supportive
	 * @returns {*[]} array with [undermine, support, undercut, overbid, rebut, noopinion]:
	 *     undermine:
     *     support:
     *     undercut:
     *     overbid:
     *     rebut:
     *     no opinion:
	 */
	this.createConfrontationsRelationsText = function(confrontation, conclusion, premise, attackType, startLowerCase, isSupportive){
		var rebutConclusion, w, r, counterJusti, undermine, support, undercut, overbid, rebut, noopinion;

		// some options for pretty print
		if (attackType == attr_undermine){			rebutConclusion = premise;
		} else if (attackType == attr_rebut){		rebutConclusion = conclusion;
		} else if (attackType == attr_undercut){
			if (isSupportive)						rebutConclusion = conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise;
			else 									rebutConclusion = premise + ', ' +  _t(doesNotJustify).toLocaleLowerCase() + ' '  + conclusion;
		}

		if (isSupportive)
			counterJusti = ' <b>' + conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise + '</b>';
		else
			counterJusti = ' <b>' + premise + ', ' + _t(doesNotJustify).toLocaleLowerCase() + ' ' + conclusion + '</b>';

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		w = startLowerCase ? this.startWithLowerCase(_t(wrong)) : this.startWithUpperCase(_t(wrong));
		r = startLowerCase ? this.startWithLowerCase(_t(right)) : this.startWithUpperCase(_t(right));
		undermine = w + ', ' + _t(itIsFalse) + ' <b>' + confrontation + '</b>.';
		support	  = r + ', ' + _t(itIsTrue) + ' <b>' + confrontation + '</b>.';
		undercut  = r + ', <b>' + confrontation + '</b>, ' + _t(butIDoNotBelieveCounter) + ' ' + counterJusti + '.';
		overbid	  = r + ', <b>' + confrontation + '</b>, ' + _t(andIDoBelieve) + ' ' + counterJusti + '.<br>'
					+ _t(howeverIHaveEvenStrongerArgumentAccepting) + ' ' + counterJusti + '.';
		rebut	  = r + ', <b>' + confrontation + '</b> ' + _t(iAcceptCounter) + ' <b>' + conclusion + '</b>.<br>'
					+ (isSupportive ? _t(howeverIHaveEvenStrongerArgumentAccepting) : _t(howeverIHaveMuchEvenArgumentRejecting))
					+ ' <b>' + premise + '</b>.';
		noopinion  = _t(iNoOpinion) + ': <b>' + confrontation + '</b>. ' + _t(goStepBack) + '.';
		return [undermine, support, undercut, overbid, rebut, noopinion];
	};

	/**
	 * Returns all real attacks for the given premise and conclusion
	 * @param premise of current argument
	 * @param conclusion of current argument
	 * @param startLowerCase boolean
	 * @returns {*[]} array with [undermine, support, undercut, overbid, rebut, noopinion]:
	 *     undermine: premise is false
	 *     support: premise is true
	 *     undercut: premise is right, but no good justification for the conclusion
	 *     overbid: premise is right and a justification for the conclusion
	 *     rebut: premise and conclusion is right, but there is a stronger premise for rejecting the conclusion
	 *     no opinion: take me back
	 */
	this.createRelationsTextWithoutConfrontation = function (premise, conclusion, startLowerCase){
		var w, r, undermine, support, undercut, overbid, rebut, noopinion;

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		w = startLowerCase ? this.startWithLowerCase(_t(wrong)) : this.startWithUpperCase(_t(wrong));
		r = startLowerCase ? this.startWithLowerCase(_t(right)) : this.startWithUpperCase(_t(right));
		undermine 	= w + ', ' + _t(itIsFalse) + ' <b>' + premise + '</b>.';
		support 	= r + ', ' + _t(itIsTrue) + ' <b>' + premise + '</b>.';
		undercut  	= r + ', <b>' + premise + '</b>, ' + _t(butIDoNotBelieveArgument) + ' <b>' + conclusion + '</b>.';
		overbid 	= r + ', <b>' + premise + '</b>, ' + _t(andIDoBelieve) + ' <b>' + conclusion + '</b>.';
		rebut	  	= r + ', <b>' + premise + '</b> ' + _t(iAcceptArgument) + ' <b>' + conclusion + '</b>. '
			+ _t(howeverIHaveMuchStrongerArgumentRejecting) + ' <b>' + conclusion + '</b>.';
		noopinion  = _t(iNoOpinion) + ': <b>' + conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise + '</b>. ' + _t(goStepBack) + '.';
		return [undermine, support, undercut, overbid, rebut, noopinion];
	};

	/**
	 * Returns all real attacks for the given premise and conclusion
	 * @param premise
	 * @param conclusion
	 * @param startLowerCase boolean
	 * @returns {*[]}
	 */
	this.createAttacksOnlyText = function (premise, conclusion, startLowerCase){
		var w, r, counterJusti, undermine, undercut, rebut, noopinion;

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		w = (startLowerCase ? this.startWithLowerCase(_t(because)) : this.startWithUpperCase(_t(because))) + ' ' + this.startWithLowerCase(_t(itIsFalse));
		r = (startLowerCase ? this.startWithLowerCase(_t(because)) : this.startWithUpperCase(_t(because))) + ' ' + this.startWithLowerCase(_t(itIsTrue));
		counterJusti = ' <b>' + conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise + '</b>';

		undermine = w + ', <b>' + premise + '</b>.';
		undercut  = r + ', <b>' + conclusion + '</b>, ' + _t(butIDoNotBelieveArgument) + ' ' + counterJusti + '.';
		rebut	  = r + ', <b>' + premise + '</b> ' + _t(iAcceptArgument) + ' <b>' + conclusion + '</b>. '
			+ _t(howeverIHaveMuchStrongerArgumentRejecting) + ' <b>' + conclusion + '</b>.';


		noopinion  = _t(iNoOpinion) + ': <b>' + conclusion + ', ' + _t(because).toLocaleLowerCase() + ' ' + premise + '</b>. ' + _t(goStepBack) + '.';
		return [undermine, undercut, rebut, noopinion];
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

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param mouseover
	 * @param classes all classes
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getExtraInputInLiWithType = function (key, val, mouseover, classes) {
		var liElement, inputElement, labelElement, extras = '', tmp;
		liElement = $('<li>');
		liElement.attr({id: 'li_' + key});

		inputElement = $('<input>');
		inputElement.attr({id: key + '_' + classes[0], type: 'radio', value: val});
		//inputElement.attr({data-dismiss: 'modal'});

		inputElement.attr({name: radioButtonGroup}).attr({onclick: 'new InteractionHandler().radioButtonChanged();'});
		for (var i = 0; i < classes.length; i++) {
			inputElement.addClass(classes[i]);
		}
		// adding label for the value
		labelElement = '<label title="' + mouseover + '" for="' + key + '_' + classes[0] + '">' + val + '</label>';

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
	 * Returns the uid of current issue
	 * @returns {number}
	 */
	this.getCurrentIssueId = function(){
		return $('#' + issueDropdownButtonID).attr('issue');
	};

	/**
	 * Sets a cookie with given name
	 * @param cookie_name string
	 */
	this.setCookie = function(cookie_name){
		this.setCookieForDays(cookie_name, 1);
	};

	/**
	 * Sets Cookie with given name for given days
	 * @param cookie_name string
	 * @param days int
	 */
	this.setCookieForDays = function(cookie_name, days){
		var d = new Date(), consent = true;
		var expiresInDays = days * 24 * 60 * 60 * 1000;
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

	/**
	 * Opens a new tab with the contact form. Given params should containt name and content
	 * @param params dictionary with at least {'name': ?, 'content': ?}
	 */
	this.redirectInNewTabForContact = function(params){
		var f = $("<form target='_blank' method='POST' style='display:none;'></form>").attr({action: mainpage + 'contact'});
		f.appendTo(document.body);
		for (var i in params) {
			if (params.hasOwnProperty(i)) {
				f.append($('<input type="hidden" />').attr({
					name: i,
					value: params[i]
				}));
			}
		}

		f.submit();
		f.remove();
	};

	/**
	 * Delays a specific function
	 */
	this.delay = (function(){
		var timer = 0;
		return function(callback, ms){
			clearTimeout (timer);
			timer = setTimeout(callback, ms);
		};
	})();
}