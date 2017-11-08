/* global $*/

/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function GuiHandler() {
	'use strict';
	
	var maxHeightOfBubbleSpace = 300;
	
	/**
	 * Adds a premise row in the 'add premise'-container
	 */
	this.appendAddPremiseRow = function () {
		var body = $('#' + addPremiseContainerBodyId);
		var send = $('#' + sendNewPremiseId);
		var id = addPremiseContainerMainInputId + '-' + new Date().getTime();
		
		var copy_div = $('.container-three-divs:first').clone();
		copy_div.find('input').attr('id', id).val('');
		copy_div.find('.text-counter-input').remove();
		var img_plus = copy_div.find('.icon-add-premise');
		var img_minus = copy_div.find('.icon-rem-premise');
		body.append(copy_div);
		setTextWatcherInputLength(copy_div.find('input'), false);
		
		img_plus.click(function () {
			new GuiHandler().appendAddPremiseRow();
			$(this).hide().prev().show(); // hide +, show -
			send.val(_t_discussion(saveMyStatements));
		});
		
		body.find('.icon-rem-premise').each(function () {
			$(this).click(function () {
				// removing bubble
				var id = $(this).parent().parent().find('input').attr('id'),
					tmpid = id.split('-').length === 6 ? id.split('-')[5] : '0';
				$('#current_' + tmpid).fadeOut().remove();
				$(this).parent().parent().remove();
				body.find('div').children().last().show();
				// hide minus icon, when there is only one child
				if (body.find('.container-three-divs').length === 1) {
					body.find('.icon-rem-premise').hide();
					send.val(_t_discussion(saveMyStatement));
				} else {
					body.find('.icon-rem-premise').show();
					send.val(_t_discussion(saveMyStatements));
				}
			});
		});
		img_minus.show();
		
		// add fuzzy search
		$('#' + id).keyup(function () {
			setTimeout(function () {
				var escapedText = escapeHtml($('#' + id).val());
				new AjaxDiscussionHandler().fuzzySearch(escapedText, id, fuzzy_add_reason, '');
			}, 200);
		});
	};
	
	/**
	 * Dialog based discussion modi
	 */
	this.setDisplayStyleAsDiscussion = function () {
		// this.setActivityOfImage($('#' + displayStyleIconGuidedId), false);
		// this.setActivityOfImage($('#' + displayStyleIconIslandId), true);
		// this.setActivityOfImage($('#' + displayStyleIconGraphId), true);
		$('#' + islandViewContainerId).hide();
		$('#' + graphViewContainerId).hide();
		$('#' + discussionContainerId).show();
		$('#' + headerContainerId).show();
		clearAnchor();
		
		// check for single input
		var elements = $('#' + discussionSpaceListId).find('li');
		if (elements.length === 1){
			new Main().setInputExtraBox(elements.find('input'), new GuiHandler());
		}
	};
	
	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsIsland = function () {
		// this.setActivityOfImage($('#' + displayStyleIconGuidedId), true);
		// this.setActivityOfImage($('#' + displayStyleIconIslandId), false);
		// this.setActivityOfImage($('#' + displayStyleIconGraphId), true);
		$('#' + islandViewContainerId).fadeIn('slow');
		//$('#' + graphViewContainerId).hide();
		//$('#' + discussionContainerId).hide();
		this.hideAddPositionContainer();
		this.hideAddPremiseContainer();
	};
	
	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsGraphView = function () {
		var graphViewContainer = $('#' + graphViewContainerId);
		var tacked_sidebar = 'tacked_graph_sidebar';
		var header = $('#' + graphViewContainerHeaderId);
		var main = new Main();
		
		// this.setActivityOfImage($('#' + displayStyleIconGuidedId), true);
		// this.setActivityOfImage($('#' + displayStyleIconIslandId), true);
		// this.setActivityOfImage($('#' + displayStyleIconGraphId), false);
		$('#' + islandViewContainerId).hide();
		$('#' + discussionContainerId).hide();
		$('#' + headerContainerId).hide();
		$('#' + addPremiseContainerId).hide();
		
		// text
		header.html($('#issue_info').data('title'));
		
		// height
		var innerHeight = this.getMaxSizeOfGraphViewContainer();
		graphViewContainer.attr('style', 'height: ' + innerHeight + 'px; margin-left: 2em; margin-right: 2em; margin-bottom: 1em;');
		innerHeight -= header.outerHeight(true) + 20;
		$('#' + graphViewContainerSpaceId).attr('style', 'height: ' + innerHeight + 'px; margin-left: 0.5em; margin-right: 0.5em; width: 95%');
		new DiscussionGraph({}, false).showGraph(false);
		main.setSidebarStyle(graphViewContainer, tacked_sidebar);
		main.setSidebarClicks(graphViewContainer, tacked_sidebar);
		// this.hideAddPositionContainer();
		// this.hideAddPremiseContainer();
	};
	
	/**
	 *
	 * @param resize
	 */
	this.setMaxHeightForDiscussionContainer = function(resize){
		var maincontainer = $('#' + discussionContainerId);
		if ($('#dialog-wrapper').height() > maincontainer.outerHeight()) {
			var sidebarwrapper = maincontainer.find('.' + sidebarWrapperClass);
			maincontainer.css({'height': maincontainer.outerHeight(true) + resize + 'px',
				'max-height': maincontainer.outerHeight(true) + resize + 'px'
			});
			sidebarwrapper.css('height', maincontainer.outerHeight() + 'px');
		}
	};
	
	/**
	 * Sets the maximal height for the bubble space. If needed, a scrollbar will be displayed.
	 */
	this.setMaxHeightForBubbleSpace = function () {
		// max size of the container
		var speechBubbles = $('#' + discussionBubbleSpaceId);
		var height = 0;
		var maxHeight = this.getMaxSizeOfDiscussionViewContainer();
		var start;
		var nowBubble = speechBubbles.find('*[id*=now]');
		var oldSize = speechBubbles.height();
		$.each(speechBubbles.find('div p'), function () {
			height += $(this).outerHeight(true);
			// clear unnecessary a tags
			if ($(this).parent().attr('href') === '?breadcrumb=true') {
				$(this).insertAfter($(this).parent());
				$(this).prev().remove();
			}
		});
		
		start = nowBubble.length === 0 ? 'bottom' : nowBubble;
		// scroll to now bubble on mobile devices and do not enable slimscroll
		if (isMobileAgent()){
			if (nowBubble.length !== 0) {
				$('html, body').animate({scrollTop: nowBubble.offset().top - 75}, 500);
			}
			speechBubbles.css({'background': '#fff'});
			return;
		}
		if (height > maxHeight && maxHeight > 0) {
			if (maxHeight < maxHeightOfBubbleSpace) {
				maxHeight = maxHeightOfBubbleSpace;
			}
			speechBubbles.slimscroll({
				position: 'right',
				height: maxHeight + 'px',
				railVisible: true,
				alwaysVisible: true,
				start: start,
				scrollBy: '10px',
				allowPageScroll: true
			});
		} else {
			height += 60;
			if (height < 50) {
				speechBubbles.css('min-height', '100px');
			} else {
				speechBubbles.css('height', height + 'px').css('min-height', '200px');
			}
			speechBubbles.css('min-height', '100px').css('max-height', maxHeight + 'px');
		}
		return speechBubbles.height() - oldSize;
	};
	
	/**
	 * Shows the 'add position'-container
	 */
	this.showAddPositionContainer = function () {
		$('#' + addStatementContainerId).show();
	};
	
	/**
	 * Shows the 'add premise'-container
	 */
	this.showAddPremiseContainer = function () {
		$('#' + addPremiseContainerId).show();
	};
	
	/**
	 * Hides the 'add position'-container
	 */
	this.hideAddPositionContainer = function () {
		$('#' + addStatementContainerId).hide();
		$('#' + discussionSpaceListId).find('li:last-child input').prop('checked', false);
	};
	
	/**
	 * Hides the 'add premise'-container
	 */
	this.hideAddPremiseContainer = function () {
		$('#' + addPremiseContainerId).hide();
		$('#' + discussionSpaceListId).find('li:last-child input').prop('checked', false);
	};
	
	/**
	 *
	 * @param data with the keywords: firstname, lastname, nickname, gender, email, password, ui_locales
	 */
	this.showCompleteLoginPopup = function(data){
		// default
		$('#popup-complete-login-inlineRadioGender1').prop('checked', true);
		var mappings = {
			'firstname': '#popup-complete-login-userfirstname-input',
			'lastname': '#popup-complete-login-userlastname-input',
			'nickname': '#popup-complete-login-nick-input',
			'email': '#popup-complete-login-email-input',
			'password1': '#popup-complete-login-password-input',
			'password2': '#popup-complete-login-passwordconfirm-input'
		};
		$.each(mappings, function( key, value ) {
			console.log(key + ' ' + (key in data.missing) + ' ' + (!(key in data.user)));
			if (key in data.missing || !(key in data.user)) {
				$(value).parent().addClass('has-warning');
			}
		});
		
		// check values
		if ('firstname' in data.user){
			$('#popup-complete-login-userfirstname-input').val(data.user.firstname).prop('disabled', true);
		}
		if ('lastname' in data.user){
			$('#popup-complete-login-userlastname-input').val(data.user.lastname).prop('disabled', true);
		}
		if ('nickname' in data.user){
			$('#popup-complete-login-nick-input').val(data.user.nickname).prop('disabled', true);
		}
		if ('gender' in data.user) {
			if (data.user.gender === 'f') {
				$('#popup-complete-login-inlineRadioGender2').prop('checked', true).prop('disabled', true);
				$('#popup-complete-login-inlineRadioGender1').prop('disabled', true);
				$('#popup-complete-login-inlineRadioGender3').prop('disabled', true);
			} else  if (data.user.gender === 'm') {
				$('#popup-complete-login-inlineRadioGender3').prop('checked', true).prop('disabled', true);
				$('#popup-complete-login-inlineRadioGender1').prop('disabled', true);
				$('#popup-complete-login-inlineRadioGender2').prop('disabled', true);
			} else {
				$('#popup-complete-login-inlineRadioGender1').prop('checked', true).prop('disabled', true);
				$('#popup-complete-login-inlineRadioGender2').prop('disabled', true);
				$('#popup-complete-login-inlineRadioGender3').prop('disabled', true);
			}
		}
		if ('email' in data.user){
			$('#popup-complete-email-input').value(data.user.email).prop('disabled', true);
		}
		
		$('#popup-complete-login-close-button').click(function(){
			$('#popup-complete-login').modal('hide');
		});
		
		$('#popup-complete-login-register-button').off('click').click(function(){
			alert('Todo: register');
		});
		
		$('#popup-complete-login').modal('show');
	};
	
	/**
	 * Shows a modal where the user has to choose how the premisegroups should be treated
	 *
	 * @param undecided_texts, array of strings
	 * @param decided_texts, array of strings
	 * @param supportive, boolean
	 * @param type, fuzzy_add_reason (adding an arguments reason) or fuzzy_start_premise for adding a positions premise
	 * @param arg, current argument id, if the type is fuzzy_add_reason
	 * @param relation, current relation as string, if the type is fuzzy_add_reason
	 * @param conclusion, current conclusion uid, if the type is fuzzy_start_premise
	 */
	this.showSetStatementContainer = function (undecided_texts, decided_texts, supportive, type, arg, relation, conclusion) {
		var gh = new GuiHandler(), page, page_no;
		var body = $('#' + popupSetPremiseGroupsBodyContent).empty();
		var prev = $('#' + popupSetPremiseGroupsPreviousButton).hide();
		var next = $('#' + popupSetPremiseGroupsNextButton).hide();
		var send = $('#' + popupSetPremiseGroupsSendButton).addClass('disabled');
		var counter = $('#' + popupSetPremiseGroupsCounter).hide();
		var prefix = 'insert_statements_page_';
		var popup = $('#' + popupSetPremiseGroups);
		var warning = $('#' + popupSetPremiseGroupsWarningText).hide();
		
		send.click(function sendClick() {
			var selections = body.find('input:checked'), i, j, splitted;
			
			// merge every text part to one array
			for (i = 0; i < undecided_texts.length; i++) {
				splitted = undecided_texts[i].split(' ' + _t_discussion(and) + ' ');
				
				if (selections[i].id.indexOf(attr_more_args) !== -1) { // each splitted text part is one argument
					for (j = 0; j < splitted.length; j++) {
						decided_texts.push([splitted[j]]);
					}
					
				} else if (selections[i].id.indexOf(attr_one_arg) !== -1) { // one argument with big premise group
					decided_texts.push(splitted);
					
				} else { // just take it!
					decided_texts.push([undecided_texts[i]]);
				}
			}
			
			if (type === fuzzy_add_reason) {
				new AjaxDiscussionHandler().sendNewPremiseForArgument(arg, relation, decided_texts);
			} else if (type === fuzzy_start_premise) {
				new AjaxDiscussionHandler().sendNewStartPremise(decided_texts, conclusion, supportive);
			}
			$('#' + popupSetPremiseGroups).modal('hide');
		});
		
		if (undecided_texts.length === 1) { // we only need one page div
			page = gh.getPageOfSetStatementContainer(0, undecided_texts[0]);
			body.append(page);
			send.text(_t_discussion(saveMyStatement));
			
			page.find('input').each(function () {
				$(this).click(function inputClick() {
					send.removeClass('disabled');
					warning.show();
				});
			});
			
		} else { // we need several pages
			prev.show().removeClass('href').attr('max', undecided_texts.length);
			prev.parent().addClass('disabled');
			next.show().attr('max', undecided_texts.length);
			counter.show().text('1/' + undecided_texts.length);
			send.text(_t_discussion(saveMyStatements));
			
			
			// for each statement a new page div will be added
			for (page_no = 0; page_no < undecided_texts.length; page_no++) {
				page = gh.getPageOfSetStatementContainer(page_no, undecided_texts[page_no]);
				body.attr('data-text-' + page_no, undecided_texts[page_no]);
				if (page_no > 0) {
					page.hide();
				}
				body.append(page);
				
				page.find('input').each(function () {
					$(this).click(function inputClick() {
						new GuiHandler().displayNextPageOffSetStatementContainer(body, prev, next, counter, prefix);
					});
				});
			}
			
			// previous button click
			prev.click(function prevClick() {
				new GuiHandler().displayPrevPageOffSetStatementContainer(body, prev, next, counter, prefix);
			});
			
			// next button click
			next.click(function nextClick() {
				new GuiHandler().displayNextPageOffSetStatementContainer(body, prev, next, counter, prefix);
			});
		}
		
		popup.find('strong').text(body.data('text-0'));
		popup.modal('show');
	};
	
	/**
	 *
	 * @param body
	 * @param prev_btn
	 * @param next_btn
	 * @param counter_text
	 * @param prefix
	 */
	this.displayNextPageOffSetStatementContainer = function (body, prev_btn, next_btn, counter_text, prefix) {
		var tmp_el = body.find('div:visible');
		var tmp_id = parseInt(tmp_el.attr('id').substr(prefix.length));
		var input = tmp_el.find('input:checked');
		
		// is current page filled?
		if (input.length === 0) {
			$('#insert_statements_page_error').fadeIn();
		} else {
			$('#insert_statements_page_error').fadeOut();
			
			if (tmp_id < (parseInt(next_btn.attr('max')) - 1 )) {
				tmp_el.hide().next().fadeIn();
				prev_btn.parent().removeClass('disabled');
				counter_text.show().text((tmp_id + 2) + '/' + next_btn.attr('max'));

				$('#' + popupSetPremiseGroups).find('strong').text(body.data('text-' + (tmp_id + 1)));
				if ((tmp_id + 2) === parseInt(next_btn.attr('max'))) {
					next_btn.parent().addClass('disabled');
				}
			} else {
				$('#' + popupSetPremiseGroupsWarningText).show();
				$('#' + popupSetPremiseGroupsSendButton).removeClass('disabled');
			}
		}
	};
	
	/**
	 *
	 * @param body
	 * @param prev_btn
	 * @param next_btn
	 * @param counter_text
	 * @param prefix
	 */
	this.displayPrevPageOffSetStatementContainer = function (body, prev_btn, next_btn, counter_text, prefix) {
		var tmp_el = body.find('div:visible');
		var tmp_id = parseInt(tmp_el.attr('id').substr(prefix.length));
		
		if (tmp_id > 0) {
			tmp_el.hide().prev().fadeIn();
			next_btn.parent().removeClass('disabled');
			counter_text.show().text((tmp_id) + '/' + prev_btn.attr('max'));

			$('#' + popupSetPremiseGroups).find('strong').text(body.data('text-' + (tmp_id - 1)));
			if (tmp_id === 1) {
				prev_btn.parent().addClass('disabled');
			}
		}
	};
	
	/**
	 *
	 * @param page_no
	 * @param text
	 * @returns {*}
	 */
	this.getPageOfSetStatementContainer = function (page_no, text) {
		var src = $('#insert_statements_page_');
		var div_page = src.clone();
		var id = src.attr('id');
		var splitted = text.split(' ' + _t_discussion(and) + ' ');
		var topic = $('#' + addPremiseContainerMainInputIntroId).text();
		var input1, input2, input3, list, bigText, bigTextSpan, connection, i, infix;
		topic = topic.substr(0, topic.length - 3);
		
		$('#popup-set-premisegroups-body-intro-statements').text(text.trim());
		
		if (topic.match(/\.$/)) {
			topic = topic.substr(0, topic.length - 1) + ', ';
		}
		
		div_page.attr('id', id + page_no);
		div_page.attr('page', page_no);
		div_page.show();
		div_page.find('#' + popupSetPremiseGroupsStatementCount).text(splitted.length);
		
		var tmp_span = div_page.find('#insert_one_argument').next();
		tmp_span.text(tmp_span.text().replace('xx', splitted.length));
		list = div_page.find('#' + popupSetPremiseGroupsListMoreArguments);
		bigTextSpan = div_page.find('#' + popupSetPremiseGroupsOneBigStatement);
		
		// rename the id-, for- and name-tags of all radio button groups
		input1 = div_page.find('#insert_more_arguments');
		input2 = div_page.find('#insert_one_argument');
		input3 = div_page.find('#insert_dont_care');
		input1.attr('id', input1.attr('id') + '_' + page_no);
		input2.attr('id', input2.attr('id') + '_' + page_no);
		input3.attr('id', input3.attr('id') + '_' + page_no);
		input1.attr('name', input1.attr('name') + '_' + page_no);
		input2.attr('name', input2.attr('name') + '_' + page_no);
		input3.attr('name', input3.attr('name') + '_' + page_no);
		input1.parent().attr('for', input1.attr('id'));
		input2.parent().attr('for', input2.attr('id'));
		input3.parent().attr('for', input3.attr('id'));
		
		//connection = supportive ? _t_discussion(isItTrueThat) : _t_discussion(isItFalseThat);
		connection = _t_discussion(isItTrueThat);
		
		if (getDiscussionLanguage() === 'de') {
			bigText = topic;
		} else {
			bigText = topic + ' ' + connection; //supportive ? _t_discussion(itIsTrueThat) : _t_discussion(itIsFalseThat);
		}
		
		list.append($('<br>'));
		for (i = 0; i < splitted.length; i++) {
			var nl = i < splitted.length - 1 ? '<br>' : '';
			var line_text = '&#9900;   ' + topic + ' ' + _t_discussion(because) + ' ' + splitted[i] + '.' + nl;
			var tmp = $('<span>').html(line_text).css('margin-left', '1em');
			// list.append($('<li>').text(topic + ' ' + splitted[i] + '.'));
			list.append(tmp);
			infix = i === 0 ? _t_discussion(because) + ' ' : ('<u>' + _t_discussion(and) + ' ' + _t_discussion(because) + '</u> ' );
			bigText += ' ' + infix + splitted[i];
		}
		
		bigTextSpan.html(bigText + '.');
		
		return div_page;
	};
	
	/**
	 *
	 * @param parsedData
	 * @param callbackId
	 * @param type
	 * @param reason
	 */
	this.setStatementsAsProposal = function (parsedData, callbackId, type, reason) {
		var callbackElement = $('#' + callbackId);
		$('#' + proposalPremiseListGroupId).empty();
		$('#' + proposalStatementListGroupId).empty();
		$('#' + proposalEditListGroupId).empty();
		$('#' + proposalUserListGroupId).empty();
		$('#' + proposalStatementSearchGroupId).empty();
		$('#' + proposalDuplicateSearchGroupId).empty();
		$('#proposal-mergesplit-list-group-' + callbackId).empty();
		
		// do we have values ?
		if (parsedData.length === 0) {
			return;
		}
		
		var token, button, span_dist, span_text, index, text, img;
		callbackElement.focus();
		
		$.each(parsedData.values, function (key, val) {
			// distance = parseInt(val.distance);
			index = val.index;
			
			token = callbackElement.val();
			
			// make all tokens bold
			var non_edited_value = val.text;
			// replacement from http://stackoverflow.com/a/280805/2648872
			text = val.text.replace(new RegExp("(" + (token + '').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1") + ")", 'gi'), "</strong>$1<strong>");
			text = '<strong>' + text;
			
			button = $('<button>')
				.attr('type', 'button')
				.attr('class', 'list-group-item')
				.attr('id', 'proposal_' + index)
				.attr('text', non_edited_value)
				.hover(function () {
						$(this).addClass('active');
					},
					function () {
						$(this).removeClass('active');
					});
			if (type === fuzzy_find_statement){
				button.attr('data-url', val.url);
			} else if (type === fuzzy_duplicate){
				button.attr('data-statement-uid', val.statement_uid);
			}
			// we do not want the "Levensthein badge"
			span_dist = '';//$('<span>').attr('class', 'badge').text(parsedData.distance_name + ' ' + distance);
			span_text = $('<span>').attr('id', 'proposal_' + index + '_text').html(text);
			img = $('<img>').addClass('preload-image').addClass('img-circle').attr('style', 'height: 20pt; margin-right: 1em;').attr('src', val.avatar);
			
			if (type === fuzzy_find_user) {
				button.append(img).append(span_text);
			} else {
				button.append(img).append(span_dist).append(span_text);
			}
			
			button.click(function () {
				callbackElement.val($(this).attr('text'));
				$('#' + proposalStatementListGroupId).empty();
				$('#' + proposalPremiseListGroupId).empty();
				$('#' + proposalEditListGroupId).empty(); // list with elements should be after the callbacker
				$('#' + proposalUserListGroupId).empty();
				$('#' + proposalStatementSearchGroupId).empty();
				$('#' + proposalDuplicateSearchGroupId).empty();
				$('#proposal-mergesplit-list-group-' + callbackId).empty();
				if (type === fuzzy_find_statement){
					window.location.href = $(this).data('url');
				} else if (type === fuzzy_duplicate){
					callbackElement.attr('data-statement-uid', $(this).data('statement-uid'));
					new PopupHandler().duplicateValueSelected(reason, val.statement_uid);
				}
			});
			
			if (type === fuzzy_start_premise){        $('#' + proposalStatementListGroupId).append(button); }
			else if (type === fuzzy_start_statement){ $('#' + proposalStatementListGroupId).append(button); }
			else if (type === fuzzy_add_reason){      $('#' + proposalPremiseListGroupId).append(button); }
			else if (type === fuzzy_statement_popup){ $('#' + proposalEditListGroupId).append(button); }
			else if (type === fuzzy_find_user){       $('#' + proposalUserListGroupId).append(button); }
			else if (type === fuzzy_find_statement){  $('#' + proposalStatementSearchGroupId).append(button); }
			else if (type === fuzzy_duplicate){       $('#' + proposalDuplicateSearchGroupId).append(button); }
			else if (type === fuzzy_find_mergesplit){ $('#proposal-mergesplit-list-group-' + callbackId).append(button); }
		});
	};
	
	/**
	 * Displays all corrections in the popup
	 * @param jsonData json encoded return data
	 */
	this.showLogfileOfPremisegroup = function (jsonData) {
		var space = $('#' + popupEditStatementLogfileSpaceId);
		space.empty();
		space.show();
		space.prev().show();
		var view = $('#' + popupEditStatementChangelogView);
		var hide = $('#' + popupEditStatementChangelogHide);
		view.text('(' + _t_discussion(changelogView) + ')').hide();
		hide.text('(' + _t_discussion(changelogHide) + ')').hide();
		
		var at_least_one_history = false;
		$.each(jsonData, function (key, value) {
			if (key === 'error' || key === 'info') {
				return true;
			}

			var table = $('<table>');
			table.attr('class', 'table table-condensed table-striped table-hover')
				.attr('border', '0')
				.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;');
			var tbody = $('<tbody>');
			
			var thead = $('<thead>')
				.append($('<td>').text(_t(text)))
				.append($('<td>').text(_t(author)))
				.append($('<td>').text(_t(date)));
			table.append(thead);
			
			var counter = 0;
			$.each(value.content, function (key, val) {
				var tr = $('<tr>')
					.append($('<td>').text(val.text))
					.append($('<td>')
						.append($('<img>').attr('src', val.author_gravatar).css('margin-right', '1em').addClass('img-circle'))
						.append($('<a>')
							.addClass('img-circle')
							.attr('target', '_blank')
							.attr('href', val.author_url)
							.text(val.author)))
					.append($('<td>').text(val.date));
				tbody.append(tr);
				counter += 1;
			});
			if (counter > 1) {
				at_least_one_history = true;
			}
			space.append(table.append(tbody));
		});

		if (!at_least_one_history) {
			space.hide();
			space.prev().hide();
			view.show();
		} else {
			hide.show();
		}
		
		view.click(function () {
			space.show();
			space.prev().show();
			hide.show();
			view.hide();
		});
		
		hide.click(function () {
			space.hide();
			space.prev().hide();
			hide.hide();
			view.show();
		});
	};
	
	/**
	 * Hides error description
	 */
	this.hideErrorDescription = function () {
		$('#' + discussionErrorDescriptionId).html('');
		$('#' + discussionErrorDescriptionSpaceId).hide();
	};
	
	/**
	 * Hides success description
	 */
	this.hideSuccessDescription = function () {
		$('#' + discussionSuccessDescriptionId).html('');
		$('#' + discussionSuccessDescriptionSpaceId).hide();
	};
	
	/**
	 * Sets style attributes to default
	 */
	this.resetChangeDisplayStyleBox = function () {
		this.setDisplayStyleAsDiscussion();
	};
	
	/**
	 *
	 * @returns {*|jQuery}
	 */
	this.getNoDecisionsAlert = function () {
		var div, strong, span;
		div = $('<div>').attr('class', 'alert alert-dismissible alert-info');
		strong = $('<strong>').text('Ohh...! ');
		span = $('<span>').text(_t_discussion(noDecisionstaken));
		div.append(strong).append(span);
		return div;
	};
	
	/**
	 *
	 * @param users_array
	 * @param gh
	 * @param element
	 * @param tbody
	 * @returns {*|jQuery|HTMLElement}
	 */
	this.closePrepareTableForOpinionDialog = function (users_array, gh, element, tbody) {
		var body = $('<div>');
		var table = $('<table>')
			.attr('class', 'table table-condensed table-hover center')
			.attr('border', '0')
			.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;');
		
		if (Object.keys(users_array).length === 0) {
			body.append(gh.getNoDecisionsAlert());
		} else {
			body.append(element).append(table.append(tbody));
		}
		return body;
	};
	
	/**
	 *
	 * @param users_array
	 * @returns {Array}
	 */
	this.createUserRowsForOpinionDialog = function (users_array) {
		var left = '';
		var middle = '';
		var right = '';
		var j = 0;
		var rows = [];
		
		$.each(users_array, function (index, val) {
			var img = $.parseHTML('<img class="img-circle" style="height: 40%; margin-left: 0.5em;" src="' + val.avatar_url + '">');
			var span = $('<span>').text(val.nickname);
			var link = $('<td>').append($('<a>').attr({
				'target': '_blank',
				'href': val.public_profile_url,
				'style': 'padding-right: 0.5em;'
			}).append(span).append(img));
			
			// three elements per row (store middle and left element, append later)
			if (j === 0) {
				left = link;
			} else if (j === 1) {
				middle = link;
			} else if (j === 2) {
				rows.push($('<tr>').append(left).append(middle).append(link));
			}
			j = (j + 1) % 3;
		});
		
		// append the last row
		if (j === 1) {
			rows.push($('<tr>').append(left));
		}
		if (j === 2) {
			rows.push($('<tr>').append(left).append(middle));
		}
		
		return rows;
	};
	
	/**
	 *
	 * @param list
	 */
	this.hoverInputListOf = function (list) {
		list.find('input').each(function () {
			$(this).hover(function () {
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prop('checked', true);
				}
			}, function () {
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prop('checked', false);
				}
			});
		});
		list.find('label').each(function () {
			$(this).hover(function () {
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prev().prop('checked', true);
				}
			}, function () {
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prev().prop('checked', false);
				}
			});
		});
	};
	
	/**
	 *
	 * @returns {*}
	 */
	this.getMaxSizeOfGraphViewContainer = function () {
		var header, footer, innerHeight;
		header = $('#' + customBootstrapMenuId);
		footer = $('#footer');
		innerHeight = window.innerHeight;
		innerHeight -= header.outerHeight(true);
		innerHeight -= footer.outerHeight(true);
		innerHeight -= this.getPaddingOfElement(header);
		innerHeight -= this.getPaddingOfElement(footer);
		return innerHeight;
	};
	
	/**
	 *
	 * @returns {number}
	 */
	this.getMaxSizeOfDiscussionViewContainer = function () {
		var bar, innerHeight, list;
		bar = $('#header-container');
		list = $('#' + discussionSpaceListId);
		innerHeight = this.getMaxSizeOfGraphViewContainer();
		innerHeight -= bar.outerHeight(true);
		innerHeight -= list.outerHeight(true);
		innerHeight -= this.getPaddingOfElement(bar);
		innerHeight -= this.getPaddingOfElement(list);
		return innerHeight - 10;
	};
	
	/**
	 *
	 * @param element
	 * @returns {number}
	 */
	this.getPaddingOfElement = function (element){
		if (typeof element !== "undefined" && typeof element.css('padding') !== "undefined") {
			var pt = parseInt(element.css('padding-top').replace('px', ''));
			var pb = parseInt(element.css('padding-bottom').replace('px', ''));
			return pt + pb;
		} else {
			return 0;
		}
	};
	
	/**
	 * Roates the little pin icon in the sidebar
	 * @param element
	 * @param degree
	 */
	this.rotateElement = function(element, degree){
		element.css('-ms-transform', 'rotate(' + degree + 'deg)')
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
	 *
	 * @param lang
	 */
	this.lang_switch = function(lang){
		if (!Cookies.get(LANG_SWITCH_WARNING)) {
			displayConfirmationDialogWithoutCancelAndFunction(get_it(lang, languageSwitchModalTitle), get_it(lang, languageSwitchModalBody));
			$('#' + popupConfirmDialogId).on('hide.bs.modal', function () {
				new AjaxMainHandler().switchDisplayLanguage(lang);
				Cookies.set(LANG_SWITCH_WARNING, true, {expires: 180});
			});
		} else {
			new AjaxMainHandler().switchDisplayLanguage(lang);
		}
	};
}