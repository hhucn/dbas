/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function GuiHandler() {
	'use strict';
	var interactionHandler;
	var maxHeightOfBubbleSpace = 300;

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
	this.appendAddPremiseRow = function(){
		var body = $('#add-premise-container-body');
		var send = $('#' + sendNewPremiseId);
		var uid = new Date().getTime();
		var div = $('<div>').attr('style', 'padding-bottom: 2em').addClass('container-three-divs');
			//var div_l = $('<div>');
		var div_m = $('<div>').addClass('flex-div');
		var div_r = $('<div>');
			//var h5 = $('<h5>').attr('style', 'float:left; line-height:20px; text-align:center;').text('Because...');
		var id = 'add-premise-container-main-input-' + uid;
		var input = $('<input>').attr('id', id)
				.attr('type', 'text')
				.attr('class', 'form-control')
				.attr('autocomplete', 'off')
				.attr('placeholder', '...')
				.data('min-length', '10')
				.keyup(function() { setTextWatcherForMinLength($(this)); })
				.focusin(function() { setTextWatcherForMinLength($(this)); });
		var imgm = $('<img>')
				.attr('class', 'icon-rem-premise')
				.attr('src', mainpage + 'static/images/icon_minus1.png')
				.attr('title', body.find('.icon-rem-premise').first().attr('title'));
		var imgp = $('<img>')
				.attr('class', 'icon-add-premise')
				.attr('src', mainpage + 'static/images/icon_plus1.png')
				.attr('title', body.find('.icon-add-premise').first().attr('title'));

		// div.append(div_l.append(h5))
		div.append(div_m.append(input))
			.append(div_r.append(imgm).append(imgp));
		$('#' + addPremiseContainerBodyId).append(div);

		imgp.click(function(){
			new GuiHandler().appendAddPremiseRow();
			$(this).hide().prev().show(); // hide +, show -
			send.val(_t(saveMyStatements));
		});

		body.find('.icon-rem-premise').each(function(){
			$(this).click(function(){
				// removing bubble
				var id = $(this).parent().parent().find('input').attr('id'),
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
		imgm.show();

		// add fuzzy search
		$('#' + id).keyup(function () {
			new Helper().delay(function () {
				var escapedText = new Helper().escapeHtml($('#' + id).val());
				new AjaxDiscussionHandler().fuzzySearch(escapedText, id, fuzzy_add_reason, '');
			}, 200);
		});
	};

	/**
	 * Setting an error description in some p-tag
	 * @param text to set
	 */
	this.setErrorDescription = function (text) {
		$('#' + discussionErrorDescriptionId).html(text);
		$('#' + discussionErrorDescriptionSpaceId).show();
	};

	/**
	 * Dialog based discussion modi
	 */
	this.setDisplayStyleAsDiscussion = function () {
		this.setImageInactive($('#' + displayStyleIconGuidedId));
		this.setImageActive($('#' + displayStyleIconIslandId));
		this.setImageActive($('#' + displayStyleIconGraphId));
		$('#' + islandViewContainerId).hide();
		$('#' + graphViewContainerId).hide();
		$('#' + discussionContainerId).show();
		$('#' + headerContainerId).show();
		new Helper().clearAnchor();
	};

	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsIsland = function () {
		this.setImageActive($('#' + displayStyleIconGuidedId));
		this.setImageInactive($('#' + displayStyleIconIslandId));
		this.setImageActive($('#' + displayStyleIconGraphId));
		$('#' + islandViewContainerId).fadeIn('slow');
		//$('#' + graphViewContainerId).hide();
		//$('#' + discussionContainerId).hide();
		new Helper().setAnchor('island');
	};

	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsGraphView = function () {
		var graphViewContainer = $('#' + graphViewContainerId);
		var main = new Main();
		var tacked_sidebar = 'tacked_graph_sidebar';
		var header = $('#graph-view-container-header');
		
		this.setImageActive($('#' + displayStyleIconGuidedId));
		this.setImageActive($('#' + displayStyleIconIslandId));
		this.setImageInactive($('#' + displayStyleIconGraphId));
		$('#' + islandViewContainerId).hide();
		$('#' + discussionContainerId).hide();
		$('#' + headerContainerId).hide();
		$('#' + addPremiseContainerId).hide();

		// text
		$('#' + graphViewContainerHeaderId).html($('#issue_info').html());

		// height
		var innerHeight = new Helper().getMaxSizeOfGraphViewContainer();
		graphViewContainer.attr('style', 'height: ' + innerHeight + 'px; margin-left: 2em; margin-right: 2em; margin-bottom: 1em;');
		innerHeight -= header.outerHeight(true) + 20;
		$('#' + graphViewContainerSpaceId).attr('style', 'height: ' + innerHeight + 'px; margin-left: 0.5em; margin-right: 0.5em; width: 95%');
		new DiscussionGraph().showGraph();
		main.setSidebarStyle(graphViewContainer, tacked_sidebar);
		main.setSidebarClicks(graphViewContainer, tacked_sidebar);
		new Helper().setAnchor('graph');
	};

	/**
	 * Adds the inactive-image-class, which includes a grayfilter and blur
	 * @param imageElement <img>-Element
	 */
	this.setImageInactive = function(imageElement){
		imageElement.addClass('inactive-image').css('cursor','not-allowed');//.removeClass('icon-badge');
	};

	/**
	 * Removes the inactive-image-class, which includes a grayfilter and blur
	 * @param imageElement <img>-Element
	 */
	this.setImageActive = function(imageElement){
		imageElement.removeClass('inactive-image').css('cursor', 'pointer');//.addClass('icon-badge');
	};

	/**
	 * Sets the maximal height for the bubble space. If needed, a scrollbar will be displayed.
	 */
	this.setMaxHeightForBubbleSpace = function() {
		// max size of the container
		var speechBubbles = $('#' + discussionBubbleSpaceId), height = 0,
			maxHeight = new Helper().getMaxSizeOfDiscussionViewContainer(), start,
			nowBubble = speechBubbles.find('*[id*=now]');
		$.each(speechBubbles.find('div p'), function () {
			height += $(this).outerHeight(true);
			// clear unnecessary a tags
			if ($(this).parent().attr('href') == '?breadcrumb=true') {
				$(this).insertAfter($(this).parent());
				$(this).prev().remove();
			}
		});

		start = nowBubble.length == 0 ? 'bottom' : nowBubble;
		if (height > maxHeight) {
			if (maxHeight < maxHeightOfBubbleSpace){//} && new Helper().isMobileAgent() ) {
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
			height += 20;
			if (height < 50)
				speechBubbles.css('min-height', '100px');
			else
				speechBubbles.css('height', height + 'px').css('min-height', '300px');
			speechBubbles.css('min-height', '100px').css('max-height', maxHeight + 'px');
		}
	};

	/**
	 * Shows the 'add position'-container
	 */
	this.showAddPositionContainer = function(){
		$('#' + addStatementContainerId).show();
	};

	/**
	 * Shows the 'add premise'-container
	 */
	this.showAddPremiseContainer = function(){
		$('#' + addPremiseContainerId).show();
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
	this.showSetStatementContainer = function(undecided_texts, decided_texts, supportive, type, arg, relation, conclusion) {
		var gh = new GuiHandler(), page, page_no,
			body = $('#' + popupSetPremiseGroupsBodyContent).empty(),
			prev = $('#' + popupSetPremiseGroupsPreviousButton).hide(),
			next = $('#' + popupSetPremiseGroupsNextButton).hide(),
			send = $('#' + popupSetPremiseGroupsSendButton).addClass('disabled'),
			counter = $('#' + popupSetPremiseGroupsCounter).hide(),
			prefix = 'insert_statements_page_';

		send.click(function sendClick(){
			var selections = body.find('input:checked'), i, j, splitted;

			// merge every text part to one array
			for (i=0; i<undecided_texts.length; i++){
				splitted = undecided_texts[i].split(' ' + _t_discussion(and) + ' ');

				if (selections[i].id.indexOf(attr_more_args) != -1){ // each splitted text part is one argument
					for (j=0; j<splitted.length; j++)
						decided_texts.push([splitted[j]]);

				} else if (selections[i].id.indexOf(attr_one_arg) != -1){ // one argument with big premisegroup
					decided_texts.push(splitted);

				} else { // just take it!
					decided_texts.push([undecided_texts[i]]);
				}
			}

			if (type == fuzzy_add_reason){
				new AjaxDiscussionHandler().sendNewPremiseForArgument(arg, relation, decided_texts);
			} else if (type == fuzzy_start_premise){
				new AjaxDiscussionHandler().sendNewStartPremise(decided_texts, conclusion, supportive);
			} else {
			 	alert("Todo: unknown type")
			}
			$('#' + popupSetPremiseGroups).modal('hide');
		});

		if (undecided_texts.length == 1){ // we only need one page div
			page = gh.getPageOfSetStatementContainer(0, undecided_texts[0]);
			body.append(page);
			send.text(_t_discussion(saveMyStatement));

			page.find('input').each(function(){
				$(this).click(function inputClick (){
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

				page.find('input').each(function(){
					$(this).click(function inputClick (){
						new GuiHandler().displayNextPageOffSetStatementContainer(body, prev, next, counter, prefix);
					})
				});
			}

			// previous button click
			prev.click(function prevClick(){
				new GuiHandler().displayPrevPageOffSetStatementContainer(body, prev, next, counter, prefix);
			});

			// next button click
			next.click(function nextClick(){
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
	this.displayNextPageOffSetStatementContainer = function(body, prev_btn, next_btn, counter_text, prefix){
		var tmp_el = body.find('div:visible'),
			tmp_id = parseInt(tmp_el.attr('id').substr(prefix.length)),
			input = tmp_el.find('input:checked');

		// is current page filled?
		if (input.length == 0){
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
	this.displayPrevPageOffSetStatementContainer = function(body, prev_btn, next_btn, counter_text, prefix){
		var tmp_el = body.find('div:visible'),
			tmp_id = parseInt(tmp_el.attr('id').substr(prefix.length));

		if (tmp_id > 0){
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
	this.getPageOfSetStatementContainer = function(page_no, text){
		var src = $('#insert_statements_page_');
		var div_page = src.clone();
		var id = src.attr('id');
		var splitted = text.split(' ' + _t_discussion(and) + ' ');
		var topic = $('#' + addPremiseContainerMainInputIntroId).text();
		var input1, input2, input3, list, bigText, bigTextSpan, connection, i, infix;
		topic = topic.substr(0, topic.length-3);

		$('#popup-set-premisegroups-body-intro-statements').text(text.trim());

		if (topic.match(/\.$/)){
			topic = topic.substr(0, topic.length-1) + ', '
		}

		div_page.attr('id', id + page_no).attr('page', page_no).show();
		div_page.find('#' + popupSetPremiseGroupsStatementCount).text(splitted.length);
		list        = div_page.find('#' + popupSetPremiseGroupsListMoreArguments);
		bigTextSpan = div_page.find('#' + popupSetPremiseGroupsOneBigStatement);
		// rename the id-, for- and name-tags of all radio button groups
		input1      = div_page.find('#insert_more_arguments');
		input2      = div_page.find('#insert_one_argument');
		input3      = div_page.find('#insert_dont_care');
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

		for (i = 0; i < splitted.length; i++) {
			list.append($('<li>').text(topic + ' ' + splitted[i] + '.'));
			infix = i == 0 ? '' : ('<em>' + _t_discussion(andAtTheSameTime) + '</em> ' + connection + ' ');
			bigText += ' ' + infix + splitted[i];
		}

		bigTextSpan.html(new Helper().startWithUpperCase(bigText) + '.');

		return div_page;
	};

	/**
	 *
	 * @param parsedData
	 * @param callbackid
	 * @param type
	 */
	this.setStatementsAsProposal = function (parsedData, callbackid, type){
		var callbackElement = $('#' + callbackid);
		var uneditted_value;
		if (type == fuzzy_start_premise)        $('#' + proposalPremiseListGroupId).empty();
		else if (type == fuzzy_start_statement) $('#' + proposalStatementListGroupId).empty();
		else if (type == fuzzy_add_reason)      $('#' + proposalPremiseListGroupId).empty();
		else if (type == fuzzy_statement_popup) $('#' + proposalEditListGroupId).empty();
		else if (type == fuzzy_find_user)       $('#' + proposalUserListGroupId).empty();

		// do we have values ?
		if (parsedData.length == 0){
			return;
		}

		var token, button, span_dist, span_text, distance, index, text, img;
		callbackElement.focus();

		$.each(parsedData.values, function (key, val) {
			distance = parseInt(val.distance);
			index = val.index;

			token = callbackElement.val();
			//var pos = val.toLocaleLowerCase().indexOf(token.toLocaleLowerCase()), newpos = 0, start = 0;

			// make all tokens bold
			uneditted_value = val.text;
			// replacement from http://stackoverflow.com/a/280805/2648872
			text = val.text.replace( new RegExp( "(" + (token + '').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1") + ")" , 'gi' ), "</strong>$1<strong>" );
			text = '<strong>' + text;

			button = $('<button>')
				.attr('type', 'button')
				.attr('class', 'list-group-item')
				.attr('id', 'proposal_' + index)
				.attr('text', uneditted_value)
				.hover(function(){$(this).addClass('active');},
					   function(){ $(this).removeClass('active');});
			span_dist = $('<span>').attr('class', 'badge').text(parsedData.distance_name + ' ' + distance);
			span_text = $('<span>').attr('id', 'proposal_' + index + '_text').html(text);
			img = $('<img>').addClass('preload-image').addClass('img-circle').attr('style', 'height: 20pt; margin-right: 1em;').attr('src', val.avatar);
			if (type == fuzzy_find_user)
				button.append(img).append(span_text);
			else
				button.append(img).append(span_dist).append(span_text);
			button.click(function(){
				callbackElement.val($(this).attr('text'));
				$('#' + proposalStatementListGroupId).empty();
				$('#' + proposalPremiseListGroupId).empty();
				$('#' + proposalEditListGroupId).empty(); // list with elements should be after the callbacker
				$('#' + proposalUserListGroupId).empty();
			});
			
			if (type == fuzzy_start_premise)        $('#' + proposalPremiseListGroupId).append(button);
			else if (type == fuzzy_start_statement) $('#' + proposalStatementListGroupId).append(button);
			else if (type == fuzzy_add_reason)      $('#' + proposalPremiseListGroupId).append(button);
			else if (type == fuzzy_statement_popup) $('#' + proposalEditListGroupId).append(button);
			else if (type == fuzzy_find_user)       $('#' + proposalUserListGroupId).append(button);
		});
	};
	
	/**
	 * Opens the edit statements popup
	 * @param statements_uids
	 */
	this.showEditStatementsPopup = function (statements_uids) {
		var input_space = $('#' + popupEditStatementInputSpaceId);
		var ajaxHandler = new AjaxDiscussionHandler();
		$('#' + popupEditStatementId).modal('show');
		input_space.empty();
		$('#' + popupEditStatementLogfileSpaceId).empty();
		$('#' + proposalEditListGroupId).empty();
		$('#' + popupEditStatementErrorDescriptionId).text('');
		$('#' + popupEditStatementSuccessDescriptionId).text('');
		$('#' + popupEditStatementInfoDescriptionId).text('');
		$('#' + popupEditStatementSubmitButtonId).addClass('disabled');
		
		// getting logfile
		ajaxHandler.getLogfileForStatements(statements_uids);
		
		// add inputs
		$.each(statements_uids, function (index, value){
			var statement = $('#' + value).text().trim().replace(/\s+/g, ' ');
			var input = $('<input>')
				.addClass('form-control')
				.attr('id', 'popup-edit-statement-input-' + index)
				.attr('name', 'popup-edit-statement-input-' + index)
				.attr('type', text)
				.attr('placeholder', statement)
				.attr('data-statement-uid', value)
				.val(statement);
			input_space.append(input);
		});
		
		// gui for editing statements
		var helper = new Helper();
		input_space.find('input').each(function(){
			$(this).keyup(function () {
				var oem = $(this).attr('placeholder');
				var now = $(this).val();
				var id = $(this).attr('id');
				var statement_uid = $(this).data('statement-uid');
				
				// reduce noise
				var levensthein = helper.levensthein(oem, now);
				$('#' + popupEditStatementInfoDescriptionId).text(levensthein < 5 ? _t_discussion(pleaseEditAtLeast) : '');
				
				if (now && oem && now.toLowerCase() == oem.toLowerCase() && levensthein < 5)
					$('#' + popupEditStatementSubmitButtonId).addClass('disabled');
				else
					$('#' + popupEditStatementSubmitButtonId).removeClass('disabled');
				
					
				new Helper().delay(function () {
					ajaxHandler.fuzzySearch(now,
						id,
						fuzzy_statement_popup,
						statement_uid);
				}, 200);
			})
		});
	};
	
	/**
	 *
	 */
	this.hideAndClearEditStatementsPopup = function(){
		$('#' + popupEditStatementId).modal('hide');
		$('#' + popupEditStatementLogfileSpaceId).empty();
		$('#' + popupEditStatementInputSpaceId).empty();
	};

	/**
	 * Display url sharing popup
	 */
	this.showUrlSharingPopup = function () {
		$('#' + popupUrlSharingId).modal('show');
		new AjaxDiscussionHandler().getShortenUrl(window.location);
		//$('#' + popupUrlSharingInputId).val(window.location);
	};

	/**
	 * Display url sharing popup
	 */
	this.showGeneratePasswordPopup = function () {
		$('#' + popupGeneratePasswordId).modal('show');
		$('#' + popupGeneratePasswordCloseButtonId).click(function(){
			$('#' + popupGeneratePasswordId).modal('hide');
		});
		$('#' + popupLoginCloseButton).click(function(){
			$('#' + popupGeneratePasswordId).modal('hide');
		});
	};

	/**
	 * Displays add topic plugin
	 *
	 * @param callbackFunctionOnDone
	 */
	this.showAddTopicPopup = function (callbackFunctionOnDone){
		$('#popup-add-topic').modal('show');
		$('#popup-add-topic-accept-btn').click(function () {
			var info = $('#popup-add-topic-info-input').val(),
				title = $('#popup-add-topic-title-input').val(),
				lang = $('#popup-add-topic-lang-input').find('input[type="radio"]:checked').attr('id');
			new AjaxDiscussionHandler().sendNewIssue(info, title, lang, callbackFunctionOnDone);
		});
		$('#popup-add-topic-refuse-btn').click(function () {
			$('#popup-add-topic').modal('hide');
		});
	};
	
	/**
	 *
	 * @param uid
	 * @param is_argument
	 */
	this.showFlagStatementPopup = function(uid, is_argument){
		var popup = $('#popup-flag-statement');
		if (is_argument){
			popup.find('.statement_text').hide();
			popup.find('.argument_text').show();
		} else {
			popup.find('.statement_text').show();
			popup.find('.argument_text').hide();
		}
		popup.modal('show');
		popup.on('hide.bs.modal', function () {
			popup.find('input').off('click').unbind('click');
		});
		popup.find('input').click(function () {
			var reason = $(this).attr('value');
			new AjaxMainHandler().ajaxFlagArgumentOrStatement(uid, reason, is_argument);
			popup.find('input').prop( 'checked', false );
			popup.modal('hide');
		});
	};
	
	/**
	 *
	 * @param uid
	 */
	this.showFlagArgumentPopup = function(uid){
		var popup = $('#popup-flag-argument');
		// var text = $('.triangle-l:last-child .triangle-content').text();
		
		// clean text
		// cut the part after <br><br>
		var text = $('.triangle-l:last-child .triangle-content').html();
		text = text.substr(0, text.indexOf('<br>'));
		// cut all spans
		while (text.indexOf('</span>') != -1)
			text = text.replace('</span>', '');
		while (text.indexOf('<span') != -1)
			text = text.substr(0, text.indexOf('<span')) + text.substr(text.indexOf('>') + 1);
		
		$('#popup-flag-argument-text').text(text);
		popup.modal('show');
		popup.on('hide.bs.modal', function () {
			popup.find('input').off('click').unbind('click');
		});
		popup.find('input').click(function () {
			if ($(this).data('special') === 'undercut'){
				$('#item_undercut').click();
				
			} else if ($(this).data('special') === 'argument'){
				$('#popup-flag-statement-text').text(text);
				new GuiHandler().showFlagStatementPopup(uid, true);
				
			} else {
				new GuiHandler().showFlagStatementPopup($(this).attr('id'), false);
				$('#popup-flag-statement-text').text($(this).next().find('em').text());
			}
			popup.find('input').prop('checked', false);
			popup.modal('hide');
		});
		
		// pretty stuff on hovering
		popup.find('input').each(function(){
			if ($(this).data('special') === '') {
				var current = $(this).next().find('em').text().trim();
				$(this).hover(function () {
					var modded_text = text.replace( new RegExp( "(" + (current + '').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1") + ")" , 'gi' ), "<span class='text-primary'>$1</span>" );
					$('#popup-flag-argument-text').html(modded_text);
					$(this).next().find('em').html("<span class='text-primary'>" + current + "</span>");
				}, function () {
					$('#popup-flag-argument-text').text(text);
					$(this).next().find('em').html(current);
				});
			}
		});
		popup.find('label').each(function(){
			if ($(this).prev().data('special') === '') {
				var current = $(this).find('em').text().trim();
				$(this).hover(function () {
					var modded_text = text.replace( new RegExp( "(" + (current + '').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1") + ")" , 'gi' ), "<span class='text-primary'>$1</span>" );
					$('#popup-flag-argument-text').html(modded_text);
					$(this).find('em').html("<span class='text-primary'>" + current + "</span>");
				}, function () {
					$('#popup-flag-argument-text').text(text);
					$(this).find('em').text(current);
				});
			}
		});
	};
	
	/**
	 *
	 * @param uid
	 * @param is_argument
	 */
	this.showDeleteContentPopup = function(uid, is_argument){
		var popup = $('#popup-delete-content');
		popup.modal('show');
		
		$('#popup-delete-content-submit').click(function(){
			new AjaxDiscussionHandler().revokeContent(uid, is_argument);
		});
		
		$('#popup-delete-content-close').click(function(){
			popup.modal('hide');
		});
	};
	
     /**
	 * Opens the edit issues popup
	 */
	this.showEditIssuesPopup = function () {
		var table, trTitle,trInfo, td_title, td_info, td_buttons, helper = new Helper(), ids = [];
		$('#' + popupEditIssueId).modal('show');
		$('#' + popupEditIssueWarning).hide();
		// top row
		table = $('<table>')
			.attr('class', 'table table-condensed table-hover')
			.attr('border', '0')
			.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;');
		td_title = $('<td>').html('<strong>' + _t_discussion(text) + '</strong>').css('text-align', 'center');
		td_info = $('<td>').html('<strong>' + _t_discussion(text) + '</strong>').css('text-align', 'center');
		td_buttons = $('<td>').html('<strong>' + _t_discussion(options) + '</strong>').css('text-align', 'right');
		trTitle.append(td_title);
		trInfo.append((td_info).append(td_buttons));
		table.append((trTitle).append(trInfo));

		$('#' + popupEditIssueContentId).empty().append(table);
		$('#' + popupEditTitleTextareaId).hide();
		$('#' + popupEditTitleDescriptionId).hide();
		$('#' + popupEditInfoTextareaId).hide();
		$('#' + popupEditInfoDescriptionId).hide();
		$('#' + popupEditIssueSubmitButtonId).hide();
		$('#' + proposalEditListGroupId).empty();
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
		$.each(jsonData, function( key, value ) {
			if (key == 'error'){
				return true;
			}
			var table, tr, tbody, thead;
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
			
			var counter = 0;
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
		
		if (!at_least_one_history){
			space.hide();
			space.prev().hide();
			view.show();
		} else {
			hide.show();
		}
		
		view.click(function(){
			space.show();
			space.prev().show();
			hide.show();
			view.hide();
		});
		
		hide.click(function(){
			space.hide();
			space.prev().hide();
			hide.hide();
			view.show();
		});
	};

	/**
	 * Closes the popup and deletes all of its content
	 */
	this.hideAndClearUrlSharingPopup = function () {
		$('#' + popupUrlSharingId).modal('hide');
		$('#' + popupUrlSharingInputId).val('');
	};

	/**
	 * Hides error description
	 */
	this.hideErrorDescription = function(){
		$('#' + discussionErrorDescriptionId).html('');
		$('#' + discussionErrorDescriptionSpaceId).hide();
	};

	/**
	 * Hides success description
	 */
	this.hideSuccessDescription = function(){
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
	this.getAlertIntoDialogNoDecisions = function(){
		var div, strong, span;
		div = $('<div>').attr('class', 'alert alert-dismissible alert-info');
		strong = $('<strong>').text('Ohh...! ');
		span = $('<span>').text(_t_discussion(noDecisionstaken));
		div.append(strong).append(span);
		return div;
	};
	
	/**
	 *
	 * @param list
	 */
	this.hoverInputListOf = function(list){
		list.find('input').each(function(){
			$(this).hover(function(){
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prop('checked', true);
				}
			}, function(){
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prop('checked', false);
				}
			})
		});
		list.find('label').each(function(){
			$(this).hover(function(){
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prev().prop('checked', true);
				}
			}, function(){
				if (!($('#' + addPremiseContainerId).is(':visible') || $('#' + addStatementContainerId).is(':visible'))) {
					$(this).prev().prop('checked', false);
				}
			})
		});
	}
}
