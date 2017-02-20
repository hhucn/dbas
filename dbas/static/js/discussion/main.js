/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */
'use strict';


function Main () {
	
	/**
	 * Sets all click functions
	 *
	 * @param guiHandler
	 * @param popupHandler
	 * @param ajaxHandler
	 */
	this.setClickFunctions = function (guiHandler, popupHandler, ajaxHandler) {
		$('.icon-add-premise').each(function () {
			$(this).click(function () {
				guiHandler.appendAddPremiseRow($(this));
				$(this).hide().prev().show();
				$('#' + sendNewPremiseId).val(_t(saveMyStatements));
			});
		});
		
		/*
		 $('.icon-rem-premise').each(function() {
		 // set in GuiHandler
		 });
		 */
		
		// admin list all users button
		$('#' + listAllUsersButtonId).click(function listAllUsersButtonId() {
			if ($(this).val() === _t(showAllUsers)) {
				ajaxHandler.getUsersOverview();
				$(this).val(_t(hideAllUsers));
			} else {
				$('#' + adminsSpaceForUsersId).empty();
				$(this).val(_t(showAllUsers));
			}
		});
		
		// admin list all attacks button
		$('#' + listAllArgumentId).click(function listAllUsersAttacksId() {
			if ($(this).val() === _t(showAllAttacks)) {
				ajaxHandler.getArgumentOverview();
			} else {
				$('#' + adminsSpaceForArgumentsId).empty();
			}
		});
		
		// hiding the argument container, when the X button is clicked
		$('#' + closeStatementContainerId).click(function closeStatementContainerId() {
			$('#' + addStatementContainerId).hide();
			$('#' + addStatementErrorContainer).hide();
			$('#' + discussionSpaceId + ' li:last-child input').prop('checked', false).enable = true;
		});
		
		// hides container
		$('#' + closePremiseContainerId).click(function closeStatementContainerId() {
			$('#' + addPremiseContainerId).hide();
			$('#' + addPremiseErrorContainer).hide();
			$('#' + discussionSpaceId + ' li:last-child input').prop('checked', false).enable = true;
		});
		
		// hiding the island view, when the X button is clicked
		$('#' + closeIslandViewContainerId).click(function () {
			guiHandler.resetChangeDisplayStyleBox();
			$('#li_' + addReasonButtonId).prop('checked', true);
		});
		
		// hiding the island view, when the X button is clicked
		$('#' + closeGraphViewContainerId).click(function () {
			guiHandler.resetChangeDisplayStyleBox();
		});
		
		// close popups
		$('#' + popupEditStatementCloseButtonXId).click(function popupEditStatementCloseButtonXId() {
			popupHandler.hideAndClearEditStatementsPopup();
		});
		$('#' + popupEditStatementCloseButtonId).click(function popupEditStatementCloseButtonId() {
			popupHandler.hideAndClearEditStatementsPopup();
		});
		$('#' + popupUrlSharingCloseButtonXId).click(function popupUrlSharingCloseButtonXId() {
			popupHandler.hideAndClearUrlSharingPopup();
		});
		$('#' + popupUrlSharingCloseButtonId).click(function popupUrlSharingCloseButtonId() {
			popupHandler.hideAndClearUrlSharingPopup();
		});
		
		$('#' + popupEditStatementSubmitButtonId).click(function popupEditStatementSubmitButton() {
			var elements = [];
			$('#' + popupEditStatementInputSpaceId).find('input').each(function(){
				elements.push({'text': $(this).val(), 'uid': $(this).data('statement-uid')})
			});
			new AjaxDiscussionHandler().sendCorrectionOfStatement(elements);
		});
		
		// share url for argument blogging
		$('#' + shareUrlId).click(function shareurlClick() {
			popupHandler.showUrlSharingPopup();
		});
		
		/**
		 * Switch between shortened and long url
		 */
		$('#' + popupUrlSharingLongUrlButtonID).click(function () {
			var input_field = $('#' + popupUrlSharingInputId);
			
			if ($(this).data('is-short-url') == '0') {
				input_field.val(input_field.data('short-url'));
				$(this).data('is-short-url', '1').text(_t_discussion(fetchLongUrl));
			} else {
				input_field.val(window.location);
				$(this).data('is-short-url', '0').text(_t_discussion(fetchShortUrl));
			}
		});
		
		/**
		 * Sharing shortened url with mail
		 */
		$('#' + shareUrlButtonMail).click(function shareUrlButtonMail() {
			new Sharing().emailShare('user@example.com', _t(interestingOnDBAS), _t(haveALookAt) + ' ' + $('#' + popupUrlSharingInputId).val());
		});
		
		/**
		 * Sharing shortened url on twitter
		 */
		$('#' + shareUrlButtonTwitter).click(function shareUrlButtonTwitter() {
			new Sharing().twitterShare($('#' + popupUrlSharingInputId).val(), '');
		});
		
		/**
		 * Sharing shortened url on google
		 */
		$('#' + shareUrlButtonGoogle).click(function shareUrlButtonGoogle() {
			new Sharing().googlePlusShare($('#' + popupUrlSharingInputId).val());
		});
		
		/**
		 * Sharing shortened url on facebook
		 */
		$('#' + shareUrlButtonFacebook).click(function shareUrlButtonFacebook() {
			var val = $('#' + popupUrlSharingInputId).val();
			new Sharing().facebookShare(val, "FB Sharing", _t(haveALookAt) + ' ' + val,
				mainpage + "static/images/logo.png");
		});
		
		//guiHandler.setDisplayStyleAsDiscussion();
		$('#' + displayStyleIconGuidedId).click(function displayStyleIconGuidedFct() {
			guiHandler.setDisplayStyleAsDiscussion();
			clearAnchor();
		});
		$('#' + displayStyleIconIslandId).click(function displayStyleIconIslandFct() {
			guiHandler.setDisplayStyleAsIsland();
			setAnchor('island');
		});
		$('#' + displayStyleIconGraphId).click(function displayStyleIconExpertFct() {
			guiHandler.setDisplayStyleAsGraphView();
			setAnchor('graph');
		});
		
		// opinion barometer
		$('#' + opinionBarometerImageId).show().click(function opinionBarometerFunction() {
			new DiscussionBarometer().showBarometer();
			setAnchor('barometer');
		});
		
		// issues
		$('#' + issueDropdownListID + ' .enabled').each(function () {
			if ($(this).children().length > 0) {
				$(this).children().click(function () {
					var href = $(this).attr('href');
					var text = _t(switchDiscussionText).replace('XXX', $(this).attr('data-value'));
					$(this).attr('href', '#');
					displayConfirmationDialogWithCheckbox(_t(switchDiscussion), text, _t.keepSetting, href, true);
				});
			}
		});
		$('#' + issueDropdownListID + ' .disabled a').off('click').unbind('click').removeAttr('href');
		$('#issue-long-info-link').click(function(){
			var title = $('#issue_info').data('title');
			var info = $(this).data('info');
			var long_info = $(this).data('long-info');
			displayConfirmationDialogWithoutCancelAndFunction(title, long_info + '<br><br>' + info);
		});
		
		// get infos about the author
		//$('[id^="' + questionBubbleId + '-"').click(function () {
		var trianglel = $('.triangle-l');
		trianglel.find('.triangle-content :not(a)').click(function () {
			var url = window.location.href;
			if (url.indexOf('/d?history') != -1) {
				url = url.split('/d?history');
				url = url[0].split('/');
				var uid = url[url.length - 1];
				ajaxHandler.getMoreInfosAboutArgument(uid, true);
			} else {
				if ($(this).closest('p').attr('id').indexOf(questionBubbleId) != -1) {
					var uid = $(this).closest('p').attr('id').replace(questionBubbleId + '-', '');
					ajaxHandler.getMoreInfosAboutArgument(uid, true);
				}
			}
		});
		
		// do not hover the other spans on hovering the name
		trianglel.find('.triangle-content a').hover(function() {
			trianglel.find('.triangle-content :not(a)').each(function(){
				if (!('argumentationType' in $(this).data())){
					$(this).css('color', '#000');
				}
			});
		}, function() {
			trianglel.find('.triangle-content :not(a)').each(function(){
				if (!('argumentationType' in $(this).data())){
					$(this).css('color', '');
				}
			});
		});
		
		var splitted_url = window.location.href.split('/');
		if (splitted_url.length > 5) {
			if (window.location.href.split('/')[5].indexOf('jump') != -1) {
				trianglel.find('.triangle-content').hover(function () {
					$(this).css('color', '#000').css('cursor', 'default');
					
				}, function () {
					$(this).css('color', '');
				});
			}
		}
		
		// remove hover on start
		if (trianglel.length == 1 && trianglel.attr('id') == 'start'){
			trianglel.html(trianglel.text().trim());
		}
		
		trianglel.find('.triangle-flag').click(function () {
			var uid = $(this).closest('.triangle-l').attr('id').replace(questionBubbleId + '-', '');
			popupHandler.showFlagArgumentPopup(uid);
		});
		
		trianglel.find('.triangle-reference').click(function () {
			var uid = $(this).parent().attr('id').replace(questionBubbleId + '-', '');
			new AjaxReferenceHandler().getReferences(uid, true);
		});
		
		trianglel.find('.triangle-trash').click(function () {
			var uid = $(this).parent().attr('id').replace(questionBubbleId + '-', '');
			popupHandler.showDeleteContentPopup(uid, true);
		});
		
		var list = $('#' + discussionSpaceListId);
		list.find('.item-flag').click(function () {
			var uid = $(this).parent().find('input').attr('id').replace('item_', '');
			var text = [];
			$.each($(this).parent().find('label'), function(){
				text.push($(this).text());
			});
			popupHandler.showFlagStatementPopup(uid, false, text.join(' '));
		});
		
		list.find('.item-edit').click(function () {
			var uids = [];
			$(this).parent().find('label:nth-child(even)').each(function(){
				uids.push($(this).attr('id'))
			});
			popupHandler.showEditStatementsPopup(uids);
		});
		
		list.find('.item-trash').click(function () {
			var uid = $(this).parent().find('label').attr('id');
			popupHandler.showDeleteContentPopup(uid, false);
		});
		
		list.find('.item-reference').click(function () {
			var uids = [];
			$(this).parent().find('label:nth-child(even)').each(function(){
				uids.push($(this).attr('id'))
			});
			new AjaxReferenceHandler().getReferences(uids, false);
		});
		
		// adding issues
		$('#' + addTopicButtonId).click(function () {
			popupHandler.showAddTopicPopup();
		});
		
		// user info click
		$('.triangle-r-info').each(function () {
			if ($(this).data('votecount') > 0) {
				$(this).click(function () {
					var data_type = $(this).data('type');
					var data_argument_uid = $(this).data('argument-uid');
					var data_statement_uid = $(this).data('statement-uid');
					var data_is_supportive = $(this).data('is-supportive');
					new AjaxDiscussionHandler().getMoreInfosAboutOpinion(data_type, data_argument_uid, data_statement_uid, data_is_supportive);
				});
			} else {
				$(this).removeClass('triangle-r-info').addClass('triangle-r-info-nohover');
			}
		});
		
		$('#' + contactSubmitButtonId).click(function () {
			setTimeout("$('body').addClass('loading')", 0);
		});
		
		$('#' + discussionSpaceShowItems).click(function(){
			$(this).hide();
			var hide_btn = $('#' + discussionSpaceHideItems);
			var space = $('#' + discussionSpaceListId);
			hide_btn.show();
			// send request if it was not send until now
			if ($(this).attr('data-send-request') !== 'true'){
				var uids = [];
				$.each(space.find('li:not(:visible)'), function(){
					$.each($(this).find('label:even'), function(){
						uids.push($(this).attr('id'));
					})
				});
				new AjaxDiscussionHandler().setSeenStatements(uids);
			}
			// fade in after we collected the missed id's!
			space.find('li[style="display: none;"]').addClass('cropped').fadeIn();
			
			// guification, resize main container and sidebar
			var container = $('#' + discussionContainerId);
			var add_height = space.find('li.cropped').length * space.find('li:visible:first').outerHeight() + hide_btn.outerHeight();
			var container_height = parseInt(container.css('max-height').replace('px',''));
			container.css('max-height', (add_height + container_height) + 'px');
			container.attr('data-add-height', add_height);
			
			var sidebar = $('.sidebar-wrapper:first');
			sidebar.height(sidebar.height() + add_height);
				
		});
		
		$('#' + discussionSpaceHideItems).click(function(){
			$(this).hide();
			$('#' + discussionSpaceShowItems).show();
			$('#' + discussionSpaceListId).find('li.cropped').fadeOut();
			var container = $('#' + discussionContainerId);
			var height = parseInt(container.css('max-height').replace('px',''));
			var new_height = height - parseInt(container.attr('data-add-height'));
			// guification, resize main container and sidebar
			setTimeout(function() {
				container.css('max-height', new_height + 'px');
				var sidebar = $('.sidebar-wrapper:first');
				sidebar.height(sidebar.height() - parseInt(container.attr('data-add-height')));
			}, 400);
		});
		
		// star click
		$('.' + checkAsUsersOpinion).click(function(){
			var id = 'star-' + new Date().getTime();
			$(this).attr('id', id);
			console.log(id);
			var info = $(this).parent().children().last();
			var is_argument = info.data('type') == 'argument';
			var uid = info.data(info.data('type') + '-uid');
			var is_supportive = info.data('is-supportive');
			var step = location.href.split('#')[0].split('?')[0].split('/').slice(5).join('/');
			var history = location.href.split('#')[0].split('?')[1];
			ajaxHandler.markStatementOrArgument(uid, is_argument, is_supportive, true, step, history, id);
		});
		
		$('.' + uncheckAsUsersOpinion).click(function(){
			var id = 'star-' + new Date().getTime();
			$(this).attr('id', id);
			var info = $(this).parent().children().last();
			var is_argument = info.data('type') == 'argument';
			var uid = info.data(info.data('type') + '-uid');
			var is_supportive = info.data('is-supportive');
			var step = location.href.split('#')[0].split('?')[0].split('/').slice(5).join('/');
			var history = location.href.split('#')[0].split('?')[1];
			ajaxHandler.markStatementOrArgument(uid, is_argument, is_supportive, false, step, history, id);
		});
		
		// styling
		$('.fa-star[data-is-users-opinion="True"]').show();
		$('.fa-star-o[data-is-users-opinion="False"]').show();
	};
	
	/**
	 * Sets click functions for the elements in the sidebar
	 * @param maincontainer - main container which contains the content on the left and the sidebar on the rigt
	 * @param localStorageId - id of the parameter in the local storage
	 */
	this.setSidebarClicks = function (maincontainer, localStorageId) {
		var gui = new GuiHandler();
		var sidebarwrapper = maincontainer.find('.' + sidebarWrapperClass);
		var wrapper = maincontainer.find('.' + contentWrapperClass);
		var hamburger = sidebarwrapper.find('.' + hamburgerIconClass);
		var tackwrapper = sidebarwrapper.find('.' + sidebarTackWrapperClass);
		var tack = sidebarwrapper.find('.' + sidebarTackClass);
		var sidebar = sidebarwrapper.find('.' + sidebarClass);
		
		$(hamburger).click(function () {
			$(this).toggleClass('open');
			var width = wrapper.width();
			var bg_color = $('#' + discussionBubbleSpaceId).css('background-color');
			
			if (sidebar.is(':visible')) {
				tackwrapper.fadeOut();
				sidebar.toggle('slide');
				hamburger.css('margin-right', '0.5em')
					.css('background-color', '');
				maincontainer.css('max-height', '');
				sidebarwrapper.css('background-color', '')
					.css('height', '');
				setTimeout(function () {
					wrapper.width('');//width + sidebar.outerWidth());
				}, 300);
				setLocalStorage(localStorageId, 'false');
			} else {
				wrapper.width(width - sidebar.outerWidth());
				maincontainer.css('max-height', maincontainer.outerHeight() + 'px');
				setTimeout(function () {
					sidebar.toggle('slide');
					hamburger.css('margin-right', (sidebarwrapper.width() - hamburger.width()) / 2 + 'px')
						.css('margin-left', 'auto')
						.css('background-color', sidebar.css('background-color'));
					sidebarwrapper.css('background-color', bg_color)
						.css('height', maincontainer.outerHeight() + 'px');
					tackwrapper.fadeIn();
				}, 200);
			}
		});
		
		// action for tacking the sidebar
		tackwrapper.click(function () {
			var shouldShowSidebar = getLocalStorage(localStorageId) == 'true';
			if (shouldShowSidebar) {
				gui.rotateElement(tack, '0');
				setLocalStorage(localStorageId, 'false');
				
				tack.data('title', _t_discussion(pinNavigation));
				
				// hide sidebar if it is visible
				if (sidebar.is(':visible')) {
					hamburger.click();
				}
			} else {
				gui.rotateElement(tack, '90');
				setLocalStorage(localStorageId, 'true');
				tack.data('title', _t_discussion(unpinNavigation));
			}
		});
		
	};
	
	/**
	 * Sets style options for the elements in the sidebar
	 * @param maincontainer - main container which contains the content on the left and the sidebar on the rigt
	 * @param localStorageId - id of the parameter in the local storage
	 */
	this.setSidebarStyle = function (maincontainer, localStorageId) {
		// read local storage for pinning the bar / set title
		var shouldShowSidebar = getLocalStorage(localStorageId) == 'true';
		var sidebarwrapper = maincontainer.find('.' + sidebarWrapperClass);
		var wrapper = maincontainer.find('.' + contentWrapperClass);
		var tackwrapper = sidebarwrapper.find('.' + sidebarTackWrapperClass);
		var tack = sidebarwrapper.find('.' + sidebarTackClass);
		var sidebar = sidebarwrapper.find('.' + sidebarClass);
		var gui = new GuiHandler();
		
		if (shouldShowSidebar) {
			var width = wrapper.width();
			var hamburger = sidebarwrapper.find('.' + hamburgerIconClass);
			
			gui.rotateElement(tack, '90');
			gui.setAnimationSpeed(wrapper, '0.0');
			gui.setAnimationSpeed(hamburger, '0.0');
			
			hamburger.addClass('open');
			
			wrapper.width(width - sidebar.outerWidth());
			maincontainer.css('max-height', maincontainer.outerHeight() + 'px');
			sidebar.show();
			hamburger.css('margin-right', (sidebarwrapper.width() - hamburger.width()) / 2 + 'px')
				.css('margin-left', 'auto')
				.css('background-color', sidebar.css('background-color'));
			sidebarwrapper.css('background-color', $('#' + discussionBubbleSpaceId).css('background-color'))
				.css('height', maincontainer.outerHeight() + 'px');
			tackwrapper.fadeIn();
			
			gui.setAnimationSpeed(wrapper, '0.5');
			gui.setAnimationSpeed(hamburger, '0.5');
			
			tackwrapper.data('title', _t_discussion(unpinNavigation));
		} else {
			tackwrapper.data('title', _t_discussion(pinNavigation));
		}
	};
	
	/**
	 * Sets all keyUp functions
	 * @param guiHandler
	 * @param ajaxHandler
	 */
	this.setKeyUpFunctions = function (guiHandler, ajaxHandler) {
		// gui for the fuzzy search (statements)
		$('#' + addStatementContainerMainInputId).keyup(function () {
			setTimeout(function () {
				var escapedText = escapeHtml($('#' + addStatementContainerMainInputId).val());
				if ($('#' + discussionBubbleSpaceId).find('.triangle-l:last-child').text().indexOf(_t_discussion(initialPositionInterest)) != -1) {
					// here we have our start statement
					ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputId, fuzzy_start_statement, '');
				} else {
					// some trick: here we have a premise for our start statement
					ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputId, fuzzy_start_premise, '');
				}
			}, 200);
		});
		
		// gui for the fuzzy search (premises)
		$('#' + addPremiseContainerMainInputId).keyup(function () {
			setTimeout(function () {
				var escapedText = escapeHtml($('#' + addPremiseContainerMainInputId).val());
				ajaxHandler.fuzzySearch(escapedText, addPremiseContainerMainInputId, fuzzy_add_reason, '');
			}, 200);
		});
	};
	
	/**
	 *
	 * @param guiHandler
	 */
	this.setStyleOptions = function (guiHandler) {
		guiHandler.setMaxHeightForBubbleSpace();
		
		guiHandler.hideSuccessDescription();
		guiHandler.hideErrorDescription();
		
		// align buttons
		// var restart, issues, restartWidth, issueWidth;
		// restart = $('#discussion-restart-btn');
		// issues = $('#' + issueDropdownButtonID);
		// restartWidth = restart.outerWidth();
		// issueWidth = issues.outerWidth();
		// restart.attr('style', restartWidth<issueWidth ? 'width: ' + issueWidth + 'px;' : '');
		// issues.attr('style', restartWidth>issueWidth ? 'width: ' + restartWidth + 'px;' : '');
		
		// no hover action on the systems bubble during the attitude question
		var trianglel = $('.triangle-l');
		var url = window.location.href.split('?')[0];
		if (url.indexOf('attitude') != -1 || url.indexOf('justify') != -1) {
			trianglel.find('.triangle-content').each(function () {
				$(this).hover(function () {
					$(this).css({'color': '#000', 'cursor': 'auto'});
				}, function () {
					$(this).css({'color': '#000', 'cursor': 'auto'});
				});
			});
		}
		
		// focus text of input elements
		// $('input[type='text']'').on("click", function () {
		$('#' + popupUrlSharingInputId).on("click", function () {
			$(this).select();
		});
		
		// hover effects on text elements
		var data = 'data-argumentation-type';
		var list = $('#' + discussionSpaceListId);
		var trianglel_last = trianglel.last();
		list.find('span[' + data + '!=""]').each(function () {
			var attr = $(this).attr(data);
			var tmp = $('<span>').addClass(attr + '-highlighter');
			tmp.appendTo(document.body);
			var old_color = $(this).css('color');
			var new_color = tmp.css('color');
			tmp.remove();
			$(this).hover(
				function () {
					$('#dialog-speech-bubbles-space').find('span[' + data + '="' + attr + '"]')
						.css({'color': new_color, 'background-color': '#edf3e6', 'border-radius': '2px'});
					if ($(this).attr(data) == 'argument') {
						trianglel_last.find('span[data-attitude="pro"]').addClass('text-success').css({'background-color': '#edf3e6', 'border-radius': '2px'});
						trianglel_last.find('span[data-attitude="con"]').addClass('text-danger').css({'background-color': '#edf3e6', 'border-radius': '2px'});
					}
				}, function () {
					$('#dialog-speech-bubbles-space').find('span[' + data + '="' + attr + '"]')
						.css({'color': old_color, 'background-color': '', 'border-radius': ''});
					trianglel_last.find('span[data-attitude="pro"]').removeClass('text-success').css({'background-color': '', 'border-radius': ''});
					trianglel_last.find('span[data-attitude="con"]').removeClass('text-danger').css({'background-color': '', 'border-radius': ''});
				}
			);
		});
		
		// hover on radio buttons
		guiHandler.hoverInputListOf($('#popup-flag-argument'));
		guiHandler.hoverInputListOf($('#popup-flag-statement'));
		guiHandler.hoverInputListOf(list);
		
		list.find('li').find('.fa').parent().hide();
		list.find('li').each(function(){
			$(this).hover(function(){
				$(this).find('.fa').parent().show();
			}, function(){
				$(this).find('.fa').parent().hide();
			})
		});
	};
	
	/**
	 * Sets some style options for the window
	 */
	this.setWindowOptions = function () {
		// some hack
		$('#navbar-left').empty();
		
		var container = $('#' + discussionContainerId);
		var oldContainerSize = container.width();
		var burger = $('.hamburger');
		var wrapper = $('#dialog-wrapper');
		
		$(window).resize(function () {
			new GuiHandler().setMaxHeightForBubbleSpace();
			
			// resize main container
			var difference = oldContainerSize - container.width();
			if (difference > 0 && burger.hasClass('open')){
				wrapper.width(wrapper.width() - difference);
			} else if (difference < 0 && burger.hasClass('open')){
				wrapper.width(wrapper.width() - difference);
			}
			oldContainerSize = container.width();
		});
	};
	
	/**
	 *
	 */
	this.setGuiOptions = function () {
		$('#' + popupLogin).on('hidden.bs.modal', function () {// uncheck login button on hide
			var login_item = $('#' + discussionSpaceListId).find('#item_login');
			if (login_item.length > 0)
				login_item.prop('checked', false)
		}).on('shown.bs.modal', function () {
			$('#' + loginUserId).focus();
		});
		
		// highlight edited statement
		var pos = window.location.href.indexOf('edited_statement=');
		if (pos != -1) {
			var ids = window.location.href.substr(pos + 'edited_statement='.length);
			var splitted = ids.split(',');
			$.each(splitted, function (index, value) {
				$('#' + value).css('background-color', '#FFF9C4');
			});
		}
	};
	
	/**
	 *
	 * @param guiHandler
	 * @param interactionHandler
	 */
	this.setInputExtraOptions = function (guiHandler, interactionHandler) {
		var spaceList = $('#' + discussionSpaceListId);
		var input = spaceList.find('li:last-child input');
		var text = [], splits, conclusion, supportive, arg, relation;
		splits = window.location.href.split('?');
		splits = splits[0].split('/');
		var sendStartStatement = function () {
			text = $('#' + addStatementContainerMainInputId).val();
			interactionHandler.sendStatement(text, '', '', '', '', fuzzy_start_statement);
		};
		var sendStartPremise = function () {
			conclusion = splits[splits.length - 2];
			supportive = splits[splits.length - 1] == 't';
			text = [];
			$('#' + addPremiseContainerBodyId + ' input').each(function () {
				if ($(this).val().length > 0)
					text.push($(this).val());
			});
			interactionHandler.sendStatement(text, conclusion, supportive, '', '', fuzzy_start_premise);
		};
		var sendArgumentsPremise = function () {
			text = [];
			$('#' + addPremiseContainerBodyId + ' input').each(function () {
				if ($(this).val().length > 0)
					text.push($(this).val());
			});
			var add = window.location.href.indexOf('support') != -1 ? 1 : 0;
			arg = splits[splits.length - 3 - add];
			supportive = splits[splits.length - 2 - add] == 't';
			relation = splits[splits.length - 1 - add];
			interactionHandler.sendStatement(text, '', supportive, arg, relation, fuzzy_add_reason);
		};
		
		if (window.location.href.indexOf('/r/') != -1) {
			$('#' + discussionSpaceId + ' label').each(function () {
				$(this).css('width', '95%');
			})
		}
		
		//$('#' + discussionSpaceId + ' input').each(function () {
		//	$(this).prop('checked', false);
		//});
		
		$('#' + sendNewStatementId).off("click").click(function () {
			if ($(this).attr('name').indexOf('start') != -1) {
				sendStartStatement();
			}
		});
		$('#' + sendNewPremiseId).off("click").click(function () {
			if (input.attr('id').indexOf('start_statement') != -1) {
				sendStartStatement();
			} else if (input.attr('id').indexOf('start_premise') != -1) {
				sendStartPremise();
			} else if (input.attr('id').indexOf('justify_premise') != -1) {
				sendArgumentsPremise();
			}
		});
		
		// hide one line options
		var children = spaceList.find('input');
		if (children.length > 0) {
			var id = children.eq(0).attr('id');
			id = id.replace('item_', '');
			var ids = ['start_statement', 'start_premise', 'justify_premise', 'login'];
			
			// if we have just one list element AND the list element has a special function AND we are logged in
			if (children.length == 1 && ($.inArray(id, ids) != -1 && $('#link_popup_login').text().trim().indexOf(_t(login)) == -1)) {
				var container = $('#' + discussionContainerId);
				var sidebar = $('.sidebar-wrapper');
				container.height(container.height() - 50);
				sidebar.height(sidebar.height() - 50);
				children.eq(0).prop('checked', true).parent().hide();
			}
		}
		
		// options for the extra buttons, where the user can add input!
		if (input.length == 0) {
			var el = $('.line-wrapper-l').last().find('span');
			el.hover(function () {
				$(this).css('color', '#000').css('pointer', 'default');
			});
			el.off('click');
		} else {
			if (spaceList.find('li').length == 1 && input.data('url') == 'add'){
				input.prop('checked', true);
			}
			id = input.attr('id').indexOf('item_' == 0) ? input.attr('id').substr('item_'.length) : input.attr('id');
			if ($.inArray(id, ids) != -1) {
				input.attr('onclick', '');
				input.click(function () {
					// new position at start
					if (input.attr('id').indexOf('start_statement') != -1) {
						// guiHandler.showHowToWriteTextPopup();
						guiHandler.showAddPositionContainer();
						$('#' + sendNewStatementId).off("click").click(function () {
							sendStartStatement();
						});
					}
					// new premise for the start
					else if (input.attr('id').indexOf('start_premise') != -1) {
						// guiHandler.showHowToWriteTextPopup();
						guiHandler.showAddPremiseContainer();
						$('#' + sendNewPremiseId).off("click").click(function () {
							sendStartPremise();
						});
					}
					// new premise while judging
					else if (input.attr('id').indexOf('justify_premise') != -1) {
						// guiHandler.showHowToWriteTextPopup();
						guiHandler.showAddPremiseContainer();
						$('#' + sendNewPremiseId).off("click").click(function () {
							sendArgumentsPremise();
						});
					}
					// login
					else if (input.attr('id').indexOf('login') != -1) {
						$('#' + popupLogin).modal('show');
					}
				});
			}
		}
	};
}

/**
 * main function
 */
$(document).ready(function mainDocumentReady() {
	var tacked_sidebar = 'tacked_sidebar';
	var guiHandler = new GuiHandler();
	var ajaxHandler = new AjaxDiscussionHandler();
	var interactionHandler = new InteractionHandler();
	var popupHandler = new PopupHandler();
	var main = new Main();
	var tmp;
	var discussionContainer = $('#' + discussionContainerId);
	
	guiHandler.setHandler(interactionHandler);
	main.setStyleOptions(guiHandler);
	main.setSidebarStyle(discussionContainer, tacked_sidebar);
	main.setSidebarClicks(discussionContainer, tacked_sidebar);
	// sidebar of the graphview is set in GuiHandler:setDisplayStyleAsGraphView()
	main.setClickFunctions(guiHandler, popupHandler, ajaxHandler);
	main.setKeyUpFunctions(guiHandler, ajaxHandler);
	main.setWindowOptions();
	main.setGuiOptions();
	main.setInputExtraOptions(guiHandler, interactionHandler);

	// displayBubbleInformationDialog();

	// some extras
	// get restart url and cut the quotes
	tmp = $('#discussion-restart-btn').attr('onclick').substr('location.href='.length);
	tmp = tmp.substr(1, tmp.length - 2);
	$('#' + discussionEndRestart).attr('href', tmp);
	$('#' + discussionEndReview).attr('href', mainpage + 'review');

	//
	tmp = window.location.href.split('?');
	if (tmp[0].indexOf('/reaction/') != -1){
		$('#island-view-undermine-button').attr('onclick', $('#item_undermine').attr('onclick'));
		$('#island-view-support-button').attr('onclick', $('#item_support').attr('onclick'));
		$('#island-view-undercut-button').attr('onclick', $('#item_undercut').attr('onclick'));
		$('#island-view-rebut-button').attr('onclick', $('#item_rebut').attr('onclick'));
	}
	
	// check anchors
	// console.log('read hash: ' + location.hash);
	if (location.hash.indexOf('graph') != -1){
		guiHandler.setDisplayStyleAsGraphView();
	}
	if (location.hash.indexOf('island') != -1){
		guiHandler.setDisplayStyleAsIsland();
	}
	if (location.hash.indexOf('barometer') != -1){
		new DiscussionBarometer().showBarometer();
	}
	if (location.hash.indexOf('sharing') != -1){
		new PopupHandler().showUrlSharingPopup();
	}
	if (location.hash.indexOf('access-review') != -1 || $('#review-link').attr('data-broke-limit') == 'true'){
		var link = '<a href="' + mainpage + 'review">'  + _t(youAreAbleToReviewNow) + '</a>';
		setGlobalInfoHandler('Hey!', link)
	}

	$(document).delegate('.open', 'click', function(event){
		$(this).addClass('opened');
		event.stopPropagation();
	});
	$(document).delegate('body', 'click', function() {
		$('.open').removeClass('opened');
	});
	$(document).delegate('.cls', 'click', function(event){
		$('.open').removeClass('opened');
		event.stopPropagation();
	});
});