/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function JsonGuiHandler() {
	'use strict';

	/**
	 * Sets given json content as start statement buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.setJsonDataToContentAsStartStatement = function (jsonData) {
		var listitems = [], guihandler = new GuiHandler(), helper = new Helper();
		guihandler.setDiscussionsDescription(startDiscussionText, '' , null);
		$.each(jsonData, function setJsonDataToContentAsConclusionEach(key, val) {
			listitems.push(helper.getKeyValAsInputInLiWithType(val.uid, val.text + '.', true, false, false, ''));
		});

		// sanity check for an empty list
		if (listitems.length === 0) {
			// todo: is this even used?
			alert('discussion-guihandler.: setJsonDataToContentAsStartStatement');
			guihandler.setDiscussionsDescription(firstOneText + '<b>' + jsonData.currentStatementText + '</b>', '' , null);
		}

		listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, newConclusionRadioButtonText, true, false, ''));

		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given json content as start premisses buttons in the discussions space
	 * @param jsonData data with json content
	 * @param currentStatement
	 */
	this.setJsonDataToContentAsStartPremisses = function (jsonData, currentStatement) {
		var listitems = [], guihandler = new GuiHandler(), text, firstOne = true, helper = new Helper();
		text = helper.startWithLowerCase(currentStatement.text);
		guihandler.setDiscussionsDescription(sentencesOpenersRequesting[0] + ' <b>' + text + '</b> ?', text, {'text': text});

		$.each(jsonData, function setJsonDataToContentAsConclusionEach(key, val) {
			text = '';
			$.each(val, function setJsonDataToContentAsConclusionEachVal(valkey, valval) {
				if (text=='')
					text = 'Because ';
				else
					text += ' <i>_AND_</i> because ';

				text += helper.startWithLowerCase(valval.text);
				firstOne = false;
			});
			text += '.';
			// we are saving the group id ad key
			listitems.push(helper.getKeyValAsInputInLiWithType(key, text, false, true, false, ''));
		});

		listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, firstOne ? addPremisseRadioButtonText : newPremisseRadioButtonText, true, false, ''));

		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 */
	this.setJsonDataAsConfrontation = function (jsonData) {
		var helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			premisse = jsonData.premisse_text,
			opinion,
			confrontationText,
			listitems = [],
			confrontation = jsonData.confrontation.substring(0, jsonData.confrontation.length),
			id = '_argument_' + jsonData.confrontation_id,
			relationArray = helper.createConfrontationsRelationsText(confrontation, conclusion, false, true),
			relation = jsonData.relation;

		if (typeof relation == 'undefined'){
			opinion = '<b>' + conclusion + ', because ' + premisse + '</b>';
		} else {
			opinion = '<b>' + conclusion + '</b> ' + relation + 's ' + '<b>' + premisse + '</b>';
		}

		// build some confrontation text
		if (jsonData.attack == 'undermine'){
			confrontationText = otherParticipantsThinkThat + ' <b>' + premisse + '</b> does not hold, because ';

		} else if (jsonData.attack == 'rebut'){
			confrontationText = otherParticipantsAcceptBut + ' they have a stronger argument for rejecting <b>' + conclusion + ':</b> ';

		} else if (jsonData.attack == 'undercut'){
			confrontationText = otherParticipantsThinkThat + ' <b>' + premisse + '</b> does not justifies that <b>' + conclusion + '</b>, because ';

		}
		confrontationText += '<b>' + confrontation + '</b>. [<i>' + jsonData.attack + '</i>]';

		// set discussions text
		guihandler.setDiscussionsDescription(sentencesOpenersForArguments[0] + ' ' + opinion + '.<br><br>'
			+ confrontationText + '.<br><br>' + whatDoYouThink,
			'This confrontation is a ' + jsonData.attack, {title: '', text: ''});

		// build the radio buttons
		listitems.push(helper.getKeyValAsInputInLiWithType('undermine' + id, relationArray[0] + ' [undermine]', false, false, true, 'undermine'));
		listitems.push(helper.getKeyValAsInputInLiWithType('support' + id, relationArray[1] + ' [support]', false, false, true, 'support'));
		listitems.push(helper.getKeyValAsInputInLiWithType('undercut' + id, relationArray[2] + ' [undercut]', false, false, true, 'undercut'));
		listitems.push(helper.getKeyValAsInputInLiWithType('overbid' + id, relationArray[3] + ' [overbid]', false, false, true, 'overbid'));
		listitems.push(helper.getKeyValAsInputInLiWithType('rebut' + id, relationArray[4] + ' [rebut]', false, false, true, 'rebut'));
		listitems.push(helper.getKeyValAsInputInLiWithType('', '<b><i><u>HOW TO INSERT ATTACKING PREMISEGROUPS?</u></i></b>', false, false, false, ''));

		// set the buttons
		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 */
	this.setJsonDataAsConfrontationWithoutConfrontation = function (jsonData) {
		var helper = new Helper(),
			guihandler = new GuiHandler(),
			conclusion = helper.startWithLowerCase(jsonData.conclusion_text),
			premisse = jsonData.premisse_text,
			opinion,
			confrontationText,
			listitems = [],
			relation = jsonData.relation;

		if (typeof relation == 'undefined'){
			opinion = '<b>' + conclusion + ', because ' + premisse + '</b>';
		} else {
			opinion = '<b>' + conclusion + '</b> ' + relation + 's ' + '<b>' + premisse + '</b>';
		}

		// build some confrontation text
		confrontationText = otherParticipantsDontThinkThat + ' <b>' + premisse + '</b>. [<i>' + jsonData.attack + '</i>]';

		// set discussions text
		guihandler.setDiscussionsDescription(sentencesOpenersForArguments[0] + ' ' + opinion + '.<br><br>'
			+ confrontationText + '.<br><br>' + whatDoYouThink,
			'This confrontation is a ' + jsonData.attack, {title: premisse, text: premisse});

		// build the radio buttons
		listitems.push(helper.getKeyValAsInputInLiWithType('', '<b><i><u>HOW TO INSERT THINGS FOR PGROUP ' + jsonData.premissesgroup_uid + '?</u></i></b>', false, false, false, ''));
		listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, addArgumentRadioButtonText, false, false, false, addArgumentRadioButtonText));

		// set the buttons
		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Sets given data in the list of the discussion space
	 * @param jsonData
	 */
	this.setJsonDataAsConfrontationReasoning = function (jsonData){
		var premisse = jsonData.premissegroup.replace('.',''),
			conclusion = new Helper().startWithLowerCase(jsonData.conclusion_text),
			relationArray = new Helper().createRelationsText(premisse, conclusion, true, false),
			text, listitems = [], i, reason, helper = new Helper(), id,
			guihandler = new GuiHandler(),
			dict;

		if (jsonData.relation === 'undermine') {		text = relationArray[0] + ', but why? (You made an undermine)';
		} else if (jsonData.relation === 'support') {	text = relationArray[1] + ', but why? (You made a support)';
		} else if (jsonData.relation === 'undercut') {	text = relationArray[2] + ', but why? (You made an undercut)';
		} else if (jsonData.relation === 'overbid') {	text = relationArray[3] + ', but why? (You made an overbid)';
		} else if (jsonData.relation === 'rebut') {		text = relationArray[4] + ', but which one? (You made a rebut)';
		}

		for (i=0; i<parseInt(jsonData.reason); i++){
			id = jsonData.relation + '_' + jsonData.type + '_' + jsonData['reason' + i + 'id'];
			reason = 'Because ' + helper.startWithLowerCase(jsonData['reason' + i]) + '.';
			listitems.push(helper.getKeyValAsInputInLiWithType(id, reason, false, true, true, reason));
		}

		dict = {'text': text, 'attack': jsonData.relation, 'attacked_argument': jsonData.argument_uid, 'premissegroup_uid': jsonData.premissegroup_uid};
		guihandler.setDiscussionsDescription(sentencesOpenersForArguments[0] + ' ' + text, '', dict);
		listitems.push(helper.getKeyValAsInputInLiWithType(addReasonButtonId, addPremisseRadioButtonText, false, false, false, addPremisseRadioButtonText));
		guihandler.addListItemsToDiscussionsSpace(listitems);
	};

	/**
	 * Adds given json content as argument buttons in the discussions space
	 * @param jsonData data with json content
	 */
	this.addJsonDataToContentAsArguments = function (jsonData) {
		var guihandler = new GuiHandler(), text, helper = new Helper();
		$.each(jsonData, function addJsonDataToContentAsArgumentsEach(key, val) {
			// we only want attacking arguments
			if (val.is_supportive === '0') {
				if (val.text.toLowerCase() !== 'because') {
					text = "Because " + helper.start(val.text);
				} else {
					text = val.text;
				}
				$('#li_' + addReasonButtonId).before(helper.getKeyValAsInputInLiWithType(val.uid, text, true));
			}
		});

		// hover style element for the list elements
		$('#' + argumentListId).children().hover(function () {
			$(this).toggleClass('table-hover');
		});
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonUserDataToAdminContent = function (jsonData) {
		var tableElement, trElement, tdElement, spanElement, i;
		tdElement = ['', '', '', '', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({class: 'table table-condensed',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({class: 'font-semi-bold'});
		}

		// add header row
		spanElement[0].text('uid');
		spanElement[1].text('Firstname');
		spanElement[2].text('Surname');
		spanElement[3].text('Nickname');
		spanElement[4].text('E-Mail');
		spanElement[5].text('Group');
		spanElement[6].text('Last Action');
		spanElement[7].text('Last Login');
		spanElement[8].text('Registered');
		spanElement[9].text('Gender');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			tableElement.append(trElement);
		}

		// add each user element
		$.each(jsonData, function setJsonDataToAdminContentEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}

			tdElement[0].text(value.uid);
			tdElement[1].text(value.firstname);
			tdElement[2].text(value.surname);
			tdElement[3].text(value.nickname);
			tdElement[4].text(value.email);
			tdElement[5].text(value.group_uid);
			tdElement[6].text(value.last_action);
			tdElement[7].text(value.last_login);
			tdElement[8].text(value.registered);
			tdElement[9].text(value.gender);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('table-hover');
			});
			tableElement.append(trElement);
		});

		$('#' + adminsSpaceId).empty().append(tableElement);
	};

}