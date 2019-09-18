// https://www.google.com/design/spec/style/color.html#color-color-palette
var fillColorSet = [
    'rgba(200,230,201,0.4)',
    'rgba(255,205,210,0.4)',
    'rgba(187,222,251,0.4)',
    'rgba(187,222,251,0.4)'
]; //100

$(document).ready(function () {
    'use strict';

    var labels = collectLabels();
    var absoluteData = collectAbsoluteDataset();
    var relativeData = collectRelativeDataset();

    var collected = collectDates(labels, absoluteData, relativeData);
    var collectedLabels = collected[0];
    var collectedAbsoluteData = collected[1];
    var collectedRelativeData = collected[2];

    if (window.location.href.indexOf('review/reputation') !== -1) {
        createChart(_t('repuationChartSum'), collectedLabels, collectedAbsoluteData, $('#reputation_absolute_graph_summary'), 'absolute_graph_summary', 0);
        createChart(_t('repuationChartDay'), collectedLabels, collectedRelativeData, $('#reputation_relative_graph_summary'), 'relative_graph_summary', 2);
        setLegendCSS();
    }

});

/**
 * Returns all labels out of the reputation_borders table
 * @returns {Array}
 */
function collectLabels() {
    'use strict';

    var labels = [];
    $.each($('#reputation_table').find('.rep_date'), function () {
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
    data.splice($.inArray(0, data), 1);
    return data;
}

/**
 * Returns all points out of the reputation_borders table
 * @returns {Array}
 */
function collectRelativeDataset() {
    'use strict';

    var data = [];
    $.each($('#reputation_table').find('.points'), function () {
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
function collectDates(labels, absoluteDataset, relativeDataset) {
    'use strict';

    var newLabels = [];
    var newAbsolute = [];
    var newRelative = [];
    $.each(labels, function (index) {
        if (labels[index] === newLabels[newLabels.length - 1]) {
            newAbsolute[newAbsolute.length - 1] += relativeDataset[index];
            newRelative[newRelative.length - 1] += relativeDataset[index];
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
function createChart(label, labels, displaydata, space, id, count) {
    'use strict';
    var canvas = $('<canvas>').attr({
        'id': id,
        'width': space.width(),
        'height': 300,
        'style': 'display: block; margin: 0 auto;'
    });
    space.append(canvas);

    var colors = new Colors();
    var color_100_rgba = colors.getAllAsRGB(100, 0.4);
    var color_500_hex = colors.getAllAsHEX(500);

    var ctx = document.getElementById(id).getContext('2d');
    var chart_data = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: displaydata,
                fillColor: fillColorSet[count],
                borderColor: color_500_hex[count],
                backgroundColor: color_100_rgba[count],
                pointColor: "#fff",
                steppedLine: true,
                hover: {
                    mode: 'single'
                }
            }]
        },
    };
    if (typeof ($('#' + id)) !== 'undefined' && document.getElementById(id) !== null) {
        try {
            var chart = new Chart(ctx, chart_data);
            var divLegend = $('<div>').addClass('chart-legend').append(chart.generateLegend());
            space.prepend(divLegend);
        } catch (err) {
        }
    }
}

/**
 * Beautifies CSS attributes of .chart-legend
 */
function setLegendCSS() {
    'use strict';

    var legend = $('.chart-legend');

    legend.find('ul').css({
        'list-style-type': 'none'
    });
    legend.find('li').css({
        'clear': 'both',
        'padding': '2px'
    });
    legend.find('span').css({
        'border-radius': '4px',
        'padding': '0.2em',
        'color': 'white'
    }).addClass('lead');
}
