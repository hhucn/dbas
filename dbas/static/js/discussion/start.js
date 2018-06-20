/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

$(function () {
    'use strict';

    // execute only in the users page
    if (window.location.href === mainpage + 'discuss/' ||
        window.location.href === mainpage + 'discuss') {
        new OverviewCharts().create();
    }
});

function OverviewCharts() {
    'use strict';
    this.options = this.__get_options_dict();
}

OverviewCharts.prototype.create = function () {
    'use strict';
    var input = $("#hidden-chart-data").text().replace(/'/g, "\"");
    var data = JSON.parse(input);
    var _this = this;

    $.each(data, function (val) {
        _this.__createChart(data[val], val);
    });
};

OverviewCharts.prototype.__createChart = function (input, no) {
    'use strict';
    var space = $('#issue_activity_chart_' + no);
    var canvas = $('<canvas>').attr({
        'id': 'c' + no,
        'width': space.width(),
        'height': space.parent().height()
    });
    space.append(canvas);

    var ctx = document.getElementById('c' + no).getContext('2d');
    var data = this.__get_data_dict(no, input);
    var chart_data = {
        type: 'line',
        data: data,
        options: this.options
    };
    try {
        new Chart(ctx, chart_data);
    } catch (err) {
    }
};

OverviewCharts.prototype.__get_data_dict = function (no, input) {
    'use strict';
    var colors = new Colors();
    var color_100_rgba = colors.getAllAsRGB(100, 0.4);
    var color_500_hex = colors.getAllAsHEX(300);
    var clen = color_100_rgba.length;
    return {
        labels: input.label,
        datasets: [{
            label: input.label,
            data: input.data,
            fillColor: fillColorSet[no % clen],
            borderColor: color_500_hex[no % clen],
            backgroundColor: color_100_rgba[no % clen],
            pointColor: colors.get_grey()[900],
            hover: {mode: 'single'}
        }]
    };
};

OverviewCharts.prototype.__get_options_dict = function () {
    'use strict';
    var xAxes = [{
        ticks: {display: false},
        gridLines: {display: false}
    }];
    var yAxes = $.extend([{ticks: {suggestMin: 0}}], xAxes);

    return {
        scales: {xAxes: xAxes, yAxes: yAxes},
        legend: {display: false},
        tooltips: {enabled: false}
    };
};

