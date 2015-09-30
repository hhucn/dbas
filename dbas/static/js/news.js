/**
 * Created by tobias on 30.09.15.
 */

/***
 *
 * @param title
 * @param date
 * @param author
 * @param news
 * @returns {string}
 */
function getNewsContainerAsHtml(title, date, author, news){
	return '<div class="container newscontainer"> <ul class="share-table"> <li> <a class="share-icon share-def"></a> <ul> <li> <a'
			+ ' class="share-icon share-mail"></a> </li> <li> <a class="share-icon share-twitter"></a> </li> <li> <a class="share-icon'
			+ ' share-google"></a></li><li>'
			+ '<a class="share-icon share-facebook"></a> </li> </ul> </li> </ul> <div class="row"> <div class="col-md-6"> <h3><span'
			+ 'class="font-semi-bold">'
			+ title
			+ '</span></h3></div><div class="col-md-4"><h4><p>'
			+ date
			+ '</p></h4></div></div><h5><span i18n:translate="author">Author</span>: '
			+ author
			+ '</h5><br>'
			+ news
			+ '</div>';
}

// *********************
//	AJAX
// *********************

/**
 *
 */
function ajaxGetNews (){
	$.ajax({
		url: 'ajax_get_news',
		type: 'POST',
		dataType: 'json',
		async: true
	}).done(function ajaxGetNewsDone(data) {
		callbackIfDoneForGettingNews(data);
	}).fail(function ajaxGetNewsFail() {
		$('#' + newsBodyId).append("<h4>" + internal_error + "</h4>");
	});
}

/**
 *
 */
function ajaxSendNews (){
	var title = $('#' + writingNewNewsTitleId).val(),
		text =  $('#' + writingNewNewsTextId).val();

	if (title.length == 0 || text.length < 10){
		$('#' + writingNewsFailedId).show();
		$('#' + writingNewsFailedMessageId).text(empty_news_input);
		return;
	} else {
		$('#' + writingNewsFailedId).hide();
		$('#' + writingNewsSuccessId).hide();
	}

	$.ajax({
		url: 'ajax_send_news',
		type: 'POST',
		data: { title: title, text:text},
		dataType: 'json',
		async: true
	}).done(function ajaxSendNewsDone(data) {
		callbackIfDoneForSendingNews(data);
	}).fail(function ajaxSendNewsFail() {
		$('#' + writingNewsFailedId).show();
		$('#' + writingNewsFailedMessageId).text(internal_error);
	});
}

// *********************
//	CALLBACKS
// *********************

/**
 *
 * @param data
 */
function callbackIfDoneForGettingNews(data) {
	var parsedData = $.parseJSON(data);
	$.each(parsedData, function callbackIfDoneForGettingNewsEach(key, val) {
		$('#' + newsBodyId).prepend(getNewsContainerAsHtml(val.title, val.date, val.author, val.news))
	});
}

/**
 *
 * @param data
 */
function callbackIfDoneForSendingNews(data) {
	var parsedData = $.parseJSON(data);
	if (parsedData.status == '1') {
		$('#' + writingNewsSuccessId).show();
		$('#' + writingNewsSuccessMessageId).text(addedEverything);
		$('#' + writingNewNewsTitleId).val('');
		$('#' + writingNewNewsTextId).val('');
		$('#' + newsBodyId).prepend(getNewsContainerAsHtml(parsedData.title, parsedData.date, parsedData.author, parsedData.news));
		window.scrollTo(0,0);
	} else {
		$('#' + writingNewsFailedId).show();
		$('#' + writingNewsFailedMessageId).text(internal_error);
	}

}


// *********************
//	SHARING IS CARING
// *********************

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
	window.open('https://twitter.com/intent/tweet?text=' + text + '&hashtags=DBAS,nrwfkop', 'sharer',
		',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
}

function mailShare(to, subject, body){
	'use strict';
	window.location.href = "mailto:" + to + "?subject=" + subject + "&body=" + body;
}

function googleShare(url){
	'use strict';
	var winTop, winLeft, winWidth, winHeight;
	winWidth = 600;
	winHeight = 400;
	winTop = (screen.height / 2) - (winHeight / 2);
	winLeft = (screen.width / 2) - (winWidth / 2);
	window.open('https://plus.google.com/share?url=' + url, 'sharer',
		',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
}

$(document).ready(function () {
	ajaxGetNews();

	$('#' + writingNewsFailedId).hide();
	$('#' + writingNewsSuccessId).hide();

	/**
	 * Sharing shortened url with mail
	 */
	$('.' + shareButtonMail).click(function(){
		if($(this).attr('id') === shareUrlButtonMail){
			return;
		}
		var container, textarraydate, textarrayauthor, textarraysubject;
		container = $(this).parents(".newscontainer");

		textarraysubject = container.html().split('<span class="font-semi-bold">');
		textarraydate 	 = container.html().split('<h4><p>');
		textarrayauthor  = container.html().split('</span>: ');
		textarraysubject = textarraysubject[1].split('</span>');
		textarraydate 	 = textarraydate[1].split('</p>');
		textarrayauthor  = textarrayauthor[1].split('</h5>');

		mailShare('user@example.com', "DBAS: " + textarraysubject[0], "News from " + textarraydate[0] + ", by " + textarrayauthor[0]);
	});

	/**
	 * Sharing shortened url on twitteer
	 */
	$('.' + shareButtonTwitter).click(function(){
		if($(this).attr('id') === shareUrlButtonTwitter){
			return;
		}
		var container = $(this).parents(".newscontainer"),
			textarraysubject = container.html().split('<span class="font-semi-bold">');
		tweetShare(textarraysubject[0]);
	});

	/**
	 * Sharing shortened url on google
	 */
	$('.' + shareButtonGoogle).click(function(){
		if($(this).attr('id') === shareUrlButtonGoogle){
			return;
		}
		googleShare(window.location.href);
	});

	/**
	 * Sharing shortened url on facebook
	 */
	$('.' + shareButtonFacebook).click(function(){
		if($(this).attr('id') === shareUrlButtonFacebook){
			return;
		}
		var container, textarraydate, textarrayauthor, textarraysubject;
		container = $(this).parents(".newscontainer");

		textarraysubject = container.html().split('<span class="font-semi-bold">');
		textarraydate 	 = container.html().split('<h4><p>');
		textarrayauthor  = container.html().split('</span>: ');
		textarraysubject = textarraysubject[1].split('</span>');
		textarraydate 	 = textarraydate[1].split('</p>');
		textarrayauthor  = textarrayauthor[1].split('</h5>');

		var message = "News '" + textarraysubject[0] + "', from " + textarraydate[0] + ", by " + textarrayauthor[0] + " on " + window.location.href;
		fbShare(window.location.href, "FB Sharing", message, "https://dbas.cs.uni-duesseldorf.de/static/images/logo.png");
	});

	/**
	 * Sharing shortened url on google
	 */
	$('#' + sendNewsButtonId).click(function(){
		ajaxSendNews();
	});
});