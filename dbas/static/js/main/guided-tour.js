/**
 * Created by tobias on 26.01.17.
 */

function GuidedTour(){
    'use strict';
    
	var lang_switcher = '';
	var tour = '';
		
	// override default template for i18n
	var template =
		'<div class="popover tour">' +
			'<div class="arrow"></div>' +
			'<h3 class="popover-title"></h3>' +
			'<div class="popover-content"></div>' +
			'<div class="popover-navigation">' +
				'<div class="btn-group">' +
					'<button class="btn btn-sm btn-default" data-role="prev">&#xab; ' + _t(prev) + '</button>' +
					'<button class="btn btn-sm btn-success" data-role="next">' + _t(next) + ' &#xbb;</button>' +
			'</div>' +
			'<button class="btn btn-sm btn-default" data-role="end">' + _t(tourEnd) + '</button>' +
		'</div>';
	
	var template_end =
		'<div class="popover tour">' +
			'<div class="arrow"></div>' +
			'<h3 class="popover-title"></h3>' +
			'<div class="popover-content"></div>' +
			'<div class="popover-navigation">' +
				'<div class="btn-group">' +
					'<button class="btn btn-sm btn-default" data-role="prev">&#xab; ' + _t(prev) + '</button>' +
					'<button class="btn btn-sm btn-default" data-role="next">' + _t(next) + ' &#xbb;</button>' +
			'</div>' +
			'<button class="btn btn-sm btn-success" data-role="end">' + _t(tourEnd) + '</button>' +
		'</div>';
		
	// click function for lang switch
	var set_lang_click = function () {
		setTimeout(function () {
			// language switch
			var switcher = getLanguage() === 'en' ? $('#switch-to-de') : $('#switch-to-en');
			var lang = getLanguage() === 'en' ? 'de' : 'en';
			switcher.click(function () { new AjaxMainHandler().ajaxSwitchDisplayLanguage(lang); });
			switcher.find('img').click(function () { new AjaxMainHandler().ajaxSwitchDisplayLanguage(lang); });
		}, 500);
	};
		
	// function on start
	var start_fct = function () {
		tour.init(); // Initialize the tour
		tour.restart(); // Start the tour
		setLocalStorage(GUIDED_TOUR_RUNNING, true);
		set_lang_click();
	};
	
	// function on end
	var end_fct = function(){
		setLocalStorage(GUIDED_TOUR_RUNNING, false);
		Cookies.set(GUIDED_TOUR, true, { expires: 180 });
		// var url = window.location.href;
		//if (url !== mainpage && url.indexOf('#tour2') === -1) {
		//	 window.location.href = mainpage;
		//}
	};
	
	this.prepareSteps = function(){
		// lang switcher
		if (getLanguage() === 'en'){
			var de_flag = $('#' + translationLinkDe).find('img').attr('src');
			lang_switcher = '<a id="switch-to-de" class="pull-right" style="cursor: pointer;"><img class="language_selector_img" src="' + de_flag + '" alt="flag_ge" style="width:25px;"></a>';
		} else {
			var en_flag = $('#' + translationLinkEn).find('img').attr('src');
			lang_switcher = '<a id="switch-to-en" class="pull-right" style="cursor: pointer;"><img class="language_selector_img" src="' + en_flag + '" alt="flag_en" style="width:25px;"></a>';
		}
		
		// steps
		var welcome = {
			element: '#logo_dbas',
			title: _t(tourWelcomeTitle) + lang_switcher,
			content: _t(tourWelcomeContent),
			placement: 'bottom',
		};
		var start_button = {
			element: '#start-discussion-button',
			title: _t(tourStartButtonTitle) + lang_switcher,
			content: _t(tourStartButtonContent),
			placement: 'bottom',
		};
		var login_button = {
			element: '#login-link',
			title: _t(tourLoginTitle),
			content: _t(tourLoginContent),
			placement: 'bottom',
		};
		var issue = {
			element: '#header-container',
			title: _t(tourIssueTitle) + lang_switcher,
			content: _t(tourIssueContent),
			placement: 'bottom',
		};
		var start_discussion = {
			element: '#dialog-speech-bubbles-space',
			title: _t(tourStartDiscussionTitle) + lang_switcher,
			content: _t(tourStartDiscussionContent),
			placement: 'bottom',
			path: '/discuss'
		};
		var mark_opinion = {
			element: '#some-element-bubble',
			title: _t(tourMarkOpinionTitle) + lang_switcher,
			content: _t(tourMarkOpinionContent),
			placement: 'bottom',
			path: '/discuss',
			onShow: function () {
				var element = '<div class="line-wrapper-r" id="some-element-bubble">' +
					'<p class="triangle-r"><i class="fa fa-star-o" aria-hidden="true" style="padding-right: 0.5em"></i>' +
					'<span class="triangle-content">' + _t(tourMarkOpinionText) + '</span></p></div>';
				$('#dialog-speech-bubbles-space').prepend($.parseHTML(element));
			},
			onHide: function () {
				$('#some-element-bubble').remove();
			},
		};
		var choose_answer = {
			element: '#discussions-space-list',
			title: _t(tourSelectAnswertTitle) + lang_switcher,
			content: _t(tourSelectAnswertContent),
			placement: 'bottom',
			path: '/discuss'
		};
		var set_input = {
			element: '#discussions-space-list li:last-child',
			title: _t(tourEnterStatementTitle) + lang_switcher,
			content: _t(tourEnterStatementContent),
			placement: 'bottom',
			path: '/discuss'
		};
		var have_fun = {
			element: '.jumbotron',
			title: _t(tourHaveFunTitle) + lang_switcher,
			content: _t(tourHaveFunContent),
			placement: 'bottom',
			path: '/#tour2',
			template: template_end
		};
		
		//data-placement="bottom"
		tour = new Tour({
			steps: [
				welcome,
				start_button,
				//login_button,
				issue,
				start_discussion,
				mark_opinion,
				choose_answer,
				set_input,
				have_fun,
				],
			backdrop: true,
			backdropPadding: 5,
			template: template,
			onEnd: end_fct,
		});
		
	};
	
	/**
	 *
	 */
	this.start = function(){
		//displayBubbleInformationDialog();
		this.prepareSteps();
		
		// params
		var url = window.location.href;
		var part0 = url === mainpage || url === location.origin;
		var part1 = url.indexOf('/discuss') !== -1;
		var part2 = url === mainpage + '#tour2' || url === location.origin + '#tour2';
		
		// decision where we are
		if (part0 && !part1 && !part2){ // first part on the start page, where we ask the user for a tour
			// build dialog
			var title = _t(tourWelcomeTitle);
			var text = _t(welcomeDialogBody) + lang_switcher.replace('style="', 'style="display: none; ');
			var dialog = $('#' + popupConfirmDialogId);
			dialog.on('shown.bs.modal', function (){
				var switcher = getLanguage() === 'en' ? $('#switch-to-de') : $('#switch-to-en');
				switcher.detach();
				switcher.removeClass('pull-right').addClass('pull-left');
				switcher.insertBefore($('#' + popupConfirmDialogAcceptBtn)).show();
			});
			dialog.on('hide.bs.modal', function (){
				var switcher = getLanguage() === 'en' ? $('#switch-to-de') : $('#switch-to-en');
				switcher.remove();
			});
			displayConfirmationDialog(title, text, start_fct, end_fct, false);
			dialog.find('#confirm-dialog-accept-btn').text(_t(yes));
			dialog.find('#confirm-dialog-refuse-btn').text(_t(no));
			set_lang_click();
		} else if(!part0 && part1 && !part2 && getLocalStorage(GUIDED_TOUR_RUNNING) === 'true'){ // part 2: discussion
			tour.init();
			tour.goTo(2);
			set_lang_click();
			setLocalStorage(GUIDED_TOUR_RUNNING, true);
		} else if(!part0 && !part1 && part2 && getLocalStorage(GUIDED_TOUR_RUNNING) === 'true'){ // part 3, the end
			tour.init();
			tour.goTo(6);
			set_lang_click();
			setLocalStorage(GUIDED_TOUR_RUNNING, true);
		}
	};
}