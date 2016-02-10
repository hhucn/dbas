/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
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
	 *
	 * @param id
	 * @param title
	 * @param text
	 * @returns {jQuery|HTMLElement}
	 */
	this.getATagForDropDown = function (id, title, text) {
		return $('<a>')
				.attr('id', id)
				.attr('role', 'menuitem')
				.attr('tabindex', '-1')
				.attr('data-toggle', 'modal')
				.attr('title', title)
				.attr('href', '#')
				.text(text);
	};

	/**
	 * Return the full HTML text of an given element
	 * @param element which should be translated
	 */
	this.getFullHtmlTextOf = function (element) {
		return $('<div>').append(element).html();
	};

	/**
	 * Turns first character into lowercase
	 * @param text
	 * @returns {string}
	 */
	this.startWithLowerCase = function (text){
		return text.substr(0, 1).toLowerCase() + text.substr(1);
	};

	/**
	 * Turns first character into uppercase
	 * @param text
	 * @returns {string}
	 */
	this.startWithUpperCase = function (text){
		return text.substr(0, 1).toLocaleUpperCase() + text.substr(1);
	};

	/**
	 *
	 * @param text
	 * @param for_id
	 * @param id_id
	 * @returns {jQuery|HTMLElement|*}
	 */
	this.createRowInEditDialog = function(text, for_id, id_id){
		var edit_button, log_button, guiHandler = new GuiHandler(), ajaxHandler = new AjaxSiteHandler(), tr,
			td_text, td_buttons, tmp;

		// table items
		tr = $('<tr>');
		td_text = $('<td>').text(text).attr({id: 'td_' + id_id, for: for_id});
		td_buttons = $('<td>').css('text-align', 'right');

		// buttons
		edit_button = $('<input>').css('margin', '2px').attr({
			type: 'button',
			value: 'edit',
			class: 'btn-sm btn button-primary'
		}).click(function edit_button_click() {
			$('#' + popupEditStatementTextareaId).text($(this).parent().prev().text());
			$('#' + popupEditStatementContentId + ' td').removeClass('text-hover');
			$(this).parent().prev().addClass('text-hover');

			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');

			guiHandler.showEditFieldsInEditPopup();
			guiHandler.hideLogfileInEditPopup();

			$('#' + popupEditStatementSubmitButtonId).click(function edit_statement_click() {
				tmp = $('#' + popupEditStatementContentId + ' .text-hover');
				new AjaxSiteHandler().sendCorrectureOfStatement(tmp.attr('id').substr(3), $('#' + popupEditStatementTextareaId).val(), tmp);
			});
		}).hover(function edit_button_hover() {
			$(this).toggleClass('btn-primary', 400);
		});

		log_button = $('<input>').css('margin', '2px').attr({
			type: 'button',
			value: 'changelog',
			class: 'btn-sm btn button-primary'
		}).click(function log_button_click() {
			$('#' + popupEditStatementLogfileHeaderId).html(_t(logfile) + ': <strong>' + $(this).parent().prev().text() + '</strong>');
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');
			$('#' + popupEditStatementContentId + ' td').removeClass('text-hover');
			$(this).parent().prev().addClass('text-hover');
			ajaxHandler.getLogfileForStatement($(this).parent().prev().attr('id').substr(3));
			guiHandler.hideEditFieldsInEditPopup();
		}).hover(function edit_button_hover() {
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
		return $('#' + issueDropdownTextID).attr('issue');
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

		f.submit().remove();
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
