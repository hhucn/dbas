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
		new AjaxSiteHandler().callSiteForChooseActionForStatement(id);
	};

	/**
	 * Handler when an start statement was clicked, which should be supported
	 * @param id of the button
	 */
	this.supportStatementButtonWasClicked = function (id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		new AjaxSiteHandler().callSiteForGetPremiseForStatement(id, true);
	};

	/**
	 * Handler when an start statement was clicked, which should be attacked
	 * @param id of the button
	 */
	this.attackStatementButtonWasClicked = function (id) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		new AjaxSiteHandler().callSiteForGetPremiseForStatement(id, false);
	};

	/**
	 * Handler when an start statement was clicked, which should be attacked
	 * @param id of the button
	 * @param isSupportive
	 */
	this.moreAboutStatementButtonWasClicked = function (id, isSupportive) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		new AjaxSiteHandler().callSiteForGetMoreForArgument(id, isSupportive);
	};

	/**
	 * Handler when an start premise was clicked
	 * @param pgroup_id
	 * @param conclusion_id
	 * @param supportive
	 */
	this.premiseButtonWasClicked = function (pgroup_id, conclusion_id, supportive) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		// new AjaxSiteHandler().getReplyForPremiseGroup(id);
		new AjaxSiteHandler().callSiteForGetReplyForPremiseGroup(pgroup_id, conclusion_id, supportive);
	};

	/**
	 * Handler when an relation button was clicked
	 * @param id of the button
	 * @param relation of the button
	 * @param isSupportive
	 */
	this.relationButtonWasClicked = function (id, relation, isSupportive) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionsDescriptionId).empty();
		new AjaxSiteHandler().callSiteForHandleReplyForResponseOfConfrontation(id, relation, isSupportive);
	};

	/**
	 * Handler when an argument button was clicked
	 * @param long_id
	 * @param pgroup_id
	 * @param isSupportive
	 */
	this.argumentButtonWasClicked = function (long_id, pgroup_id, isSupportive) {
		// clear the discussion space
		$('#' + discussionSpaceId).empty();
		$('#' + discussionsDescriptionId).empty();
		// new AjaxSiteHandler().getReplyForArgument(id);
		new AjaxSiteHandler().callSiteForGetReplyForArgument(long_id, pgroup_id, isSupportive);
	};

	/**
	 * Method for some style attributes, when the radio buttons are chaning
	 */
	this.radioButtonChanged = function () {// TODO KILL
		var guiHandler = new GuiHandler(), text, isStart = $('#' + discussionSpaceId + ' ul li input').hasClass('start'), addReasonButton = $('#' + addReasonButtonId);
		// did we have an "add statement" action or just "argumentation" ?
		if (addReasonButton.is(':checked')) {

			guiHandler.displayHowToWriteTextPopup();

			// get the second child, which is the label
			text = addReasonButton.parent().children().eq(1).text();
			if (text.indexOf(_t(newConclusionRadioButtonText)) >= 0 || text.indexOf(_t(firstConclusionRadioButtonText)) >= 0) {
				// statement
				//guiHandler.setDisplayStylesOfAddStatementContainer(true, isStart, false, true, false);
				guiHandler.showAddStatementContainer(isStart);
			} else if (text.indexOf(_t(addArgumentRadioButtonText)) >= 0 || text.indexOf(_t(addPremiseRadioButtonText)) >= 0) {
				// argument
				//guiHandler.setDisplayStylesOfAddStatementContainer(true, isStart, false, false, true);
				guiHandler.showAddPremiseOrArgumentContainer(true, isStart);
			} else {
				// premise
				//guiHandler.setDisplayStylesOfAddStatementContainer(true, isStart, true, false, false);
				guiHandler.showAddPremiseOrArgumentContainer(false, isStart);
			}
		} else {
			//guiHandler.setDisplayStylesOfAddStatementContainer(false, isStart, false, true, false);
			guiHandler.hideAddStatementContainer();

			this.radioButtonWasChoosen();
			$('#' + islandViewContainerId).fadeOut('slow');
		}
	};

	/**
	 * Segmented button for display style was pressed
	 * @param buttonId current id
	 */
	this.styleButtonChanged = function (buttonId) { // TODO KILL
		var guiHandler = new GuiHandler(),
				style1 = $('#' + scStyleDialogId),
				style2 = $('#' + scStyleIslandId),
				style3 = $('#' + scStyleCompleteId);
		switch (buttonId){
			case scStyleDialogId:
				style2.attr('checked', false).prop('checked', false);
				style3.attr('checked', false).prop('checked', false);
				guiHandler.setDisplayStyleAsDiscussion();
				break;
			case scStyleIslandId:
				style1.attr('checked', false).prop('checked', false);
				style3.attr('checked', false).prop('checked', false);
				guiHandler.setDisplayStyleAsIsland();
				break;
			case scStyleCompleteId:
				style1.attr('checked', false).prop('checked', false);
				style2.attr('checked', false).prop('checked', false);
				guiHandler.setDisplayStyleAsGraphView();
				break;
			default: alert ('unknown id: ' + buttonId);
		}
	};

	/**
	 * Fetches all premises out of the textares and send them
	 * @param useIntro
	 * @returns {boolean} true, if all input is not empty
	 */
	this.getPremisesAndSendThem = function (useIntro) { // TODO KILL
		var i = 0,
				dict = {},
				no, intro,
				lastAttack,
				disc_desc = $('#' + discussionsDescriptionId),
				type,
				escapedText,
				helper = new Helper(),
				emptyInput = false,
				exceptionForRebut,
				isSupportive,
				conTextareaPremisegroupCheckbox = $('#' + conTextareaPremisegroupCheckboxId),
				proTextareaPremisegroupCheckbox = $('#' + proTextareaPremisegroupCheckboxId);
		// all pro statements
		 $('#' + proPositionTextareaId + ' div[id^="div-content-"]').children().each(function (){
			// differ between textarea and inputs
			type = $(this).prop('tagName').toLowerCase().indexOf('textarea') != -1 ? 'textarea' : 'input';
			escapedText = helper.escapeHtml($(this).val());
			// check if this type is visible and if the input is not empty
		    if ($(this).is(":visible") && $(this).prop('tagName').toLowerCase().indexOf(type) != -1) {
				if (escapedText.length > 0) {
					// get current number and then the value of the dropdown
					no = $(this).prop('id').substr($(this).prop('id').length-1);
					intro = useIntro ? $('#left-dropdown-sentences-openers-' + no).text() : '';
					dict['pro_' + i] = intro + escapedText;
					i = i + 1;
					isSupportive = true;
				} else {
					emptyInput = true;
					return true;
				}
			}
		});
		if (emptyInput) return false;

		i = 0;
		// all con statements
		$('#' + conPositionTextareaId + ' div[id^="div-content-"]').children().each(function (){
			// differ between textarea and inputs
			type = $(this).prop('tagName').toLowerCase().indexOf('textarea') != -1 ? 'textarea' : 'input';
			escapedText = helper.escapeHtml($(this).val());
			// check if this type is visible and if the input is not empty
		    if ($(this).is(":visible") && $(this).prop('tagName').toLowerCase().indexOf(type) > -1) {
				if (escapedText.length > 0) {
					// get current number and then the value of the dropdown
					no = $(this).prop('id').substr($(this).prop('id').length - 1);
					intro = useIntro ? $('#right-dropdown-sentences-openers-' + no).text() : '';
					dict['con_' + i] = intro + escapedText;
					i = i + 1;
					isSupportive = false;
				} else {
					emptyInput = true;
					return true;
				}
			}
		});
		if (emptyInput) return false;

		lastAttack = window.location.href.substr(window.location.href.indexOf('relation=') + 'relation='.length);
		lastAttack = lastAttack.substr(0,lastAttack.indexOf('&'));

		// special case, again for the attacking branch and rebut
		exceptionForRebut = lastAttack == attr_rebut && window.location.href.substr(window.location.href.indexOf('id=')).indexOf('_attacking_') != -1;

		// get some id's
		dict[attr_conclusion_id] 	  	= disc_desc.attr('conclusion_id');
		dict[attr_related_argument]  	= disc_desc.attr('related_argument');
		dict[attr_premisegroup_id]  	= disc_desc.attr('premisegroup_uid');
		dict[attr_current_attack] 	  	= disc_desc.attr('attack');
		dict[attr_last_attack] 	  		= lastAttack;
		dict[attr_confrontation_uid] 	= disc_desc.attr(attr_confrontation_uid);
		dict[attr_premisegroup_con] 	= conTextareaPremisegroupCheckbox.prop('checked');
		dict[attr_premisegroup_pro] 	= proTextareaPremisegroupCheckbox.prop('checked');
		dict['exceptionForRebut'] 		= exceptionForRebut;

		// new Helper().alertWithJsonData(dict);

		conTextareaPremisegroupCheckbox.prop('checked', false);
		proTextareaPremisegroupCheckbox.prop('checked', false);

		new AjaxSiteHandler().sendNewPremiseForX(dict);
		return true;
	};

	/**
	 * Defines the action for the send button
	 */
	this.radioButtonWasChoosen = function () { // TODO KILL
		var guiHandler = new GuiHandler(),
			radioButton= $('input[name=' + radioButtonGroup + ']:checked'),
			discussionsDescription = $('#' + discussionsDescriptionId),
			hasRelation = radioButton.hasClass(attr_relation),
			hasPremise = radioButton.hasClass(attr_premise),
			hasStart = radioButton.hasClass(attr_start),
			hasAttack = radioButton.hasClass(attr_attack),
			hasSupport = radioButton.hasClass(attr_support),
			hasMore = radioButton.hasClass(attr_more_about),
			id = radioButton.attr(attr_id),
			long_id = radioButton.attr(attr_long_id),
			value = radioButton.val(),
			id_pgroup, id_conclusion, relation, supportive, statementBtnClick, supportStatementBtnClick,
			attackStatementBtnClick, moreAboutStatementBtnClick, premiseBtnClick, relationBtnClick, argumentBtnClick;
		// should we step back?
		if (id.indexOf(attr_no_opinion) != -1){
			this.oneStepBack();
			return;
		}

		// if we differentiate between the attack, support or dont know case, we have to trim the id
		// this is so, because every input had the same id, because it is the same and we only differentiate between the different cases

		// differentiate
		if (hasStart && !hasRelation && !hasPremise) {
			statementBtnClick           = !hasAttack && !hasSupport && !hasMore;
			supportStatementBtnClick    = !hasAttack && hasSupport && !hasMore;
			attackStatementBtnClick     = hasAttack && !hasSupport && !hasMore;
			moreAboutStatementBtnClick  = !hasAttack && !hasSupport && hasMore;
		} else if (!hasAttack && !hasSupport && !hasMore){
			premiseBtnClick  = !hasRelation && hasPremise;
			relationBtnClick = hasRelation && !hasPremise;
			argumentBtnClick = hasRelation && hasPremise;
		}

		// is something wrong?
		if (typeof id === 'undefined' || typeof value === 'undefined') {
			guiHandler.setErrorDescription(_t(selectStatement));
			
		} else {
			guiHandler.hideErrorDescription();
			guiHandler.hideSuccessDescription();

			if (statementBtnClick){
				this.statementButtonWasClicked(id);
			} else if (supportStatementBtnClick) {
				id = id.substr(0, id.indexOf('_'));
				this.supportStatementButtonWasClicked(id);
			} else if (attackStatementBtnClick) {
				id = id.substr(0, id.indexOf('_'));
				this.attackStatementButtonWasClicked(id);
			} else if (moreAboutStatementBtnClick) {
				id = id.substr(0, id.indexOf('_'));
				this.moreAboutStatementButtonWasClicked(id, true);
			} else if (premiseBtnClick) {
				supportive = discussionsDescription.attr(attr_supportive).toLocaleLowerCase().indexOf('true') != -1;
				id_pgroup = id;
				id_conclusion = discussionsDescription.attr(attr_conclusion_id);
				this.premiseButtonWasClicked(id_pgroup, id_conclusion, supportive);
			} else if (relationBtnClick) {
				supportive = discussionsDescription.attr(attr_supportive).toLocaleLowerCase().indexOf('true') != -1;
				relation = discussionsDescription.attr(attr_current_attack);
				// differentiate between an attack of a new argument or the old style
				if (typeof relation == 'undefined') {
					relation = radioButton.attr('id').substr(0,radioButton.attr('id').indexOf('_'));
					id = relation + '_attacking_' + discussionsDescription.attr('argument_uid');
				}
				this.relationButtonWasClicked(id, relation, supportive);
			} else if (argumentBtnClick){
				id_pgroup = discussionsDescription.attr(attr_premisegroup_uid);
				supportive = discussionsDescription.attr(attr_supportive).toLocaleLowerCase().indexOf('true') != -1;
				this.argumentButtonWasClicked(long_id, id_pgroup, supportive);
			} else {
				alert('new class in InteractionHandler: radioButtonWasChoosen\n' +
				'has start: ' + hasStart + '\n' +
				'has premise: ' + hasPremise + '\n' +
				'has relation: ' + hasRelation + '\n' +
				'has attack: ' + hasAttack + '\n' +
				'has support: ' + hasSupport + '\n' +
				'has more: ' + hasMore);
			}
		}

		// reset style box
		guiHandler.resetChangeDisplayStyleBox();
	};

	/**
	 * Sets the links in the discussion end text (go back and restart)
	 */
	this.setDiscussionEndLinksInText = function (){
		$('#' + discussionEndStepBack)
				.attr('title', _t(goStepBack))
				.attr('href','#')
				.click(function(){
			new InteractionHandler().oneStepBack();
		});
		$('#' + discussionEndRestart)
				.attr('title', _t(restartDiscussion))
				.attr('href', mainpage + 'discussion/start/issue=' + new Helper().getCurrentIssueId());
	};

	/**
	 *
	 */
	this.oneStepBack = function(){
		parent.history.back();
	};

	/**
	 * Callback for the ajax method getPremisesForStatement
	 * @param data returned json data
	 * @param isSupportive, true when the premisses are supportive
	 */
	this.callbackIfDoneForGetPremisesForStatement = function (data, isSupportive) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataToContentAsStartPremises(parsedData, isSupportive);
		} else {
			gh.setDiscussionsDescription(_t(firstPositionText), '' , null);
			gh.setNewArgumentButtonOnly(_t(addPremiseRadioButtonText), true);
		}
		gh.resetEditAndRefactorButton();
	};

	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForTextGetTextForStatement = function (data){
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setActionsForStatement(parsedData);
		} else {
			new GuiHandler().setErrorDescription(_t(internalError));
		}
		gh.resetEditAndRefactorButton(false);
	};

	/**
	 * Callback for the ajax method getPremiseForStatement
	 * @param data returned json data
	 */
	this.callbackIfDoneForGetPremiseForStatement = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataToContentAsSingleArgument(parsedData, true);
		} else {
			gh.setErrorDescription("Some error happened, please contact the author. (Error is in callback for AttackForStatement)");
			gh.setDiscussionsDescription(_t(discussionEnd) + ' ' + _t(discussionEndText), _t(discussionEnd), null);
			new InteractionHandler().setDiscussionEndLinksInText();
		}
		gh.resetEditAndRefactorButton(false);
	};

	/**
	 * Callback for the ajax method getPremiseForStatement
	 * @param data returned json data
	 * @param isSupportive, true when the premisses are supportive
	 */
	this.callbackIfDoneReplyForPremisegroup = function (data, isSupportive) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataAsConfrontation(parsedData, isSupportive);
		} else if (parsedData.status == '0') {
			new JsonGuiHandler().setJsonDataAsConfrontationWithoutConfrontation(parsedData, isSupportive);
		} else {
			alert('error in callbackIfDoneReplyForPremisegroup');
		}
		gh.resetEditAndRefactorButton();
	};

	/**
	 * Callback for the ajax method getReplyForArgument
	 * @param data returned json data
	 * @param isSupportive
	 */
	this.callbackIfDoneReplyForArgument = function (data, isSupportive) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataAsConfrontation(parsedData, isSupportive);
		} else if (parsedData.status == '0') {
			new JsonGuiHandler().setJsonDataAsConfrontationWithoutConfrontation(parsedData, isSupportive);
		} else {
			alert('error in callbackIfDoneReplyForArgument');
		}
		gh.resetEditAndRefactorButton();
	};

	/**
	 * Callback for the ajax method handleReplyForResponseOfConfrontation
	 * @param data
	 * @param isSupportive
	 */
	this.callbackIfDoneHandleReplyForResponseOfConfrontation = function (data, isSupportive) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		if (parsedData.status == '1') {
			new JsonGuiHandler().setJsonDataAsConfrontationReasoning(parsedData, isSupportive);
		} else if (parsedData.status == '0') {
			alert('callbackIfDoneHandleReplyForResponseOfConfrontation status 0');
		} else {
			alert(_t('wrongURL'));
		}
		gh.resetEditAndRefactorButton();
	};

	/**
	 * Callback for the ajax method getStartStatements
	 * @param data returned json data
	 */
	this.callbackIfDoneForGetStartStatements = function (data) {
		var parsedData = $.parseJSON(data), gh = new GuiHandler();

		// correction of an undefined issue
		if (parsedData.reset_url === 'true'){
			window.location.replace(mainpage + 'discussion/start/issue=' + parsedData.reset_issue);
		}

		if (parsedData.status == '-1') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(internalError));
		} else {
			new JsonGuiHandler().setJsonDataToContentAsStartStatement(parsedData);
		}
		gh.resetEditAndRefactorButton();
	};

	/**
	 * Callback, when a new position was send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewStartStatement = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			alert('success -1 in callbackIfDoneForSendNewStartStatement');
		} else {
			 $('#' + discussionSpaceId + 'input:last-child').attr('checked', false).prop('checked', false);
			window.location.href = parsedData.url;
		}
	};

	/**
	 * Callback, when new statements were send
	 * @param data returned data
	 */
	this.callbackIfDoneForSendNewPremisesX = function (data) {
		var parsedData = $.parseJSON(data);
		if (parsedData.status == '-1') {
			$('#' + addStatementErrorContainer).show();
			$('#' + addStatementErrorMsg).text(_t(notInsertedErrorBecauseInternal));
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
			 new InteractionHandler().premiseButtonWasClicked(parsedData.premisegroup_uid, $('#' + discussionsDescriptionId).attr('conclusion_id'), isSupportive)
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
			new GuiHandler().displayStatementCorrectionsInPopup(parsedData.content);
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
	 * Callback for the Issue List
	 * @param data
	 */
	this.callbackIfDoneForGetIssueList = function(data){
		var parsedData = $.parseJSON(data), gh = new GuiHandler();
		gh.setIssueList(parsedData);

		// are we restarting ?
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
				gh.setIssueDropDownText(new Helper().resizeIssueText($('#issue_' + issue_id).children().first().attr('text')));
			} else {
				issue_id = new Helper().getCurrentIssueId();
			}
			new AjaxSiteHandler().getStartStatements(issue_id);
		}
	};
}