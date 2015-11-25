/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function NavigationHandler(){
	'use strict';
	var navigationBreadcrumb = $('#navigation-breadcrumb'), textThreshold = 25;

	/**
	 *
	 * @param uid
	 * @returns {*|jQuery|HTMLElement}
	 */
	this.getLiElement = function(uid){
		var element = $('<li>');
		element.attr('uid',uid);
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
		aElement.attr('href', link).html(text).attr('title', text);
		return aElement;
	};

	/**
	 * Removes active class of the last child and adds an a-tag to the li-child
	 */
	this.setLastChildAsActive = function(text){
		var lastChild = navigationBreadcrumb.children().eq(navigationBreadcrumb.children().length-1);
		lastChild.addClass('active').empty().text(text);
	};

	/**
	 *
	 * @param url
	 * @param text
	 * @param uid
	 * @param useCutting
	 */
	this.addNavigationCrumb = function(url, text, uid, useCutting){
		var liElement = this.getLiElement(uid),
				shorttext = text.length > textThreshold ? text.substr(0, textThreshold) + '...' : text,
				aElement = this.getAElement(url, shorttext);
		liElement.append(aElement);
		navigationBreadcrumb.append(liElement);

		if (useCutting)
			liElement.hover(function(){
				aElement.html(text);
			}, function(){
				aElement.html(shorttext + '...');
			});
	};

	/**
	 * Set jsonData.history as bread crumbs
	 * @param jsonData
	 */
	this.setNavigationBreadcrumbs = function (jsonData){
		var parsedData = $.parseJSON(jsonData), nh = new NavigationHandler(), text = '';

		// check for data
		if (Object.keys(parsedData.history).length == 0){
			return;
		}

		navigationBreadcrumb.parent().parent().parent().show();

		$.each(parsedData.history, function addJsonDataToContentAsArgumentsEach(index, history) {
			if (history.url.indexOf(attrStart) != -1) {										text = _t(keywordStart);
			} else if (history.url.indexOf(attrChooseActionForStatement) != -1){ 			text = _t(keywordChooseActionForStatement) + ': ' + history.keyword;
			} else if (history.url.indexOf(attrGetPremisesForStatement) != -1){				text = _t(keywordGetPremisesForStatement) + ': ' + history.keyword;
			} else if (history.url.indexOf(attrMoreAboutArgument) != -1){ 					text = _t(keywordMoreAboutArgument) + ': ' + history.keyword;
			} else if (history.url.indexOf(attrReplyForPremisegroup) != -1){				text = _t(keywordReplyForPremisegroup) + ': ' + history.keyword;
			} else if (history.url.indexOf(attrReplyForResponseOfConfrontation) != -1){		text = _t(keywordReplyForResponseOfConfrontation) + ': ' + history.keyword;
			} else if (history.url.indexOf(attrReplyForArgument) != -1){					text = _t(keywordReplyForArgument) + ': ' + history.keyword;
			}
			nh.addNavigationCrumb(history.url, text, history.uid, history.url.indexOf(attrStart) == -1);
		});
		this.setLastChildAsActive(text);
	};
}