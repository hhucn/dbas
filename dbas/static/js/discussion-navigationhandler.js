/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function NavigationHandler(){
	'use strict';
	var navigationBreadcrumb = $('#navigation-breadcrumb');

	/**
	 *
	 * @param classes[]
	 * @param attributes
	 * @param text
	 * @returns {*|jQuery|HTMLElement}
	 */
	this.getLiElement = function(classes, attributes, text){
		var element = $('<li>');
		element.html(text);
		$.each(classes, function eachClasses(index, value) {
			element.addClass(value);
		});
		$.each(attributes, function eachAttributes(key, value) {
			element.attr(key, value);
		});
		return element;
	};

	/**
	 *
	 * @param link
	 * @param text
	 * @returns {*|jQuery|HTMLElement}
	 */
	this.getAElement = function(link, text){
		var aElement = $('<a>');
		aElement.attr('href', link).html(text);
		return aElement;
	};

	/**
	 * Removes active class of the last child and adds an a-tag to the li-child
	 */
	this.setLastChildAsNonActive = function(){
		var length = navigationBreadcrumb.children().length(),
				lastChild = navigationBreadcrumb.children().eq(length-1),
				aElement = this.getAElement(lastChild.attr('url'), lastChild.attr('t') + ' ' + lastChild.attr('s'));
		lastChild.removeClass('active').empty().append(aElement);

	};


	/**
	 * Reset the navigation breadcrumb
	 */
	this.resetNavigation = function(){
		var liElement = this.getLiElement(['active'], {'url': window.location.href, 't': initialPosition, 's':''}, _t(initialPosition));
		navigationBreadcrumb.empty().append(liElement);
	};

	/**
	 * Adding a new, active child
	 * @param textId id of text phrase
	 * @param statement stirng of the current statement
	 */
	this.addNavigationCrumb = function(textId, statement){
		var liElement = this.getLiElement(['active'], {'url': window.location.href, 't': textId, 's': statement}, _t(textId) + ' ' + statement);
		this.setLastChildAsNonActive();
		navigationBreadcrumb.append(liElement);
	}
}