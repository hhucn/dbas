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

    this.create = function () {
        var input = $("#hidden-chart-data").text().replace(/'/g, "\"");
        var data = JSON.parse(input);
        var _this = this;

        $.each(data, function (val) {
            _this.__createChart(data[val], val);
        });
    };

    this.__createChart = function (input, id) {
        var colors = new Colors();
        var color_100_rgba = colors.getAllAsRGB(100, 0.4);
        var color_500_hex = colors.getAllAsHEX(300);
        var clen = color_100_rgba.length;

        var space = $('#issue_activity_chart_' + id);
        var canvas = $('<canvas>').attr({
            'id': 'c' + id,
            'width': space.width(),
            'height': space.parent().height()
        });
        space.append(canvas);

        var ctx = document.getElementById('c' + id).getContext('2d');
        var chart_data = {
            type: 'line',
            data: {
                labels: input.label,
                datasets: [{
                    label: input.label,
                    data: input.data,
                    fillColor: fillColorSet[id % clen],
                    borderColor: color_500_hex[id % clen],
                    backgroundColor: color_100_rgba[id % clen],
                    pointColor: "#fff",
                    hover: {
                        mode: 'single'
                    }
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            display: false,
                            suggestedMin: 0
                        },
                        gridLines: {
                            display:false
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            display: false
                        },
                        gridLines: {
                            display: false
                        }
                    }]
                },
                legend: {
                    display: false
                },
                tooltips: {
                    enabled: false,
                }
            }
        };
        try {
            new Chart(ctx, chart_data);
        } catch (err) {
        }
    };
}
