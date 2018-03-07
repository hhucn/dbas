/**
 * Script to get more data on the user pages.
 *
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

$(function () {
    'use strict';
    
    // execute only in the users page
    if (window.location.href.indexOf(mainpage + 'user/') === -1) {
        return;
    }
    
    var u = new User();
    u.setNotificationBtn();
    u.getPublicUserData();
});

function User() {
    'use strict';

    // https://www.google.com/design/spec/style/color.html#color-color-palette
    var blue = 'rgba(187,222,251,0.4)';
    var teal = 'rgba(178,223,219,0.4)';
    var deepOrange = 'rgba(255,204,188,0.4)';
    var brown = 'rgba(215,204,200,0.4';
    var fillColorSet = [blue, teal, deepOrange, brown]; // 100
    var strokeColorSet = ['#2196F3', '#009688', '#FF5722', '#795548']; // 500
    var pointStrokeColorSet = ['#1565C0', '#00695C', '#D84315', '#4E342E']; // 800
    
    /**
     * Sets click listener to send notifications to a user
     */
    this.setNotificationBtn = function () {
        // send notification to users
        $('#send-notification').each(function () {
            $(this).click(function () {
                $('#' + popupWritingNotificationRecipient).closest('.form-group').hide();
                $('#' + popupWritingNotification).modal('show');
                $('#' + popupWritingNotificationSuccess).hide();
                $('#' + popupWritingNotificationFailed).hide();
                $('#' + popupWritingNotificationSend).click(function () {
                    var url = window.location.href;
                    var splitted = url.split('/');
                    var recipient;
                    if (url.indexOf('/user/') === -1) {
                        recipient = $(this).prev().text();
                    } else {
                        recipient = splitted[splitted.length - 1];
                    }
                    new AjaxNotificationHandler().sendNotification(recipient.trim()); // declared in notification.js
                });
            });
        });
    };
    
    /**
     * Requests specific user data and will display these in charts
     */
    this.getPublicUserData = function () {
        var url = 'get_public_user_data';
        var d = {
            'nickname': $('#public_nick').text()
        };
        var done = function getPublicUserDataDone(data) {
            var u = new User();
            u.createChart(data, $('#user-activity-chart-space'), 'user-activity-canvas', 0);
            u.createChart(data, $('#user-vote-chart-space'), 'user-vote-canvas', 1);
            u.setLegendCSS();
        };
        var fail = function getPublicUserDataFail(data) {
            setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     * @param parsedData
     * @param space
     * @param id
     * @param count
     */
    this.createChart = function (parsedData, space, id, count) {
        var chart, data, divLegend;
        space.append('<canvas id="' + id + '" width="' + space.width() + '" height="300" style= "display: block; margin: 0 auto;"></canvas>');
        data = {
            labels: parsedData['labels' + (count + 1)],
            datasets: [{
                label: parsedData['label' + (count + 1)],
                fillColor: fillColorSet[count],
                strokeColor: strokeColorSet[count],
                pointStrokeColor: pointStrokeColorSet[count],
                pointColor: "#fff",
                // pointHitRadius: 1,
                // pointHoverRadius: 1,
                // pointHoverBorderWidth: 1,
                data: parsedData['data' + (count + 1)],
                hover: {mode: 'single'}
            }]
        };
        try {
            chart = new Chart(document.getElementById(id).getContext('2d')).Line(data);
            divLegend = $('<div>').addClass('chart-legend').append(chart.generateLegend());
            space.prepend(divLegend);
        } catch (err) {
            //
        }
    };

    /**
     *
     */
    this.setLegendCSS = function () {
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
    };
}
