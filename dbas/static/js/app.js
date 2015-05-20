// just a countdowntimer by http://stackoverflow.com/a/1192001/2648872
function Countdown(options) {
	'use strict';
	var timer,
		instance = this,
		seconds = options.seconds || 10,
		updateStatus = options.onUpdateStatus || function () {},
		counterEnd = options.onCounterEnd || function () {};

	function decrementCounter() {
		updateStatus(seconds);
		if (seconds === 0) {
			counterEnd();
			instance.stop();
		}
		seconds = seconds - 1;
	}

	this.start = function () {
		clearInterval(timer);
		timer = 0;
		seconds = options.seconds;
		timer = setInterval(decrementCounter, 1000);
	};

	this.stop = function () {
		clearInterval(timer);
	};
}


/*global $, jQuery, alert, addActiveLinksInNavBar, removeActiveLinksInNavBar*/
//jQuery(function ($) {
$(document).ready(function () {
	'use strict';

	// jump to chapter-function
	$('a[href^=#]').on('click', function (e) {
		var href = $(this).attr('href');
		$('html, body').animate({
			scrollTop: ($(href).offset().top - 100)
		}, 'slow');
		e.preventDefault();
	});

	// back to top arrow
	$(window).scroll(function () {
		if (jQuery(this).scrollTop() > 220) {
			$('.back-to-top').fadeIn(500);
		} else {
			$('.back-to-top').fadeOut(500);
		}
	});

	// going back to top
	$('.back-to-top').click(function (event) {
		event.preventDefault();
		$('html, body').animate({
			scrollTop: 0
		}, 500);
		return false;
	});

	// set current file to active
	var path = document.location.pathname.match(/[^\/]+$/)[0];
	if (path === "contact") {
		$('#contactLink').addClass('active');
		$('#loginLink').removeClass('active');
		$('#newsLink').removeClass('active');
		$('#contentLink').removeClass('active');
	} else if (path === "login") {
		$('#loginLink').addClass('active');
		$('#contactLink').removeClass('active');
		$('#newsLink').removeClass('active');
		$('#contentLink').removeClass('active');
	} else if (path === "news") {
		$('#newsLink').addClass('active');
		$('#contactLink').removeClass('active');
		$('#loginLink').removeClass('active');
		$('#contentLink').removeClass('active');
	} else if (path === "content") {
		$('#contentLink').addClass('active');
		$('#contactLink').removeClass('active');
		$('#loginLink').removeClass('active');
		$('#newsLink').removeClass('active');
	} else {
		$('#contactLink').removeClass('active');
		$('#loginLink').removeClass('active');
		$('#newsLink').removeClass('active');
		$('#contentLink').removeClass('active');
	}

	// Your application has indicated you are logged out
	if (path === "logout") {
		var myCounter = new Countdown({
			seconds: 4, // seconds to count down
			onUpdateStatus: function (sec) {
				$('.timer').text(sec + " s");
			},
			onCounterEnd: function () {
					//this gets the full url and an index
					var url = document.location.href,
						index = url.indexOf("/logout");
					//this removes the logout at the end, if there is one
					url = url.substring(0, (index === -1) ? url.length : index);
					url = url + "/logout_redirect";
					// new text to the button
					$('#homebutton').text("Redirecting to " + url);
					// Move to a new location or you can do something else
					window.location.href = url;
				} // final action
		});
		myCounter.start();
	}
});