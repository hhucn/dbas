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
		$('#delete-track').fadeIn('slow');
		new TrackHandler().setDataInTrackTable(data);
	};

	this.getUserTrackDataFail = function(){
		$('#track-table-success').hide();
		$('#track-table-failure').fadeIn('slow');
		$('#track-failure-msg').text("Internal Failure");
	};

	this.removeUserTrackDataDone = function(){
		$('#track-table-space').empty();
		$('#delete-track').hide();
		$('#track-table-success').show();
		$('#track-table-failure').hide();
		$('#track-success-msg').text("Data was successfully removed.");

	};

	this.removeUserTrackDataFail = function(){
		$('#track-table-success').hide();
		$('#track-table-failure').show();
		$('#track-failure-msg').text("Internal Failure");
	};


	/**
	 *
	 * @param jsonData
	 */
	this.setDataInTrackTable = function (jsonData) {
		'use strict';
		var tableElement, trElement, tdElement, spanElement, i, is_argument;
		tdElement = ['', '', '', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', '', '', ''];
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
		spanElement[0].text('No');
		spanElement[1].text('Track ID');
		spanElement[2].text('Statement ID');
		spanElement[3].text('PremisseGroup ID');
		spanElement[4].text('Argument ID');
		spanElement[5].text('Attacked by');
		spanElement[6].text('Attacked with');
		spanElement[7].text('Text');
		spanElement[8].text('Date');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			tableElement.append(trElement);
		}

		// adding the tracks
		var has_data = false;
		$.each($.parseJSON(jsonData), function setDataInTrackTableEach(key, value) {
			has_data = true;
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}
			is_argument = value.is_argument;
			tdElement[0].text(key);
			tdElement[1].text(value.uid);
			tdElement[2].text(value.statement_uid);
			tdElement[3].text(value.premissesGroup_uid);
			tdElement[4].text(value.attacked_by_relation);
			tdElement[5].text(value.argument_uid);
			tdElement[6].text(value.attacked_with_relation);
			tdElement[7].text(value.text);
			tdElement[8].text(value.timestamp);

			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			// trElement.hover(function () {
			// $(this).toggleClass('table-hover');
			// });
			tableElement.append(trElement);
		});

		$('#track-table-space').empty();
		if (has_data) {
			$('#track-table-space').append(tableElement);
		} else {
			$('#track-table-success').show();
			$('#track-success-msg').text("No data was tracked.");
			$('#delete-track').hide();
			$('#request-track').hide();
		}
	};
}

$(function () {
	'use strict';

	$('#request-track').click(function requestTrack() {
		new TrackHandler().manageUserTrackData(true);
		$('#track-table-success').fadeOut('slow');
		$('#track-table-failure').fadeOut('slow');
		$('#track-table-space').empty();
		$('#request-track').val('Refresh track');
	});

	$('#delete-track').click(function requestTrack() {
		new TrackHandler().manageUserTrackData(false);
		$('#track-table-success').fadeOut('slow');
		$('#track-table-failure').fadeOut('slow');
		$('#request-track').val('Request track');
	});

	$('#delete-track').hide();
	$('#track-table-success').hide();
	$('#track-table-failure').hide();
});