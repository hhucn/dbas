/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

/**
 * Insert a <br>-tag after the given maxTextWidth or char
 *
 * @param text string
 * @param maxTextWidth int
 * @param charr char
 * @returns {String}
 */
function cutTextOnChar (text, maxTextWidth, charr) {
	var i, p, l;
		i = 1;
		l = text.length;
	while (i * maxTextWidth < l) {
		p = text.indexOf(charr, i * maxTextWidth);
		text =  text.substr(0, p) + '<br>' + text.substr(p + charr.length);
		i = i + 1;
	}
	return text;
}

/**
 * Use the browser's built-in functionality to quickly and safely escape the string
 * Based on http://shebang.brandonmintern.com/foolproof-html-escaping-in-javascript/
 *
 * @param text to escape
 * @returns {*} escaped string
 */
function escapeHtml (text) {
	var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

/**
 * Returns the uid of current issue
 *
 * @returns {number}
 */
function getCurrentIssueId (){
	return $('#' + issueDropdownButtonID).attr('issue');
}

/**
 * Sets Cookie with given name for given days
 *
 * @param cookie_name string
 * @param days int
 * @param content value
 */
function setCookieForDays (cookie_name, days, content){
	var d = new Date();
	var expiresInDays = days * 24 * 60 * 60 * 1000;
	d.setTime( d.getTime() + expiresInDays );
	var expires = 'expires=' + d.toGMTString();
	document.cookie = cookie_name + '=' + content + '; ' + expires + ';path=/';

	$(document).trigger('user_cookie_consent_changed', {'consent' : content});
}

/**
 * Returns true if the cookie with given name is set.
 *
 * @param cookie_name string
 * @returns {boolean}
 */
function isCookieSet (cookie_name){
	var cookies = document.cookie.split(";"), userAcceptedCookies = false;
	for (var i = 0; i < cookies.length; i++) {
		var c = cookies[i].trim();
		if (c.indexOf(cookie_name) == 0) {
			userAcceptedCookies = c.substring(cookie_name.length + 1, c.length);
		}
	}
	return userAcceptedCookies;
}

/**
 * Opens a new tab with the contact form. Given params should contain name and content
 *
 * @param params dictionary with at least {'name': ?, 'content': ?}
 */
function redirectInNewTabForContact (params){
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
}
	
/**
 * Writes key-value-pair into local storage and returns boolean
 *
 * @param key
 * @param value
 * @returns {boolean}
 */
function setLocalStorage (key, value){
	try {
		localStorage.setItem(key, value);
		return true;
	} catch(err){
		console.log('Error while set item in local storage.');
		return false;
	}
}

/**
 * Reads the entry of local storage by key
 *
 * @param key
 * @returns {undefined}
 */
function getLocalStorage (key){
	try {
		return localStorage.getItem(key);
	} catch(err){
		console.log('Error while get item in local storage.');
		return undefined;
	}
}
	
/**
 * Sets an anchor into the location
 *
 * @param anchor string
 */
function setAnchor (anchor){
	location.hash = anchor;
}

/**
 * Clears all anchors in the location
 */
function clearAnchor (){
	location.hash = '';
}
