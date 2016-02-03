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
		if (parsedData.status == '0'){
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
		} else if (parsedData.status == '0'){
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
		if (parsedData.status == '1'){
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
	this.callbackIfDoneFuzzySearch = function (data, callbackid, type){
		var parsedData = $.parseJSON(data);
		// if there is no returned data, we will clean the list
		if (Object.keys(parsedData).length == 0){
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
	this.sendStatement = function (text, conclusion, supportive, arg, relation, type){
		if (text.length == 0){
			new GuiHandler().setErrorDescription(_t(inputEmpty));
		} else{
			// handle case 'hello and '
			if ((type == 0 || type == 1) && text.toLocaleLowerCase().indexOf(' ' + _t(and) + ' ') != -1){
				var splitted = text.split(' ' + _t(and) + ' '),
					list = $('<ul>').attr({'id': 'insert_statements_options', 'style': 'list-style-type: none;'}),
					input, label, li, i;
				for (i=0; i<splitted.length; i++) {
					if (splitted[i].replace(' ','').length() > 0) {
						li = $('<li>');
						input = $('<input>').attr({
							'id': 'insert_st_' + i,
							'type': 'radio',
							'name': 'insert_something_group'
						});
						label = $('<label>').attr('for', 'insert_st_' + i).text(splitted[i]);
						li.append(input);
						li.append(label);
						list.append(li);
					}
				}

				list = '... but you have used the word and.<br><br>' + new Helper().getFullHtmlTextOf(list);
				displayConfirmationDialogWithoutCancelAndFunction('It may seems not obvious...', list);

				$('#' + popupConfirmDialogAcceptBtn).text('Cancel');
				$('#' + popupConfirmDialogId + ' .modal-body').addClass('lead');
				$('#insert_statements_options' + ' li').hover(function(){$(this).toggleClass('text-hover')});
				$('#insert_statements_options' + ' input').click(function() {
					alert('send ' + $(this).next().text());
				});

			} else if (type==0){
				new AjaxSiteHandler().sendNewPremiseForArgument(arg, relation, supportive, text);
			} else if (type==1){
				new AjaxSiteHandler().sendNewStartStatement(text);
			} else if (type==2){
				new AjaxSiteHandler().sendNewStartPremise(text, conclusion, supportive);
			}
		}
	};

	this.appendAddPremiseRow = function(image){
		var div = $('<div>'),
		h5 = $('<h5>').attr({'stlye': 'float:left; line-height:60px; text-align:center;'}).text('Because...'),
		input = $('<input>').attr({'type': 'text', 'class': 'form-control', 'autocomplete': 'off', 'placeholder':'example: There is some reason!'}),
		img = $('<img>').attr({'class': 'icon-add-premise icon-badge', 'alt': 'icon-add', 'src': mainpage + 'static/images/icon_pplus.png', 'style': 'height: 30px; padding-left: 1em'}),
		br = $('<br>');
		div.append(h5).append(input).append(img);
		$('#add-premise-container-body').append(br).append(div);
		img.click(function(){
			new InteractionHandler().appendAddPremiseRow($(this));
		});
		image.attr('src', mainpage + 'static/images/icon_pminus.png');
		image.off('click').click(function(){
			$(this).parent().remove();
		});
	}
}