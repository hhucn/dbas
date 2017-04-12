/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function News() {
    'use strict';
    
	var BOOTSTRAP_COLLAPSE = 990;
	
	/**
	 *
	 */
	this.setNewsInRow = function()  {
		var input = $('#raw-elements');
		var array = input.find('.col-md-4');
		var length = array.length;

		// build rows
		var div = '';
		var counter;
		var row = 0;
		var container = '';
		for (counter = 0; counter < length; counter++) {
			if (counter % 3 === 0) {
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
		if (counter % 3 !== 0) {
			$('#' + newsBodyId).append(container);
		}

		input.remove();
		$('#dummy-news').remove();
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForSendingNews = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length === 0) {
			// $('#' + writingNewsSuccessId).show();
			// $('#' + writingNewsSuccessMessageId).text(_t(addedEverything));
			// $('#' + writingNewNewsTitleId).val('');
			// $('#' + writingNewNewsTextId).val('');
			// $('#' + newsBodyId).prepend(new News().getNewsContainerAsHtml(parsedData.title, parsedData.date, parsedData.author, parsedData.news));
			// new News().setSharingClickEvents();
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
			var children = $('#row_' + counter).children();
			heights = children.map(function () {
				return $(this).height();
			}).get();
			maxHeight = Math.max.apply(Math, heights);
			
			$.each(children, function () {
				$(this).children().eq(0).css({'min-height': maxHeight + 'px'});
			});
		}
	};

	/**
	 *
	 */
	this.setSlimscrollForNewsRows = function () {
		var wrapperContent = $('#wrapper-content');
		wrapperContent.attr('style', 'padding-bottom: 0px');
		var h = this.getMaxHeight();

		$('.panel-body').each(function() {
			if ($(this).height() <= h - $(this).prev().height()) {
				$(this).height(h);
				return true;
			}
			var p = $(this).parent();
			var ph = p.children().eq(0).outerHeight(true);
			$(this).slimScroll({
				position: 'right',
				height: h + 'px',
				railVisible: true,
				alwaysVisible: false
			}).css({'height': h + 'px'});
			p.css({'height': (ph + h) + 'px'});
		});
	};
	
	/**
	 *
	 * @returns {number|*}
	 */
	this.getMaxHeight = function(){
		var placeholders = [];
		var h;
		var wrapperContent = $('#wrapper-content');
		placeholders.push($('#custom-bootstrap-menu').outerHeight(true));
		placeholders.push(parseInt(wrapperContent.css('padding-top').replace('px','')));
		placeholders.push(parseInt(wrapperContent.css('padding-bottom').replace('px','')));
		placeholders.push(parseInt(wrapperContent.css('margin-top').replace('px','')));
		placeholders.push(parseInt(wrapperContent.css('margin-bottom').replace('px','')));
		placeholders.push($('#footer').outerHeight(true));
		placeholders.push($('#news-navigation-container').outerHeight(true));
		placeholders.push(2 * parseInt($('#news-body').children().eq(0).css('margin-bottom').replace('px','')));
		h = document.body.clientHeight;
		placeholders.forEach(function(p) {
			h -= p;
		});
		h = h/2;
		return h;
	};

	/**
	 *
	 */
	this.setPageNavigation = function () {
		var counter;
		var row = $('#' + newsBodyId).children().length;
		var pagebreak = 2;
		var _this = this;
		var pagecounter = 1;
		var newsNavigator = $('#news-navigation');
		var html;
		var back;
		var forth;
		var pages='';

		newsNavigator.empty();

		// adding page classes to every news
		for (counter = 0; counter < row; counter++) {
			if (counter !== 0 && counter % pagebreak === 0) {
				pagecounter++;
			}
			$('#container_' + counter).addClass('news-page-' + pagecounter).hide();
		}

		// create navbar
		back = '<li><a href="#" id="news-back"><span aria-hidden="true">&laquo;</span></a></li>';
		for (counter = 1; counter <= pagecounter; counter++) {
			pages += '<li><a href="#" data-counter="' + counter + '" id="news-' + counter + '">' + counter + '</a></li>';
		}

		forth= '<li><a href="#" id="news-forth"><span aria-hidden="true">&raquo;</span></a></li>';
		html = '<ul class="pagination">' + back + pages + forth + '</ul>';
		newsNavigator.append(html);

		// click events
		for (counter = 0; counter <= pagecounter; counter++) {
			$('#news-' + (counter + 1)).click(function () {
				newsNavigator.children().eq(0).children().removeClass('active');
				$(this).parent().addClass('active');

				$('#' + newsBodyId).children().hide();
				$('.news-page-' + $(this).data('counter')).show();
				_this.checkNewsForthAndBackButtons($(this).data('counter'), pagecounter);
			});
		}

		var news1 = $('#news-1');
		var news_back = $('#news-back');
		news1.parent().addClass('active');
		$('.news-page-1').show();
		news_back.parent().addClass('disabled');
		_this.setPlaceholder(news1.data('counter'), pagecounter);

		// add page limitation to each click
		$('.pagination a').click(function(){
			if (!$(this).hasClass('news-placeholder')) {
				_this.setPlaceholder($(this).data('counter'), pagecounter);
			}
		});

		news_back.off('click').click(function () {
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
	
	/**
	 *
	 * @param index
	 * @param pagecounter
	 */
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

		if (p-3 > 0) {
			placeholder.insertAfter($('#news-' + (p - 1)).parent());
		}
		if (pagecounter-2-s > 0) {
			placeholder.insertAfter($('#news-' + s).parent());
		}
	};

	/**
	 *
	 * @param isBack
	 * @param pagecounter
	 */
	this.turnThePage = function (isBack, pagecounter){
		var activeElement = $('#news-navigation').find('.active');
		var counter = parseInt(activeElement.children().eq(0).data('counter'));
		activeElement.removeClass('active');
		if (isBack) {
			activeElement.prev().addClass('active');
		} else {
			activeElement.next().addClass('active');
		}
		var news_counter = $('.news-page-' + counter);
		news_counter.hide();
		counter = isBack ? counter-1 : counter+1;
		news_counter.show();
		this.checkNewsForthAndBackButtons(counter, pagecounter);
		this.setPlaceholder(counter, pagecounter);
	};

	/**
	 *
	 * @param currentCounter
	 * @param max
	 */
	this.checkNewsForthAndBackButtons = function(currentCounter, max) {
		if (currentCounter === 0) {
			$('#news-back').parent().addClass('disabled');
		} else {
			$('#news-back').parent().removeClass('disabled');
		}
		
		if (currentCounter === max){
			$('#news-forth').parent().addClass('disabled');
		} else {
			$('#news-forth').parent().removeClass('disabled');
		}
	};

	// *********************
	//	SHARING IS CARING
	// *********************
	this.setSharingClickEvents = function () {
		var news = new News();
		/**
		 * Sharing shortened url with mail
		 */
		$('.' + shareButtonMail).click(function () {
			news.mailShare(this);
		});

		/**
		 * Sharing shortened url on twitter
		 */
		$('.' + shareButtonTwitter).click(function () {
			news.twitterShare(this);
		});

		/**
		 * Sharing shortened url on google
		 */
		$('.' + shareButtonGoogle).click(function () {
			news.googleShare(this);
		});

		/**
		 * Sharing shortened url on facebook
		 */
		$('.' + shareButtonFacebook).click(function () {
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
		var id = $(_this).closest('.panel-heading').attr('id'),
				title = $('#' + id + '_title').text(),
				date = $('#' + id + '_date').text(),
				author = $('#' + id + '_author').text();

		new Sharing().emailShare('', "DBAS: " + title, _t(interestingNews) + ' ' + date + ", by " + author + " - " + window.location.href);
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
    'use strict';
    
	if (window.location.href.indexOf(mainpage + 'news') === -1){
		return;
	}
	
	var news = new News();
	news.setNewsInRow();
	$('.panel-body').css('height', '');
	news.setMaxHeightOfNewsRows();
	//news.setPageNavigation();
	news.setSharingClickEvents();
	news.setSharingClickEvents();
	//news.setSlimscrollForNewsRows();

	$('#' + writingNewsFailedId).hide();
	$('#' + writingNewsSuccessId).hide();


	/**
	 * Sharing shortened url on google
	 */
	$('#' + sendNewsButtonId).click(function(){
		new AjaxNewsHandler().ajaxSendNews();
	});

	$('#icon-add-news').click(function(){
		$('#popup-writing-news').modal('show');
	});

	// make some things pretty
	$(window).on('resize', function resizeWindow(){
		//new News().setMaxHeightOfNewsRows();
	});
});
