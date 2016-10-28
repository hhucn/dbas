/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function InteractionHandler() {
	'use strict';

	/**
	 * Callback, when a new position was send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewStartStatement = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length > 0) {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(parsedData.error);
		} else {
			$('#' + discussionSpaceId + 'input:last-child').prop('checked', false);
			window.location.href = parsedData.url;
		}
	};

	/**
	 * Callback, when new statements were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewPremisesArgument = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length > 0) {
			$('#' + addPremiseErrorContainer).show();
			$('#' + addPremiseErrorMsg).text(parsedData.error);
		} else {
			window.location.href = parsedData.url;
		}
	};

	/**
	 * Callback, when new premises were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewStartPremise = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length > 0) {
			$('#' + addPremiseErrorContainer).show();
			$('#' + addPremiseErrorMsg).text(parsedData.error);
		} else {
			window.location.href = parsedData.url;
		}
	};

	/**
	 * Callback, when the logfile was fetched
	 * @param data of the ajax request
	 */
	this.callbackIfDoneForGettingLogfile = function (data) {
		var parsedData = $.parseJSON(data);
		// status is the length of the content
		if (parsedData.error.length == 0) {
			new GuiHandler().showLogfileOfPremisegroup(parsedData);
		} else {
			$('#' + popupEditStatementErrorDescriptionId).text(parsedData.error);
		}
	};

	/**
	 * Callback, when a correcture could be send
	 * @param data of the ajax request
	 */
	this.callbackIfDoneForSendCorrectureOfStatement = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.error.length != 0) {
			setGlobalErrorHandler(_t_discussion(ohsnap), parsedData.error);
		} else {
			setGlobalSuccessHandler('Yeah!', _t_discussion(proposalsWereForwarded));
			new GuiHandler().hideAndClearEditStatementsPopup();
		}
	};

	/**
	 * Callback, when a url was shortend
	 * @param data of the ajax request
	 * @param long_url url which should be shortend
	 */
	this.callbackIfDoneForShortenUrl = function (data, long_url) {
		var parsedData = $.parseJSON(data), service;
		if (parsedData.error.length == 0) {
			service = '<a href="' + parsedData.service_url + '" title="' + parsedData.service + '" target="_blank">' + parsedData.service + '</a>';
			$('#' + popupUrlSharingDescriptionPId).html(_t_discussion(feelFreeToShareUrl) + ', ' + _t_discussion(shortenedBy) + ' ' + service + ':');
			$('#' + popupUrlSharingInputId).val(parsedData.url).data('short-url', parsedData.url);
		} else {
			$('#' + popupUrlSharingDescriptionPId).text(_t_discussion(feelFreeToShareUrl) + '.');
			$('#' + popupUrlSharingInputId).val(long_url);
		}
	};

	/**
	 * Callback for Fuzzy Search
	 * @param data
	 * @param callbackid
	 * @param type
	 */
	this.callbackIfDoneFuzzySearch = function (data, callbackid, type) {
		var parsedData = $.parseJSON(data);
		// if there is no returned data, we will clean the list

		if (Object.keys(parsedData).length == 0) {
			$('#' + proposalStatementListGroupId).empty();
			$('#' + proposalPremiseListGroupId).empty();
			$('#' + proposalEditListGroupId).empty();
			$('#' + proposalUserListGroupId).empty();
		} else {
			new GuiHandler().setStatementsAsProposal(parsedData, callbackid, type);
		}
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForGettingInfosAboutArgument = function(data){
		var parsedData = $.parseJSON(data), text, element;
		// status is the length of the content
		if (parsedData.error.length == 0) {
			var body = $('<div>'),
				table = $('<table>')
					.attr('class', 'table table-condensed table-hover')
					.attr('border', '0')
					.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;'),
				tr = $('<tr>')
					.append($('<td>').html('<strong>' + _t_discussion(avatar) + '</strong>').css('text-align', 'left'))
					.append($('<td>').html('<strong>' + _t_discussion(nickname) + '</strong>').css('text-align', 'left'))
					.append($('<td>').html('<strong>' + _t_discussion(avatar) + '</strong>').css('text-align', 'left'))
					.append($('<td>').html('<strong>' + _t_discussion(nickname) + '</strong>').css('text-align', 'left')),
				tbody = $('<tbody>'),
				td_nick, td_avatar, stored_td_nick='', stored_td_avatar='', i=0;
			
			if (Object.keys(parsedData.supporter).length > 1)
				tr.append($('<td>').html('<strong>' + _t_discussion(avatar) + '</strong>').css('text-align', 'left'))
					.append($('<td>').html('<strong>' + _t_discussion(nickname) + '</strong>').css('text-align', 'left'));

			// supporters = parsedData.supporter.join(', ');
			text = parsedData.text + '<br><br>';
			text += _t_discussion(messageInfoStatementCreatedBy) + ' ' + parsedData.author  + ', ';
			text += parsedData.timestamp + '.<br>';
			text += _t_discussion(messageInfoCurrentlySupported) + ' ' + parsedData.vote_count + ' ';
			text +=_t_discussion(messageInfoParticipant) + (parsedData.vote_count==1 ? '' : _t_discussion(messageInfoParticipantPl)) + '.';

			if (parsedData.vote_count>0) {
				$.each(parsedData.supporter, function(index, nick){
					td_nick = $('<td>').append($('<a>').attr('target', '_blank').attr('href', parsedData.public_page[nick]).text(nick));
					td_avatar = $('<td>').html('<img class="preload-image" style="height: 40%;" src="' + parsedData.gravatars[nick] + '"></td>');
					if (i==1){
						i=0;
						tbody.append($('<tr>').append(stored_td_avatar).append(stored_td_nick).append(td_avatar).append(td_nick));
					} else {
						i=1;
						stored_td_nick = td_nick;
						stored_td_avatar = td_avatar;
					}
				});
				if (i==1)
					tbody.append($('<tr>').append(stored_td_avatar).append(stored_td_nick));
			}

			if (tbody.find('tr').length==0)
				body.append(new GuiHandler().getAlertIntoDialogNoDecisions());
			else
				body.append(table.append(tbody));

			body.append(text).append(table.append(tbody));
			displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(messageInfoTitle), body);
			$('#' + popupConfirmDialogId).find('.modal-dialog');//.addClass('modal-sm');
			new Helper().delay(function(){
				var popup_table = $('#' + popupConfirmDialogId).find('.modal-body div');
				if ($( window ).height() > 400 && popup_table.outerHeight(true) > $( window ).height()) {
					popup_table.slimScroll({
						position: 'right',
						railVisible: true,
						alwaysVisible: true,
						height: ($( window ).height() / 3 * 2) + 'px'
					});
				}
			}, 300);
		} else {
			text = parsedData.error;
			element = $('<p>').html(text);
			displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(messageInfoTitle), element);
		}
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForSendNewIssue = function(data){
		var parsedData = $.parseJSON(data);

		if (parsedData.error.length == 0) {
			$('#popup-add-topic').modal('hide');
			var li = $('<li>').addClass('enabled'),
				a = $('<a>').attr('href', parsedData.issue.url).attr('value', parsedData.issue.title),
				spanTitle = $('<span>').text(parsedData.issue.title),
				spanBadge = $('<span>').addClass('badge').attr('style', 'float: right; margin-left: 1em;').text(parsedData.issue.arg_count),
				divider = $('#' + issueDropdownListID).find('li.divider');
			li.append(a.append(spanTitle).append(spanBadge));
			if (divider.length>0){
				li.insertBefore(divider);
			}
		} else {
			$('#popup-add-topic-error-text').text(parsedData.error);
			$('#popup-add-topic-error').show();
			new Helper().delay(function(){
				$('#popup-add-topic-error').hide();
			}, 2500);
		}
	};
	
	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForSendNewIssueTable = function(data){
	var parsedData = $.parseJSON(data);

        if (parsedData.error.length == 0) {
			$('#popup-add-topic').modal('hide');

			var space = $('#issue-table');

			var tr = $('<tr>')
					.append($('<td>').html( parsedData.issue.uid ))
					.append($('<td>').html( parsedData.issue.title ))
					.append($('<td>').html( parsedData.issue.info ))
					.append($('<td>').html( parsedData.issue.date ))
			        .append($('<td>').append($('<a>').attr('target', '_blank').attr('href', parsedData.issue.public_url).text(parsedData.issue.author)))
			        .append($('<td>').append( $('<a>').attr('href', '#').attr('class' , 'btn btn-info btn-lg').append($('<span>').attr('class', 'glyphicon glyphicon-edit'))));
           	 space.append(tr);
		} else {
			$('#popup-add-topic-error-text').text(parsedData.error);
			$('#popup-add-topic-error').show();
			new Helper().delay(function(){
				$('#popup-add-topic-error').hide();
			}, 2500);
		}
	};
	
	/**
	 *
	 * @param data
	 * @param is_argument
	 */
	this.callbackIfDoneRevokeContent = function(data, is_argument) {
		var parsedData = $.parseJSON(data);
		
		if (parsedData.error.length != 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else {
			if (is_argument)
				setGlobalSuccessHandler('Yeah', _t_discussion(dataRemoved));
			else
				window.location.reload();
		}
	};

	/**
	 *
	 * @param data
	 * @param is_argument
	 */
	this.callbackIfDoneForGettingMoreInfosAboutOpinion = function(data, is_argument){
		var parsedData = $.parseJSON(data), users_array, popup_table;

		if (parsedData.error.length == 0) {
			var body = $('<div>'),
				span = is_argument? $('<span>').text(parsedData.opinions.message) : $('<span>').text(parsedData.opinions[0].message),
				table = $('<table>')
					.attr('class', 'table table-condensed table-hover')
					.attr('border', '0')
					.attr('style', 'border-collapse: separate; border-spacing: 5px 5px;'),
				tr = $('<tr>')
					.append($('<td>').html('<strong>' + _t_discussion(avatar) + '</strong>').css('text-align', 'left'))
					.append($('<td>').html('<strong>' + _t_discussion(nickname) + '</strong>').css('text-align', 'left')),
				tbody = $('<tbody>'),
				td_nick, td_avatar, stored_td_nick='', stored_td_avatar='', j=0;

			users_array = is_argument ? parsedData.opinions.users : parsedData.opinions[0].users;
			if (Object.keys(users_array).length > 1)
				tr.append($('<td>').html('<strong>' + _t_discussion(avatar) + '</strong>').css('text-align', 'left'))
					.append($('<td>').html('<strong>' + _t_discussion(nickname) + '</strong>').css('text-align', 'left'));
			table.append($('<thead>').append(tr));

			$.each(users_array, function (i, val) {
				td_nick = $('<td>').append($('<a>').attr('target', '_blank').attr('href', val.public_profile_url).text(val.nickname));
				td_avatar = $('<td>').html('<img class="preload-image" style="height: 40%;" src="' + val.avatar_url + '"></td>');
				if (j==1){
					j=0;
					tbody.append($('<tr>').append(stored_td_avatar).append(stored_td_nick).append(td_avatar).append(td_nick));
				} else {
					j=1;
					stored_td_nick = td_nick;
					stored_td_avatar = td_avatar;
				}
			});
			if (j==1)
				tbody.append($('<tr>').append(stored_td_avatar).append(stored_td_nick));

			if (tbody.find('tr').length==0)
				body.append(new GuiHandler().getAlertIntoDialogNoDecisions());
			else
				body.append(span).append(table.append(tbody));

			displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(usersWithSameOpinion), body);
			$('#' + popupConfirmDialogId).find('.modal-dialog');//.addClass('modal-sm');
			new Helper().delay(function(){
				popup_table = $('#' + popupConfirmDialogId).find('.modal-body div');
				if ($( window ).height() > 400 && popup_table.outerHeight(true) > $( window ).height()) {
					popup_table.slimScroll({
						position: 'right',
						railVisible: true,
						alwaysVisible: true,
						height: ($( window ).height() / 3 * 2) + 'px'
					});
				}
			}, 300);
		} else {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		}
	};

	/**
	 *
	 * @param text
	 * @param conclusion
	 * @param supportive
	 * @param arg
	 * @param relation
	 * @param type
	 */
	this.sendStatement = function (text, conclusion, supportive, arg, relation, type) {
		// error on "no text"
		if (text.length == 0) {
			if (type==fuzzy_start_statement){
				$('#' + addStatementErrorContainer).show();
				$('#' + addStatementErrorMsg).text(_t(inputEmpty));
			} else {
				$('#' + addPremiseErrorContainer).show();
				$('#' + addPremiseErrorMsg).text(_t(inputEmpty));
			}
		} else {
			var undecided_texts = [], decided_texts = [];
			if ($.isArray(text)) {
				for (var i = 0; i < text.length; i++) {
					// replace multiple whitespaces
					text[i] = text[i].replace(/\s\s+/g, ' ');

					// cutting all 'and ' and 'and'
					while (text[i].indexOf((_t_discussion(and) + ' '), text[i].length - (_t_discussion(and) + ' ').length) !== -1 ||
					text[i].indexOf((_t_discussion(and)), text[i].length - (_t_discussion(and) ).length) !== -1) {
						if (text[i].indexOf((_t_discussion(and) + ' '), text[i].length - (_t_discussion(and) + ' ').length) !== -1)
							text[i] = text[i].substr(0, text[i].length - (_t_discussion(and) + ' ').length);
						else
							text[i] = text[i].substr(0, text[i].length - (_t_discussion(and)).length);
					}

					// whitespace at the end
					while (text[i].indexOf((' '), text[i].length - (' ').length) !== -1)
						text[i] = text[i].substr(0, text[i].length - (' ').length);

					// sorting the statements, whether they include the keyword 'AND'
					if (text[i].toLocaleLowerCase().indexOf(' ' + _t_discussion(and) + ' ') != -1)
						undecided_texts.push(text[i]);
					else
						decided_texts.push(text[i]);
				}
			}

			if (undecided_texts.length > 0){
				var helper = new Helper();
				for (var j=0; j<undecided_texts.length; j++){
					undecided_texts[j] = helper.startWithLowerCase(undecided_texts[j]);
					if (undecided_texts[j].match(/\.$/))
						undecided_texts[j] = undecided_texts[j].substr(0, undecided_texts[j].length -1)
				}
				new GuiHandler().showSetStatementContainer(undecided_texts, decided_texts, supportive, type, arg, relation, conclusion);
			} else {
				if (type == fuzzy_start_statement) {
					if (decided_texts.length > 0)
						alert("TODO: more than one decided text");
					else
						new AjaxDiscussionHandler().sendNewStartStatement(text);
				} else if (type == fuzzy_start_premise) {
					new AjaxDiscussionHandler().sendNewStartPremise(text, conclusion, supportive);
				} else  if (type == fuzzy_add_reason) {
					new AjaxDiscussionHandler().sendNewPremiseForArgument(arg, relation, text);
				}
			}
		}
	}
}
