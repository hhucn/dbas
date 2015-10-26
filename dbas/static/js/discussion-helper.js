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

		var w = startLowerCase ? this.startWithLowerCase(_t(wrong)) : this.startWithUpperCase(_t(wrong)),
			r = startLowerCase ? this.startWithLowerCase(_t(right)) : this.startWithUpperCase(_t(right)),
			enddot = endWithDot ? '.' : '',
			counterJusti = ' <b>' + conclusion + ', </b>' + _t(because).toLocaleLowerCase() + '<b> ' + premisse + '</b>', // todo with or without premisse ?
			undermine = '<b>' + w + ', ' + _t(itIsFalse) + " " + premisse + '</b>' + enddot,
			support	  = '<b>' + r + ', ' + _t(itIsTrue) + " " + premisse + '</b>' + enddot,
			undercut  = '<b>' + r + ', ' + confrontation + '</b>, ' + _t(butIDoNotBelieve) + ' ' + counterJusti + enddot,
			overbid	  = '<b>' + r + ', ' + confrontation + '</b>, ' + _t(andIDoBelieve) + ' ' + counterJusti + enddot,
			rebut	  = '<b>' + r + ', ' + confrontation + '</b> ' + _t(iAcceptCounter) + ' <b>' + conclusion
				+ '</b>.<br><br>' + _t(iHaveStrongerArgument) + ' <b>' + premisse + '</b>' + enddot,
			noopinion  = _t(iNoOpinion) + ' <b>' + conclusion + '</b>. ' + _t(goStepBack) + '.';
		return [undermine, support, undercut, overbid, rebut, noopinion];
	};

	/**
	 * Returns all kinds of attacks for the given confrontation and conclusion
	 * @param confrontation current confrontation
	 * @param conclusion current conclusion
	 * @param premisse current premisse
	 * @param attackType current type of the attack
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param endWithDot, true, when each sentences should end with a dot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut, dontknow, irrelevant]
	 */
	this.createConfrontationsRelationsText = function(confrontation, conclusion, premisse, attackType, startLowerCase, endWithDot){
		var rebutConclusion;
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// if (attackType == 'undermine'){			rebutConclusion = premisse;
		// } else if (attackType == 'rebut'){		rebutConclusion = conclusion;
		// } else if (attackType == 'undercut'){	rebutConclusion = conclusion + ' ' + _t(because).toLocaleLowerCase() + ' ' + premisse;
		// }
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?
		// TODO THIS! Ajax: ajax_reply_for_response_of_confrontation; But how are statements inserted on the following page?

		if (conclusion.substr(conclusion.length-1) == '.')
			conclusion = conclusion.substr(0, conclusion.length-1);

		var w = startLowerCase ? this.startWithLowerCase(_t(wrong)) : this.startWithUpperCase(_t(wrong)),
			r = startLowerCase ? this.startWithLowerCase(_t(right)) : this.startWithUpperCase(_t(right)),
			enddot = endWithDot ? '.' : '',
			counterJusti = ' <b>' + conclusion + ', </b>' + _t(because).toLocaleLowerCase() + '<b> ' + premisse + '</b>', // todo with or without premisse ?
			undermine = w + ', ' + _t(itIsFalse) + ' <b>' + confrontation + '</b>' + enddot,
			support	  = r + ', ' + _t(itIsTrue) + ' <b>' + confrontation + '</b>' + enddot,
			undercut  = r + ', <b>' + confrontation + '</b>, ' + _t(butIDoNotBelieve) + ' ' + counterJusti + enddot,
			overbid	  = r + ', <b>' + confrontation + '</b>, ' + _t(andIDoBelieve) + ' ' + counterJusti + enddot,
			rebut	  = r + ', <b>' + confrontation + '</b> ' + _t(iAcceptCounter) + ' <b>' + conclusion + ' ' + _t(because).toLocaleLowerCase() + ' ' + premisse
				+ '</b>. ' + _t(iHaveStrongerArgument) + ' <b>' + rebutConclusion + '</b>' + enddot,
			noopinion  = _t(iNoOpinion) + ': <b>' + confrontation + '</b>. ' + _t(goStepBack) + '.';
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
			$('#' + popupEditStatementTableId + ' td').removeClass('table-hover');
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
}