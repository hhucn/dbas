/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function Helper() {

	/**
	 * Insert a <br>-tag after the given maxTextWidth or char
	 * @param text string
	 * @param maxTextWidth int
	 * @param charr char
	 * @returns {String}
	 */
	this.cutTextOnChar = function (text, maxTextWidth, charr) {
		var i, p, l;
			i = 1;
			l = text.length;
		while (i * maxTextWidth < l) {
			p = text.indexOf(charr, i * maxTextWidth);
			text =  text.substr(0, p) + '<br>' + text.substr(p + charr.length);
			i = i + 1;
		}
		return text;
	};

	/**
	 * Swaps the element with the paramter
	 * @param from element
	 * @param to element
	 * @returns {*}
	 */
	this.swapElements = function(from, to) {
	    var copy_to = $(to).clone(true),
		    copy_from = $(from).clone(true);
		$(to).replaceWith(copy_from);
		$(from).replaceWith(copy_to);
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
	 * Creates an row in the edit statement modal dialog
	 * @param text String
	 * @param for_id int
	 * @param id_id int
	 * @returns {jQuery|HTMLElement|*} tr-Tag
	 */
	this.createRowInEditDialog = function(text, for_id, id_id){
		var edit_button, log_button, guiHandler = new GuiHandler(), ajaxHandler = new AjaxSiteHandler(), tr,
			td_text, td_buttons, tmp;

		// table items
		tr = $('<tr>');
		td_text = $('<td>').text(text).attr('id', 'td_' + id_id).attr('for', for_id);
		td_buttons = $('<td>').css('text-align', 'right');

		// buttons
		edit_button = $('<input>').css('margin', '2px')
			.attr('type', 'button')
			.attr('value', _t_discussion(edit))
			.attr('class', 'btn btn-primary btn-xs')
			.click(function edit_button_click() {
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

		log_button = $('<input>').css('margin', '2px')
			.attr('type', 'button')
			.attr('value', _t_discussion(changelog))
			.attr('class', 'btn btn-primary btn-xs')
			.click(function log_button_click() {
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
		return $('#' + issueDropdownButtonID).attr('issue');
	};

	/**
	 * Sets a cookie with given name
	 * @param cookie_name string
	 */
	this.setCookie = function(cookie_name){
		this.setCookieForDays(cookie_name, 7);
	};

	/**
	 * Sets Cookie with given name for given days
	 * @param cookie_name string
	 * @param days int
	 * @param consent value
	 */
	this.setCookieForDays = function(cookie_name, days, consent){
		var d = new Date();
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
	 * Opens a new tab with the contact form. Given params should containt name and content
	 * @param params dictionary with at least {'name': ?, 'content': ?}
	 */
	this.redirectInNewTabForContact = function(params){
		var csrfToken = $('#' + hiddenCSRFTokenId).val();
		var csrfField = '<input type="hidden" name="csrf_token" value="' + csrfToken + '">';
		var f = $("<form target='_blank' method='POST' style='display:none;'>" + csrfField + "</form>").attr('action', mainpage + 'contact');
		f.appendTo(document.body);
		for (var prms in params) {
			if (params.hasOwnProperty(prms)) {
				f.append($('<input type="hidden" />').attr('name', prms).attr('value', params[prms]));
			}
		}
		f.submit().remove();
	};

	this.getMaxSizeOfGraphViewContainer = function(){
		var header, footer, innerHeight;
		header = $('#' + customBootstrapMenuId);
		footer = $('#footer');
		innerHeight = window.innerHeight;
		innerHeight -= header.outerHeight(true);
		innerHeight -= footer.outerHeight(true);
		innerHeight -= this.getPaddingOfElement(header);
		innerHeight -= this.getPaddingOfElement(footer);
		return innerHeight;
	};

	this.getMaxSizeOfDiscussionViewContainer = function(){
		var bar, innerHeight, list;
		bar = $('#header-container');
		list = $('#' + discussionSpaceListId);
		innerHeight = this.getMaxSizeOfGraphViewContainer();
		innerHeight -= bar.outerHeight(true);
		innerHeight -= list.outerHeight(true);
		innerHeight -= this.getPaddingOfElement(bar);
		innerHeight -= this.getPaddingOfElement(list);
		return innerHeight - 10;
	};

	this.getPaddingOfElement = function (element){
		return parseInt(element.css('padding-top').replace('px','')) + parseInt(element.css('padding-bottom').replace('px',''))
	};

	this.isMobileAgent = function(){
		return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
	};

	/**
	 * Delays a specific function
	 */
	this.delay = function(){
		var timer = 0;
		return function(callback, ms){
			clearTimeout (timer);
			timer = setTimeout(callback, ms);
		};
	}();
}
