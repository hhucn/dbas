/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */
'use strict';


function Main () {
	var tacked_sidebar = 'tacked_sidebar';

	/**
	 * Sets all click functions
	 * @param guiHandler
	 * @param ajaxHandler
	 */
	this.setClickFunctions = function (guiHandler, ajaxHandler) {
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
			$('#' + discussionSpaceId + ' li:last-child input').attr('checked', false).prop('checked', false).enable = true;
		});

		// hides container
		$('#' + closePremiseContainerId).click(function closeStatementContainerId() {
			$('#' + addPremiseContainerId).hide();
			$('#' + addPremiseErrorContainer).hide();
			$('#' + discussionSpaceId + ' li:last-child input').attr('checked', false).prop('checked', false).enable = true;
		});

		// hiding the island view, when the X button is clicked
		$('#' + closeIslandViewContainerId).click(function () {
			guiHandler.resetChangeDisplayStyleBox();
			$('#li_' + addReasonButtonId).attr('checked', true).prop('checked', true);
		});

		// hiding the island view, when the X button is clicked
		$('#' + closeGraphViewContainerId).click(function () {
			guiHandler.resetChangeDisplayStyleBox();
		});

		// open edit statement
		$('#' + editStatementButtonId).click(function () {
			guiHandler.showEditStatementsPopup();
		});

		// close popups
		$('#' + popupEditStatementCloseButtonXId).click(function popupEditStatementCloseButtonXId() {
			guiHandler.hideandClearEditStatementsPopup();
		});
		$('#' + popupEditStatementCloseButtonId).click(function popupEditStatementCloseButtonId() {
			guiHandler.hideandClearEditStatementsPopup();
		});
		$('#' + popupUrlSharingCloseButtonXId).click(function popupUrlSharingCloseButtonXId() {
			guiHandler.hideAndClearUrlSharingPopup();
		});
		$('#' + popupUrlSharingCloseButtonId).click(function popupUrlSharingCloseButtonId() {
			guiHandler.hideAndClearUrlSharingPopup();
		});

		// share url for argument blogging
		$('#' + shareUrlId).click(function shareurlClick() {
			guiHandler.showUrlSharingPopup();
		});

		/**
		 * Switch between shortened and long url
		 */
		$('#' + popupUrlSharingLongUrlButtonID).click(function () {
			var input_field = $('#' + popupUrlSharingInputId);

			if ($(this).attr('data-is-short-url') == '0') {
				input_field.val(input_field.attr('data-short-url'));
				$(this).attr('data-is-short-url', '1').text(_t_discussion(fetchLongUrl));
			} else {
				input_field.val(window.location);
				$(this).attr('data-is-short-url', '0').text(_t_discussion(fetchShortUrl));
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

		guiHandler.setDisplayStyleAsDiscussion();
		$('#' + displayStyleIconGuidedId).click(function displayStyleIconGuidedFct() {
			guiHandler.setDisplayStyleAsDiscussion();
		});
		$('#' + displayStyleIconIslandId).click(function displayStyleIconIslandFct() {
			guiHandler.setDisplayStyleAsIsland();
		});
		$('#' + displayStyleIconExpertId).click(function displayStyleIconExpertFct() {
			guiHandler.setDisplayStyleAsGraphView();
		});

		/**
		 * Handling report button
		 */
		$('#' + reportButtonId).click(function reportFunction() {
			// jump to contact tab
			var line1 = 'Report ' + new Helper().getTodayAsDate(),
				line2 = 'URL: ' + window.location.href,
				line3 = _t(fillLine).toUpperCase(),
				params = {
					'content': line1 + '\n' + line2 + '\n' + line3,
					'name': $('#header_user').parent().text().replace(/\s/g, '')
				};

			new Helper().redirectInNewTabForContact(params);

		});

		// opinion barometer
		$('#' + opinionBarometerImageId).show().click(function opinionBarometerFunction() {
			new DiscussionBarometer().showBarometer()
		});

		// issues
		$('#' + issueDropdownListID + ' .enabled').each(function () {
			if ($(this).children().length > 0) {
				$(this).children().click(function () {
					var href = $(this).attr('href'),
						text = _t(switchDiscussionText1) + ' <strong>' + $(this).attr('value') + '</strong> ';
					text += _t(switchDiscussionText2);
					text += '<br><br>';
					text += _t(switchDiscussionText3);
					$(this).attr('href', '#');
					displayConfirmationDialogWithCheckbox(_t(switchDiscussion), text, _t.keepSetting, href, true);
				});
			}
		});
		$('#' + issueDropdownListID + ' .disabled a').off('click').unbind('click');

		// get infos about the author
		//$('[id^="' + questionBubbleId + '-"').click(function () {
		$('.triangle-l').click(function () {
			if ($(this).attr('id').indexOf(questionBubbleId) != -1){
				var uid = $(this).attr('id').replace(questionBubbleId + '-', '');
				ajaxHandler.getMoreInfosAboutArgument(uid, true);
			}
		});

		// adding issues
		$('#' + addTopicButtonId).click(function () {
			guiHandler.showAddTopicPopup(new InteractionHandler().callbackIfDoneForSendNewIssue);
		});

		// user info click
		$('.triangle-r-info').each(function () {
			if ($(this).attr('data-votecount') > 0) {
				$(this).click(function () {
					var data_type = $(this).attr('data-type'),
						data_argument_uid = $(this).attr('data-argument-uid'),
						data_statement_uid = $(this).attr('data-statement-uid'),
						data_is_supportive = $(this).attr('data-is-supportive');
					new AjaxDiscussionHandler().getMoreInfosAboutOpinion(data_type, data_argument_uid, data_statement_uid, data_is_supportive);
				});
			} else {
				$(this).removeClass('triangle-r-info').addClass('triangle-r-info-nohover');
			}
		});

		$('#' + contactSubmitButtonId).click(function(){
			setTimeout("$('body').addClass('loading')", 0);
		});

		// sliding menu
		$('#' + sidebarHamburgerIconId).click(function(){
			$(this).toggleClass('open');
			var wrapper = $('#dialog-wrapper');
			var width = wrapper.width();
			var sidebar = $('#discussion-icon-sidebar');
			var hamburger = $('#' + sidebarHamburgerIconId);
			var sidebarw = $('#sidebar-wrapper');
			var discussion = $('#' + discussionContainerId);
			var tack = $('#' + sidebarTackWrapperId);

			if (sidebar.is(':visible')) {
				tack.fadeOut();
				sidebar.toggle('slide');
				hamburger.css('margin-right', '0.5em')
					.css('background-color', '');
				discussion.css('max-height', '');
				sidebarw.css('background-color', '')
					.css('height', '');
				new Helper().delay(function(){
					wrapper.width(width + sidebar.outerWidth());
				}, 300);
			} else {
				wrapper.width(width - sidebar.outerWidth());
				discussion.css('max-height', discussion.outerHeight() + 'px');
				new Helper().delay(function(){
					sidebar.toggle('slide');
					hamburger.css('margin-right', (sidebarw.width() - hamburger.width())/2 + 'px')
						.css('margin-left', 'auto')
						.css('background-color', sidebar.css('background-color'));
					sidebarw.css('background-color', $('#' + discussionBubbleSpaceId).css('background-color'))
						.css('height', discussion.outerHeight() + 'px');
					tack.fadeIn();
				}, 200);
			}
		});

		// action for tacking the sidebar
		$('#' + sidebarTackWrapperId).click(function() {
			if (localStorage.getItem(tacked_sidebar) == 'true') {
				new Main().rotateTack('0');
				localStorage.setItem(tacked_sidebar, 'false');
				$(this).attr('data-original-title', _t_discussion(pinNavigation));

				// hide sidebar if it is visible
				if ($('#discussion-icon-sidebar').is(':visible')) {
					$('#' + sidebarHamburgerIconId).click();
				}
			} else {
				new Main().rotateTack('90');
				localStorage.setItem(tacked_sidebar, 'true');
				$(this).attr('data-original-title', _t_discussion(unpinNavigation));
			}
		});
	};

	/**
	 * Sets all keyUp functions
	 * @param guiHandler
	 * @param ajaxHandler
	 */
	this.setKeyUpFunctions = function (guiHandler, ajaxHandler) {
		// gui for the fuzzy search (statements)
		$('#' + addStatementContainerMainInputId).keyup(function () {
			new Helper().delay(function () {
				var escapedText = new Helper().escapeHtml($('#' + addStatementContainerMainInputId).val());
				if ($('#' + discussionBubbleSpaceId).find('p:last-child').text().indexOf(_t(initialPositionInterest)) != -1) {
					// here we have our start statement
					ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputId, fuzzy_start_statement, '');
				} else {
					// some trick: here we have a premise for our start statement
					ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputId, fuzzy_start_premise, '');
				}
			}, 200);
			setTextWatcherForMaxLength($(this));
		}).focusin(function () {
			setTextWatcherForMaxLength($(this));
		});

		// gui for the fuzzy search (premises)
		$('#' + addPremiseContainerMainInputId).keyup(function () {
			new Helper().delay(function () {
				var escapedText = new Helper().escapeHtml($('#' + addPremiseContainerMainInputId).val());
				ajaxHandler.fuzzySearch(escapedText, addPremiseContainerMainInputId, fuzzy_add_reason, '');
			}, 200);
			setTextWatcherForMaxLength($(this));
		}).focusin(function () {
			setTextWatcherForMaxLength($(this));
		});

		// gui for editing statements
		$('#' + popupEditStatementTextareaId).keyup(function popupEditStatementTextareaKeyUp() {
			new Helper().delay(function () {
				ajaxHandler.fuzzySearch($('#' + popupEditStatementTextareaId).val(),
					popupEditStatementTextareaId,
					fuzzy_statement_popup,
					$('#' + popupEditStatementContentId + ' .text-hover').attr('id').substr(3));
				$('#' + popupEditStatementWarning).hide();
				$('#' + popupEditStatementWarningMessage).text('');
			}, 200);
			setTextWatcherForMaxLength($(this));
		}).focusin(function () {
			setTextWatcherForMaxLength($(this));
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

		// focus text of input elements
		// $('input[type='text']'').on("click", function () {
		$('#' + popupUrlSharingInputId).on("click", function () {
			$(this).select();
		});

		new Main().setNavigationSidebar(window.innerWidth);

		// remove html chars  // TODO #122
		$('#discussion-space-answer-buttons').find('a').each(function(){
			var title = $(this).attr('title');
			var href = $(this).attr('href');
			while (title.indexOf('<strong>') != -1)
				title = title.replace('<strong>', '');
			while (title.indexOf('</strong>') != -1)
				title = title.replace('</strong>', '');
			$(this).attr('title', title);
			$(this).attr('href', href.replace('location.href="', '').replace('"', ''));
		});

		// read local storage for pinning the bar / set title
		if (localStorage.getItem(tacked_sidebar) == 'true') {
			var wrapperAndBurger = $('#dialog-wrapper, #hamburger');
			var wrapper = $('#dialog-wrapper');
			var width = wrapper.width();
			var sidebar = $('#discussion-icon-sidebar');
			var hamburger = $('#' + sidebarHamburgerIconId);
			var sidebarw = $('#sidebar-wrapper');
			var discussion = $('#' + discussionContainerId);
			var tack = $('#' + sidebarTackWrapperId);
			var main = new Main();

			main.rotateTack('90');
			main.setAnimationSpeed(wrapperAndBurger, '0.0');

			hamburger.addClass('open');

			wrapper.width(width - sidebar.outerWidth());
			discussion.css('max-height', discussion.outerHeight() + 'px');
			sidebar.show();
			hamburger.css('margin-right', (sidebarw.width() - hamburger.width())/2 + 'px')
				.css('margin-left', 'auto')
				.css('background-color', sidebar.css('background-color'));
			sidebarw.css('background-color', $('#' + discussionBubbleSpaceId).css('background-color'))
				.css('height', discussion.outerHeight() + 'px');
			tack.fadeIn();

			main.setAnimationSpeed(wrapperAndBurger, '0.5');

			tack.attr('data-original-title', _t_discussion(unpinNavigation));
		} else {
			$('#' + sidebarTackWrapperId).attr('data-original-title', _t_discussion(pinNavigation));
		}

		// hover effects on text elements
		var data = 'data-argumentation-type';
		$('#' + discussionSpaceListId).find('span[' + data + '!=""]').each(function(){
			var attr = $(this).attr(data);
			$(this).hover(
				function(){
					$('#dialog-speech-bubbles-space').find('span[' + data + '="' + attr + '"]')
						.css('background-color', '#ffe0b2')
						.css('font-weight', '500')
						.css('border-radius', '5px 5px 5px 5px');
				}, function(){
					$('#dialog-speech-bubbles-space').find('span[' + data + '="' + attr + '"]')
						.css('background-color', '')
						.css('font-weight', '400')
						.css('font-size', '14px')
						.css('letter-spacing', '0px')
						.css('border-radius', '0 0 0 0');
				}
			);
		});
	};

	/**
	 * Roates the little pin icon in the sidebar
	 * @param degree
	 */
	this.rotateTack = function(degree){
		$('#' + sidebarTackId).css('-ms-transform', 'rotate(' + degree + 'deg)')
			.css('-webkit-transform', 'rotate(' + degree + 'deg)')
			.css('transform', 'rotate(' + degree + 'deg)');
	};

	/**
	 * Sets an animation speed for a specific element
	 * @param element
	 * @param speed
	 */
	this.setAnimationSpeed = function(element, speed){
		element.css('-webkit-transition', 'all ' + speed + 's ease')
			.css('-moz-transition', 'all ' + speed + 's ease')
			.css('-o-transition', 'all ' + speed + 's ease')
			.css('transition', 'all ' + speed + 's ease');
	};

	/**
	 * Resizes the sidebar, whether bootstrap collapsed or not
	 * @param windowInnerWidth
	 */
	this.setNavigationSidebar = function (windowInnerWidth) {
		if (windowInnerWidth < 992) {
			$('#discussion-sidebar').addClass('list-inline').css('text-align', 'left');
			$('#site-navigation').addClass('list-inline').css('text-align', 'left').find('img').each(function () {
				$(this).attr('data-placement', 'bottom');
			});
		} else {
			$('#discussion-sidebar').removeClass('list-inline').css('text-align', 'right');
			$('#site-navigation').removeClass('list-inline').css('text-align', 'right').find('img').each(function () {
				$(this).attr('data-placement', 'left');
			});
		}
		$('#' + sidebarMoreButtonId).attr('data-placement', windowInnerWidth < 992 ? 'top' : 'left');
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

		$(window).load(function windowLoad() {
		});

		$(window).resize(function () {
			new Main().setNavigationSidebar(window.innerWidth);
			new GuiHandler().setMaxHeightForBubbleSpace();
		});
	};

	/**
	 *
	 */
	this.setGuiOptions = function () {
		// set do not hide on hover popup
		var originalLeave = $.fn.popover.Constructor.prototype.leave,
			body = $('body');
		// http://jsfiddle.net/WojtekKruszewski/Zf3m7/22/
		$.fn.popover.Constructor.prototype.leave = function (obj) {
			var self = obj instanceof this.constructor ?
				obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type);
			var container, timeout;

			originalLeave.call(this, obj);

			if (obj.currentTarget) {
				container = $(obj.currentTarget).siblings('.popover');
				timeout = self.timeout;
				container.one('mouseenter', function () {
					//We entered the actual popover – call off the dogs
					clearTimeout(timeout);
					// Let's monitor popover content instead
					container.one('mouseleave', function () {
						$.fn.popover.Constructor.prototype.leave.call(self, self);
					});
				})
			}
		};
		$('#site-navigation').hide();
		body.popover({
			selector: '[data-popover]',
			trigger: 'click hover',
			delay: {show: 50, hide: 50}
		}).on('inserted.bs.popover', function () {
			var element = $('#site-navigation').detach().show();
			$('#discussion-sidebar-style-menu').find('.popover-content').append(element);
		}).on('hide.bs.popover', function () {
			var element = $('#site-navigation').detach().hide();
			$('#discussion-sidebar-style-menu').append(element);
		});

		// relation buttons
		if (false && window.location.href.indexOf('/reaction/') != -1) {
			var cl = 'icon-badge',
				style = 'height: 30px; width:30px; margin-right: 0.5em;',
				src = mainpage + 'static/images/icon_discussion_',
				item_undermine = $('#item_undermine'),
				item_support = $('#item_support'),
				item_undercut = $('#item_undercut'),
				item_overbid = $('#item_overbid'),
				item_rebut = $('#item_rebut'),
				item_no_opinion = $('#item_no_opinion'),
				undermine = $('<img>').addClass(cl).attr({
					'style': style,
					'src': src + 'undermine.png',
					'onclick': item_undermine.attr('onclick')
				}),
				support = $('<img>').addClass(cl).attr({
					'style': style,
					'src': src + 'support.png',
					'onclick': item_support.attr('onclick')
				}),
				undercut = $('<img>').addClass(cl).attr({
					'style': style,
					'src': src + 'undercut.png',
					'onclick': item_undercut.attr('onclick')
				}),
				overbid = $('<img>').addClass(cl).attr({
					'style': style,
					'src': src + 'overbid.png',
					'onclick': item_overbid.attr('onclick')
				}),
				rebut = $('<img>').addClass(cl).attr({
					'style': style,
					'src': src + 'rebut.png',
					'onclick': item_rebut.attr('onclick')
				}),
				no_opinion = $('<img>').addClass(cl).attr({
					'style': style,
					'src': src + 'no_opinion.png',
					'onclick': item_no_opinion.attr('onclick')
				});
			item_undermine.hide().next().prepend(undermine);
			item_support.hide().next().prepend(support);
			item_undercut.hide().next().prepend(undercut);
			item_overbid.hide().next().prepend(overbid);
			item_rebut.hide().next().prepend(rebut);
			item_no_opinion.hide().next().prepend(no_opinion);
		}


		$('#' + popupLogin).on('hidden.bs.modal', function () {// uncheck login button on hide
			var login_item = $('#' + discussionSpaceListId).find('#item_login');
			if (login_item.length > 0)
				login_item.attr('checked', false).prop('checked', false)
		}).on('shown.bs.modal', function () {
			$('#' + loginUserId).focus();
		});
	};

	/**
	 *
	 * @param guiHandler
	 * @param interactionHandler
	 */
	this.setInputExtraOptions = function (guiHandler, interactionHandler) {
		var input = $('#' + discussionSpaceListId).find('li:last-child input'),
			text = [], splits, conclusion, supportive, arg, relation;
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

		$('#' + discussionSpaceId + ' input').each(function () {
			$(this).attr('checked', false).prop('checked', false);
		});

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
		var children = $('#' + discussionSpaceListId).find('input');
		if (children.length == 1 && (
			children.eq(0).attr('id').indexOf('start_statement') != -1 ||
			children.eq(0).attr('id').indexOf('start_premise') != -1 ||
			children.eq(0).attr('id').indexOf('justify_premise') != -1 ||
			(children.eq(0).attr('id').indexOf('login') != -1) && $('#link_popup_login').text().trim().indexOf(_t(login)) == -1)) {
			children.eq(0).attr('checked', true).prop('checked', true).parent().hide();
		}

		// TODO CLEAR DESIGN
		// options for the extra buttons, where the user can add input!
		if (input.attr('id') && (
			input.attr('id').indexOf('start_statement') != -1 ||
			input.attr('id').indexOf('start_premise') != -1 ||
			input.attr('id').indexOf('justify_premise') != -1 ||
			input.attr('id').indexOf('login') != -1)
		) {
			input.attr('onclick', '');
			input.change(function () {
				if (input.prop('checked')) {
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
				}
			});
		}
	};
}

/**
 * main function
 */
$(document).ready(function mainDocumentReady() {
	var guiHandler = new GuiHandler(),
		ajaxHandler = new AjaxDiscussionHandler(),
		interactionHandler = new InteractionHandler(),
		tmp,
		main = new Main();

	guiHandler.setHandler(interactionHandler);
	main.setStyleOptions(guiHandler);
	main.setClickFunctions(guiHandler, ajaxHandler);
	main.setKeyUpFunctions(guiHandler, ajaxHandler);
	main.setWindowOptions();
	main.setGuiOptions();
	main.setInputExtraOptions(guiHandler, interactionHandler);

	// displayBubbleInformationDialog();

	// some extras
	// get restart url and cut the quotes
	tmp = $('#discussion-restart-btn').attr('onclick').substr('location.href='.length);
	tmp = tmp.substr(1, tmp.length-2);
	$('#' + discussionEndRestart).attr('href', tmp);

	//
	tmp = window.location.href.split('?');
	if (tmp[0].indexOf('/reaction/') != -1){
		$('#island-view-undermine-button').attr('onclick', $('#item_undermine').attr('onclick'));
		$('#island-view-support-button').attr('onclick', $('#item_support').attr('onclick'));
		$('#island-view-undercut-button').attr('onclick', $('#item_undercut').attr('onclick'));
		$('#island-view-rebut-button').attr('onclick', $('#item_rebut').attr('onclick'));
	}

	$(document).delegate('.open', 'click', function(event){
		$(this).addClass('oppenned');
		event.stopPropagation();
	});
	$(document).delegate('body', 'click', function(event) {
		$('.open').removeClass('oppenned');
	});
	$(document).delegate('.cls', 'click', function(event){
		$('.open').removeClass('oppenned');
		event.stopPropagation();
	});
});