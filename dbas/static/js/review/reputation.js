/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

// https://www.google.com/design/spec/style/color.html#color-color-palette
var fillColorSet = ['rgba(200,230,201,0.4)', 'rgba(255,205,210,0.4)', 'rgba(187,222,251,0.4)', 'rgba(187,222,251,0.4)']; //100
var strokeColorSet = ['#4CAF50', '#F44336', '#2196F3', '#795548']; // 500
var pointStrokeColorSet = ['#2E7D32', '#C62828', '#1565C0', '#4E342E']; // 800

$(document).ready(function () {
    'use strict';

	var labels = collectLabels();
	var absoluteData = collectAbsoluteDataset();
	var relativeData = collectRelativeDataset();

	var collected = collectDates(labels, absoluteData, relativeData);
	var collectedLabels = collected[0];
	var collectedAbsoluteData = collected[1];
	var collectedRelativeData = collected[2];

	createChart(_t('repuationChartSum'), collectedLabels,  collectedAbsoluteData, $('#reputation_absolute_graph_summary'), 'absolute_graph_summary', 0);
	createChart(_t('repuationChartDay'), collectedLabels,  collectedRelativeData, $('#reputation_relative_graph_summary'), 'relative_graph_summary', 2);
	setLegendCSS();

});

/**
 * Returns all labels out of the reputation_borders table
 * @returns {Array}
 */
function collectLabels(){
    'use strict';

	var labels = [];
	$.each($('#reputation_table').find('.rep_date'), function(){
		labels.push($(this).text());
	});
	return labels;
}

/**
 * Returns all points out of the reputation_borders table (cumulative)
 * @returns {number[]}
 */
function collectAbsoluteDataset() {
    'use strict';

	var data = [0];
	$.each($('#reputation_table').find('.points'), function (index) {
		data.push(data[index] + parseInt($(this).text()));
	});
	data.splice( $.inArray(0, data), 1 );
	return data;
}

/**
 * Returns all points out of the reputation_borders table
 * @returns {Array}
 */
function collectRelativeDataset(){
    'use strict';

	var data = [];
	$.each($('#reputation_table').find('.points'), function(){
		data.push(parseInt($(this).text()));
	});
	return data;
}

/**
 * Summarizes data by duplicated labels
 * @param labels array with labels
 * @param absoluteDataset array with values
 * @param relativeDataset array with values
 * @returns {*[]} labels, absoluteDataset, relativeDataset
 */
function collectDates(labels, absoluteDataset, relativeDataset){
    'use strict';

	var newLabels = [];
	var newAbsolute = [];
	var newRelative = [];
	$.each(labels, function(index){
		if (labels[index] === newLabels[newLabels.length - 1]){
			newAbsolute[newAbsolute.length - 1] = newAbsolute[newAbsolute.length - 1] + relativeDataset[index];
			newRelative[newRelative.length - 1] = newRelative[newRelative.length - 1] + relativeDataset[index];
		} else {
			newLabels.push(labels[index]);
			newAbsolute.push(absoluteDataset[index]);
			newRelative.push(relativeDataset[index]);
		}
	});

	return [newLabels, newAbsolute, newRelative];
}

/**
 * Creates and line chart
 *
 * @param label of the line
 * @param labels for the x-axis
 * @param displaydata for the y-axis
 * @param space where the graph will be embedded
 * @param id for the canvas of the graph (with #)
 * @param count int for the color array
 */
function createChart (label, labels, displaydata, space, id, count){
    'use strict';

	space.append('<canvas id="' + id + '" width="' + space.width() + 'px" height="300" style= "display: block; margin: 0 auto;"></canvas>');
	var data = {
		labels : labels,
		datasets : [{
			label: label,
			fillColor : fillColorSet[count],
			strokeColor : strokeColorSet[count],
			pointStrokeColor : pointStrokeColorSet[count],
			pointColor : "#fff",
			// pointHitRadius: 1,
			// pointHoverRadius: 1,
			// pointHoverBorderWidth: 1,
			steppedLine: true,
			data : displaydata,
			hover: {mode: 'single'}
		}]
	};
	if (typeof($('#' + id)) !== 'undefined' && document.getElementById(id) !== null) {
		var chart = new Chart(document.getElementById(id).getContext('2d')).Line(data);
		var div_legend = $('<div>').addClass('chart-legend').append(chart.generateLegend());
		space.prepend(div_legend);
	}
}

/**
 * Beautifies CSS attributes of .chart-legend
 */
function setLegendCSS () {
    'use strict';

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
}
