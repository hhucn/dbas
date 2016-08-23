/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */
	
// https://www.google.com/design/spec/style/color.html#color-color-palette
var fillColorSet = ['rgba(200,230,201,0.4)', 'rgba(255,205,210,0.4)', 'rgba(187,222,251,0.4)', 'rgba(187,222,251,0.4)']; //100
var strokeColorSet = ['#4CAF50', '#F44336', '#2196F3', '#795548']; // 500
var pointStrokeColorSet = ['#2E7D32', '#C62828', '#1565C0', '#4E342E']; // 800

$(document).ready(function mainDocumentReady() {
	
	var labels = collectLabels();
	var absoluteData = collectAbsoluteDataset();
	var relativeData = collectRelativeDataset();
	
	var collected = collectDates(labels, absoluteData, relativeData);
	var collectedLabels = collected[0];
	var collectedAbsoluteData = collected[1];
	var collectedRelativeData = collected[2];
	
	createChart(collectedLabels, 'Collected Absolute', collectedAbsoluteData, $('#reputation_absolute_graph_summary'), '#absolute_graph_summary', 0);
	createChart(collectedLabels, 'Collected Relative', collectedRelativeData, $('#reputation_relative_graph_summary'), '#relative_graph_summary', 1);
	
	createChart(labels, 'Absolute', absoluteData, $('#reputation_absolute_graph'), '#absolute_graph', 2);
	createChart(labels, 'Relative', relativeData, $('#reputation_relative_graph'), '#relative_graph', 3);
	setLegendCSS();
	
});

function collectLabels(){
	var labels = [];
	$.each($('#reputation_table').find('.rep_date'), function(){
		labels.push($(this).text());
	});
	return labels;
}

function collectAbsoluteDataset() {
	var data = [0];
	$.each($('#reputation_table').find('.points'), function (index) {
		data.push(data[index] + parseInt($(this).text()));
	});
	data.splice( $.inArray(0, data), 1 );
	return data;
}

function collectRelativeDataset(){
	var data = [];
	$.each($('#reputation_table').find('.points'), function(){
		data.push(parseInt($(this).text()));
	});
	console.log(data);
	return data;
}

function collectDates(labels, absoluteDataset, relativeDataset){
	var newLables = [];
	var newAbsolute = [];
	var newRelative = [];
	$.each(labels, function(index){
		console.log(labels[index] + ' ' + newLables[newLables.length - 1] + ' ' + (labels[index] == newLables[newLables.length - 1]));
		if (labels[index] == newLables[newLables.length - 1]){
			newAbsolute[newAbsolute.length - 1] = newAbsolute[newAbsolute.length - 1]+ absoluteDataset[index];
			newRelative[newRelative.length - 1] = newRelative[newRelative.length - 1] + relativeDataset[index];
		} else {
			newLables.push(labels[index]);
			newAbsolute.push(absoluteDataset[index]);
			newRelative.push(relativeDataset[index]);
		}
	});
	console.log(newLables);
	console.log(newAbsolute);
	console.log(newRelative);
	
	return [newLables, newAbsolute, newRelative];
}

function createChart (labels, label, displaydata, space, id, count){
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
		}]};
	var chart = new Chart(document.getElementById(id).getContext('2d')).Line(data);
	var div_legend = $('<div>').addClass('chart-legend').append(chart.generateLegend());
	space.prepend(div_legend);
}

function setLegendCSS () {
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