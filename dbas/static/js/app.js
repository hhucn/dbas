/*global $, jQuery*/
jQuery(function ($) {
	"use strict";
	
	// open contact popup
	$(".popup_author_open").click(function () {
		$(".popup_author").fadeIn("normal");
		$("#popup_background").css("opacity", "0.7");
		$("#popup_background").fadeIn("normal");
		$(".popup_licence").fadeOut("normal");
		$(".popup_privacy").fadeOut("normal");
	});

	// open licence popup
	$(".popup_licence_open").click(function () {
		$(".popup_licence").fadeIn("normal");
		$("#popup_background").css("opacity", "0.7");
		$("#popup_background").fadeIn("normal");
		$(".popup_author").fadeOut("normal");
		$(".popup_privacy").fadeOut("normal");
	});

	// open privacy popup
	$(".popup_privacy_open").click(function () {
		$(".popup_privacy").fadeIn("normal");
		$("#popup_background").css("opacity", "0.7");
		$("#popup_background").fadeIn("normal");
		$(".popup_licence").fadeOut("normal");
		$(".popup_author").fadeOut("normal");
	});

	// close all popups with image close
	$(".popup_close").click(function () {
		$(".popup_author").fadeOut("normal");
		$(".popup_licence").fadeOut("normal");
		$(".popup_privacy").fadeOut("normal");
		$("#popup_background").fadeOut("normal");
	});

	// close all popups with clicking on the background
	$("#popup_background").click(function () {
		$(".popup_author").fadeOut("normal");
		$(".popup_licence").fadeOut("normal");
		$(".popup_privacy").fadeOut("normal");
		$("#popup_background").fadeOut("normal");
	});

	// jump to chapter-function
	$('a[href^=#]').on('click', function (e) {
		var href = $(this).attr('href');
		$('html, body').animate({
			scrollTop: ($(href).offset().top - 100)
		}, 'slow');
		e.preventDefault();
	});

	// back to top arrow
	jQuery(window).scroll(function () {
		if (jQuery(this).scrollTop() > 220) {
			jQuery('.back-to-top').fadeIn(500);
		} else {
			jQuery('.back-to-top').fadeOut(500);
		}
	});

	jQuery('.back-to-top').click(function (event) {
		event.preventDefault();
		jQuery('html, body').animate({
			scrollTop: 0
		}, 500);
		return false;
	});
});