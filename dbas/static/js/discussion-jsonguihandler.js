/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function JsonGuiHandler() {
	'use strict';
	var DEBUG_ATTACK = false;

	/**
	 * Sets three different actios for the statement: agree, disagree, dont know
	 * @param jsonData with text, and uid
	 */
	this.setActionsForStatement = function(jsonData){
		var txt, tmp, dict, helper = new Helper(), guihandler = new GuiHandler(), listItems = [];

		dict = {'conclusion_uid': jsonData.uid, 'text': jsonData.text};

		txt = helper.startWithLowerCase(jsonData.text);
		guihandler.setDiscussionsDescription(_t(whatDoYouThink) + ' <b>' + txt + '</b>?', '', dict);

		// build input-tags
		txt = ': <b>' + txt + '</b>.';
		tmp = _t(iAgreeWithInColor) + txt;
		listItems.push(helper.getExtraInputInLiWithType(jsonData.uid, tmp, '', [attr_support, attr_start]));
		tmp = _t(iDisagreeWithInColor) + txt;
		listItems.push(helper.getExtraInputInLiWithType(jsonData.uid, tmp, '', [attr_attack, attr_start]));
		tmp = _t(iDoNotKnowInColor) + ', ' + helper.startWithLowerCase(_t(showMeAnArgumentFor)) + txt;
		listItems.push(helper.getExtraInputInLiWithType(jsonData.uid, tmp, '', [attr_more_about, attr_start]));

		guihandler.addListItemsToDiscussionsSpace(listItems);
	};

	/**
	 * Sets given json content as start statement buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsStartStatement = function (jsonData) {
		var listitems = [], guihandler = new GuiHandler(), helper = new Helper();
		guihandler.setDiscussionsDescription(_t(initialPositionInterest), '' , null);
		$.each(jsonData.statements, function setJsonDataToContentAsConclusionEach(key, val) {
			listitems.push(helper.getKeyValAsInputInLiWithType(val.uid, val.text + '.', true, false, false,''));
		});

		// sanity check for an empty list
		if (listitems.length === 0) {
			// todo: is this even used?
			alert('discussion-guihandler.: setJsonDataToContentAsStartStatement');
			guihandler.setDiscussionsDescription(_t(firstOneText) + '<b>' + jsonData.statements.currentStatementText + '</b>', '' , null);
		}

		if (typeof jsonData.logged_in == "string") {
			listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(newConclusionRadioButtonText), false, false, false, ''));
		}

		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given json content as start premises buttons in the discussions space
	 * @param jsonData data with json content
	 * @param isSupportive, true when the premisses are supportive
	 */
	this.setJsonDataToContentAsStartPremises = function (jsonData, isSupportive) {
		var listitems = [],
			guihandler = new GuiHandler(),
			text,
			helper = new Helper(),
			attributes,
			index=0,
			dict;

		text = helper.startWithLowerCase(jsonData.currentStatement.text);
		dict =  {'text': text, 'conclusion_id': jsonData.conclusion_id, 'supportive': isSupportive};

		// check length of premises-dict and set specifix text elements
		if (Object.keys(jsonData.premises).length == 0) {
			dict.text += !isSupportive? ' ' + _t(doesNotHold) : '';
			guihandler.setDiscussionsDescription(_t(firstPremiseText1) + ' <b>' + text + '</b>' + (!isSupportive? ' ' + _t(doesNotHold): '')
					+ '.<br><br>' + _t(firstPremiseText2), text, dict);
		} else {
			guihandler.setDiscussionsDescription(_t(sentencesOpenersRequesting[0]) + ' <b>' + text + '</b> '
					+ (isSupportive? _t(isTrue) : _t(isFalse)) + '?', text, dict);
		}

		// adding every premise as radio button
		$.each(jsonData.premises, function setJsonDataToContentAsConclusionEach(key, val) {
			text = '';
			index = 0;
			attributes = {};
			$.each(val, function setJsonDataToContentAsConclusionEachVal(valkey, valval) {
				if (text=='')
					text = _t(because) + ' ';
				else
					text += ' <i>' + _t(and) + '</i> ' + helper.startWithLowerCase(_t(because)) + ' ';
				text += helper.startWithLowerCase(valval.text);
				index += 1;
				attributes['text_' + index + '_statement_id'] = valkey;
				attributes['text_' + index] = valval.text + '.';
			});
			text += '.';
			attributes['text_count'] = index;
			// we are saving the group id ad key
			listitems.push(helper.getKeyValAsInputInLiWithType(key, text, false, true, false, text, attributes));
		});

		// adding new premises will be available, if the user is logged in
		if (typeof jsonData.logged_in == "string") {
			// would be this premise the first premise for the statement?
			text = parseInt(jsonData.premises) == 0 ? _t(newPremiseRadioButtonTextAsFirstOne) : _t(newPremisesRadioButtonText);
			listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, text, false, false, false, ''));
			guihandler.addListItemsToDiscussionsSpace(listitems);

			// if there is no argument
			if (Object.keys(jsonData.premises).length == 0){
				$('#' + addReasonButtonId).attr('checked', true).prop('checked', true);
				$('#li_' + addReasonButtonId).hide();
				new InteractionHandler().radioButtonChanged();
			}
		} else {
			if (Object.keys(jsonData.premises).length == 0) {
				text = '<b>' + text + '</b><br><br>' + _t(discussionEnd) + '<br><br>' + _t(discussionEndText);
				new InteractionHandler().setDiscussionEndLinksInText();
			}

			if (index == 0){
				guihandler.setErrorDescription(_t(discussionEndFeelFreeToLogin) + '<br>' + _t(clickHereForRegistration));
				guihandler.addListItemsToDiscussionsSpace(listitems);
			} else {
				guihandler.addListItemsToDiscussionsSpace(listitems);
			}

			guihandler.addListItemsToDiscussionsSpace(listitems);
		}
	};

	/**
	 * Sets given json content as start attack buttons in the discussions space
	 * @param jsonData data with json
	 * @param isSupportive, true when we are supportive
	 */
	this.setJsonDataToContentAsSingleArgument = function (jsonData, isSupportive){
		var guihandler = new GuiHandler(),
			helper = new Helper(),
			conclusion = helper.startWithLowerCase(jsonData.currentStatement.text),
			conclusion_id = jsonData.currentStatement.uid,
			text, premise = '', relationArray, listitems = [], dict, argument, premisegroup_uid = 0, id = [], tmp = [];

		// build premise, if there is any
		if (jsonData.premises == '0'){

			// different discussions text, when we are supportive or not
			argument = '<b>' + conclusion + '</b>';
			if (isSupportive) {
				text = _t(unfortunatelyNoMoreArgument) + ' ' + argument + '.<br><br>' + _t(canYouGiveAReason)
						+ '<br><br>' + _t(alternatively) + ': ' + _t(discussionEndText);
			} else {
				text = _t(soYouWantToArgueAgainst) + ' ' + argument + ', ' + _t(butOtherParticipantsDontHaveArgument);
			}

			// adding new premises will be available, if the user is logged in
			if (typeof jsonData.logged_in == "string") {
				listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, '-', false, false, false, ''));
				guihandler.addListItemsToDiscussionsSpace(listitems);

				$('#' + addReasonButtonId).attr('checked', true).prop('checked', true);
				$('#li_' + addReasonButtonId).hide();
				new InteractionHandler().radioButtonChanged();
				if (isSupportive)
					$('#' + addStatementContainerH4Id).html(_t(canYouGiveAReasonFor) + ' ' + argument + '?');
				else
					$('#' + addStatementContainerH4Id).html(_t(canYouGiveACounterArgumentWhy1) + ' ' + argument + ' ' +_t(canYouGiveACounterArgumentWhy2));
			} else {
				text += '<br><br>' + _t(discussionEndFeelFreeToLogin);
				guihandler.setErrorDescription(_t(discussionEndFeelFreeToLogin) + '<br>' + _t(clickHereForRegistration));
			}

			dict = {'argument_uid': jsonData.argument_uid, 'conclusion_id': conclusion_id, 'text': argument, 'supportive': isSupportive};
			guihandler.setDiscussionsDescription(text, '', dict);
				new InteractionHandler().setDiscussionEndLinksInText();

		} else {
			$.each(jsonData.premises, function setJsonDataToContentAsStartAttackEach(key, val) {
				if (premise == '')
					premise += helper.startWithLowerCase(jsonData.premises[key].text);
				else
					premise += ' <i>' + _t(and) + '</i> ' + helper.startWithLowerCase(jsonData.premises[key].text);
				premisegroup_uid = jsonData.premises[key].premisegroup_uid;
			});

			argument = conclusion + ' ' + helper.startWithLowerCase(_t(because)) + ' ' + premise;
			text = _t(otherParticipantsThinkThat) + ' <b>' + conclusion
					+ '</b>, ' + helper.startWithLowerCase(_t(because))
					+ ' <b>' + premise + '</b>.<br><br>';
			text += isSupportive ? (_t(whatDoYouThink) + '?') : (_t(whyAreYouDisagreeing));

			dict = {'argument_uid': jsonData.argument_uid,
				'conclusion_id': conclusion,
				'text': argument,
				'supportive': 'false',
				'premisegroup_uid' : premisegroup_uid};
			guihandler.setDiscussionsDescription(text, '', dict);

			// get attacks

			// build the radio buttons
			id[0] = attr_undermine	+ '_' + premisegroup_uid;
			id[1] = attr_support	+ '_' + premisegroup_uid;
			id[2] = attr_undercut 	+ '_' + premisegroup_uid;
			id[3] = attr_overbid 	+ '_' + premisegroup_uid;
			id[4] = attr_rebut 		+ '_' + premisegroup_uid;
			id[5] = attr_no_opinion + '_' + premisegroup_uid;
			// all radio buttons, if we are supportive
			// only the attacking buttons, if we are attackingd;

			if (isSupportive){
				relationArray = helper.createRelationsTextWithoutConfrontation(premise, conclusion, false);
				tmp[0] = relationArray[0] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undermine + '</i>]') : '');
				tmp[1] = relationArray[1] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_support + '</i>]') : '');
				tmp[2] = relationArray[2] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undercut + '</i>]') : '');
				tmp[3] = relationArray[3] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_overbid + '</i>]') : '');
				tmp[4] = relationArray[4] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_rebut + '</i>]') : '');
				tmp[5] = relationArray[5] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_no_opinion + '</i>]') : '');
				listitems.push(helper.getKeyValAsInputInLiWithType(id[0], tmp[0], false, false, true, _t(description_undermine)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[1], tmp[1], false, false, true, _t(description_support)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[2], tmp[2], false, false, true, _t(description_undercut)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[3], tmp[3], false, false, true, _t(description_overbid)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[4], tmp[4], false, false, true, _t(description_rebut)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[5], tmp[5], false, false, true, _t(description_no_opinion)));
			} else {

				relationArray = helper.createAttacksOnlyText(premise, conclusion, false);
				tmp[0] = relationArray[0] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undermine + '</i>]') : '');
				tmp[1] = relationArray[1] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undercut + '</i>]') : '');
				tmp[2] = relationArray[2] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_rebut + '</i>]') : '');
				tmp[3] = relationArray[3] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_no_opinion + '</i>]') : '');
				listitems.push(helper.getKeyValAsInputInLiWithType(id[0], tmp[0], false, false, true, _t(description_undermine)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[2], tmp[1], false, false, true, _t(description_undercut)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[4], tmp[2], false, false, true, _t(description_rebut)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[5], tmp[3], false, false, true, _t(description_no_opinion)));
			}
			// TODO HOW TO INSERT ATTACKING PREMISEGROUPS?

			// set the buttons
			guihandler.addListItemsToDiscussionsSpace(listitems);
		}

	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData parsed data
	 * @param isSupportive, true when the premisses are supportive
	 */
	this.setJsonDataAsConfrontation = function (jsonData, isSupportive) {
		var helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			premise = helper.cutOffPunctiation(jsonData.premise_text),
			opinion, confrontationText, listitems = [], dict, double_attack, text = [],
			confrontation = jsonData.confrontation.substring(0, jsonData.confrontation.length),
			confronation_id = '_argument_' + jsonData.confrontation_argument_id,
			argument_id = '_argument_' + jsonData.argument_id,
			relationArray = helper.createConfrontationsRelationsText(confrontation, conclusion, premise, jsonData.attack, false, isSupportive);

		// sanity check
		if (typeof jsonData.relation == 'undefined'){
			opinion = '<b>' + conclusion + (isSupportive ? ', ' + _t(because).toLocaleLowerCase() : ' ' + _t(doesNotHoldBecause).toLocaleLowerCase()) + ' ' + premise + '</b>';
		} else {
			opinion = '<b>' + premise + '</b> ' + _t('relation_' + jsonData.relation) + ' ' + '<b>' + conclusion + '</b>';
		}

		// does we have an attack for an attack? if true, we have to pretty print a little bit
		double_attack = helper.stringContainsAnAttack(window.location.href) && helper.stringContainsAnAttack(jsonData.attack);

		// build some confrontation text
		if (jsonData.attack == attr_undermine){
			confrontationText = _t(otherParticipantsThinkThat) + ' <b>' + premise + '</b> ' + _t(doesNotHoldBecause) + ' ';
		} else if (jsonData.attack == attr_rebut){
			// distinguish between reply for argument and reply for premise group
			if (window.location.href.indexOf(attrReplyForArgument) != 0){
				// reply for argument
				confrontationText = (double_attack ? _t(otherUsersClaimStrongerArgumentAccepting) : _t(otherUsersClaimStrongerArgumentRejecting))
						+ ' <b>' + conclusion + '</b>.' + ' ' + _t(theySay) + ': ';
			} else {
				// reply for premise group
				confrontationText = _t(otherParticipantsAcceptBut) + ' ' + _t(strongerStatementForRecjecting) + ' <b>' + conclusion
						+ '</b>.' + ' ' + _t(theySay) + ': ';
			}
		} else if (jsonData.attack == attr_undercut){
			confrontationText = _t(otherParticipantsThinkThat) + ' <b>' + premise + '</b> ' + (isSupportive ? _t(doesNotJustify) : _t(doesJustify))
					+ ' <b>' + conclusion + '</b>,' + ' ' + _t(because).toLocaleLowerCase() + ' ';
		}
		confrontationText += '<b>' + confrontation + '</b>' + (DEBUG_ATTACK ? (' [<i>' + jsonData.attack + '</i>]') : '');

		// set discussions text - dictionary needs strings, no variables as keys!
		dict = {'confrontation_uid': jsonData.confrontation_argument_id, 'current_attack': jsonData.attack, 'supportive': isSupportive};
		guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ': ' + opinion + '.<br><br>'
			+ confrontationText + '.<br><br>' + _t(whatDoYouThink) + '?', _t(thisConfrontationIs) + ' ' + jsonData.attack + '.', dict);

		// build the radio buttons
		text[0] = relationArray[0] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undermine + '</i>]') : '');
		text[1] = relationArray[1] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_support + '</i>]') : '');
		text[2] = relationArray[2] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undercut + '</i>]') : '');
		text[3] = relationArray[3] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_overbid + '</i>]') : '');
		text[4] = relationArray[4] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_rebut + '</i>]') : '');
		text[5] = relationArray[5] + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_no_opinion + '</i>]') : '');
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_undermine	+ confronation_id,	text[0], false, false, true, _t(description_undermine)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_support 	+ confronation_id,	text[1], false, false, true, _t(description_support)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_undercut 	+ confronation_id,	text[2], false, false, true, _t(description_undercut)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_overbid 	+ confronation_id,	text[3], false, false, true, _t(description_overbid)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_rebut 		+ confronation_id,	text[4], false, false, true, _t(description_rebut)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_no_opinion 	+ argument_id,		text[5], false, false, true, _t(description_no_opinion)));
		// TODO HOW TO INSERT ATTACKING PREMISEGROUPS?

		// set the buttons
		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 * @param isSupportive, true when the premisses are supportive
	 */
	this.setJsonDataAsConfrontationWithoutConfrontation = function (jsonData, isSupportive) {
		var helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			premise = jsonData.premise_text,
			opinion, confrontationText, dict,
			relation = jsonData.relation,
			conclusion_uid = jsonData.conclusion_uid,
			argument_uid = jsonData.argument_uid,
			premisegroup_uid = jsonData.premisegroup_uid;
		alert("todo today 1"); // TODO TODAY
		if (typeof relation == 'undefined'){
			opinion = '<b>' + conclusion + ', ' + helper.startWithLowerCase(_t(because)) + ' ' + premise + '</b>';
		} else {
			opinion = '<b>' + premise + '</b> ' + _t('relation_' + relation) + ' ' + '<b>' + conclusion + '</b>';
		}

		// build some confrontation text
		confrontationText = _t(otherParticipantsDontHaveCounter) + ' <b>' + premise + '</b>';

		// set discussions text
		dict = {
			'text': premise,
			'attack': relation,
			'related_argument': argument_uid,
			'premisegroup_uid': premisegroup_uid,
			'conclusion_id': conclusion_uid};

		guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ': ' + opinion + '.<br><br>'
			+ confrontationText + '.<br><br>' + _t(discussionEnd) + ' ' + _t(discussionEndText), _t(discussionEnd), dict);
			new InteractionHandler().setDiscussionEndLinksInText();
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 * @param isSupportive
	 */
	this.setJsonDataAsConfrontationReasoning = function (jsonData, isSupportive){
		var premise = jsonData.premisegroup.replace('.',''),
			helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			listitems = [], i, reason, id, long_id, dict, lastAttack, text, isAttacking;
		lastAttack = window.location.href.substr(window.location.href.indexOf('relation=') + 'relation='.length);
		lastAttack = lastAttack.substr(0,lastAttack.indexOf('&'));
		isAttacking = window.location.href.substr(window.location.href.indexOf('id=') + 'id='.length).indexOf('_attacking_') != -1;

		// different case, when we are attacking
		text = helper.createRelationsTextWithConfrontation(jsonData.confrontation_text, premise, jsonData.relation, lastAttack, conclusion, true, isAttacking, isSupportive);
		text += DEBUG_ATTACK ? (' (' + _t(youMadeA) + ' ' + jsonData.relation + ')' ): '';

		// build the reasons
		for (i=0; i<parseInt(jsonData.reason); i++){
			long_id = jsonData.relation + '_' + jsonData.type + '_' + jsonData['reason' + i + 'id'];
			id = jsonData['reason' + i + '_statement_id'];
			reason = _t(because) + ' ' + helper.startWithLowerCase(jsonData['reason' + i]) + '.';
			listitems.push(helper.getKeyValAsInputInLiWithType(id, reason, false, true, true, reason, {'long_id': long_id}));
		}

		// dictionary needs strings, no variables as keys!
		dict = {
			'text': jsonData.confrontation_text,
			'conclusion': conclusion,
			'premise': premise,
			'attack': jsonData.relation,
			'related_argument': jsonData.argument_uid,
			'premisegroup_uid': jsonData.premisegroup_uid,
			'conclusion_id': jsonData.conclusion_uid,
			'last_relation': jsonData.last_relation,
			'confrontation_text': jsonData.confrontation_text,
			'confrontation_uid': jsonData.confrontation_uid,
			'supportive': isSupportive};

		if (typeof jsonData.logged_in == "string") {
			text += '<br><br>' + _t(canYouGiveAReasonForThat);
			guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ': ' + text, '', dict);
			// check this item, if it is the only one
			if (parseInt(jsonData.reason) == 0){
				listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(firstOneReason), false, false, false, _t(addPremiseRadioButtonText)));
				guihandler.addListItemsToDiscussionsSpace(listitems);
				$('#' + addReasonButtonId).attr('checked', true).prop('checked', true).parent().hide();
				new InteractionHandler().radioButtonChanged();

			} else {
				listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(addPremiseRadioButtonText), false, false, false, _t(addPremiseRadioButtonText)));
				guihandler.addListItemsToDiscussionsSpace(listitems);
			}
		} else {
			text += '<br><br>' + _t(discussionEnd);
			guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ': ' + text, '', dict);
			if (parseInt(jsonData.reason) == 0){
				guihandler.setErrorDescription(_t(discussionEndFeelFreeToLogin) + '<br>' + _t(clickHereForRegistration));
				guihandler.addListItemsToDiscussionsSpace(listitems);
			} else {
				guihandler.addListItemsToDiscussionsSpace(listitems);
			}
		}
	};

	/**
	 * Adds given json content as argument buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.addJsonDataToContentAsArguments = function (jsonData) {
		var text, helper = new Helper();
		$.each(jsonData, function addJsonDataToContentAsArgumentsEach(key, val) {
			// we only want attacking arguments
			if (val.is_supportive === '0') {
				if (val.text.toLowerCase() !== helper.startWithLowerCase(_t(because))) {
					text = _t(because) + ' ' + helper.start(val.text);
				} else {
					text = val.text;
				}
				$('#li_' + addReasonButtonId).before(helper.getKeyValAsInputInLiWithType(val.uid, text, true, false, false, ''));
			}
		});

		// hover style element for the list elements
		$('#' + argumentListId).children().hover(function () {
			$(this).toggleClass('text-hover');
		});
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonUserDataToAdminContent = function (jsonData) {
		//var tableElement, trElement, tbody, thead, tdElement, spanElement, i;
		var tableElement, trElement, tElement, i, is_argument, thead, tbody;
		tElement = ['', '', '', '', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({class: 'table table-striped table-hover',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});

		trElement = $('<tr>');
		thead = $('<thead>');
		tbody = $('<tbody>');

		for (i = 0; i < tElement.length; i += 1) {
			tElement[i] = $('<th>');
		}

		// add header row
		tElement[0] = $('<th>').text('#');
		tElement[1] = $('<th>').text(_t(firstname));
		tElement[2] = $('<th>').text(_t(surname));
		tElement[3] = $('<th>').text(_t(nickname));
		tElement[4] = $('<th>').text(_t(email));
		tElement[5] = $('<th>').text(_t(group_uid));
		tElement[6] = $('<th>').text(_t(last_action));
		tElement[7] = $('<th>').text(_t(last_login));
		tElement[8] = $('<th>').text(_t(registered));
		tElement[9] = $('<th>').text(_t(gender));

		for (i = 0; i < tElement.length; i += 1) {
			trElement.append(tElement[i]);
		}
		thead.append(trElement);
		tableElement.append(thead);

		// add each user element
		$.each(jsonData, function setJsonDataToAdminContentEach(key, value) {
			trElement = $('<tr>');

			tElement[0] = $('<td>').text(value.uid);
			tElement[1] = $('<td>').text(value.firstname);
			tElement[2] = $('<td>').text(value.surname);
			tElement[3] = $('<td>').text(value.nickname);
			tElement[4] = $('<td>').text(value.email);
			tElement[5] = $('<td>').text(value.group_uid);
			tElement[6] = $('<td>').text(value.last_action);
			tElement[7] = $('<td>').text(value.last_login);
			tElement[8] = $('<td>').text(value.registered);
			tElement[9] = $('<td>').text(value.gender);

			trElement = $('<tr>');
			for (i = 0; i < tElement.length; i += 1) {
				trElement.append(tElement[i]);
			}
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + adminsSpaceForUsersId).empty().append(tableElement);
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonAttackDataToAdminContent = function (jsonData) {
		var tableElement, trElement, tdElement, tbody, thead, spanElement, i, attacks = [], counter;

		tdElement = ['', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({class: 'table table-condensed tablesorter',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});
		tbody = $('<tbody>');
		thead = $('<thead>');

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({class: 'font-semi-bold'});
		}

		// add header row
		spanElement[0].text(_t(uid));
		spanElement[1].text(_t(text));
		counter = 2;
		$.each(jsonData.attacks, function setJsonAttackDataToAdminContentEach(key, value) {
			spanElement[counter].text(value);
			attacks[(counter-2)] = value;
			counter += 1;
		});

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			thead.append(trElement);
		}
		tableElement.append(thead);

		// add each attack element
		$.each(jsonData, function setJsonAttackDataToAdminContentEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}

			tdElement[0].text(value.id);
			tdElement[1].text(value.text);
			tdElement[2].text(value[attacks[0]]);
			tdElement[3].text(value[attacks[1]]);
			tdElement[4].text(value[attacks[2]]);
			tdElement[5].text(value[attacks[3]]);
			tdElement[6].text(value[attacks[4]]);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('text-hover');
			});
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + adminsSpaceForAttacksId).empty().append(tableElement);
	};

}