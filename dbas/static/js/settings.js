/*global $, alert*/


function TrackHandler() {
	'use strict';

	/**
	 *
	 * @param nickname
	 */
	this.getUserTrack = function (nickname) {
		'use strict';
		$.ajax({
			url: 'ajax_get_user_track',
			method: 'POST',
			data: {
				nickname: nickname
			},
			dataType: 'json',
			async: true
		}).done(function ajaxGetUserTrackDone(data) {
			new TrackHandler().setDataInTrackTable(data);

			$('#delete-track').show();
		}).fail(function ajaxGetUserTrackFail() {
			$('#track-table-success').hide();
			$('#track-table-failure').show();
			$('#track-failure-msg').text("Internal Failure");
		});
	};

	/**
	 *
	 * @param nickname
	 */
	this.removeUserTrack = function (nickname) {
		'use strict';
		$.ajax({
			url: 'ajax_remove_user_track',
			method: 'POST',
			data: {
				nickname: nickname
			},
			dataType: 'json',
			async: true
		}).done(function ajaxRemoveUserTrackDone() {
			$('#track-table-space').empty();
			$('#delete-track').hide();
			$('#track-table-success').show();
			$('#track-table-failure').hide();
			$('#track-success-msg').text("Data was successfully removed.");
		}).fail(function ajaxRemoveUserTrackFail() {
			$('#track-table-success').hide();
			$('#track-table-failure').show();
			$('#track-failure-msg').text("Internal Failure");
		});
	};


	/**
	 *
	 * @param jsonData
	 */
	this.setDataInTrackTable = function (jsonData) {
		'use strict';
		var tableElement, trElement, tdElement, spanElement, i;
		tdElement = ['', ''];
		spanElement = ['', ''];
		tableElement = $('<table>');
		tableElement.attr({
			class: 'table table-condensed',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 0px;'
		});

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({
				class: 'font-semi-bold'
			});
		}

		// add header row
		spanElement[0].text('Date / Time');
		spanElement[1].text('Track');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			tableElement.append(trElement);
		}

		// adding the tracks
		$.each($.parseJSON(jsonData), function setDataInTrackTableEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}
			tdElement[0].text(value.date);
			tdElement[1].text(value.track);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			// trElement.hover(function () {
			// $(this).toggleClass('table-hover');
			// });
			tableElement.append(trElement);
		});

		$('#track-table-space').empty();
		$('#track-table-space').append(tableElement);
	};

}

$(function () {
	'use strict';
	$('#request-track').click(function requestTrack() {
		new TrackHandler().getUserTrack($('#table_nickname').text());
		$('#track-table-success').hide();
	$('#track-table-failure').hide();
	});
	$('#delete-track').click(function requestTrack() {
		new TrackHandler().removeUserTrack($('#table_nickname').text());
		$('#track-table-success').hide();
		$('#track-table-failure').hide();
	});

	$('#delete-track').hide();
	$('#track-table-success').hide();
	$('#track-table-failure').hide();

});