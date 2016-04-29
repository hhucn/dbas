/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(function () {
	'use strict';

	// send notification to users
	$('#send-notification').each(function () {
		$(this).click(function () {
			var _this = $(this);
			$('#popup-writing-notification-recipient').hide();
			$('#popup-writing-notification').modal('show');
			$('#popup-writing-notification-success').hide();
			$('#popup-writing-notification-failed').hide();
			$('#popup-writing-notification-send').click(function () {
				var url = window.location.href,
					splitted = url.split('/'),
					recipient;
				if (url.indexOf('/user/') != -1) {
					recipient = splitted[splitted.length - 1];
				} else {
					recipient = _this.prev().text();
				}
				sendNotification(recipient.trim()); // declared in notification.js
			});
		});
	});

	new User().getPublicUserData();
});

function User() {
	// https://www.google.com/design/spec/style/color.html#color-color-palette
	// 0 is Blue
	// 1 is Teal
	// 2 is Deep Orange
	// 3 is Brown
	var fillColorSet = ['rgba(187,222,251,0.4)', 'rgba(178,223,219,0.4)', 'rgba(255,204,188,0.4)', 'rgba(215,204,200,0.4']; //100
	var strokeColorSet = ['#2196F3', '#009688', '#FF5722', '#795548']; // 500
	var pointStrokeColorSet = ['#1565C0', '#00695C', '#D84315', '#4E342E']; // 800

	this.getPublicUserData = function () {
		$.ajax({
			url: 'ajax_get_public_user_data',
			method: 'GET',
			data:{'nickname': $('#public_nick').text()},
			dataType: 'json',
			async: true
		}).done(function getPublicUserDataDone(data) {
			new User().callbackDone(data);
		}).fail(function getPublicUserDataFail() {
			new User().callbackFail();
		});
	};

	this.callbackDone = function(jsonData){
		$('#user-activity-chart-space').append('<canvas id="user-activity-canvas" width="500" height="300" style= "display: block; margin: 0 auto;"></canvas>');
		var ctx_act = document.getElementById('user-activity-canvas').getContext('2d'),
			parsedData = $.parseJSON(jsonData),
			datas_act = {
				labels : parsedData.labels1,
				datasets : [{
					label: parsedData.label1,
					fillColor : fillColorSet[0],
					strokeColor : strokeColorSet[0],
					pointStrokeColor : pointStrokeColorSet[0],
					pointColor : "#fff",
					data : parsedData.data1,
					hover: {mode: 'single'}
				}]};

		new Chart(ctx_act).Line(datas_act);

		$('#user-vote-chart-space').append('<canvas id="user-vote-canvas" width="500" height="300" style= "display: block; margin: 0 auto;"></canvas>');
		var ctx_vot = document.getElementById('user-vote-canvas').getContext('2d'),
			datas_vot = {
				labels : parsedData.labels2,
				datasets : [{
					label: parsedData.label2,
					fillColor : fillColorSet[1],
					strokeColor : strokeColorSet[1],
					pointStrokeColor : pointStrokeColorSet[1],
					pointColor : "#fff",
					data : parsedData.data2,
					hover: {mode: 'single'}
				}]};

		new Chart(ctx_vot).Line(datas_vot);
	};

	this.getPublicUserDataFail = function(){
		alert('fail');
	};



}