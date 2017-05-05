/**
 * Created by tobias on 26.01.17.
 */

function GuidedTour(){
    'use strict';
    
	var lang_switcher = '';
	var tour = '';
	var step_list = [];
	var start_from_index = false;
		
	// override default template for i18n
	var template =
		'<div class="popover tour">' +
			'<div class="arrow"></div>' +
			'<h3 class="popover-title"></h3>' +
			'<div class="popover-content"></div>' +
			'<div class="popover-navigation">' +
				'<div class="btn-group">' +
					'<button class="btn btn-sm btn-secondary" data-role="prev">&#xab; ' + _t(prev) + '</button>' +
					'<button class="btn btn-sm btn-success" data-role="next">' + _t(next) + ' &#xbb;</button>' +
			'</div>' +
			'<button class="btn btn-sm btn-secondary" data-role="end">' + _t(tourEnd) + '</button>' +
		'</div>';
	
	var template_end =
		'<div class="popover tour">' +
			'<div class="arrow"></div>' +
			'<h3 class="popover-title"></h3>' +
			'<div class="popover-content"></div>' +
			'<div class="popover-navigation">' +
				'<div class="btn-group">' +
					'<button class="btn btn-sm btn-secondary" data-role="prev">&#xab; ' + _t(prev) + '</button>' +
					'<button class="btn btn-sm btn-secondary" data-role="next">' + _t(next) + ' &#xbb;</button>' +
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
		setLocalStorage(GUIDED_TOUR_RUNNING_START, start_from_index);
		setLocalStorage(GUIDED_TOUR_RUNNING_DISCUSSION, !start_from_index);
		set_lang_click();
	};
	
	// function on end
	var end_fct = function(){
		setLocalStorage(GUIDED_TOUR_RUNNING_START, false);
		setLocalStorage(GUIDED_TOUR_RUNNING_DISCUSSION, false);
		Cookies.set(GUIDED_TOUR, true, { expires: 60 });
	};
	
	/**
	 * Prepares the steps of the tour as well as the tour itself
	 */
	this.prepareSteps = function(startFromIndex){
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
			element: '#start-text',
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
			path: '/discuss',
		};
		var start_discussion = {
			element: '#dialog-speech-bubbles-space',
			title: _t(tourStartDiscussionTitle) + lang_switcher,
			content: _t(tourStartDiscussionContent),
			placement: 'bottom',
		};
		var mark_opinion = {
			element: '#some-element-bubble .triangle-r',
			title: _t(tourMarkOpinionTitle) + lang_switcher,
			content: _t(tourMarkOpinionContent),
			placement: 'bottom',
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
		};
		var set_input = {
			element: '#discussions-space-list li:last-child',
			title: _t(tourEnterStatementTitle) + lang_switcher,
			content: _t(tourEnterStatementContent),
			placement: 'bottom',
		};
		var first_child = $('#discussions-space-list li:first');
		var statement_action = {
			element: '#discussions-space-list li:first',
			title: _t(tourStatementActionTitle) + lang_switcher,
			content: _t(tourStatementActionContent),
			placement: 'bottom',
			onShow: function () {
				first_child.trigger("mouseenter");
			},
			onHide: function () {
				first_child.trigger("mouseleave");
			}
		};
		var have_fun = {
			element: startFromIndex? '.jumbotron' : '#discussion-container',
			title: _t(tourHaveFunTitle) + lang_switcher,
			content: _t(tourHaveFunContent),
			placement: 'bottom',
			path: startFromIndex ? '/#tour2' : '/discuss',
			template: template_end
		};
		
		if (startFromIndex){
			step_list = [
				start_button,       // 1
				//login_button,
				issue,              // 2
				start_discussion,   // 3
				mark_opinion,       // 4
				choose_answer,      // 5
				set_input,          // 6
				statement_action,   // 7
				have_fun,           // 8
				];
		} else {
			step_list = [
				issue,              // 0
				start_discussion,   // 1
				mark_opinion,       // 2
				choose_answer,      // 3
				set_input,          // 4
				have_fun,           // 5
			];
		}
		//data-placement="bottom"
		tour = new Tour({
			steps: step_list,
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
		this.prepareSteps(true);
		
		// are we on the discuss-page?
		var split = window.location.href.replace('discuss#', 'discuss').split('/');
		var pos = split.indexOf('discuss');
		var startOnDiscussionPage = split.length === pos + 2 || split.length === pos + 1;
		
		// params
		var url = window.location.href;
		var part0 = url === mainpage || url === location.origin;
		var part1 = url.indexOf('/discuss') !== -1;
		var part2 = url === mainpage + '#tour2' || url === location.origin + '#tour2';
		
		// decision where we are
		if (part0 && !part1 && !part2){
			start_from_index = true;
			this.__startTour();
		} else if(!part0 && part1 && !part2 || startOnDiscussionPage){
			if (getLocalStorage(GUIDED_TOUR_RUNNING_START) === 'true') {
				console.log(0);
				this.__continueIndexTourOnDiscussionPage();
			} else if (startOnDiscussionPage){
				start_from_index = false;
				this.prepareSteps(false);
				console.log(1);
				this.__startTour();
			}
			
		} else if(!part0 && !part1 && part2 && getLocalStorage(GUIDED_TOUR_RUNNING_START) === 'true' && getLocalStorage(GUIDED_TOUR_RUNNING_DISCUSSION) === 'false'){
			this.__endIndexTourOnDiscussionPage();
		}
	};
	
	this.__startTour = function(){
		// build dialog
		var title = _t(tourWelcomeTitle);
		var text = _t(welcomeDialogBody) + lang_switcher.replace('style="', 'style="display: none; ');
		var dialog = $('#' + popupConfirmDialogId);
		
		// add language switcher
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
	};
	
	this.__continueIndexTourOnDiscussionPage = function(){
		tour.init();
		tour.goTo(1);
		set_lang_click();
		setLocalStorage(GUIDED_TOUR_RUNNING_START, true);
	};
	
	this.__endIndexTourOnDiscussionPage = function(){
		tour.init();
		tour.goTo(step_list.length - 1);
		set_lang_click();
		setLocalStorage(GUIDED_TOUR_RUNNING_START, true);
		
		// modify both buttons on start page for ending the tour
		var btn1 = $('.btn-warning');
		var btn2 = $('.btn-info');
		var url1 = btn1.attr('href');
		var url2 = btn2.attr('href');
		btn1.click(function(){
			end_fct();
			window.location.href = url1;
		}).attr('href', '#');
		btn2.click(function(){
			end_fct();
			window.location.href = url2;
		}).attr('href', '#');
	};
}