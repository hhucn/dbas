/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function GuiHandler() {
	'use strict';
	let interactionHandler;
	let maxHeightOfBubbleSpace = 300;
	
	/**
	 *
	 * @param externInteractionHandler
	 */
	this.setHandler = function (externInteractionHandler) {
		interactionHandler = externInteractionHandler;
	};
	
	/**
	 * Adds a premise row in the 'add premise'-container
	 */
	this.appendAddPremiseRow = function () {
		let body = $('#' + addPremiseContainerBodyId);
		let send = $('#' + sendNewPremiseId);
		let id = addPremiseContainerMainInputId + '-' + new Date().getTime();
		
		let copy_div = $('.container-three-divs:first').clone();
		copy_div.find('input').attr('id', id).val('');
		copy_div.find('.text-counter-input').remove();
		let img_plus = copy_div.find('.icon-add-premise');
		let img_minus = copy_div.find('.icon-rem-premise');
		body.append(copy_div);
		setTextWatcherInputLength(copy_div.find('input'));
		
		img_plus.click(function () {
			new GuiHandler().appendAddPremiseRow();
			$(this).hide().prev().show(); // hide +, show -
			send.val(_t(saveMyStatements));
		});
		
		body.find('.icon-rem-premise').each(function () {
			$(this).click(function () {
				// removing bubble
				let id = $(this).parent().parent().find('input').attr('id'),
					tmpid = id.split('-').length == 6 ? id.split('-')[5] : '0';
				$('#current_' + tmpid).fadeOut().remove();
				$(this).parent().parent().remove();
				body.find('div').children().last().show();
				// hide minus icon, when there is only one child
				if (body.find('.container-three-divs').length == 1) {
					body.find('.icon-rem-premise').hide();
					send.val(_t(saveMyStatement));
				} else {
					body.find('.icon-rem-premise').show();
					send.val(_t(saveMyStatements));
				}
			});
		});
		img_minus.show();
		
		// add fuzzy search
		$('#' + id).keyup(function () {
			setTimeout(function () {
				let escapedText = escapeHtml($('#' + id).val());
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
		const graphViewContainer = $('#' + graphViewContainerId);
		const main = new Main();
		const tacked_sidebar = 'tacked_graph_sidebar';
		const header = $('#' + graphViewContainerHeaderId);
		
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
		let innerHeight = this.getMaxSizeOfGraphViewContainer();
		graphViewContainer.attr('style', 'height: ' + innerHeight + 'px; margin-left: 2em; margin-right: 2em; margin-bottom: 1em;');
		innerHeight -= header.outerHeight(true) + 20;
		$('#' + graphViewContainerSpaceId).attr('style', 'height: ' + innerHeight + 'px; margin-left: 0.5em; margin-right: 0.5em; width: 95%');
		new DiscussionGraph().showGraph();
		main.setSidebarStyle(graphViewContainer, tacked_sidebar);
		main.setSidebarClicks(graphViewContainer, tacked_sidebar);
		this.hideAddPositionContainer();
		this.hideAddPremiseContainer();
	};
	
	/**
	 *
	 * @param resize
	 */
	this.setMaxHeightForDiscussionContainer = function(resize){
		const maincontainer = $('#' + discussionContainerId);
		const sidebarwrapper = maincontainer.find('.' + sidebarWrapperClass);
		maincontainer.css('max-height', maincontainer.outerHeight() + resize + 'px');
		sidebarwrapper.css('height', maincontainer.outerHeight() + 'px');
	};
	
	/**
	 * Sets the maximal height for the bubble space. If needed, a scrollbar will be displayed.
	 */
	this.setMaxHeightForBubbleSpace = function () {
		// max size of the container
		let speechBubbles = $('#' + discussionBubbleSpaceId);
		let height = 0;
		let maxHeight = this.getMaxSizeOfDiscussionViewContainer();
		let start;
		let nowBubble = speechBubbles.find('*[id*=now]');
		let oldSize = speechBubbles.height();
		$.each(speechBubbles.find('div p'), function () {
			height += $(this).outerHeight(true);
			// clear unnecessary a tags
			if ($(this).parent().attr('href') == '?breadcrumb=true') {
				$(this).insertAfter($(this).parent());
				$(this).prev().remove();
			}
		});
		
		start = nowBubble.length == 0 ? 'bottom' : nowBubble;
		// scroll to now bubble on mobile devices and do not enable slimscroll
		if (isMobileAgent()){
			if (nowBubble.length != 0)
				$('html, body').animate({scrollTop: nowBubble.offset().top - 75}, 500);
			speechBubbles.css({'background': '#fff'});
			return;
		}
		if (height > maxHeight) {
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
			height += 30;
			if (height < 50)
				speechBubbles.css('min-height', '100px');
			else
				speechBubbles.css('height', height + 'px').css('min-height', '200px');
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
	 * @param undecided_texts
	 * @param decided_texts
	 * @param supportive
	 * @param type
	 * @param arg
	 * @param relation
	 * @param conclusion
	 */
	this.showSetStatementContainer = function (undecided_texts, decided_texts, supportive, type, arg, relation, conclusion) {
		let gh = new GuiHandler(), page, page_no,
			body = $('#' + popupSetPremiseGroupsBodyContent).empty(),
			prev = $('#' + popupSetPremiseGroupsPreviousButton).hide(),
			next = $('#' + popupSetPremiseGroupsNextButton).hide(),
			send = $('#' + popupSetPremiseGroupsSendButton).addClass('disabled'),
			counter = $('#' + popupSetPremiseGroupsCounter).hide(),
			prefix = 'insert_statements_page_';
		
		send.click(function sendClick() {
			let selections = body.find('input:checked'), i, j, splitted;
			
			// merge every text part to one array
			for (i = 0; i < undecided_texts.length; i++) {
				splitted = undecided_texts[i].split(' ' + _t_discussion(and) + ' ');
				
				if (selections[i].id.indexOf(attr_more_args) != -1) { // each splitted text part is one argument
					for (j = 0; j < splitted.length; j++)
						decided_texts.push([splitted[j]]);
					
				} else if (selections[i].id.indexOf(attr_one_arg) != -1) { // one argument with big premisegroup
					decided_texts.push(splitted);
					
				} else { // just take it!
					decided_texts.push([undecided_texts[i]]);
				}
			}
			
			if (type == fuzzy_add_reason) {
				new AjaxDiscussionHandler().sendNewPremiseForArgument(arg, relation, decided_texts);
			} else if (type == fuzzy_start_premise) {
				new AjaxDiscussionHandler().sendNewStartPremise(decided_texts, conclusion, supportive);
			} else {
				alert("Todo: unknown type")
			}
			$('#' + popupSetPremiseGroups).modal('hide');
		});
		
		if (undecided_texts.length == 1) { // we only need one page div
			page = gh.getPageOfSetStatementContainer(0, undecided_texts[0]);
			body.append(page);
			send.text(_t_discussion(saveMyStatement));
			
			page.find('input').each(function () {
				$(this).click(function inputClick() {
					send.removeClass('disabled');
				});
			});
			
		} else { // we need several pages
			prev.show().removeClass('href').attr('max', undecided_texts.length);
			prev.parent().addClass('disabled');
			next.show().attr('max', undecided_texts.length);
			counter.show().text('1/' + undecided_texts.length);
			send.text(_t(saveMyStatements));
			
			// for each statement a new page div will be added
			for (page_no = 0; page_no < undecided_texts.length; page_no++) {
				page = gh.getPageOfSetStatementContainer(page_no, undecided_texts[page_no]);
				if (page_no > 0)
					page.hide();
				body.append(page);
				
				page.find('input').each(function () {
					$(this).click(function inputClick() {
						new GuiHandler().displayNextPageOffSetStatementContainer(body, prev, next, counter, prefix);
					})
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
		
		$('#' + popupSetPremiseGroups).modal('show');
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
		let tmp_el = body.find('div:visible'),
			tmp_id = parseInt(tmp_el.attr('id').substr(prefix.length)),
			input = tmp_el.find('input:checked');
		
		// is current page filled?
		if (input.length == 0) {
			$('#insert_statements_page_error').fadeIn();
		} else {
			$('#insert_statements_page_error').fadeOut();
			
			if (tmp_id < (parseInt(next_btn.attr('max')) - 1 )) {
				tmp_el.hide().next().fadeIn();
				prev_btn.parent().removeClass('disabled');
				counter_text.show().text((tmp_id + 2) + '/' + next_btn.attr('max'));
				
				if ((tmp_id + 2) == parseInt(next_btn.attr('max')))
					next_btn.parent().addClass('disabled');
			} else {
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
		let tmp_el = body.find('div:visible'),
			tmp_id = parseInt(tmp_el.attr('id').substr(prefix.length));
		
		if (tmp_id > 0) {
			tmp_el.hide().prev().fadeIn();
			next_btn.parent().removeClass('disabled');
			counter_text.show().text((tmp_id) + '/' + prev_btn.attr('max'));
			if (tmp_id == 0)
				prev_btn.parent().addClass('disabled');
		}
	};
	
	/**
	 *
	 * @param page_no
	 * @param text
	 * @returns {*}
	 */
	this.getPageOfSetStatementContainer = function (page_no, text) {
		let src = $('#insert_statements_page_');
		let div_page = src.clone();
		let id = src.attr('id');
		let splitted = text.split(' ' + _t_discussion(and) + ' ');
		let topic = $('#' + addPremiseContainerMainInputIntroId).text();
		let input1, input2, input3, list, bigText, bigTextSpan, connection, i, infix;
		topic = topic.substr(0, topic.length - 3);
		
		$('#popup-set-premisegroups-body-intro-statements').text(text.trim());
		
		if (topic.match(/\.$/)) {
			topic = topic.substr(0, topic.length - 1) + ', '
		}
		
		div_page.attr('id', id + page_no).attr('page', page_no).show();
		div_page.find('#' + popupSetPremiseGroupsStatementCount).text(splitted.length);
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
		input1.parent().attr('for', input1.parent().attr('for') + '_' + page_no);
		input2.parent().attr('for', input2.parent().attr('for') + '_' + page_no);
		input3.parent().attr('for', input3.parent().attr('for') + '_' + page_no);
		
		//connection = supportive ? _t_discussion(isItTrueThat) : _t_discussion(isItFalseThat);
		connection = _t_discussion(isItTrueThat);
		
		if (getDiscussionLanguage() == 'de')
			bigText = topic;
		else
			bigText = topic + ' ' + connection; //supportive ? _t_discussion(itIsTrueThat) : _t_discussion(itIsFalseThat);
		
		list.append($('<br>'));
		for (i = 0; i < splitted.length; i++) {
			let nl = i < splitted.length - 1 ? '<br>' : '';
			let tmp = $('<span>').html('&#9900;   ' + topic + ' ' + splitted[i] + '.' + nl).css('padding-left', '20px');
			// list.append($('<li>').text(topic + ' ' + splitted[i] + '.'));
			list.append(tmp);
			infix = i == 0 ? '' : ('<em>' + _t_discussion(andAtTheSameTime) + '</em> ' + connection + ' ');
			bigText += ' ' + infix + splitted[i];
		}
		
		bigTextSpan.html(bigText + '.');
		
		return div_page;
	};
	
	/**
	 *
	 * @param parsedData
	 * @param callbackid
	 * @param type
	 */
	this.setStatementsAsProposal = function (parsedData, callbackid, type) {
		let callbackElement = $('#' + callbackid);
		let uneditted_value;
		$('#' + proposalPremiseListGroupId).empty();
		$('#' + proposalStatementListGroupId).empty();
		$('#' + proposalEditListGroupId).empty();
		$('#' + proposalUserListGroupId).empty();
		
		// do we have values ?
		if (parsedData.length == 0) {
			return;
		}
		
		let token, button, span_dist, span_text, distance, index, text, img;
		callbackElement.focus();
		
		$.each(parsedData.values, function (key, val) {
			distance = parseInt(val.distance);
			index = val.index;
			
			token = callbackElement.val();
			//let pos = val.toLocaleLowerCase().indexOf(token.toLocaleLowerCase()), newpos = 0, start = 0;
			
			// make all tokens bold
			uneditted_value = val.text;
			// replacement from http://stackoverflow.com/a/280805/2648872
			text = val.text.replace(new RegExp("(" + (token + '').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1") + ")", 'gi'), "</strong>$1<strong>");
			text = '<strong>' + text;
			
			button = $('<button>')
				.attr('type', 'button')
				.attr('class', 'list-group-item')
				.attr('id', 'proposal_' + index)
				.attr('text', uneditted_value)
				.hover(function () {
						$(this).addClass('active');
					},
					function () {
						$(this).removeClass('active');
					});
			// we do not want the "Levensthein badge"
			span_dist = '';//$('<span>').attr('class', 'badge').text(parsedData.distance_name + ' ' + distance);
			span_text = $('<span>').attr('id', 'proposal_' + index + '_text').html(text);
			img = $('<img>').addClass('preload-image').addClass('img-circle').attr('style', 'height: 20pt; margin-right: 1em;').attr('src', val.avatar);
			
			if (type == fuzzy_find_user)
				button.append(img).append(span_text);
			else
				button.append(img).append(span_dist).append(span_text);
			
			button.click(function () {
				callbackElement.val($(this).attr('text'));
				$('#' + proposalStatementListGroupId).empty();
				$('#' + proposalPremiseListGroupId).empty();
				$('#' + proposalEditListGroupId).empty(); // list with elements should be after the callbacker
				$('#' + proposalUserListGroupId).empty();
			});
			
			if (type == fuzzy_start_premise)        $('#' + proposalStatementListGroupId).append(button);
			else if (type == fuzzy_start_statement) $('#' + proposalStatementListGroupId).append(button);
			else if (type == fuzzy_add_reason)      $('#' + proposalPremiseListGroupId).append(button);
			else if (type == fuzzy_statement_popup) $('#' + proposalEditListGroupId).append(button);
			else if (type == fuzzy_find_user)       $('#' + proposalUserListGroupId).append(button);
		});
	};
	
	/**
	 * Displays all corrections in the popup
	 * @param jsonData json encoded return data
	 */
	this.showLogfileOfPremisegroup = function (jsonData) {
		let space = $('#' + popupEditStatementLogfileSpaceId);
		space.empty();
		space.show();
		space.prev().show();
		let view = $('#' + popupEditStatementChangelogView);
		let hide = $('#' + popupEditStatementChangelogHide);
		view.text('(' + _t_discussion(changelogView) + ')').hide();
		hide.text('(' + _t_discussion(changelogHide) + ')').hide();
		
		let at_least_one_history = false;
		$.each(jsonData, function (key, value) {
			if (key == 'error') {
				return true;
			}
			let table, tr, tbody, thead;
			table = $('<table>');
			table.attr('class', 'table table-condensed table-striped table-hover')
				.attr('border', '0')
				.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;');
			tbody = $('<tbody>');
			
			thead = $('<thead>')
				.append($('<td>').text(_t(text)))
				.append($('<td>').text(_t(author)))
				.append($('<td>').text(_t(date)));
			table.append(thead);
			
			let counter = 0;
			$.each(value.content, function (key, val) {
				tr = $('<tr>')
					.append($('<td>').text(val.text))
					.append($('<td>')
						.append($('<img>').attr('src', val.author_gravatar).css('margin-right', '1em'))
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
	 * Updates an statement in the discussions list
	 * @param jsonData
	 */
	this.updateOfStatementInDiscussion = function (jsonData) {
		$('#td_' + jsonData.uid).text(jsonData.text);
		$('#' + jsonData.uid).text(jsonData.text);
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
		let div, strong, span;
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
	this.closePrepareTableForOpinonDialog = function (users_array, gh, element, tbody) {
		let body = $('<div>');
		let table = $('<table>')
			.attr('class', 'table table-condensed table-hover center')
			.attr('border', '0')
			.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;');
		
		if (Object.keys(users_array).length == 0)
			body.append(gh.getNoDecisionsAlert());
		else
			body.append(element).append(table.append(tbody));
		return body;
	};
	
	/**
	 *
	 * @param users_array
	 * @returns {Array}
	 */
	this.createUserRowsForOpinionDialog = function (users_array) {
		let left = '';
		let middle = '';
		let right = '';
		let j = 0;
		let rows = [];
		
		$.each(users_array, function (index, val) {
			let img = $.parseHTML('<img class="img-circle" style="height: 40%; padding-left: 0.5em;" src="' + val.avatar_url + '">');
			let span = $('<span>').text(val.nickname);
			let link = $('<td>').append($('<a>').attr({
				'target': '_blank',
				'href': val.public_profile_url,
				'style': 'padding-right: 0.5em;'
			}).append(span).append(img));
			
			// three elements per row (store middle and left element, append later)
			if (j == 0) {
				left = link;
			} else if (j == 1) {
				middle = link;
			} else if (j == 2) {
				rows.push($('<tr>').append(left).append(middle).append(link));
			}
			j = (j + 1) % 3;
		});
		
		// append the last row
		if (j == 1)
			rows.push($('<tr>').append(left));
		if (j == 2)
			rows.push($('<tr>').append(left).append(middle));
		
		return rows
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
			})
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
			})
		});
	};
	
	/**
	 *
	 * @returns {*}
	 */
	this.getMaxSizeOfGraphViewContainer = function () {
		let header, footer, innerHeight;
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
		let bar, innerHeight, list;
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
		return parseInt(element.css('padding-top').replace('px','')) + parseInt(element.css('padding-bottom').replace('px',''))
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
	
}