/*global $, alert, _t, statement_uid, premisesGroup_uid, argument_uid, attacked_by_relation_uid, attacked_with_relation_uid*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function TrackHandler() {
	'use strict';

	/**
	 *
	 */
	this.getUserTrackData = function(){
		'use strict';
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_user_track',
			method: 'POST',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetUserTrackDone(data) {
			new TrackHandler().getUserTrackDataDone(data);
		}).fail(function ajaxGetUserTrackFail() {
			new TrackHandler().getDataFail();
		});
	};

	/**
	 *
	 */
	this.deleteUserTrackData = function(){
		'use strict';
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_user_track',
			method: 'POST',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetUserTrackDone(data) {
			new TrackHandler().removeUserTrackDataDone(data);
		}).fail(function ajaxGetUserTrackFail() {
			new TrackHandler().getDataFail();
		});
	};

	/**
	 *
	 * @param data
	 */
	this.getUserTrackDataDone = function(data){
		new TrackHandler().setDataInTrackTable(data);
	};

	/**
	 *
	 */
	this.getDataFail = function(){
		$('#' + trackTableSuccessId).hide();
		$('#' + trackTableFailureId).fadeIn('slow');
		$('#' + trackFailureMessageId).text(_t(internalError));
	};

	/**
	 *
	 */
	this.removeUserTrackDataDone = function(){
		$('#' + trackTableSpaceId).empty();
		$('#' + deleteTrackButtonId).hide();
		$('#' + requestTrackButtonId).hide();
		$('#' + trackTableSuccessId).show();
		$('#' + trackTableFailureId).hide();
		$('#' + trackSuccessMessageId).text(_t(dataRemoved));

	};

	/**
	 *
	 * @param jsonData
	 */
	this.setDataInTrackTable = function (jsonData) {
		'use strict';
		var tableElement, trElement, tElement, i, is_argument, parsedData, topic, date, thead, tbody;
		tElement = ['', '', '', '', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({
			class: 'table table-striped table-hover',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 0px;'
		});

		trElement = $('<tr>');
		thead = $('<thead>');
		tbody = $('<tbody>');

		for (i = 0; i < tElement.length; i += 1) {
			tElement[i] = $('<th>');
		}

		// add header row
		tElement[0] = $('<th>').text('#');
		tElement[1] = $('<th>').text(_t(track));
		tElement[2] = $('<th>').text(_t(topicString));
		tElement[3] = $('<th>').text(_t(statement));
		tElement[4] = $('<th>').text(_t(premiseGroup));
		tElement[5] = $('<th>').text(_t(argument));
		tElement[6] = $('<th>').text(_t(attackedBy));
		tElement[7] = $('<th>').text(_t(attackedWith));
		tElement[8] = $('<th>').text(_t(text));
		tElement[9] = $('<th>').text(_t(dateString));

		for (i = 0; i < tElement.length; i += 1) {
			trElement.append(tElement[i]);
		}
		thead.append(trElement);
		tableElement.append(thead);

		// adding the tracks
		var has_data = false;
		parsedData = $.parseJSON(jsonData);
		$.each(parsedData, function setDataInTrackTableEach(issue_key, issue_value) {
			date = issue_value.date;
			topic = issue_value.text;

			$.each(issue_value, function setDataInTrackTableEach(key, value) {
				if (key != 'uid' && key != 'date' && key != 'text' ) {
					has_data = true;
					is_argument = value.is_argument;
					tElement[0] = $('<td>').text(key).attr('title', 'No: ' + key);
					tElement[1] = $('<td>').text(value.uid).attr('title', 'Track ID: ' + value.uid);
					tElement[2] = $('<td>').text(topic).attr('title', 'Date: ' + date);
					tElement[3] = $('<td>').text(value.statement).attr('title', 'Statement ID: ' + value.statement_uid);
					tElement[4] = $('<td>').text(value.premisesGroup).attr('title', 'Premises Groups ID: ' + value.premisesGroup_uid);
					tElement[5] = $('<td>').text(value.argument).attr('title', 'Argument ID: ' + value.argument_uid);
					tElement[6] = $('<td>').text(value.attacked_by_relation).attr('title', 'Relation ID: ' + value.attacked_by_relation_uid);
					tElement[7] = $('<td>').text(value.attacked_with_relation).attr('title', 'Relation ID: ' + value.attacked_with_relation_uid);
					tElement[8] = $('<td>').html(value.text).attr('title', 'Text: ' + value.text);
					tElement[9] = $('<td>').text(value.timestamp).attr('title', 'Timestamp: ' + value.timestamp);

					trElement = $('<tr>');
					for (i = 0; i < tElement.length; i += 1) {
						trElement.append(tElement[i]);
					}
					tbody.append(trElement);
				}
			});
			tableElement.append(tbody);
		});

		$('#' + trackTableSpaceId).empty();
		if (has_data) {
			$('#' + trackTableSpaceId).append(tableElement);
			$('#' + deleteTrackButtonId).fadeIn('slow');
		} else {
			$('#' + trackTableSuccessId).show();
			$('#' + trackSuccessMessageId).text(_t(noTrackedData));
			$('#' + deleteTrackButtonId).hide();
			$('#' + requestTrackButtonId).hide();
		}
	};
}

function HistoryHandler(){
	'use strict';

	/**
	 *
	 */
	this.getUserHistoryData = function(callback){
		'use strict';
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_user_history',
			method: 'POST',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().getUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail() {
			new HistoryHandler().getDataFail();
		});
	};

	/**
	 *
	 */
	this.deleteUserHistoryData = function(){
		'use strict';
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_user_history',
			method: 'POST',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().removeUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail() {
			new HistoryHandler().getDataFail();
		});
	};

	/**
	 *
	 * @param data
	 */
	this.getUserHistoryDataDone = function(data){
		new HistoryHandler().setDataInHistoryTable(data);
	};

	/**
	 *
	 */
	this.getDataFail = function(){
		$('#' + historyTableSuccessId).hide();
		$('#' + historyTableFailureId).fadeIn('slow');
		$('#' + historyFailureMessageId).text(_t(internalError));
	};

	/**
	 *
	 */
	this.removeUserHistoryDataDone = function(){
		$('#' + historyTableSpaceId).empty();
		$('#' + deleteHistoryButtonId).hide();
		$('#' + requestHistoryButtonId).hide();
		$('#' + historyTableSuccessId).show();
		$('#' + historyTableFailureId).hide();
		$('#' + historySuccessMessageId).text(_t(dataRemoved));

	};

	/**
	 *
	 * @param jsonData
	 */
	this.setDataInHistoryTable = function (jsonData) {
		'use strict';
		var tableElement, trElement, tElement, i, parsedData, thead, tbody;
		tElement = ['', '', ''];
		tableElement = $('<table>');
		tableElement.attr({
			class: 'table table-striped table-hover',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 0px;'
		});

		trElement = $('<tr>');
		thead = $('<thead>');
		tbody = $('<tbody>');

		for (i = 0; i < tElement.length; i += 1) {
			tElement[i] = $('<th>');
		}

		// add header row
		tElement[0] = $('<th>').text('#');
		tElement[1] = $('<th>').text('ID');
		tElement[2] = $('<th>').text('URL');
		tElement[3] = $('<th>').text(_t(dateString));

		for (i = 0; i < tElement.length; i += 1) {
			trElement.append(tElement[i]);
		}
		thead.append(trElement);
		tableElement.append(thead);

		// adding the historys
		var has_data = false;
		parsedData = $.parseJSON(jsonData);
		$.each(parsedData, function setDataInHistoryTableEach(history_index, history) {
			has_data = true;
			tElement[0] = $('<td>').text(history_index).attr('title', 'No: ' + history_index);
			tElement[1] = $('<td>').text(history.uid).attr('title', 'History ID: ' + history.uid);
			tElement[2] = $('<td>').html('<a href="' + history.url + '">' + history.url + '</a>').attr('title', 'URL: ' + history.url);
			tElement[3] = $('<td>').text(history.timestamp).attr('title', 'Date: ' + history.timestamp);

			trElement = $('<tr>');
			for (i = 0; i < tElement.length; i += 1) {
				trElement.append(tElement[i]);
			}
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + historyTableSpaceId).empty();
		if (has_data) {
			$('#' + historyTableSpaceId).append(tableElement);
			$('#' + deleteHistoryButtonId).fadeIn('slow');
		} else {
			$('#' + historyTableSuccessId).show();
			$('#' + historySuccessMessageId).text(_t(noTrackedData));
			$('#' + deleteHistoryButtonId).hide();
			$('#' + requestHistoryButtonId).hide();
		}
	};

}

function PasswordHandler(){
	// check password strength
	// based on http://git.aaronlumsden.com/strength.js/
	var upperCase = new RegExp('[A-Z]'),
		lowerCase = new RegExp('[a-z]'),
		numbers = new RegExp('[0-9]'),
		keylist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!%&@#$?_~<>+-*/',
		specialchars = new RegExp('([!,%,&,@,#,$,^,*,?,_,~])');

	this.set_total = function (total, passwordMeter, passwordStrength, passwordExtras) {
		'use strict';
		passwordMeter.removeClass().addClass('col-sm-9');
		passwordStrength.text(_t(strength) + ': ' + _t(veryweak)).fadeIn("slow");

		if (total === 1) {			passwordMeter.addClass('veryweak');	passwordStrength.text(_t(strength) + ': ' + _t(veryweak));
		} else if (total === 2) {	passwordMeter.addClass('weak');		passwordStrength.text(_t(strength) + ': ' + _t(weak));
		} else if (total === 3) {	passwordMeter.addClass('medium');	passwordStrength.text(_t(strength) + ': ' + _t(medium));
		} else if (total > 3) {		passwordMeter.addClass('strong');	passwordStrength.text(_t(strength) + ': ' + _t(strong));
		} else if (passwordExtras){	passwordExtras.fadeOut('slow');
		}
	};

	this.check_strength = function (passwordInput, passwordMeter, passwordStrength, passwordExtras) {
		'use strict';
		var total = 0,
			pw = passwordInput.val();
		if (pw.length > 8) {			total = total + 1;	}
		if (upperCase.test(pw)) {		total = total + 1;	}
		if (lowerCase.test(pw)) {		total = total + 1;	}
		if (numbers.test(pw)) {			total = total + 1;	}
		if (specialchars.test(pw)) {	total = total + 1;	}
		new PasswordHandler().set_total(total, passwordMeter, passwordStrength, passwordExtras);
	};

	// password generator
	this.generate_password = function (output) {
		'use strict';
		var password = '',
			i = 0;
		while (!(upperCase.test(password) && lowerCase.test(password) && numbers.test(password) && specialchars.test(password))) {
			i = 0;
			password = '';
			for (i; i < 8; i = i + 1) {
				password += keylist.charAt(Math.floor(Math.random() * keylist.length));
			}
		}
		output.val(password);
	};
}

$(function () {
	'use strict';

	$('#' + requestTrackButtonId).click(function requestTrack() {
		new TrackHandler().getUserTrackData(true);
		$('#' + trackTableSuccessId).fadeOut('slow');
		$('#' + trackTableFailureId).fadeOut('slow');
		$('#' + trackTableSpaceId).empty();
		$('#' + requestTrackButtonId).val(_t(refreshTrack));
	});

	$('#' + deleteTrackButtonId).hide().click(function deleteTrack() {
		new TrackHandler().deleteUserTrackData();
		$('#' + trackTableSuccessId).fadeOut('slow');
		$('#' + trackTableFailureId).fadeOut('slow');
		$('#' + requestTrackButtonId).val(_t(requestTrack));
	});

	$('#' + requestHistoryButtonId).click(function requestTrack() {
		new HistoryHandler().getUserHistoryData();
		$('#' + historyTableSuccessId).fadeOut('slow');
		$('#' + historyTableFailureId).fadeOut('slow');
		$('#' + historyTableSpaceId).empty();
		$('#' + requestHistoryButtonId).val(_t(refreshHistory));
	});

	$('#' + deleteHistoryButtonId).hide().click(function deleteTrack() {
		new HistoryHandler().deleteUserHistoryData();
		$('#' + historyTableSuccessId).fadeOut('slow');
		$('#' + historyTableFailureId).fadeOut('slow');
		$('#' + requestHistoryButtonId).val(_t(requestHistory));
	});

	$('#' + settingsPasswordInputId).keyup(function passwordInputKeyUp() {
		new PasswordHandler().check_strength($('#' + settingsPasswordInputId), $('#' + settingsPasswordMeterId), $('#' + settingsPasswordStrengthId), $('#' + settingsPasswordExtrasId));
		if ($(this).val().length > 0){
			$('#' + settingsPasswordExtrasId).fadeIn('slow');
		} else {
			$('#' + settingsPasswordExtrasId).fadeOut('slow');
		}
	});

	$('#' + settingsPasswordInfoIconId).click(function passwordInfoIcon() {
		new GuiHandler().showGeneratePasswordPopup();
	});

	$('#' + passwordGeneratorButton).click(function passwordGeneratorButton() {
		new PasswordHandler().generate_password($('#' + passwordGeneratorOutput));
	});

	$('#' + popupPasswordGeneratorButton).click(function passwordGeneratorButton() {
		new PasswordHandler().generate_password($('#' + popupPasswordGeneratorOutput));
	});

	$('#' + settingsPasswordExtrasId).hide();
	$('#' + trackTableSuccessId).hide();
	$('#' + trackTableFailureId).hide();
	$('#' + historyTableSuccessId).hide();
	$('#' + historyTableFailureId).hide();

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); }, // delay, because we do not want a
		// flickering screen
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});
});