/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function InteractionHandler() {
	'use strict';

	/**
	 * Handler when an start statement was clicked
	 * @param id of the button
	 */
	this.statementButtonWasClicked = function (id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		// new AjaxSiteHandler().getPremisseForStatement(id);
		new AjaxSiteHandler().callSiteForGetPremisseForStatement(id);
	};

	/**
	 * Handler when an start premisse was clicked
	 * @param pgroup_id
	 * @param conclusion_id
	 */
	this.premisseButtonWasClicked = function (pgroup_id, conclusion_id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		// new AjaxSiteHandler().getReplyForPremisseGroup(id);
		new AjaxSiteHandler().callSiteForGetReplyForPremisseGroup(pgroup_id, conclusion_id);
	};

	/**
	 * Handler when an relation button was clicked
	 * @param id of the button
	 * @param relation of the button
	 * @param confrontation_uid
	 */
	this.relationButtonWasClicked = function (id, relation, confrontation_uid) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionsDescriptionId).empty();
		new AjaxSiteHandler().callSiteForHandleReplyForResponseOfConfrontation(id, relation, confrontation_uid);
	};

	/**
	 * Handler when an argument button was clicked
	 * @param long_id
	 * @param pgroup_id
	 */
	this.argumentButtonWasClicked = function (long_id, pgroup_id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionsDescriptionId).empty();
		// new AjaxSiteHandler().getReplyForArgument(id);
		new AjaxSiteHandler().callSiteForGetReplyForArgument(long_id, pgroup_id);
	};

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 */
	this.radioButtonChanged = function () {
		var guiHandler = new GuiHandler(), text, isStart = $('#' + discussionSpaceId + ' ul li input').hasClass('start'), addReasonButton = $('#' + addReasonButtonId);
		// did we have an "add statement" action or just "argumentation" ?
		if (addReasonButton.is(':checked')) {

			guiHandler.displayHowToWriteTextPopup();

			// get the second child, which is the label
			text = addReasonButton.parent().children().eq(1).text();
			if (text.indexOf(_t(newConclusionRadioButtonText)) >= 0 || text.indexOf(_t(firstConclusionRadioButtonText)) >= 0) {
				// statement
				guiHandler.setDisplayStylesOfAddStatementContainer(true, isStart, false, true, false);
			} else if (text.indexOf(_t(addArgumentRadioButtonText)) >= 0 || text.indexOf(_t(addPremisseRadioButtonText)) >= 0) {
				// argument
				guiHandler.setDisplayStylesOfAddStatementContainer(true, isStart, false, false, true);
			} else {
				// premisse
				guiHandler.setDisplayStylesOfAddStatementContainer(true, isStart, true, false, false);
			}
		} else {
			guiHandler.setDisplayStylesOfAddStatementContainer(false, isStart, false, true, false);

			this.radioButtonWasChoosen();
			guiHandler.setVisibilityOfDisplayStyleContainer(false, ''); // TODO setVisibilityOfDisplayStyleContainer
			$('#' + islandViewContainerId).fadeOut('slow');
		}
	};

	/**
	 * Segmented button for display style was pressed
	 * @param buttonId current id
	 */
	this.styleButtonChanged = function (buttonId) {
		var guiHandler = new GuiHandler();
		switch (buttonId){
			case scStyle1Id:
				guiHandler.setDisplayStyleAsDiscussion();
				break;
			case scStyle2Id:
				guiHandler.setDisplayStyleAsProContraList();
				break;
			case scStyle3Id:
				guiHandler.setDisplayStyleAsFullView();
				break;
			default: alert ('unknown id: ' + buttonId);
		}
	};

	/**
	 * Fetches all premisses out of the textares and send them
	 * @param useIntro
	 */
	this.getPremissesAndSendThem = function (useIntro) {
		var i = 0, dict = {}, no, intro, lastAttack, disc_desc = $('#' + discussionsDescriptionId),
			conTextareaPremissegroupCheckbox = $('#' + conTextareaPremissegroupCheckboxId),
			proTextareaPremissegroupCheckbox = $('#' + proTextareaPremissegroupCheckboxId);
		// all pro statements
		$('#' + proPositionTextareaId + ' div[id^="div-content-"]').children().each(function (){
		    if ($(this).prop("tagName").toLowerCase().indexOf('textarea') > -1 && $(this).val().length > 0) {
				// get current number and then the value of the dropdown
				no = $(this).prop('id').substr($(this).prop('id').length-1);
				intro = useIntro ? $('#left-dropdown-sentences-openers-' + no).text() : '';
				dict['pro_' + i] = intro + $(this).val();
				i = i + 1;
			}
		});
		i = 0;
		// all con statements
		$('#' + conPositionTextareaId + ' div[id^="div-content-"]').children().each(function (){
		    if ($(this).prop("tagName").toLowerCase().indexOf('textarea') > -1 && $(this).val().length > 0) {
				// get current number and then the value of the dropdown
				no = $(this).prop('id').substr($(this).prop('id').length-1);
				intro = useIntro ? $('#right-dropdown-sentences-openers-' + no).text() : '';
				dict['con_' + i] = intro + $(this).val();
				i = i + 1;
			}
		});

		lastAttack = window.location.href.substr(window.location.href.indexOf('relation=') + 'relation='.length);
		lastAttack = lastAttack.substr(0,lastAttack.indexOf('&'));

		// get some id's
		dict['conclusion_id'] 	  = disc_desc.attr('conclusion_id');
		dict['related_argument']  = disc_desc.attr('related_argument');
		dict['premissegroup_id']  = disc_desc.attr('premissegroup_uid');
		dict['current_attack'] 	  = disc_desc.attr('attack');
		dict['last_attack'] 	  = lastAttack;
		dict['confrontation_uid'] = disc_desc.attr('confrontation_uid');
		dict['premissegroup_con'] = conTextareaPremissegroupCheckbox.prop('checked');
		dict['premissegroup_pro'] = proTextareaPremissegroupCheckbox.prop('checked');

		conTextareaPremissegroupCheckbox.prop('checked', false);
		proTextareaPremissegroupCheckbox.prop('checked', false);

		// var txt='dict:\n';
		// $.each(dict, function (key, val) {
		// 	txt += '\n' + key + ': ' + val;
		// });
		// alert(txt);

		new AjaxSiteHandler().sendNewPremisseForX(dict);
	};

	/**
	 * Defines the action for the send button
	 */
	this.radioButtonWasChoosen = function () {
		var guiHandler = new GuiHandler(),
			radioButton= $('input[name=' + radioButtonGroup + ']:checked'),
			hasRelation = radioButton.hasClass(attr_relation),
			hasPremisse = radioButton.hasClass(attr_premisse),
			hasStart = radioButton.hasClass(attr_start),
			id = radioButton.attr(attr_id),
			long_id = radioButton.attr(attr_long_id),
			value = radioButton.val(),
			id_pgroup, id_conclusion, relation, confrontation_uid;

		if (id.indexOf(attr_no_opinion) != -1){
			parent.history.back();
			return;
		}

		if (typeof id === 'undefined' || typeof value === 'undefined') {
			guiHandler.setErrorDescription(_t(selectStatement));
			
		} else {
			guiHandler.setErrorDescription('');
			guiHandler.setSuccessDescription('');
			if (hasStart && !hasRelation && !hasPremisse) {
				this.statementButtonWasClicked(id);
			} else if (hasPremisse && !hasRelation && !hasStart) {
				id_pgroup = id;
				id_conclusion = $('#' + discussionsDescriptionId).attr(attr_conclusion_id);
				this.premisseButtonWasClicked(id_pgroup, id_conclusion);
			} else if (hasRelation && !hasPremisse && !hasStart) {
				relation = $('#' + discussionsDescriptionId).attr(attr_current_attack);
				confrontation_uid = $('#' + discussionsDescriptionId).attr(attr_confrontation_uid);
				this.relationButtonWasClicked(id, relation, confrontation_uid);
			} else if (hasPremisse && hasRelation && !hasStart){
				id_pgroup = $('#' + discussionsDescriptionId).attr(attr_premissegroup_uid);
				this.argumentButtonWasClicked(long_id, id_pgroup);
			} else {
				alert('new class in InteractionHandler: radioButtonWasChoosen\n' +
				'has start: ' + hasStart + '\n' +
				'has premisse: ' + hasPremisse + '\n' +
				'has relation: ' + hasRelation)
			}
		}

		// reset style box
		guiHandler.resetChangeDisplayStyleBox();
	};

	/**
	 * Callback for the ajax method getPremisseForStatement
	 * @param data returned json data
	 */
	this.callbackIfDoneForPremisseForStatement = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataToContentAsStartPremisses(parsedData);
		} else {
			gh.setDiscussionsDescription(_t(firstPositionText), '' , null);
			gh.setNewArgumentButtonOnly(_t(addPremisseRadioButtonText), true);
		}
		gh.resetEditButton();
	};

	/**
	 * Callback for the ajax method getPremisseForStatement
	 * @param data returned json data
	 */
	this.callbackIfDoneReplyForPremissegroup = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataAsConfrontation(parsedData);
		} else if (parsedData.status == '0') {
			new JsonGuiHandler().setJsonDataAsConfrontationWithoutConfrontation(parsedData);
		} else {
			alert('error in callbackIfDoneReplyForPremissegroup');
		}
		gh.resetEditButton();
	};

	/**
	 * Callback for the ajax method getReplyForArgument
	 * @param data returned json data
	 */
	this.callbackIfDoneReplyForArgument = function (data) {
		this.callbackIfDoneReplyForPremissegroup(data);
	};

	/**
	 * Callback for the ajax method handleReplyForResponseOfConfrontation
	 * @param data
	 */
	this.callbackIfDoneHandleReplyForResponseOfConfrontation = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataAsConfrontationReasoning(parsedData);
		} else if (parsedData.status == '0') {
			alert('callbackIfDoneHandleReplyForResponseOfConfrontation status 0');
		} else {
			alert(_t('wrongURL'));
		}
		gh.resetEditButton();
	};

	/**
	 * Callback for the ajax method getStartStatements
	 * @param data returned json data
	 */
	this.callbackIfDoneForGetStartStatements = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '-1') {
			gh.setDiscussionsDescription(_t(firstPositionText), _t(firstPositionText), null);
			gh.setNewArgumentButtonOnly(_t(firstConclusionRadioButtonText), false);
		} else {
			new JsonGuiHandler().setJsonDataToContentAsStartStatement(parsedData);
		}
		gh.resetEditButton();
	};

	/**
	 * Callback, when a new position was send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewStartStatement = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			alert('success -1 in callbackIfDoneForSendNewStartStatement');
		} else if (parsedData.status == '0') {
			// $('#' + addStatementErrorContainer).show();
			// $('#' + addStatementErrorMsg).text(alreadyInserted);
			new InteractionHandler().statementButtonWasClicked(parsedData.statement.uid);
		} else {
			$('#' + addStatementContainerId).hide();
			$('#' + addStatementContainerMainInputId).text('');
			new GuiHandler().setNewStatementAsLastChild(parsedData);
		}
	};

	/**
	 * Callback, when new statements were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewPremissesX = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseInternal));
		} else {
			new GuiHandler().setPremissesAsLastChild(parsedData);
		}
	};

	/**
	 * Callback, when new premisses were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewStartPremisse= function (data) {
		var parsedData = $.parseJSON(data);
		 if (parsedData.status == '0') {
			 new InteractionHandler().premisseButtonWasClicked(parsedData.premissegroup_uid, $('#' + discussionsDescriptionId).attr('conclusion_id'))
		 } else {
			 this.callbackIfDoneForSendNewPremissesX(data);
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
			new GuiHandler().displayStatementCorrectionsInPopup(parsedData.content);
		}
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneGetUsersOverview = function (data){
		var parsedData = $.parseJSON(data);
		new JsonGuiHandler().setJsonUserDataToAdminContent(parsedData);
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneAttackOverview = function (data){
		var parsedData = $.parseJSON(data);
		new JsonGuiHandler().setJsonAttackDataToAdminContent(parsedData);
	};

	/**
	 * Callback, when a correcture could be send
	 * @param data of the ajax request
	 * @param edit_dialog_td_id
	 */
	this.callbackIfDoneForSendCorrectureOfStatement = function (data, edit_dialog_td_id) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			$('#' + popupEditStatementErrorDescriptionId).text(_t(noCorrectionsSet));
		} else if (parsedData.status == '0'){
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text('');
			$('#' + popupEditStatementWarning).show();
			$('#' + popupEditStatementWarningMessage).text(_t(duplicateDialog));
		} else {
			new GuiHandler().updateOfStatementInDiscussion(parsedData);
			$('#' + popupEditStatementErrorDescriptionId).text('');
			$('#' + popupEditStatementSuccessDescriptionId).text(_t(correctionsSet));
			$('#' + edit_dialog_td_id).text(parsedData.text);
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
			$('#' + popupUrlSharingDescriptionPId).html(_t(feelFreeToShareUrl) + ',' + _t(shortenedWith) + ' ' + service + ':');
			$('#' + popupUrlSharingInputId).val(parsedData.url);
		} else {
			$('#' + popupUrlSharingDescriptionPId).text(_t(feelFreeToShareUrl) + ":");
			$('#' + popupUrlSharingInputId).val(long_url);
		}
	};

	/**
	 *
	 * @param data
	 * @param callbackid
	 */
	this.callbackIfDoneFuzzySearch = function (data, callbackid){
		var parsedData = $.parseJSON(data);
		new GuiHandler().setStatementsAsProposal(parsedData, callbackid);
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForGetIssueList = function(data){
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		gh.setIssueList(parsedData);

		// are we starting ?
			var url = window.location.href, issue_id;
		if (url.indexOf(mainpage + 'discussion/start') != -1) {
			// do we have a link with issue id?
			if (url.indexOf(mainpage + 'discussion/start/issue=') != -1) {
				// get issue id out of the url
				issue_id = url.substr((mainpage + 'discussion/start/issue=').length);
				// set inactive class
				$('#' + issueDropdownListID).children('li').each(function () {
					$(this).removeClass('disabled');
				});
				$('#issue_' + issue_id).addClass('disabled');
				// set button text
				$('#' + issueDropdownButtonID).text($('#issue_' + issue_id).text());
			} else {
				issue_id = new Helper().getCurrentIssueId();
			}
			new AjaxSiteHandler().getStartStatements(issue_id);
		}
	};
}