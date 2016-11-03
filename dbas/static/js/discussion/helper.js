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
	 * Returns the uid of current issue
	 * @returns {number}
	 */
	this.getCurrentIssueId = function(){
		return $('#' + issueDropdownButtonID).attr('issue');
	};

	/**
	 * Sets Cookie with given name for given days
	 * @param cookie_name string
	 * @param days int
	 * @param content value
	 */
	this.setCookieForDays = function(cookie_name, days, content){
		var d = new Date();
		var expiresInDays = days * 24 * 60 * 60 * 1000;
		d.setTime( d.getTime() + expiresInDays );
		var expires = 'expires=' + d.toGMTString();
		document.cookie = cookie_name + '=' + content + '; ' + expires + ';path=/';

		$(document).trigger('user_cookie_consent_changed', {'consent' : content});
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
	
	/**
	 *
	 * @returns {*}
	 */
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
	
	/**
	 *
	 * @returns {number}
	 */
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
	
	/**
	 *
	 * @param element
	 * @returns {number}
	 */
	this.getPaddingOfElement = function (element){
		return parseInt(element.css('padding-top').replace('px','')) + parseInt(element.css('padding-bottom').replace('px',''))
	};
	
	/**
	 *
	 * @returns {boolean}
	 */
	this.isMobileAgent = function(){
		return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
	};
	
	/**
	 *
	 * @param key
	 * @param value
	 * @returns {boolean}
	 */
	this.setLocalStorage = function (key, value){
		try {
			localStorage.setItem(key, value);
			return true;
		} catch(err){
			console.log('Error while set item in local storage.');
			return false;
		}
	};
	
	/**
	 *
	 * @param key
	 * @returns {undefined}
	 */
	this.getLocalStorage = function (key){
		try {
			return localStorage.getItem(key);
		} catch(err){
			console.log('Error while get item in local storage.');
			return undefined;
		}
	};

	/**
	 * Roates the little pin icon in the sidebar
	 * @param element
	 * @param degree
	 */
	this.rotateElement = function(element, degree){
		element.css('-ms-transform', 'rotate(' + degree + 'deg)')
			.css('-webkit-transform', 'rotate(' + degree + 'deg)')
			.css('transform', 'rotate(' + degree + 'deg)');
	};

	/**
	 * Sets an animation speed for a specific element
	 * @param element
	 * @param speed
	 */
	this.setAnimationSpeed = function(element, speed){
		element.css('-webkit-transition', 'all ' + speed + 's ease')
			.css('-moz-transition', 'all ' + speed + 's ease')
			.css('-o-transition', 'all ' + speed + 's ease')
			.css('transition', 'all ' + speed + 's ease');
	};
	
	/**
	 *
	 * @param anchor
	 */
	this.setAnchor = function(anchor){
		location.hash = anchor;
		console.log('Set Anchor: ' + anchor);
	};
	
	/**
	 *
	 */
	this.clearAnchor = function(){
		location.hash = '';
		console.log('Cleared Anchor');
	};
	
	/**
	 * Src: http://stackoverflow.com/questions/11919065/sort-an-array-by-the-levenshtein-distance-with-best-performance-in-javascript
	 * @param s1
	 * @param s2
	 */
	this.levensthein = function(s1, s2){
		var row2=[];
		if (s1 === s2) {
			return 0;
		} else {
			var s1_len = s1.length, s2_len = s2.length;
			if (s1_len && s2_len) {
				var i1 = 0, i2 = 0, a, b, c, c2, row = row2;
				while (i1 < s1_len)
					row[i1] = ++i1;
				while (i2 < s2_len) {
					c2 = s2.charCodeAt(i2);
					a = i2;
					++i2;
					b = i2;
					for (i1 = 0; i1 < s1_len; ++i1) {
						c = a + (s1.charCodeAt(i1) === c2 ? 0 : 1);
						a = row[i1];
						b = b < a ? (b < c ? b + 1 : c) : (a < c ? a + 1 : c);
						row[i1] = b;
					}
				}
				return b;
			} else {
				return s1_len + s2_len;
			}
		}
	};
}
