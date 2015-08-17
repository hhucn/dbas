/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function fbShare(url, title, descr, image) {
	'use strict';
	var winTop, winLeft, winWidth, winHeight;
	winWidth = 520;
	winHeight = 350;
	winTop = (screen.height / 2) - (winHeight / 2);
	winLeft = (screen.width / 2) - (winWidth / 2);
	window.open('http://www.facebook.com/sharer.php?s=100&p[title]=' + title + '&p[summary]=' + descr + '&p[url]='
		+ url + '&p[images][0]=' + image, 'sharer',
		',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width='	+ winWidth + ',height=' + winHeight);
}

function tweetShare(text){
	'use strict';
	var winTop, winLeft, winWidth, winHeight;
	winWidth = 550;
	winHeight = 420;
	winTop = (screen.height / 2) - (winHeight / 2);
	winLeft = (screen.width / 2) - (winWidth / 2);
	window.open('https://twitter.com/intent/tweet?text=' + text + '&hashtags=DBAS', 'sharer',
		',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
}

function mailShare(to, subject, body){
	'use strict';
	window.location.href = "mailto:" + to + "?subject=" + subject + "&body=" + body;
}

function googleShare(url){
	'use strict';
	'use strict';
	var winTop, winLeft, winWidth, winHeight;
	winWidth = 600;
	winHeight = 400;
	winTop = (screen.height / 2) - (winHeight / 2);
	winLeft = (screen.width / 2) - (winWidth / 2);
	window.open('https://plus.google.com/share?url=' + url, 'sharer',
		',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
}

function getDateFromContainer(container) {
	'use strict';
	var textarray = container.html().split('<h3><p>');
	textarray = textarray[1].split('</p>');
	return textarray[0];
}

function getAuthorFromContainer(container) {
	'use strict';
	var textarray = container.html().split('Author: ');
	textarray = textarray[1].split('</h4>');
	return textarray[0];

}

function getSubjectFromContainer(container) {
	'use strict';
	var textarray = container.html().split('<span class="font-semi-bold">');
	textarray = textarray[1].split('</span>');
	return textarray[0];
}

$(document).ready(function () {
	'use strict';

	// share email button
	$(".share-mail").click(function (event) {
		var container, subject, message, date, body, author, to;
		to = 'user@example.com';
		container = $(this).parents(".newscontainer");
		subject = "DBAS: " + getSubjectFromContainer(container);
		date = getDateFromContainer();
		author = getAuthorFromContainer();
		message = getSubjectFromContainer(container);

		body = "News from " + date + ", by " + author + ": " + message;

		mailShare(to, subject, body);

	});

	// share twitter button
	$(".share-twitter").click(function (event) {
		var container;
		container = $(this).parents(".newscontainer");
		tweetShare(getSubjectFromContainer(container));
	});

	// share google+ button
	$(".share-google").click(function (event) {
		var url;
		url = document.location.pathname;
		url = 'https://dbas.cn.uni-duesseldorf.de';
		googleShare(url);
	});

	// share facebook button
	$(".share-facebook").click(function (event) {
		var url;
		url = document.location.pathname;
		url = 'https://dbas.cn.uni-duesseldorf.de';
		fbShare(url, "FB Sharing", "Sharing of DBAS", "https://dbas.cs.uni-duesseldorf.de/static/images/logo.png");
	});
	

});

