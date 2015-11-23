/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function NavigationHandler(){
	'use strict';
	var navigationBreadcrumb = $('#navigation-breadcrumb'),
		breadcrumbHome = $('#breadcrumb-home');

	/**
	 *
	 * @param id
	 * @param classes[]
	 * @param attributes
	 * @param text
	 * @returns {*|jQuery|HTMLElement}
	 */
	this.getLiElement = function(id, classes, attributes, text){
		var element = $('<li>');
		element.attr('id', id).html(text);
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
	 *
	 */
	this.resetNavigation = function(){
		var liElement = this.getLiElement('breadcrumb-home', ['active'], {'url': window.location.href}, _t(initialPosition));
		navigationBreadcrumb.empty().append(liElement);
	};

	/**
	 *
	 */
	this.addNavigationChooseAction = function(){
		var aElement = this.getAElement(breadcrumbHome.attr('url'), _t(initialPosition)),
			liElement = this.getLiElement('breadcrumb-choose-action', ['active'], {'url': window.location.href}, 'c');
		breadcrumbHome.removeClass('active').empty().append(aElement);

		navigationBreadcrumb.append(liElement);
	}
}