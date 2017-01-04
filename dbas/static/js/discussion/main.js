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
			let elements = [];
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
			let input_field = $('#' + popupUrlSharingInputId);
			
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
			let val = $('#' + popupUrlSharingInputId).val();
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
					const href = $(this).attr('href');
					let text = _t(switchDiscussionText).replace('XXX', $(this).attr('data-value'));
					$(this).attr('href', '#');
					displayConfirmationDialogWithCheckbox(_t(switchDiscussion), text, _t.keepSetting, href, true);
				});
			}
		});
		$('#' + issueDropdownListID + ' .disabled a').off('click').unbind('click').removeAttr('href');
		
		// get infos about the author
		//$('[id^="' + questionBubbleId + '-"').click(function () {
		let trianglel = $('.triangle-l');
		trianglel.find('.triangle-content :not(a)').click(function () {
			if ($(this).closest('p').attr('id').indexOf(questionBubbleId) != -1) {
				let uid = $(this).closest('p').attr('id').replace(questionBubbleId + '-', '');
				ajaxHandler.getMoreInfosAboutArgument(uid, true);
			}
		});
		
		trianglel.find('.triangle-flag').click(function () {
			let uid = $(this).parent().attr('id').replace(questionBubbleId + '-', '');
			popupHandler.showFlagArgumentPopup(uid);
		});
		
		trianglel.find('.triangle-reference').click(function () {
			let uid = $(this).parent().attr('id').replace(questionBubbleId + '-', '');
			new AjaxReferenceHandler().getReferences(uid, true);
		});
		
		trianglel.find('.triangle-trash').click(function () {
			let uid = $(this).parent().attr('id').replace(questionBubbleId + '-', '');
			popupHandler.showDeleteContentPopup(uid, true);
		});
		
		let list = $('#' + discussionSpaceListId);
		list.find('.item-flag').click(function () {
			let uid = $(this).parent().find('input').attr('id').replace('item_', '');
			$('#popup-flag-statement-text').text($(this).parent().find('label').text());
			popupHandler.showFlagStatementPopup(uid, false);
		});
		
		list.find('.item-edit').click(function () {
			let uids = [];
			$(this).parent().find('label:nth-child(even)').each(function(){
				uids.push($(this).attr('id'))
			});
			popupHandler.showEditStatementsPopup(uids);
		});
		
		list.find('.item-trash').click(function () {
			let uid = $(this).parent().find('label').attr('id');
			popupHandler.showDeleteContentPopup(uid, false);
		});
		
		list.find('.item-reference').click(function () {
			let uids = [];
			$(this).parent().find('label:nth-child(even)').each(function(){
				uids.push($(this).attr('id'))
			});
			new AjaxReferenceHandler().getReferences(uids, false);
		});
		
		// adding issues
		$('#' + addTopicButtonId).click(function () {
			popupHandler.showAddTopicPopup(new InteractionHandler().callbackIfDoneForSendNewIssue);
		});
		
		// user info click
		$('.triangle-r-info').each(function () {
			if ($(this).data('votecount') > 0) {
				$(this).click(function () {
					const data_type = $(this).data('type');
					const data_argument_uid = $(this).data('argument-uid');
					const data_statement_uid = $(this).data('statement-uid');
					const data_is_supportive = $(this).data('is-supportive');
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
			let hide_btn = $('#' + discussionSpaceHideItems);
			let space = $('#' + discussionSpaceListId);
			hide_btn.show();
			// send request if it was not send until now
			if ($(this).attr('data-send-request') !== 'true'){
				let uids = [];
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
			let container = $('#' + discussionContainerId);
			let add_height = space.find('li.cropped').length * space.find('li:visible:first').outerHeight() + hide_btn.outerHeight();
			let container_height = parseInt(container.css('max-height').replace('px',''));
			container.css('max-height', (add_height + container_height) + 'px');
			container.attr('data-add-height', add_height);
			
			let sidebar = $('.sidebar-wrapper:first');
			sidebar.height(sidebar.height() + add_height);
				
		});
		
		$('#' + discussionSpaceHideItems).click(function(){
			$(this).hide();
			$('#' + discussionSpaceShowItems).show();
			$('#' + discussionSpaceListId).find('li.cropped').fadeOut();
			let container = $('#' + discussionContainerId);
			let height = parseInt(container.css('max-height').replace('px',''));
			let new_height = height - parseInt(container.attr('data-add-height'));
			// guification, resize main container and sidebar
			setTimeout(function() {
				container.css('max-height', new_height + 'px');
				let sidebar = $('.sidebar-wrapper:first');
				sidebar.height(sidebar.height() - parseInt(container.attr('data-add-height')));
			}, 400);
		});
	};
	
	/**
	 * Sets click functions for the elements in the sidebar
	 * @param maincontainer - main container which contains the content on the left and the sidebar on the rigt
	 * @param localStorageId - id of the parameter in the local storage
	 */
	this.setSidebarClicks = function (maincontainer, localStorageId) {
		let gui = new GuiHandler();
		let sidebarwrapper = maincontainer.find('.' + sidebarWrapperClass);
		let wrapper = maincontainer.find('.' + contentWrapperClass);
		let hamburger = sidebarwrapper.find('.' + hamburgerIconClass);
		let tackwrapper = sidebarwrapper.find('.' + sidebarTackWrapperClass);
		let tack = sidebarwrapper.find('.' + sidebarTackClass);
		let sidebar = sidebarwrapper.find('.' + sidebarClass);
		
		$(hamburger).click(function () {
			$(this).toggleClass('open');
			let width = wrapper.width();
			let bg_color = $('#' + discussionBubbleSpaceId).css('background-color');
			
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
			let shouldShowSidebar = getLocalStorage(localStorageId) == 'true';
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
		let shouldShowSidebar = getLocalStorage(localStorageId) == 'true';
		let sidebarwrapper = maincontainer.find('.' + sidebarWrapperClass);
		let wrapper = maincontainer.find('.' + contentWrapperClass);
		let tackwrapper = sidebarwrapper.find('.' + sidebarTackWrapperClass);
		let tack = sidebarwrapper.find('.' + sidebarTackClass);
		let sidebar = sidebarwrapper.find('.' + sidebarClass);
		let gui = new GuiHandler();
		
		if (shouldShowSidebar) {
			let width = wrapper.width();
			let hamburger = sidebarwrapper.find('.' + hamburgerIconClass);
			
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
				let escapedText = escapeHtml($('#' + addStatementContainerMainInputId).val());
				if ($('#' + discussionBubbleSpaceId).find('p:last-child').text().indexOf(_t(initialPositionInterest)) != -1) {
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
				let escapedText = escapeHtml($('#' + addPremiseContainerMainInputId).val());
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
		// let restart, issues, restartWidth, issueWidth;
		// restart = $('#discussion-restart-btn');
		// issues = $('#' + issueDropdownButtonID);
		// restartWidth = restart.outerWidth();
		// issueWidth = issues.outerWidth();
		// restart.attr('style', restartWidth<issueWidth ? 'width: ' + issueWidth + 'px;' : '');
		// issues.attr('style', restartWidth>issueWidth ? 'width: ' + restartWidth + 'px;' : '');
		
		// focus text of input elements
		// $('input[type='text']'').on("click", function () {
		$('#' + popupUrlSharingInputId).on("click", function () {
			$(this).select();
		});
		
		// hover effects on text elements
		let data = 'data-argumentation-type';
		let list = $('#' + discussionSpaceListId);
		list.find('span[' + data + '!=""]').each(function () {
			let attr = $(this).attr(data);
			let tmp = $('<span>').addClass(attr + '-highlighter');
			tmp.appendTo(document.body);
			let old_color = $(this).css('color');
			let new_color = tmp.css('color');
			tmp.remove();
			$(this).hover(
				function () {
					$('#dialog-speech-bubbles-space').find('span[' + data + '="' + attr + '"]')
						.css('color', new_color)
						.css('background-color', '#edf3e6')
						.css('border-radius', '2px');
				}, function () {
					$('#dialog-speech-bubbles-space').find('span[' + data + '="' + attr + '"]')
						.css('color', old_color)
						.css('background-color', '')
						.css('border-radius', '0');
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
	 *
	 */
	this.setWindowOptions = function () {
		// ajax loading animation
		$(document).on({
			ajaxStart: function ajaxStartFct() {
				setTimeout("$('body').addClass('loading')", 0);
			},
			ajaxStop: function ajaxStopFct() {
				setTimeout("$('body').removeClass('loading')", 0);
			}
		});
		
		// some hack
		$('#navbar-left').empty();
		
		//$(window).load(function windowLoad() {
		//});
		
		let container = $('#' + discussionContainerId);
		let oldContainerSize = container.width();
		let burger = $('.hamburger');
		let wrapper = $('#dialog-wrapper');
		
		$(window).resize(function () {
			new GuiHandler().setMaxHeightForBubbleSpace();
			
			// resize main container
			let difference = oldContainerSize - container.width();
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
			let login_item = $('#' + discussionSpaceListId).find('#item_login');
			if (login_item.length > 0)
				login_item.prop('checked', false)
		}).on('shown.bs.modal', function () {
			$('#' + loginUserId).focus();
		});
		
		// highlight edited statement
		let pos = window.location.href.indexOf('edited_statement=');
		if (pos != -1) {
			let ids = window.location.href.substr(pos + 'edited_statement='.length);
			let splitted = ids.split(',');
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
		let spaceList = $('#' + discussionSpaceListId);
		let input = spaceList.find('li:last-child input');
		let text = [], splits, conclusion, supportive, arg, relation;
		splits = window.location.href.split('?');
		splits = splits[0].split('/');
		const sendStartStatement = function () {
			text = $('#' + addStatementContainerMainInputId).val();
			interactionHandler.sendStatement(text, '', '', '', '', fuzzy_start_statement);
		};
		const sendStartPremise = function () {
			conclusion = splits[splits.length - 2];
			supportive = splits[splits.length - 1] == 't';
			text = [];
			$('#' + addPremiseContainerBodyId + ' input').each(function () {
				if ($(this).val().length > 0)
					text.push($(this).val());
			});
			interactionHandler.sendStatement(text, conclusion, supportive, '', '', fuzzy_start_premise);
		};
		const sendArgumentsPremise = function () {
			text = [];
			$('#' + addPremiseContainerBodyId + ' input').each(function () {
				if ($(this).val().length > 0)
					text.push($(this).val());
			});
			let add = window.location.href.indexOf('support') != -1 ? 1 : 0;
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
		let children = spaceList.find('input');
		let id = children.eq(0).attr('id');
		let ids = ['start_statement', 'start_premise', 'justify_premise', 'login'];
		// if we have just one list element AND the list element has a special function AND we are logged in
		if (children.length == 1 && ($.inArray(id, ids) != -1 && $('#link_popup_login').text().trim().indexOf(_t(login)) == -1)) {
			children.eq(0).prop('checked', true).parent().hide();
		}
		
		// options for the extra buttons, where the user can add input!
		
		if (input.length == 0) {
			let el = $('.line-wrapper-l').last().find('span');
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
	let tacked_sidebar = 'tacked_sidebar';
	let guiHandler = new GuiHandler();
	let ajaxHandler = new AjaxDiscussionHandler();
	let interactionHandler = new InteractionHandler();
	let popupHandler = new PopupHandler();
	let main = new Main();
	let tmp;
	let discussionContainer = $('#' + discussionContainerId);
	
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
	if (location.hash.indexOf('access-review') != -1 || $('#review-link').attr('data-broke-limit') == 'true'){
		const link = '<a href="' + mainpage + 'review">'  + _t(youAreAbleToReviewNow) + '</a>';
		setGlobalInfoHandler('Hey!', link)
	}

	$(document).delegate('.open', 'click', function(event){
		$(this).addClass('opened');
		event.stopPropagation();
	});
	$(document).delegate('body', 'click', function(event) {
		$('.open').removeClass('opened');
	});
	$(document).delegate('.cls', 'click', function(event){
		$('.open').removeClass('opened');
		event.stopPropagation();
	});
});