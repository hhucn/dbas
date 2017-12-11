/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

$(function () {
    'use strict';

	if (window.location.href.indexOf(mainpage + 'user/') === -1){
		return;
	}

	// send notification to users
	$('#send-notification').each(function () {
		$(this).click(function () {
			var _this = $(this);
			$('#' + popupWritingNotificationRecipient).hide();
			$('#' + popupWritingNotification).modal('show');
			$('#' + popupWritingNotificationSuccess).hide();
			$('#' + popupWritingNotificationFailed).hide();
			$('#' + popupWritingNotificationSend).click(function () {
				var url = window.location.href;
				var splitted = url.split('/');
				var recipient;
				if (url.indexOf('/user/') !== -1) {
					recipient = splitted[splitted.length - 1];
				} else {
					recipient = _this.prev().text();
				}
				new AjaxNotificationHandler().sendNotification(recipient.trim()); // declared in notification.js
			});
		});
	});

	new AjaxUserHandler().getPublicUserData();
});

function User() {
    'use strict';

	// https://www.google.com/design/spec/style/color.html#color-color-palette
	// 0 is Blue
	// 1 is Teal
	// 2 is Deep Orange
	// 3 is Brown
	var fillColorSet = ['rgba(187,222,251,0.4)', 'rgba(178,223,219,0.4)', 'rgba(255,204,188,0.4)', 'rgba(215,204,200,0.4']; //100
	var strokeColorSet = ['#2196F3', '#009688', '#FF5722', '#795548']; // 500
	var pointStrokeColorSet = ['#1565C0', '#00695C', '#D84315', '#4E342E']; // 800

	/**
	 *
	 * @param data
	 */
	this.callbackDone = function(data){
		if (data.error.length !== 0) {
			setGlobalErrorHandler(_t(ohsnap), data.error);
		}

		this.createChart(data, $('#user-activity-chart-space'), 'user-activity-canvas', 0);
		this.createChart(data, $('#user-vote-chart-space'), 'user-vote-canvas', 1);
		// this.createChart(data, $('#user-statement-chart-space'), 'user-statement-canvas', 2);
		// this.createChart(data, $('#user-edit-chart-space'), 'user-edit-canvas', 3);
		this.setLegendCSS();
	};

	/**
	 *
	 * @param parsedData
	 * @param space
	 * @param id
	 * @param count
	 */
	this.createChart = function(parsedData, space, id, count){
		var chart, data, div_legend;
		console.log(space.width());
		space.append('<canvas id="' + id + '" width="' + space.width() + '" height="300" style= "display: block; margin: 0 auto;"></canvas>');
		data = {
			labels : parsedData['labels' + (count+1)],
			datasets : [{
				label: parsedData['label' + (count+1)],
				fillColor : fillColorSet[count],
				strokeColor : strokeColorSet[count],
				pointStrokeColor : pointStrokeColorSet[count],
				pointColor : "#fff",
				// pointHitRadius: 1,
				// pointHoverRadius: 1,
                // pointHoverBorderWidth: 1,
				data : parsedData['data' + (count+1)],
				hover: {mode: 'single'}
			}]};
		chart = new Chart(document.getElementById(id).getContext('2d')).Line(data);
		div_legend = $('<div>').addClass('chart-legend').append(chart.generateLegend());
		space.prepend(div_legend);
	};

	/**
	 *
	 */
	this.setLegendCSS = function() {
		var legend = $('.chart-legend');

		legend.find('ul').css({
			'list-style-type': 'none'
		});
		legend.find('li').css({
			'clear' : 'both',
			'padding': '2px'

		});
		legend.find('span').css({
			'border-radius': '4px',
			'padding': '0.2em',
			'color': 'white'
		}).addClass('lead');
	};
}
