/*global $, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function TrackHandler() {
	'use strict';

	/**
	 *
	 * @param get_track_data is true, when the data should be get, false, when it should be deleted
	 */
	this.manageUserTrackData = function(get_track_data){
		'use strict';
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_manage_user_track',
			method: 'POST',
			data: {
				get_data: get_track_data ? '1' : '0'
			},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrfToken }
		}).done(function ajaxGetUserTrackDone(data) {
			var th = new TrackHandler();
			get_track_data ? th.getUserTrackDataDone(data) : th.removeUserTrackDataDone();
		}).fail(function ajaxGetUserTrackFail() {
			var th = new TrackHandler();
			get_track_data ? th.getUserTrackDataFail() : th.removeUserTrackDataFail();
		});
	};

	this.getUserTrackDataDone = function(data){
		$('#' + deleteTrackButtonId).fadeIn('slow');
		new TrackHandler().setDataInTrackTable(data);
	};

	this.getUserTrackDataFail = function(){
		$('#' + trackTableSuccessId).hide();
		$('#' + trackTableFailureId).fadeIn('slow');
		$('#' + trackFailureMessageId).text(_t(internalError));
	};

	this.removeUserTrackDataDone = function(){
		$('#' + trackTableSpaceId).empty();
		$('#' + deleteTrackButtonId).hide();
		$('#' + trackTableSuccessId).show();
		$('#' + trackTableFailureId).hide();
		$('#' + trackSuccessMessageId).text(_t(dataRemoved));

	};

	this.removeUserTrackDataFail = function(){
		$('#' + trackTableSuccessId).hide();
		$('#' + trackTableFailureId).show();
		$('#' + trackFailureMessageId).text(_t(internalError));
	};


	/**
	 *
	 * @param jsonData
	 */
	this.setDataInTrackTable = function (jsonData) {
		'use strict';
		var tableElement, trElement, tdElement, spanElement, i, is_argument, parsedData, topic, date;
		tdElement = ['', '', '', '', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({
			class: 'table table-condensed',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 0px;'
		});

		// todo: DEBUG HERE

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({
				class: 'font-semi-bold'
			});
		}

		// add header row
		spanElement[0].text(_t(number));
		spanElement[1].text(_t(track));
		spanElement[2].text(_t(topicString));
		spanElement[3].text(_t(statement));
		spanElement[4].text(_t(premisseGroup));
		spanElement[5].text(_t(argument));
		spanElement[6].text(_t(attackedBy));
		spanElement[7].text(_t(attackedWith));
		spanElement[8].text(_t(text));
		spanElement[9].text(_t(dateString));

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			tableElement.append(trElement);
		}

		// adding the tracks
		var has_data = false;
		parsedData = $.parseJSON(jsonData);
		$.each(parsedData, function setDataInTrackTableEach(issue_key, issue_value) {
			date = issue_value.date;
			topic = issue_value.text;

			$.each(issue_value, function setDataInTrackTableEach(key, value) {
				if (key != 'uid' && key != 'date' && key != 'text' ) {
					has_data = true;
					for (i = 0; i < tdElement.length; i += 1) {
						tdElement[i] = $('<td>');
					}
					is_argument = value.is_argument;
					tdElement[0].text(key).attr('title', 'No: ' + key);
					tdElement[1].text(value.uid).attr('title', 'Track ID: ' + value.uid);
					tdElement[2].text(topic).attr('title', 'Date: ' + date);
					tdElement[3].text(value.statement).attr('title', 'Statement ID: ' + value.statement_uid);
					tdElement[4].text(value.premissesGroup).attr('title', 'Premisses Groups ID: ' + value.premissesGroup_uid);
					tdElement[5].text(value.argument).attr('title', 'Argument ID: ' + value.argument_uid);
					tdElement[6].text(value.attacked_by_relation).attr('title', 'Relation ID: ' + value.attacked_by_relation_uid);
					tdElement[7].text(value.attacked_with_relation).attr('title', 'Relation ID: ' + value.attacked_with_relation_uid);
					tdElement[8].html(value.text).attr('title', 'Text: ' + value.text);
					tdElement[9].text(value.timestamp).attr('title', 'Timestamp: ' + value.timestamp);

					trElement = $('<tr>');
					for (i = 0; i < tdElement.length; i += 1) {
						trElement.append(tdElement[i]);
					}
					trElement.hover(function () {
						$(this).toggleClass('table-hover');
					});
					tableElement.append(trElement);
				}
			});
		});

		$('#' + trackTableSpaceId).empty();
		if (has_data) {
			$('#' + trackTableSpaceId).append(tableElement);
		} else {
			$('#' + trackTableSuccessId).show();
			$('#' + trackSuccessMessageId).text(_t(noTrackedData));
			$('#' + deleteTrackButtonId).hide();
			$('#request-track').hide();
		}
	};
}

$(function () {
	'use strict';

	$('#request-track').click(function requestTrack() {
		new TrackHandler().manageUserTrackData(true);
		$('#' + trackTableSuccessId).fadeOut('slow');
		$('#' + trackTableFailureId).fadeOut('slow');
		$('#' + trackTableSpaceId).empty();
		$('#request-track').val(_t(refreshTrack));
	});

	$('#' + deleteTrackButtonId).click(function requestTrack() {
		new TrackHandler().manageUserTrackData(false);
		$('#' + trackTableSuccessId).fadeOut('slow');
		$('#' + trackTableFailureId).fadeOut('slow');
		$('#request-track').val(requestTrack);
	});

	$('#' + deleteTrackButtonId).hide();
	$('#' + trackTableSuccessId).hide();
	$('#' + trackTableFailureId).hide();

	// ajax loading animation
	$(document).on({
		ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0); }, // delay, because we do not want a
		// flickering screen
		ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0); }
	});
});