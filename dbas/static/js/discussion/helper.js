/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

/**
 * Insert a <br>-tag after the given maxTextWidth or pattern
 *
 * @param text string
 * @param maxTextWidth int
 * @param pattern string
 * @returns {String}
 */
function cutTextOnChar (text, maxTextWidth, pattern) {
	'use strict';
	var i, p, l;
		i = 1;
		l = text.length;
	while (i * maxTextWidth < l) {
		p = text.indexOf(pattern, i * maxTextWidth);
		text =  text.substr(0, p) + '<br>' + text.substr(p + pattern.length);
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
	'use strict';
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
	'use strict';
	var issue = $('#' + issueDropdownButtonID).attr('issue');
	if (!issue) {
		issue = $('#issue_info').data('issue');
	}
	return issue;
}

/**
 * Opens a new tab with the contact form. Given params should contain name and content
 *
 * @param params dictionary with at least {'name': ?, 'content': ?}
 */
function redirectInNewTabForContact (params){
	'use strict';
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
	'use strict';
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
	'use strict';
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
	'use strict';
	location.hash = anchor;
}

/**
 * Clears all anchors in the location
 */
function clearAnchor (){
	'use strict';
	location.hash = '';
}

/**
 * Returns true, if the used device is a mobile agent
 *
 * @returns {boolean}
 */
function isMobileAgent(){
	'use strict';
	return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}