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
	 * @param shorttext
	 * @returns {*|jQuery|HTMLElement}
	 */
	this.getAElement = function(link, text, shorttext){
		var aElement = $('<a>');
		aElement.attr('href', link).html(shorttext).attr('title', text);
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
	 * @param useHoverDueToCutting
	 */
	this.addNavigationCrumb = function(url, text, uid, useHoverDueToCutting){
		var liElement = this.getLiElement(uid),
				shorttext = text.length > textThreshold ? text.substr(0, textThreshold) + '...' : text,
				aElement = this.getAElement(url, text, shorttext);
		liElement.append(aElement);
		navigationBreadcrumb.append(liElement);

		if (useHoverDueToCutting)
			liElement.hover(function(){
				aElement.html(text);
			}, function(){
				aElement.html(shorttext);
			});
	};

	/**
	 * Set jsonData.history as bread crumbs
	 * @param jsonData
	 */
	this.setNavigationBreadcrumbs = function (jsonData){
		var parsedData = $.parseJSON(jsonData), nh = new NavigationHandler(), before = '', after = '';

		// check for data
		if (Object.keys(parsedData.history).length == 0){
			return;
		}

		// show breadcrumbs
		navigationBreadcrumb.parent().parent().parent().show();

		$.each(parsedData.history, function addJsonDataToContentAsArgumentsEach(index, history) {
			//before = history.keyword_before_decission;
			after = history.keyword_after_decission;
			/*
			if (history.url.indexOf(attrStart) != -1) {										before = _t(keywordStart);
			} else if (history.url.indexOf(attrChooseActionForStatement) != -1){ 			before = _t(keywordChooseActionForStatement) + ': ' + before;
			} else if (history.url.indexOf(attrGetPremisesForStatement) != -1){				before = _t(keywordGetPremisesForStatement) + ': ' + before;
			} else if (history.url.indexOf(attrMoreAboutArgument) != -1){ 					before = _t(keywordMoreAboutArgument) + ': ' + before;
			} else if (history.url.indexOf(attrReplyForPremisegroup) != -1){				before = _t(keywordReplyForPremisegroup) + ': ' + before;
			} else if (history.url.indexOf(attrReplyForResponseOfConfrontation) != -1){		before = _t(keywordReplyForResponseOfConfrontation) + ': ' + before;
			} else if (history.url.indexOf(attrReplyForArgument) != -1){					before = _t(keywordReplyForArgument) + ': ' + before;
			}
			*/
			nh.addNavigationCrumb(history.url, after, history.uid, false); //history.url.indexOf(attrStart) == -1);
		});
		before = $('#' + discussionsDescriptionId).html();
		before = before.substr(0, (before.indexOf('<br>') != -1 ? before.indexOf('<br>') : before.length));
		before = new Helper().clearHtml(before);
		this.setLastChildAsActive(before);

		// change document title
		document.title = document.title.substr(0, document.title.indexOf(' - ')) + ' - ' + before;
	};
}