/**
 * Created by tobias on 30.09.15.
 */

/***
 *
 * @param title
 * @param date
 * @param author
 * @param news
 * @param no
 * @returns {string}
 */
function getNewsContainerAsHtml(title, date, author, news, no) {
	return '<div class="col-md-4">'
			//+ '<div class="container newscontainer" id="news_' + no + '">'
			+ '<div class="news colored_container" id="news_' + no + '">'
					+ '<a class="share-icon share-mail"></a>'
					+ '<a class="share-icon share-twitter"></a>'
					+ '<a class="share-icon share-google"></a>'
					+ '<a class="share-icon share-facebook"></a>'
			+ '<div class="row">'
					+ '<h4><span class="font-semi-bold" id="news_' + no + '_title">' + title + '</span></h4>'
			+ '</div>'
			+ '<h6><span i18n:translate="author">Author</span>: '
				+ '<span id="news_' + no + '_author">' + author + '</span>' + ', '
				+ '<span id="news_' + no + '_date">' + date + '</span>'
			+ '</h6>'
			+ '<br>'
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
		$('#' + newsBodyId).append("<h4>" + internalError + "</h4>");
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
		$('#' + writingNewsFailedMessageId).text(_t(empty_news_input));
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
		$('#' + writingNewsFailedMessageId).text(_t(internalError));
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
	var parsedData = $.parseJSON(data),
			counter = 1,
			div = '',
			row = 0,
			id,
			length = Object.keys(parsedData).length,
			array = new Array(length),
			container = '';

	// add every news in reverted order
	$.each(parsedData, function callbackIfDoneForGettingNewsEach(key, val) {
		array[length - counter] = getNewsContainerAsHtml(val.title, val.date, val.author, val.news, val.uid);
		counter += 1;
	});
	counter = 0;

	// build rows
	for (counter = 0; counter<length; counter++){
		if (counter % 3 == 0){
			if (div !== '') {
				$('#' + newsBodyId).append(container);
			}
			div = $('<div>').attr('id','row_' + row).addClass('row');
			container = $('<div>').attr('id','container_' + row).addClass('container');
			row += 1;
		}
		div.append(array[counter]);
		container.append(div);
	}

	// set length of last row
	length = container.children().eq(0).children().length;
	$.each(container.children().eq(0).children(), function(){
		$(this).attr('class','').attr('class', 'col-md-' + (12/length));
	});

	// add last row
	counter -=1;
	if (counter %3 != 0){
		$('#' + newsBodyId).append(container);
	}

	// find max height of each row and set it
	for (counter = 0; counter < row; counter ++) {
		var heights = $('#row_' + counter + ' div').children(':first-child').map(function () {
			return $(this).height();
		}).get(), maxHeight = Math.max.apply(null, heights);

		$.each($('#row_' + counter).children(), function () {
			id = $(this).children(':first-child').attr('id');
			$('div#' + id).height(maxHeight);

		});
	}

	// set sharing
	setSharingClasses();
}

/**
 *
 * @param data
 */
function callbackIfDoneForSendingNews(data) {
	var parsedData = $.parseJSON(data);
	if (parsedData.status == '1') {
		$('#' + writingNewsSuccessId).show();
		$('#' + writingNewsSuccessMessageId).text(_t(addedEverything));
		$('#' + writingNewNewsTitleId).val('');
		$('#' + writingNewNewsTextId).val('');
		$('#' + newsBodyId).prepend(getNewsContainerAsHtml(parsedData.title, parsedData.date, parsedData.author, parsedData.news));
		setSharingClasses();
		window.scrollTo(0,0);
	} else {
		$('#' + writingNewsFailedId).show();
		$('#' + writingNewsFailedMessageId).text(_t(internalError));
	}

}


// *********************
//	SHARING IS CARING
// *********************

function setSharingClasses(){
	/**
	 * Sharing shortened url with mail
	 */
	$('.' + shareButtonMail).click(function(){
		if($(this).attr('id') === shareUrlButtonMail){
			return;
		}
		var id = $(this).parent().attr('id'),
				title = $('#' + id + '_title').text(),
				date = $('#' + id + '_date').text(),
				author = $('#' + id + '_author').text();

		new Sharing().emailShare('user@example.com', "DBAS: " + title, "Interesting news from " + date + ", by " + author + " - " + window.location.href);
	});

	/**
	 * Sharing shortened url on twitteer
	 */
	$('.' + shareButtonTwitter).click(function(){
		if($(this).attr('id') === shareUrlButtonTwitter){
			return;
		}
		var id = $(this).parent().attr('id'),
				title = $('#' + id + '_title').text();
		new Sharing().twitterShare(title, window.location.href);
	});

	/**
	 * Sharing shortened url on google
	 */
	$('.' + shareButtonGoogle).click(function(){
		if($(this).attr('id') === shareUrlButtonGoogle){
			return;
		}
		new Sharing().googlePlusShare(window.location.href);
	});

	/**
	 * Sharing shortened url on facebook
	 */
	$('.' + shareButtonFacebook).click(function(){
		if($(this).attr('id') === shareUrlButtonFacebook){
			return;
		}

		var id = $(this).parent().attr('id'),
				title = $('#' + id + '_title').text(),
				date = $('#' + id + '_date').text(),
				author = $('#' + id + '_author').text();

		var message = "News '" + title + "', from " + date + ", by " + author + " on " + window.location.href;
		new Sharing().facebookShare(window.location.href, "FB Sharing", message, mainpage + "static/images/logo.png");
	});
}

$(document).ready(function () {
	ajaxGetNews();

	$('#' + writingNewsFailedId).hide();
	$('#' + writingNewsSuccessId).hide();

	setSharingClasses();

	/**
	 * Sharing shortened url on google
	 */
	$('#' + sendNewsButtonId).click(function(){
		ajaxSendNews();
	});
});