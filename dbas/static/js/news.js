/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function News() {
	var BOOTSTRAP_COLLAPSE = 990;

	/***
	 *
	 * @param title
	 * @param date
	 * @param author
	 * @param news
	 * @param no
	 * @returns {string}
	 */
	this.getNewsContainerAsHtml = function (title, date, author, news, no) {
		return '<div class="col-md-4">'
				+ '<div class="panel panel-default">'
				+ '<div class="panel-heading" id="news_' + no + '">'
				+ '<a class="share-icon-small share-mail-small" data-toggle="tooltip" data-placement="bottom" title="Mail"></a>'
				+ '<a class="share-icon-small share-twitter-small" data-toggle="tooltip" data-placement="bottom" title="Twitter"></a>'
				+ '<a class="share-icon-small share-google-small" data-toggle="tooltip" data-placement="bottom" title="Google+"></a>'
				+ '<a class="share-icon-small share-facebook-small" data-toggle="tooltip" data-placement="bottom" title="Facebook"></a>'
				+ '<h5><span class="font-semi-bold" id="news_' + no + '_title">' + title + '</span></h5>'
				+ '</div>'
				+ '<div class="panel-body" style="text-align: justify;">'
				+ '<h6>'
					//+ '<span i18n:translate="author">Author</span>: '
				+ '<span id="news_' + no + '_author">' + author + '</span>' + ', '
				+ '<span id="news_' + no + '_date">' + date + '</span>'
				+ '</h6>'
				+ '<br>'
				+ news
				+ '</div>'
				+ '</div>'
				+ '</div>';
	};


	// *********************
	//	AJAX
	// *********************

	/**
	 *
	 */
	this.ajaxGetNews = function () {
		var csrfToken = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_get_news',
			type: 'POST',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxGetNewsDone(data) {
			new News().callbackIfDoneForGettingNews(data);
		}).fail(function ajaxGetNewsFail() {
			$('#' + newsBodyId).append("<h4>" + internalError + "</h4>");
		});
	};

	/**
	 *
	 */
	this. ajaxSendNews = function () {
		var title = $('#' + writingNewNewsTitleId).val(),
				text = $('#' + writingNewNewsTextId).val();

		if (title.length == 0 || text.length < 10) {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).text(_t(empty_news_input));
			new Helper().delay(function(){
				$('#' + writingNewsFailedId).fadeOut();
				new Helper().delay(function(){
					$('#' + writingNewsFailedMessageId).text('');
				}, 2000);
			}, 2000);
			return;
		} else {
			$('#' + writingNewsFailedId).hide();
			$('#' + writingNewsSuccessId).hide();
		}

		var csrfToken = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: 'ajax_send_news',
			type: 'POST',
			data: {title: title, text: text},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendNewsDone(data) {
			new News().callbackIfDoneForSendingNews(data);
		}).fail(function ajaxSendNewsFail() {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).html(_t(internalError));
		});
	};

	// *********************
	//	CALLBACKS
	// *********************

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForGettingNews = function (data) {
		var parsedData = $.parseJSON(data),
				counter = 1,
				div = '',
				row = 0,
				id,
				length = Object.keys(parsedData).length,
				array = new Array(length),
				container = '',
				news = new News();

		// add every news in reverted order
		$.each(parsedData, function callbackIfDoneForGettingNewsEach(key, val) {
			array[length - counter] = news.getNewsContainerAsHtml(val.title, val.date, val.author, val.news, val.uid);
			counter += 1;
		});
		counter = 0;

		// build rows
		for (counter = 0; counter < length; counter++) {
			if (counter % 3 == 0) {
				if (div !== '') {
					$('#' + newsBodyId).append(container);
				}
				div = $('<div>').attr('id', 'row_' + row).addClass('row');
				container = $('<div>').attr('id', 'container_' + row).addClass('container');
				row += 1;
			}
			div.append(array[counter]);
			container.append(div);
		}

		// set length of last row
		length = container.children().eq(0).children().length;
		$.each(container.children().eq(0).children(), function () {
			$(this).attr('class', '').attr('class', 'col-md-' + (12 / length));
		});

		// add last row
		counter -= 1;
		if (counter % 3 != 0) {
			$('#' + newsBodyId).append(container);
		}

		//news.setMaxHeightOfNewsRows();
		news.setSlimscrollForNewsRows();
		news.setPageNavigation();
		news.setSharingClasses();
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForSendingNews = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length == 0) {
			// $('#' + writingNewsSuccessId).show();
			// $('#' + writingNewsSuccessMessageId).text(_t(addedEverything));
			// $('#' + writingNewNewsTitleId).val('');
			// $('#' + writingNewNewsTextId).val('');
			// $('#' + newsBodyId).prepend(new News().getNewsContainerAsHtml(parsedData.title, parsedData.date, parsedData.author, parsedData.news));
			// new News().setSharingClasses();
			// window.scrollTo(0, 0);
			location.reload();
		} else {
			$('#' + writingNewsFailedId).show();
			$('#' + writingNewsFailedMessageId).html(parsedData.error);
		}

	};

	/**
	 *
	 */
	this.setMaxHeightOfNewsRows = function () {
		var counter, row = $('#' + newsBodyId).children().length, heights, maxHeight;

		// bootstrap collapse
		if ($(window).width() < BOOTSTRAP_COLLAPSE) {
			return;
		}

		// find max height of each row and set it
		for (counter = 0; counter < row; counter++) {
			heights = $('#row_' + counter + ' div').children(':first-child').map(function () {
				return $(this).height();
			}).get();
			maxHeight = Math.max.apply(null, heights);

			$.each($('#row_' + counter).children(), function () {
				$(this).children().eq(0).height(maxHeight);
			});
		}
	};

	/**
	 *
	 */
	this.setSlimscrollForNewsRows = function () {
		var placeholders = [], h, wrapperContent = $('#wrapper-content'), footer = $('#footer');
		placeholders.push($('.navbar-collapse').height());
		placeholders.push(parseInt(wrapperContent.css('padding-top').replace('px','')));
		placeholders.push(parseInt(wrapperContent.css('padding-bottom').replace('px','')));
		placeholders.push(parseInt(wrapperContent.css('margin-top').replace('px','')));
		placeholders.push(parseInt(wrapperContent.css('margin-bottom').replace('px','')));
		placeholders.push(footer.height());
		placeholders.push(parseInt(footer.css('padding-top').replace('px','')));
		placeholders.push(parseInt(footer.css('margin-top').replace('px','')));
		placeholders.push($('#news-navigation-container').height());
		placeholders.push(2 * parseInt($('#news-body').children().eq(0).css('margin-bottom').replace('px','')));
		placeholders.push(50); // magic
		h = $(window).height();
		placeholders.forEach(function(p) {
			h -= p;
		});
		h = h/2;
		wrapperContent.attr('style', 'padding-bottom: 0px');

		$('.panel-heading').height(67);
		$('.panel-body').slimScroll({
            position: 'right',
            height: h + 'px',
            railVisible: true,
            alwaysVisible: false
		});
	};

	/**
	 *
	 */
	this.setPageNavigation = function () {
		var counter, row = $('#' + newsBodyId).children().length, pagebreak = 2, _this = this,
			pagecounter = 1, newsNavigator = $('#news-navigation'), html, back, forth, pages='';

		newsNavigator.empty();

		// adding page classes to every news
		for (counter = 0; counter < row; counter++) {
			if (counter != 0 && counter % pagebreak == 0) {
				pagecounter++;
			}
			$('#container_' + counter).addClass('news-page-' + pagecounter).hide();
		}

		// create navbar
		back = '<li><a href="#" id="news-back"><span aria-hidden="true">&laquo;</span></a></li>';
		for (counter = 1; counter <= pagecounter; counter++) {
			pages += '<li><a href="#" counter="' + counter + '" id="news-' + counter + '">' + counter + '</a></li>';
		}

		forth= '<li><a href="#" id="news-forth"><span aria-hidden="true">&raquo;</span></a></li>';
		html = '<ul class="pagination">' + back + pages + forth + '</ul>';
		newsNavigator.append(html);

		// click events
		for (counter = 0; counter <= pagecounter; counter++) {
			$('#news-' + (counter + 1)).click(function () {
				$('#news-navigation').children().eq(0).children().removeClass('active');
				$(this).parent().addClass('active');

				$('#' + newsBodyId).children().hide();
				$('.news-page-' + $(this).attr('counter')).show();
				_this.checkNewsForthAndBackButtons($(this).attr('counter'), pagecounter);
			});
		}

		$('#news-1').parent().addClass('active');
		$('.news-page-1').show();
		$('#news-back').parent().addClass('disabled');
		_this.setPlaceholder($('#news-1').attr('counter'), pagecounter);

		// add page limitation to each click
		$('.pagination a').click(function(){
			if (!$(this).hasClass('news-placeholder'))
				_this.setPlaceholder($(this).attr('counter'), pagecounter);
		});

		$('#news-back').off('click').click(function () {
			if (!$(this).parent().hasClass('disabled')) {
				_this.turnThePage(true, pagecounter);
			}
		}).hide();

		$('#news-forth').off('click').click(function () {
			if (!$(this).parent().hasClass('disabled')) {
				_this.turnThePage(false, pagecounter);
			}
		}).hide();
	};

	this.setPlaceholder = function(index, pagecounter){
		var i, p, s,
			placeholder = $('<li>').addClass('disabled').append($('<a>').addClass('news-placeholder').text('...'));
		$('.news-placeholder').remove();

		for (i=3; i<pagecounter-1; i++){
			$('#news-' + i).parent().hide();
		}

		p = index - 1;
		i = p + 1;
		s = i + 1;

		$('#news-' + p).parent().show();
		$('#news-' + i).parent().show();
		$('#news-' + s).parent().show();

		if (p-3 > 0)
			placeholder.insertAfter($('#news-' + (p-1)).parent());
		if (pagecounter-2-s > 0)
			placeholder.insertAfter($('#news-' + s).parent());
	};

	/**
	 *
	 * @param isBack
	 * @param pagecounter
	 */
	this.turnThePage = function (isBack, pagecounter){
		var activeElement = $('#news-navigation .active'),
			counter = parseInt(activeElement.children().eq(0).attr('counter'));
		activeElement.removeClass('active');
		if (isBack)
			activeElement.prev().addClass('active');
		else
			activeElement.next().addClass('active');
		$('.news-page-' + counter).hide();
		counter = isBack ? counter-1 : counter+1;
		$('.news-page-' + counter).show();
		this.checkNewsForthAndBackButtons(counter, pagecounter);
		this.setPlaceholder(counter, pagecounter);
	};

	/**
	 *
	 * @param currentCounter
	 * @param max
	 */
	this.checkNewsForthAndBackButtons = function(currentCounter, max){
		if (currentCounter == 0)   $('#news-back').parent().addClass('disabled');
		else                       $('#news-back').parent().removeClass('disabled');

		if (currentCounter == max) $('#news-forth').parent().addClass('disabled');
		else                       $('#news-forth').parent().removeClass('disabled');
	};

	// *********************
	//	SHARING IS CARING
	// *********************
	this.setSharingClasses = function () {
		var news = new News();
		/**
		 * Sharing shortened url with mail
		 */
		$('.' + shareButtonMail).click(function () {
			news.mailShare(this);
		});
		$('.' + shareButtonMailSmall).click(function () {
			news.mailShare(this);
		});

		/**
		 * Sharing shortened url on twitteer
		 */
		$('.' + shareButtonTwitter).click(function () {
			news.twitterShare(this);
		});
		$('.' + shareButtonTwitterSmall).click(function () {
			news.twitterShare(this);
		});

		/**
		 * Sharing shortened url on google
		 */
		$('.' + shareButtonGoogle).click(function () {
			news.googleShare(this);
		});
		$('.' + shareButtonGoogleSmall).click(function () {
			news.googleShare(this);
		});

		/**
		 * Sharing shortened url on facebook
		 */
		$('.' + shareButtonFacebook).click(function () {
			news.facebookShare(this);
		});
		$('.' + shareButtonFacebookSmall).click(function () {
			news.facebookShare(this);
		});
	};

	/**
	 * Sharing shortened url via mail
	 */
	this.mailShare = function (_this) {
		if ($(_this).attr('id') === shareUrlButtonMail) {
			return;
		}
		var id = $(_this).parent().attr('id'),
				title = $('#' + id + '_title').text(),
				date = $('#' + id + '_date').text(),
				author = $('#' + id + '_author').text();

		new Sharing().emailShare('user@example.com', "DBAS: " + title, "Interesting news from " + date + ", by " + author + " - " + window.location.href);
	};

	/**
	 * Sharing shortened url on google
	 */
	this.googleShare = function (_this) {
		if ($(_this).attr('id') === shareUrlButtonGoogle) {
			return;
		}
		new Sharing().googlePlusShare(window.location.href);

	};

	/**
	 * Sharing shortened url on facebook
	 */
	this.facebookShare = function (_this) {
		if ($(_this).attr('id') === shareUrlButtonFacebook) {
			return;
		}

		var id = $(_this).parent().attr('id'),
				title = $('#' + id + '_title').text(),
				date = $('#' + id + '_date').text(),
				author = $('#' + id + '_author').text(),
				message = "News '" + title + "', from " + date + ", by " + author + " on " + window.location.href;
		new Sharing().facebookShare(window.location.href, "FB Sharing", message, mainpage + "static/images/logo.png");
	};

	/**
	 * Sharing shortened url on twitter
	 */
	this.twitterShare = function (_this) {
		if ($(_this).attr('id') === shareUrlButtonTwitter) {
			return;
		}
		var id = $(_this).parent().attr('id'),
				title = $('#' + id + '_title').text();
		new Sharing().twitterShare(title, window.location.href);
	};

}

$(document).ready(function () {
	var news = new News();
	news.ajaxGetNews();

	$('#' + writingNewsFailedId).hide();
	$('#' + writingNewsSuccessId).hide();

	news.setSharingClasses();

	/**
	 * Sharing shortened url on google
	 */
	$('#' + sendNewsButtonId).click(function(){
		news.ajaxSendNews();
	});

	$('#icon-add-news').click(function(){
		$('#popup-writing-news').modal('show');
	});

	// make some things pretty
	$(window).on('resize', function resizeWindow(){
		news.setMaxHeightOfNewsRows();
	});
});
