/**
 * @author Tobias Krauthoff, Teresa Uebber
 * @email krauthoff@cs.uni-duesseldorf.de, teresa.uebber@hhu.de
 */

// colors from https://www.google.com/design/spec/style/color.html#color-color-palette
const colors = [
	'#F44336', //  0 red
	'#673AB7', //  1 deep purple
	'#03A9F4', //  2 light blue
	'#4CAF50', //  3 green
	'#FFEB3B', //  4 yellow
	'#FF5722', //  5 deep orange
	'#607D8B', //  6 blue grey
	'#E91E63', //  7 pink
	'#3F51B5', //  8 indigo
	'#00BCD4', //  9 cyan
	'#8BC34A', // 10 light green
	'#FFC107', // 11 amber
	'#795548', // 12 brown
	'#000000', // 13 black
	'#9C27B0', // 14 purple
	'#2196F3', // 15 blue
	'#009688', // 16 teal
	'#CDDC39', // 17 lime
	'#FF9800', // 18 orange
	'#9E9E9E'  // 19 grey
	],
	highlightColors = [
	'#e57373', //  0 red
	'#9575cd', //  1 deep purple
	'#64b5f6', //  2 light blue
	'#81c784', //  3 green
	'#fff176', //  4 yellow
	'#ff8a65', //  5 deep orange
	'#90a4ae', //  6 blue grey
	'#f06292', //  7 pink
	'#7986cb', //  8 indigo
	'#4dd0e1', //  9 cyan
	'#aed581', // 10 light green
	'#ffd54f', // 11 amber
	'#a1887f', // 12 brown
	'#424242', // 13 black
	'#ba68c8', // 14 purple
	'#64b5f6', // 15 blue
	'#4db6ac', // 16 teal
	'#dce775', // 17 lime
	'#ffb74d', // 18 orange
	'#e0e0e0'  // 19 grey
	];

function DiscussionBarometer(){
	'use strict';


	/**
	 * Displays the barometer
	 */
	this.showBarometer = function(){
		let uid = 0, uid_array = [],
			url = window.location.href.split('?')[0],
			splitted = url.split('/'),
			adress = 'position';

		// parse url
		if (url.indexOf('/attitude/') != -1){
			adress = 'attitude';
			uid = splitted[splitted.length-1];
			new AjaxGraphHandler().getUserGraphData(uid, adress);
		} else if (url.indexOf('/justify/') != -1 || window.location.href.indexOf('/choose/') != -1) {
			adress = 'justify';
			$('#discussions-space-list li:not(:last-child) input').each(function(){
				uid_array.push($(this).attr('id').substr(5));
			});
			new AjaxGraphHandler().getUserGraphData(uid_array, adress);
		} else if (url.indexOf('/reaction/') != -1){
			adress = 'argument';
			uid_array.push(splitted[splitted.length-3]);
			uid_array.push(splitted[splitted.length-1]);
			new AjaxGraphHandler().getUserGraphData(uid_array, adress);
		} else {
			adress = 'position';
			$('#discussions-space-list li:not(:last-child) label').each(function(){
				uid_array.push($(this).attr('id'));
			});
			new AjaxGraphHandler().getUserGraphData(uid_array, adress);
		}
	};

	/**
	 * Callback if the ajax request was successfull
	 * @param data: unparsed data of the request
	 * @param adress: step of the discussion
	 */
	this.callbackIfDoneForGetDictionary = function(data, adress){
		let obj, _db = new DiscussionBarometer();
        try{
	        obj = JSON.parse(data);
			console.log(obj);
        } catch(e) {
	        setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(internalError));
			alert('parsing-json: ' + e);
	        return;
        }
		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' div.modal-body')
			.html('<canvas id="chartCanvas" width="400" height="400" style= "display: block; margin: 0 auto; margin-bottom: 20px;"></canvas>');
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		}).removeClass('btn-success');
		$('#' + popupConfirmDialogRefuseBtn).hide();


		switch(adress){
			case 'attitude': _db.createAttitudeBarometer(obj); break;
			case 'position': _db.createStatementBarometer(obj); break;
			case 'justify':  _db.createStatementBarometer(obj); break;
			case 'argument': _db.createArgumentBarometer(obj); break;
		}
		$('#' + popupConfirmDialogId).find('.modal-title').text(obj.title).css({'line-height': '1.0'});
	};

	/**
	 * Creates chart for attitude
	 * @param obj: parsed JSON-object
	 */
	this.createAttitudeBarometer = function(obj) {
		$('#' + popupConfirmDialogId + ' h4.modal-title').html(obj.text);
    	let ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d");

		let pieData = [
        {
			value: obj.agree_users.length,
        	color: colors[3],
			highlight: highlightColors[3],
            label: obj.agree_text
        },
		{
			value: obj.disagree_users.length,
        	color: colors[0],
			highlight: highlightColors[0],
			label: obj.disagree_text
		}
		];

		if (obj.agree_users.length + obj.disagree_users.length == 0){
			this.setAlertIntoDialog();
			$('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").remove();
		} else {
			options = new DiscussionBarometer().createLegendOptions();
			let chart = new Chart(ctx).Pie(pieData, options);
			new DiscussionBarometer().createLegend(chart);
		}
	};

	/**
	 * Creates chart for statement
	 * @param obj: parsed JSON-object
	 */
	this.createStatementBarometer = function(obj) {
		let ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d"),
			chart = new Chart(ctx).Pie(),
			index = 0,
			users = 0;
		$.each(obj.opinions, function(key,value){
			if (value.text != null) {
				chart.addData({
					value: value.users.length,
					color: colors[index],
					highlight: highlightColors[index],
					label: value.text
				});
				users += value.users.length;
				index += 1;
			}
		});

		if (users == 0){
			this.setAlertIntoDialog();
			$('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").remove();
		}
		else {
			let options = new DiscussionBarometer().createLegendOptions();
			$.extend(chart.options, options);
			new DiscussionBarometer().createLegend(chart);
		}
	};

	/**
	 * Creates chart for argument
	 * @param obj: parsed JSON-object
	 */
	this.createArgumentBarometer = function(obj) {
		let ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d"),
			chart = new Chart(ctx).Pie(),
			index = 0,
			users = 0;
		$.each(obj.opinions, function(key, entry) {
			if(key != 'error') {
				chart.addData({
					value: entry.users.length,
					color: colors[index],
					highlight: highlightColors[index],
					label: entry.text
				});
				users += entry.users.length;
				index += 1;
			}
		});

		if (users == 0){
			this.setAlertIntoDialog();
			$('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").remove();
		}
		else{
			let options = new DiscussionBarometer().createLegendOptions();
			$.extend(chart.options, options);
			new DiscussionBarometer().createLegend(chart);
		}
	};

	/**
	 * @return options
	 */
	this.createLegendOptions = function() {
		return options = {
			legendTemplate: '<ul class = "chart">'
				+ '<% for (let i=0; i<segments.length; i++) { %>'
					+ '<li class = "chart">'
						+ '<span class = "chart" style = "background-color: <%=segments[i].fillColor%>"> </span>'
						+ '<% if (segments[i].label) { %><%= segments[i].label %><% } %>'
						+ '<% if (segments[i].value == 0) { %><%= " (0 " + _t_discussion(votes) + ")" %><% } %>'
						+ '<% if (segments[i].value == 1) { %><%= " (" + segments[i].value + " " + _t_discussion(vote) + ")" %><% } %>'
						+ '<% if (segments[i].value > 1) { %><%= " (" + segments[i].value + " " + _t_discussion(votes) + ")" %><% } %>'
					+ '</li>'
				+ '<% } %>'
			+ '</ul>',
			tooltipTemplate: "<%=value%>"
		};
	};

	/**
	 * @param chart
	 */
	this.createLegend = function(chart) {
		let legend = chart.generateLegend();
		$('#' + popupConfirmDialogId + ' div.modal-body').append('<div id = "chart-legend">' + legend + '</div>');
	};

	this.setAlertIntoDialog = function(){
		let div, strong, span;
		div = $('<div>').attr('class', 'alert alert-dismissible alert-info');
		strong = $('<strong>').text('Ohh...! ');
		span = $('<span>').text(_t_discussion(noDecisionstaken));
		div.append(strong).append(span);
		$('#' + popupConfirmDialogId + ' div.modal-body').append(div);
		$('#' + popupConfirmDialogId).on('hidden.bs.modal', function (e) {
			div.remove();
		});
	};
}
