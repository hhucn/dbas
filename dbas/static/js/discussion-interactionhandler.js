/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function InteractionHandler() {
	'use strict';

	/**
	 * Callback, when a new position was send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewStartStatement = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseInternal));
		} else if (parsedData.status == '0') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseTooShort));
		} else {
			$('#' + discussionSpaceId + 'input:last-child').attr('checked', false).prop('checked', false);
			window.location.href = parsedData.url;
		}
	};

	/**
	 * Callback, when new statements were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewPremisesArgument = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseInternal));
		} else if (parsedData.status == '0') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseTooShort));
		} else {
			window.location.href = parsedData.url;
		}
	};

	/**
	 * Callback, when new premises were send
	 * @param data returned data
	 * @param isSupportive
	 */
	this.callbackIfDoneForSendNewStartPremise = function (data, isSupportive) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '0') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseInternal));
		} else if (parsedData.status == '0') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseTooShort));
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
		if (parsedData.status == '0') {
			$('#' + popupEditStatementLogfileSpaceId).text(_t(noCorrections));
		} else {
			$('#' + popupEditStatementLogfileSpaceId).text('');
			new GuiHandler().showStatementCorrectionsInPopup(parsedData.content);
		}
	};

	/**
	 * Callback, when a correcture could be send
	 * @param data of the ajax request
	 * @param element
	 */
	this.callbackIfDoneForSendCorrectureOfStatement = function (data, element) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			$('#' + popupEditStatementErrorDescriptionId).text(_t(noCorrectionsSet));
		} else if (parsedData.status == '0') {
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');
			$('#' + popupEditStatementWarning).show();
			$('#' + popupEditStatementWarningMessage).text(_t(duplicateDialog));
		} else {
			new GuiHandler().updateOfStatementInDiscussion(parsedData, element);
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text(_t(correctionsSet));
		}
	};

	/**
	 * Callback, when a url was shortend
	 * @param data of the ajax request
	 * @param long_url url which should be shortend
	 */
	this.callbackIfDoneForShortenUrl = function (data, long_url) {
		var parsedData = $.parseJSON(data), service;
		if (parsedData.status == '1') {
			service = '<a href="' + parsedData.service_url + '" title="' + parsedData.service + '" target="_blank">' + parsedData.service + '</a>';
			$('#' + popupUrlSharingDescriptionPId).html(_t(feelFreeToShareUrl) + ', ' + _t(shortenedBy) + ' ' + service + ':');
			$('#' + popupUrlSharingInputId).val(parsedData.url);
		} else {
			$('#' + popupUrlSharingDescriptionPId).text(_t(feelFreeToShareUrl) + ":");
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
		} else {
			new GuiHandler().setStatementsAsProposal(parsedData, callbackid, type);
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
		// TODO CLEAR DESIGN
		// TODO CLEAR DESIGN
		// TODO CLEAR DESIGN
		if (text.length == 0) {
			new GuiHandler().setErrorDescription(_t(inputEmpty));
		} else {
			// TODO handle case 'hello and '
			if (type == fuzzy_add_reason || type == fuzzy_start_premise) {
				// for (var i = 0; i < text.length; i++) {
				// 	if (text[i].toLocaleLowerCase().indexOf(' ' + _t(and) + ' ') != -1) {
				// 	}
				// }

				if (text[0].toLocaleLowerCase().indexOf(' ' + _t(and) + ' ') != -1) {

					var splitted = text[0].split(' ' + _t(and) + ' '),
						list = $('<ul>').attr({'id': 'insert_statements_options', 'style': 'list-style-type: none; cursor: pointer;'}),
						listA = $('<ol>').attr({'id': 'insert_statements_options_a'}),
						listB = $('<ol>').attr({'id': 'insert_statements_options_b'}),
						input1, input2, input3,
						label1, label2, label3,
						li1, li2, li3,
						span1, span2, span3,
						tmp, topic = $('#' + addPremiseContainerMainInputIntroId).text(), i;

					for(i=0; i<splitted.length; i++){
						listA.append($('<li>').append($('<span>').text(splitted[i])).append($('<em>').text(' and ')));
					}
					for(i=0; i<splitted.length; i++){
						listB.append($('<li>').append($('<span>').text(splitted[i])).append($('<em>').text(' or ')));
					}
					listA.children().last().children().last().remove();
					listB.children().last().children().last().remove();

					input1 = $('<input>').attr({'id': 'insert_st1_' + i, 'type': 'radio', 'name': 'insert_statements_options' });
					input2 = $('<input>').attr({'id': 'insert_st2_' + i, 'type': 'radio', 'name': 'insert_statements_options' });
					input3 = $('<input>').attr({'id': 'insert_st3_' + i, 'type': 'radio', 'name': 'insert_statements_options' });

					label1 = $('<label>').attr('for', 'insert_st1_' + i).attr('style', 'width: 95%').text('Related statements');
					label2 = $('<label>').attr('for', 'insert_st2_' + i).attr('style', 'width: 95%').text('Independent statements');
					label3 = $('<label>').attr('for', 'insert_st3_' + i).attr('style', 'width: 95%').text('One statement');

					span1 = $('<span>').append($('<span>').text('You think that \'' + topic + '\' holds, if every statement is true:')).append(listA);
					span2 = $('<span>').append($('<span>').text('You think that \'' + topic + '\' holds, if at least one statement is true:')).append(listB);
					span3 = $('<span>').attr('style', 'padding-left: 1em;').text('We do not care about the keyword ').append($('<em>').text(_t(and) + ':').append($('<br>')).append($('<span>').text(splitted[0])));

					li1 = $('<li>').append(input1).append(label1).append($('<br>')).append(span1).append($('<br>'));
					li2 = $('<li>').append(input2).append(label2).append($('<br>')).append(span2).append($('<br>'));
					li3 = $('<li>').append(input3).append(label3).append($('<br>')).append(span3);

					list.append(li1).append(li2).append(li3);

					// topic = topic.substr(0,1).toLocaleLowerCase(). topic.substr(1);
					tmp = '... but you have used the word <em>and</em>. Please select from the list:<br><br>'
						+ new Helper().getFullHtmlTextOf(list);
					displayConfirmationDialogWithoutCancelAndFunction('It may seems not obvious...', tmp);

					$('#' + popupConfirmDialogAcceptBtn).text('Cancel');
					$('#' + popupConfirmDialogId + ' .modal-body').addClass('lead');
					$('#insert_statements_options' + ' li').hover(function () {
						$(this).toggleClass('text-hover')
					});
					$('#insert_statements_options' + ' input').click(function () {
						alert('send ' + $(this).next().text());
					});

					// TODO
					var ul = $('<ul>').attr({'class': 'pager', 'style': 'margin: 0px;'}),
						li_next = $('<li>').addClass('previous').append($('<a>').attr('href', '#').text('← previous')),
						li_prev = $('<li>').addClass('next').append($('<a>').attr('href', '#').text('Next →'));
					// <button id="confirm-dialog-accept-btn" type="button" class="btn btn-default">Cancel</button>
					ul.append(li_prev).append(li_next);
					$('#confirm-dialog-accept-btn').parent().prepend(ul);

				} else if (type == 0) {
					new AjaxSiteHandler().sendNewPremiseForArgument(arg, relation, supportive, text);
				} else if (type == 1) {
					new AjaxSiteHandler().sendNewStartStatement(text);
				} else if (type == 2) {
					new AjaxSiteHandler().sendNewStartPremise(text, conclusion, supportive);
				}
			}
		}
	}
}