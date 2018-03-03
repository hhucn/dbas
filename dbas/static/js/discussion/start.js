/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

$(function () {
    'use strict';
    
    // execute only in the users page
    if (window.location.href.indexOf(mainpage + 'discuss/') !== -1 ||
        window.location.href.indexOf(mainpage + 'discuss') !== -1) {
        new OverviewCharts().create();
    }
});


function OverviewCharts() {
    'use strict';
    
    this.create = function () {
        var input = $("#hidden-chart-data").text().replace(/'/g, "\"");
        var data = eval('(' + input + ')');
        var _this = this;
    
        $.each(data, function (val) {
            _this.__createChart(data[val], val);
        });
    };
        
    this.__createChart = function (input, id) {
        var chart, data, divLegend;
        var space = $('#' + id);
        var canvas = $('<canvas>').attr({
                'id': 'c' + id,
                'width': space.width(),
                'height': space.parent().height(),
                'style': 'display: block; margin: 0 auto;'
            });
        space.append(canvas);
        data = {
            labels: input.labels,
            datasets: [{
                label: input.label,
                fillColor: fillColorSet[id],
                strokeColor: strokeColorSet[id],
                pointStrokeColor: pointStrokeColorSet[id],
                pointColor: "#fff",
                data: input.data,
                hover: {mode: 'single'}
            }]
        };
        try {
            chart = new Chart(document.getElementById('c' + id).getContext('2d')).Line(data);
            divLegend = $('<div>').addClass('chart-legend').append(chart.generateLegend());
            space.prepend(divLegend);
        } catch (err) {
            console.log(err);
        }
    };
}