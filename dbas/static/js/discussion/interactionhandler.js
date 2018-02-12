/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function InteractionHandler() {
	'use strict';

	/**
	 * Callback, when the logfile was fetched
	 * @param data of the ajax request
	 */
	this.callbackIfDoneForGettingLogfile = function (data) {
		// status is the length of the content
		var description = $('#' + popupEditStatementErrorDescriptionId);
		if ('info' in data && data.info.length !== 0) {
			description.text(data.error);
			description.removeClass('text-danger');
			description.addClass('text-info');
			$('#' + popupEditStatementLogfileSpaceId).prev().hide();
		} else {
			new GuiHandler().showLogfileOfPremisegroup(data);
		}
	};

	/**
	 * Callback, when a correcture could be send
	 * @param data of the ajax request
	 * @param statements_uids
	 */
	this.callbackIfDoneForSendCorrectureOfStatement = function (data, statements_uids) {
		if (data.info.length !== 0) {
			setGlobalInfoHandler('Ohh!', data.info);
		} else {
			setGlobalSuccessHandler('Yeah!', _t_discussion(proposalsWereForwarded));
			new PopupHandler().hideAndClearEditStatementsPopup();
			// find the list element and manipulate the edit buttons
			var parent_statement = $('#' + statements_uids[0]).parent();
			parent_statement.find('#item-edit-disabled-hidden-wrapper').show();
			parent_statement.find('.item-edit').remove();
		}
	};

	/**
	 * Callback for Fuzzy Search
	 * @param data
	 * @param callbackid
	 * @param type
	 * @param reason
	 */
	this.callbackIfDoneFuzzySearch = function (data, callbackid, type, reason) {
		// if there is no returned data, we will clean the list

		if (Object.keys(data).length === 0) {
			$('#' + proposalStatementListGroupId).empty();
			$('#' + proposalPremiseListGroupId).empty();
			$('#' + proposalEditListGroupId).empty();
			$('#' + proposalUserListGroupId).empty();
			$('#' + proposalStatementSearchGroupId).empty();
			$('#proposal-mergesplit-list-group-' + callbackid).empty();
		} else {
			new GuiHandler().setStatementsAsProposal(data, callbackid, type, reason);
		}
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForGettingInfosAboutArgument = function(data){
		var text, element;
		// status is the length of the content
		if (data.error.length !== 0) {
			text = data.error;
			element = $('<p>').html(text);
			displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(messageInfoTitle), element);
			return;
		}

		var author;
		if (data.author !== 'anonymous'){
			var img = '<img class="img-circle" style="height: 1em;" src="' + data.gravatar + '">';
			author = '<a href="' + data.author_url + '">' + img + ' ' + data.author + '</a>';
		} else {
			author = _t_discussion(an_anonymous_user);
		}
		text = _t_discussion(messageInfoStatementCreatedBy) + ' ' + author;
		text += ' (' + data.timestamp + ') ';
		text += _t_discussion(messageInfoCurrentlySupported) + ' ' + data.vote_count + ' ';
		text +=_t_discussion(messageInfoParticipant) + '.';

		var users_array = [];
		$.each(data.supporter, function (index, val) {
			users_array.push({
				'avatar_url': data.gravatars[val],
				'nickname': val,
				'public_profile_url': data.public_page[val]
			});
		});

		var gh = new GuiHandler();
		var tbody = $('<tbody>');
		var rows = gh.createUserRowsForOpinionDialog(users_array);
		$.each( rows, function( key, value ) {
			tbody.append(value);
		});

		var body = gh.closePrepareTableForOpinionDialog(data.supporter, gh, text, tbody);

		displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(messageInfoTitle), body);
		$('#' + popupConfirmDialogId).find('.modal-dialog').addClass('modal-lg').on('hidden.bs.modal', function () {
			$(this).removeClass('modal-lg');
		});

		setTimeout(function(){
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
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForSendNewIssue = function(data){
		$('#popup-add-topic').modal('hide');
		var li = $('<li>').addClass('enabled'),
			a = $('<a>').attr('href', data.issue.url).attr('value', data.issue.title),
			spanTitle = $('<span>').text(data.issue.title),
			spanBadge = $('<span>').addClass('badge').attr('style', 'float: right; margin-left: 1em;').text(data.issue.arg_count),
			divider = $('#' + issueDropdownListID).find('li.divider');
		li.append(a.append(spanTitle).append(spanBadge));
		if (divider.length > 0) {
			li.insertBefore(divider);
		}
		setGlobalSuccessHandler('Yeah!', _t(dataAdded));
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForSendNewIssueTable = function(data){
	var parsedData = $.parseJSON(data);

        if (parsedData.error.length === 0) {
			$('#popup-add-topic').modal('hide');

			var space = $('#issue-table');

			var tr = $('<tr>')
					.append($('<td>').html( parsedData.issue.uid ))
					.append($('<td>').html( parsedData.issue.title ))
					.append($('<td>').html( parsedData.issue.info ))
					.append($('<td>').html( parsedData.issue.date ))
			        .append($('<td>').append($('<a>').attr('target', '_blank').attr('href', parsedData.issue.public_url).text(parsedData.issue.author)))
			        .append($('<td>').append( $('<a>').attr('href', '#').attr('class' , 'btn btn-info btn-lg').append($('<i>').attr('class', 'fa fa-pencil-square-o'))));
           	 space.append(tr);
		} else {
			$('#popup-add-topic-error-text').text(parsedData.error);
			$('#popup-add-topic-error').show();
			setTimeout(function(){
				$('#popup-add-topic-error').hide();
			}, 2500);
		}
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneRevokeContent = function(data) {
		var parsedData = $.parseJSON(data);

		if (parsedData.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), parsedData.error);
		} else {
			if (parsedData.success) {
				setGlobalSuccessHandler('Yeah!', _t_discussion(dataRemoved) + ' ' + _t_discussion(yourAreNotTheAuthorOfThisAnymore));
			} else {
				setGlobalSuccessHandler('Yeah!', _t_discussion(contentWillBeRevoked));
			}
		}
	};

	/**
	 *
	 * @param data
	 * @param is_argument
	 */
	this.callbackIfDoneForGettingMoreInfosAboutOpinion = function(data, is_argument){
		var users_array, popup_table;

		if (data.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), data.error);
			return;
		}
		if (data.info.length !== 0) {
			setGlobalInfoHandler('Hey', data.info);
			return;
		}

		var gh = new GuiHandler();
		var tbody = $('<tbody>');
		var span = is_argument? $('<span>').text(data.opinions.message) : $('<span>').text(data.opinions[0].message);

		users_array = is_argument ? data.opinions.users : data.opinions[0].users;
		var rows = gh.createUserRowsForOpinionDialog(users_array);
		$.each( rows, function( key, value ) {
			tbody.append(value);
		});

		var body = gh.closePrepareTableForOpinionDialog(users_array, gh, span, tbody);

		displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(usersWithSameOpinion), body);
		$('#' + popupConfirmDialogId).find('.modal-dialog').addClass('modal-lg').on('hidden.bs.modal', function (e) {
			$(this).removeClass('modal-lg');
		});
		setTimeout(function(){
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

	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForGettingReferences = function(data){
		if (data.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), data.error);
		} else {
			new PopupHandler().showReferencesPopup(data);
		}
	};

	/**
	 *
	 * @param toggle_element
	 * @param data
	 */
	this.callbackForSetAvailabilityOfDiscussion = function(toggle_element, data){
		if (data.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), data.error);
		} else {
			setGlobalSuccessHandler('Yeah!', _t(discussionsPropertySet));
		}
	};

	/**
	 *
	 * @param position
	 * @param reason
	 */
	this.sendArgument = function(position, reason){
		if (position.length === 0 || reason.length === 0) {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(inputEmpty));
		} else {
			$('#' + addStatementErrorContainer).hide();
			new AjaxDiscussionHandler().sendNewStartArgument(position, reason);
		}
	};

	/**
	 *
	 * @param t_array
	 * @param conclusion
	 * @param supportive
	 * @param arg
	 * @param relation
	 * @param type
	 */
	this.sendStatement = function (t_array, conclusion, supportive, arg, relation, type) {
		// error on "no text"
		if (t_array.length === 0) {
			$('#' + addPremiseErrorContainer).show();
			$('#' + addPremiseErrorMsg).text(_t(inputEmpty));
		} else {
			var undecided_texts = [], decided_texts = [];
			if ($.isArray(t_array)) {
				for (var i = 0; i < t_array.length; i++) {
					// replace multiple whitespaces
					t_array[i] = t_array[i].replace(/\s\s+/g, ' ');

					// cutting all 'and ' and 'and'
					while (t_array[i].indexOf((_t_discussion(and) + ' '), t_array[i].length - (_t_discussion(and) + ' ').length) !== -1 ||
					t_array[i].indexOf((_t_discussion(and)), t_array[i].length - (_t_discussion(and) ).length) !== -1) {
						if (t_array[i].indexOf((_t_discussion(and) + ' '), t_array[i].length - (_t_discussion(and) + ' ').length) !== -1) {
							t_array[i] = t_array[i].substr(0, t_array[i].length - (_t_discussion(and) + ' ').length);
						} else {
							t_array[i] = t_array[i].substr(0, t_array[i].length - (_t_discussion(and)).length);
						}
					}

					// whitespace at the end
					while (t_array[i].indexOf((' '), t_array[i].length - (' ').length) !== -1) {
						t_array[i] = t_array[i].substr(0, t_array[i].length - (' ').length);
					}

					// sorting the statements, whether they include the keyword 'AND'
					if (t_array[i].toLocaleLowerCase().indexOf(' ' + _t_discussion(and) + ' ') !== -1) {
						undecided_texts.push(t_array[i]);
					} else {
						decided_texts.push(t_array[i]);
					}
				}
			}

			if (undecided_texts.length > 0){
				for (var j=0; j<undecided_texts.length; j++){
					if (undecided_texts[j].match(/\.$/)) {
						undecided_texts[j] = undecided_texts[j].substr(0, undecided_texts[j].length - 1);
					}
				}
				new GuiHandler().showSetStatementContainer(undecided_texts, decided_texts, supportive, type, arg, relation, conclusion);
			} else {
			
				// pack the data
				$.each(t_array, function( index, value ) {
					if ($.type(value) !== "array"){
						t_array[index] = [value];
					}
				});
				
				if (type === fuzzy_start_premise) {
					new AjaxDiscussionHandler().sendNewStartPremise(t_array, conclusion, supportive);
				} else  if (type === fuzzy_add_reason) {
					new AjaxDiscussionHandler().sendNewPremiseForArgument(arg, relation, t_array);
				}
			}
		}
	};
}
