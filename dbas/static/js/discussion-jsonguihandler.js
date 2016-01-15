/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function JsonGuiHandler() {
	'use strict';
	var DEBUG_ATTACK = false;

	/**
	 * Sets three different actions for the statement: agree, disagree, dont know
	 * @param jsonData with text, and uid
	 */
	this.setActionsForStatement = function(jsonData){
		var dict, helper = new Helper(), guihandler = new GuiHandler(), listItems = [];

		dict = {'conclusion_uid': jsonData.uid, 'text': jsonData.text};

		guihandler.setDiscussionsDescription(jsonData.discussion_description, '', dict);

		// build input-tags
		listItems.push(helper.getExtraInputInLiWithType(jsonData.uid, jsonData.agree, '', [attr_support, attr_start]));
		listItems.push(helper.getExtraInputInLiWithType(jsonData.uid, jsonData.disagree, '', [attr_attack, attr_start]));
		listItems.push(helper.getExtraInputInLiWithType(jsonData.uid, jsonData.dont_know, '', [attr_more_about, attr_start]));

		guihandler.addListItemsToDiscussionsSpace(listItems);
	};

	/**
	 * Sets given json content as start statement buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsStartStatement = function (jsonData) {
		var listitems = [], guihandler = new GuiHandler(), helper = new Helper();
		guihandler.setDiscussionsDescription(_t(initialPositionInterest), '' , null);

		// status 1 = we have issues; 0, we habe nothing
		if (jsonData.status == '1') {
			$.each(jsonData.statements, function setJsonDataToContentAsConclusionEach(key, val) {
				listitems.push(helper.getKeyValAsInputInLiWithType(val.uid, val.text + '.', true, false, false, ''));
			});

			if (typeof jsonData.logged_in == "string") {
				listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(newConclusionRadioButtonText), false, false, false, ''));
			}
			guihandler.addListItemsToDiscussionsSpace(listitems);
		} else {
			if (typeof jsonData.logged_in == "string") {
				guihandler.setDiscussionsDescription(_t(firstPositionText), _t(firstPositionText), null);
				guihandler.setNewArgumentButtonOnly(_t(firstConclusionRadioButtonText), true);
				guihandler.checkAndHideNewArgumentButton();
				new InteractionHandler().radioButtonChanged();

			} else {
				guihandler.setDiscussionsDescription(_t(discussionEndFeelFreeToLogin), '', null);
			}
		}

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
		}
		guihandler.setDiscussionsDescription(jsonData.discussion_description, text, dict);

		// adding every premise as radio button
		$.each(jsonData.premises, function setJsonDataToContentAsConclusionEach(key, val) {
			text = '';
			index = 0;
			attributes = {};
			$.each(val, function setJsonDataToContentAsConclusionEachVal(valkey, valval) {
				if (text == '')
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
				new GuiHandler().checkAndHideNewArgumentButton();
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
			listitems = [], dict, premisegroup_uid = 0, id = [], tmp = [];

		// build premise, if there is any
		if (jsonData.premises == '0'){

			// adding new premises will be available, if the user is logged in
			if (typeof jsonData.logged_in == "string") {
				listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, '-', false, false, false, ''));
				guihandler.addListItemsToDiscussionsSpace(listitems);

				guihandler.checkAndHideNewArgumentButton();
				new InteractionHandler().radioButtonChanged();
				if (isSupportive)
					$('#' + addStatementContainerTitleId).html(_t(canYouGiveAReasonFor) + ' ' + jsonData.argument + '?');
				else
					$('#' + addStatementContainerTitleId).html(_t(canYouGiveACounterArgumentWhy1) + ' ' + jsonData.argument + ' ' +_t(canYouGiveACounterArgumentWhy2));
			} else {
				guihandler.setErrorDescription(_t(discussionEndFeelFreeToLogin) + '<br>' + _t(clickHereForRegistration));
			}

			dict = {'argument_uid': jsonData.argument_uid, 'conclusion_id': conclusion_id, 'text': jsonData.argument, 'supportive': isSupportive};
			guihandler.setDiscussionsDescription(jsonData.discussion_description, '', dict);
				new InteractionHandler().setDiscussionEndLinksInText();

		} else {
			dict = {'argument_uid': jsonData.argument_uid,
				'conclusion_id': conclusion,
				'text': jsonData.argument,
				'supportive': 'false',
				'premisegroup_uid' : premisegroup_uid};
			guihandler.setDiscussionsDescription(jsonData.discussion_description, '', dict);

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
				tmp[0] = jsonData.undermine_text    + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undermine + '</i>]') : '');
				tmp[1] = jsonData.support_text      + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_support + '</i>]') : '');
				tmp[2] = jsonData.undercut_text     + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undercut + '</i>]') : '');
				tmp[3] = jsonData.overbid_text      + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_overbid + '</i>]') : '');
				tmp[4] = jsonData.rebut_text        + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_rebut + '</i>]') : '');
				tmp[5] = jsonData.no_opinion_text   + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_no_opinion + '</i>]') : '');
				listitems.push(helper.getKeyValAsInputInLiWithType(id[0], tmp[0], false, false, true, _t(description_undermine)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[1], tmp[1], false, false, true, _t(description_support)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[2], tmp[2], false, false, true, _t(description_undercut)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[3], tmp[3], false, false, true, _t(description_overbid)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[4], tmp[4], false, false, true, _t(description_rebut)));
				listitems.push(helper.getKeyValAsInputInLiWithType(id[5], tmp[5], false, false, true, _t(description_no_opinion)));
			} else {
				tmp[0] = jsonData.undermine_text    + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undermine + '</i>]') : '');
				tmp[1] = jsonData.undercut_text     + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undercut + '</i>]') : '');
				tmp[2] = jsonData.rebut_text        + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_rebut + '</i>]') : '');
				tmp[3] = jsonData.no_opinion_text   + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_no_opinion + '</i>]') : '');
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
			listitems = [], dict, text = [],
			confronation_id = '_argument_' + jsonData.confrontation_argument_id,
			argument_id = '_argument_' + jsonData.argument_id;

		// set discussions text - dictionary needs strings, no variables as keys!
		dict = {'argument': jsonData.argument,
			'argument_uid': jsonData.argument_uid,
			'confrontation_uid': jsonData.confrontation_argument_id,
			'current_attack': jsonData.attack,
			'supportive': isSupportive};
		guihandler.setDiscussionsDescription(jsonData.discussion_description,
				_t(informationForExperts) + ': ' + _t(thisConfrontationIs) + ' ' + jsonData.attack + '.', dict);

		// build the radio buttons
		text[0] = jsonData.undermine_text   + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undermine + '</i>]') : '');
		text[1] = jsonData.support_text     + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_support + '</i>]') : '');
		text[2] = jsonData.undercut_text    + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_undercut + '</i>]') : '');
		text[3] = jsonData.overbid_text     + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_overbid + '</i>]') : '');
		text[4] = jsonData.rebut_text       + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_rebut + '</i>]') : '');
		text[5] = jsonData.no_opinion_text  + ' ' + (DEBUG_ATTACK ? ('[<i>' + attr_no_opinion + '</i>]') : '');
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_undermine	+ confronation_id,	text[0], false, false, true, _t(description_undermine)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_support 	+ confronation_id,	text[1], false, false, true, _t(description_support)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_undercut 	+ confronation_id,	text[2], false, false, true, _t(description_undercut)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_overbid 	+ confronation_id,	text[3], false, false, true, _t(description_overbid)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_rebut 		+ confronation_id,	text[4], false, false, true, _t(description_rebut)));
		listitems.push(helper.getKeyValAsInputInLiWithType(attr_no_opinion 	+ argument_id,		text[5], false, false, true, _t(description_no_opinion)));
		// TODO HOW TO INSERT ATTACKING PREMISEGROUPS?

		// set the buttons
		guihandler.addListItemsToDiscussionsSpace(listitems);

		guihandler.showDisplayControlContainer();
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 * @param isSupportive, true when the premisses are supportive
	 */
	this.setJsonDataAsConfrontationWithoutConfrontation = function (jsonData, isSupportive) {
		var guihandler = new GuiHandler(),
			dict;

		// set discussions text
		dict = {
			'text': jsonData.premise_text,
			'attack': jsonData.relation,
			'related_argument': jsonData.argument_uid,
			'premisegroup_uid': jsonData.premisegroup_uid,
			'conclusion_id': jsonData.conclusion_uid};

		guihandler.setDiscussionsDescription(jsonData.discussion_description, dict);
			new InteractionHandler().setDiscussionEndLinksInText();

		guihandler.hideDisplayControlContainer();
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
			listitems = [], i, reason, id, long_id, dict, text;

		// different case, when we are attacking
		text = jsonData.header_text;
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
			guihandler.setDiscussionsDescription(_t(sentencesOpenersForArguments[0]) + ': ' + text, '', dict);
			// check this item, if it is the only one
			if (parseInt(jsonData.reason) == 0){
				listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(firstOneReason), false, false, false, _t(addPremiseRadioButtonText)));
				guihandler.addListItemsToDiscussionsSpace(listitems);
				guihandler.checkAndHideNewArgumentButton();
				new InteractionHandler().radioButtonChanged();

			} else {
				listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, _t(addPremiseRadioButtonText), false, false, false, _t(addPremiseRadioButtonText)));
				guihandler.addListItemsToDiscussionsSpace(listitems);
			}
			guihandler.hideDiscussionDescriptionsNextElement();
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

}