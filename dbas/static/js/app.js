/*global $, jQuery, alert, addActiveLinksInNavBar, removeActiveLinksInNavBar*/

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

function setLinkActive(linkname) {
	'use strict';
	var linkIds = ['#contact-link', '#login-link', '#news-link', '#content-link'],
		i;
	for (i = 0; i < linkIds.length; i++) {
		if (linkIds[i] === linkname) {
			$(linkIds[i]).addClass('active');
		} else {
			$(linkIds[i]).removeClass('active');
		}
	}
}
/**
 * Displays dialog for language translation and send ajax requests
 * @param id of the selected translation link
 */
function displayConfirmTranslationDialog(id) {
	// if parent is already active, nothing will happen
	if ($('#' + translationLink + id).parent().hasClass('active')){
		return;
	}
	// display dialog
	$('#' + popupConfirmDialogId).modal('show');
	$('#' + popupConfirmDialogId + ' h4.modal-title').text(confirmation);
	$('#' + popupConfirmDialogId + ' div.modal-body').text(confirmTranslation);
	// ask for display switch
	$('#' + confirmDialogAcceptBtn).click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
		// ajax
		switchDisplayLanguage(id);
	});
	$('#' + confirmDialogRefuseBtn).click( function () {
		$('#' + popupConfirmDialogId).modal('hide');
	});
}

/**
 * Will display a dialog, when we are on the content page, otherwise it will change de language
 * @param path current path
 * @param lang current language code
 */
function language_switcher (path, lang){
	// preserve reload, when the user is arguing
	if (path == 'content')
		displayConfirmTranslationDialog(lang);
	else
		switchDisplayLanguage(lang);
}

/**
 * Sends a request for language change
 * @param new_lang is the shortcut for the language
 */
function switchDisplayLanguage (new_lang){
	$.ajax({
		url: 'ajax_switch_language',
		type: 'POST',
		data: { lang: new_lang},
		dataType: 'json',
		async: true
	}).done(function ajaxSwitchDisplayLanguage(data) {
		callbackIfDoneForSwitchDisplayLanguage(data, new_lang);
	}).fail(function ajaxSwitchDisplayLanguage() {
		alert('Unfortunately, the language could not be switched');
	});
}
/**
 * Callback, when language is switched
 */
function callbackIfDoneForSwitchDisplayLanguage (data, new_lang) {
	location.reload(true);
	setActiveLanguage(new_lang);
}

/**
 * DOM manipulation for the active class
 * @param lang current language code
 */
function setActiveLanguage(lang){
	if (lang === 'en'){
		$('#' + translationLinkDe).parent().removeClass('active');
		$('#' + translationLinkEn).parent().addClass('active');
		$('.logo').attr('src','../static/images/logo.png');
	} else {
		$('#' + translationLinkEn).parent().removeClass('active');
		$('#' + translationLinkDe).parent().addClass('active');
		$('.logo').attr('src','../static/images/logo_de.png');
	}
}

/**
 * Jumps to clicked chapter, which is defined in the header
 */
function jmpToChapter() {
	// jump to chapter-function
	$('a[href^=#]').on('click', function (e) {
		try {
			var href = $(this).attr('href');
			$('html, body').animate({
				scrollTop: ($(href).offset().top - 100)
			}, 'slow');
			e.preventDefault();
		} catch (err) {
			// something like 'Cannot read property 'top' of undefined'
		}
	});
}

/**
 * Go back to top arrow
 */
function goBackToTop() {
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
}

$(document).ready(function () {
	'use strict';

	jmpToChapter();

	goBackToTop();

	setActiveLanguage($('#hidden_language').val());

	// set current file to active
	var path = window.location.href;
		 if (path.indexOf('contact') != -1){ 	setLinkActive('#contact-link');	$('#navbar-left').hide(); }
	else if (path.indexOf('login') != -1){		setLinkActive('#login-link');	$('#navbar-left').hide(); }
	else if (path.indexOf('news') != -1){ 		setLinkActive('#news-link');	$('#navbar-left').hide(); }
	else if (path.indexOf('content') != -1){ 	setLinkActive('#content-link');	$('#navbar-left').hide(); }
	else if (path.indexOf('settings') != -1 ||
			 path.indexOf('imprint') != -1 ||
			 path.indexOf('logout') != -1){										$('#navbar-left').hide(); }
	else {										setLinkActive(''); 				$('#navbar-left').show(); }

	// language switch
	$('#' + translationLinkDe).click(function(){ language_switcher(path, 'de') });
	$('#' + translationLinkEn).click(function(){ language_switcher(path, 'en') });
	$('#' + translationLinkDe + " img").click(function(){ language_switcher(path, 'de') });
	$('#' + translationLinkEn + " img").click(function(){ language_switcher(path, 'en') });
});