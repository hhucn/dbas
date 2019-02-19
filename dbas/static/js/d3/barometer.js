function DiscussionBarometer() {
    'use strict';
    this._is_attitude = false;
    this._data = [];
    this._address = 'position';
    this._barWidth = 0;
    this._modeEnum = {
        'attitude': 1,
        'justify': 2,
        'argument': 3,
        'position': 4,
    };
    this._mode = 0;
    // colors from https://www.google.com/design/spec/style/color.html#color-color-palette
    // green, red, blue, yellow, deep purple, indigo, light blue, cyan, pink, purple, teal, light green, lime, amber, orange, deep orange
    this.google_colors = [
        //0          1          2          3          4          5          6          7          8          9          10         11         12         13         14
        ['#4caf50', '#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50', '#43a047', '#388e3c', '#2e7d32', '#1b5e20', '#b9f6ca', '#69f0ae', '#00e676', '#00c853'],
        ['#f44336', '#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#ef5350', '#f44336', '#e53935', '#d32f2f', '#c62828', '#b71c1c', '#ff8a80', '#ff5252', '#ff1744', '#d50000'],
        ['#2196f3', '#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1e88e5', '#1976d2', '#1565c0', '#0d47a1', '#82b1ff', '#448aff', '#2979ff', '#2962ff'],
        ['#ffeb3b', '#fffde7', '#fff9c4', '#fff59d', '#fff176', '#ffee58', '#ffeb3b', '#fdd835', '#fbc02d', '#f9a825', '#f57f17', '#ffff8d', '#ffff00', '#ffea00', '#ffd600'],
        ['#673ab7', '#ede7f6', '#d1c4e9', '#b39ddb', '#9575cd', '#7e57c2', '#673ab7', '#5e35b1', '#512da8', '#4527a0', '#311b92', '#b388ff', '#7c4dff', '#651fff', '#6200ea'],
        ['#3f51b5', '#e8eaf6', '#c5cae9', '#9fa8da', '#7986cb', '#5c6bc0', '#3f51b5', '#3949ab', '#303f9f', '#283593', '#1a237e', '#8c9eff', '#536dfe', '#3d5afe', '#304ffe'],
        ['#03a9f4', '#e1f5fe', '#b3e5fc', '#81d4fa', '#4fc3f7', '#29b6f6', '#03a9f4', '#039be5', '#0288d1', '#0277bd', '#01579b', '#80d8ff', '#40c4ff', '#00b0ff', '#0091ea'],
        ['#00bcd4', '#e0f7fa', '#b2ebf2', '#80deea', '#4dd0e1', '#26c6da', '#00bcd4', '#00acc1', '#0097a7', '#00838f', '#006064', '#84ffff', '#18ffff', '#00e5ff', '#00b8d4'],
        ['#e91e63', '#fce4ec', '#f8bbd0', '#f48fb1', '#f06292', '#ec407a', '#e91e63', '#d81b60', '#c2185b', '#ad1457', '#880e4f', '#ff80ab', '#ff4081', '#f50057', '#c51162'],
        ['#9c27b0', '#f3e5f5', '#e1bee7', '#ce93d8', '#ba68c8', '#ab47bc', '#9c27b0', '#8e24aa', '#7b1fa2', '#6a1b9a', '#4a148c', '#ea80fc', '#e040fb', '#d500f9', '#aa00ff'],
        ['#009688', '#e0f2f1', '#b2dfdb', '#80cbc4', '#4db6ac', '#26a69a', '#009688', '#00897b', '#00796b', '#00695c', '#004d40', '#a7ffeb', '#64ffda', '#1de9b6', '#00bfa5'],
        ['#8bc34a', '#f1f8e9', '#dcedc8', '#c5e1a5', '#aed581', '#9ccc65', '#8bc34a', '#7cb342', '#689f38', '#558b2f', '#33691e', '#ccff90', '#b2ff59', '#76ff03', '#64dd17'],
        ['#cddc39', '#f9fbe7', '#f0f4c3', '#e6ee9c', '#dce775', '#d4e157', '#cddc39', '#c0ca33', '#afb42b', '#9e9d24', '#827717', '#f4ff81', '#eeff41', '#c6ff00', '#aeea00'],
        ['#ffc107', '#fff8e1', '#ffecb3', '#ffe082', '#ffd54f', '#ffca28', '#ffc107', '#ffb300', '#ffa000', '#ff8f00', '#ff6f00', '#ffe57f', '#ffd740', '#ffc400', '#ffab00'],
        ['#ff9800', '#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726', '#ff9800', '#fb8c00', '#f57c00', '#ef6c00', '#e65100', '#ffd180', '#ffab40', '#ff9100', '#ff6d00'],
        ['#ff5722', '#fbe9e7', '#ffccbc', '#ffab91', '#ff8a65', '#ff7043', '#ff5722', '#f4511e', '#e64a19', '#d84315', '#bf360c', '#ff9e80', '#ff6e40', '#ff3d00', '#dd2c00']
    ];
}

/**
 * Displays barometer.
 */
DiscussionBarometer.prototype.showBarometer = function () {
    'use strict';
    var uid = 0, uid_array = [];

    var url = window.location.href;
    url = url.split('#')[0];
    url = url.split('?')[0];

    var splitted = url.split('/');
    var inputs = $('#discussions-space-list').find('li:visible:not(:last-child) input');

    // parse url
    if (url.indexOf('/attitude/') !== -1) {
        this._address = 'attitude';
        uid = parseInt(splitted[splitted.length - 1]);
        new AjaxGraphHandler().getUserGraphData([uid], this._address);

    } else if (url.indexOf('/justify/') !== -1 || url.indexOf('/choose/') !== -1) {
        this._address = 'justify';
        // dont know step
        var tmp = url.split('?')[0].split('/');
        if (tmp[tmp.length - 1] === 'dontknow') {
            this._address = 'dont_know';
            uid_array.push(parseInt(tmp[tmp.length - 2]));
        } else {
            inputs.each(function () {
                uid_array.push($(this).attr('id').substr(5));
            });
        }
        new AjaxGraphHandler().getUserGraphData(uid_array, this._address);

    } else if (url.indexOf('/reaction/') !== -1) {
        this._address = 'argument';
        uid_array.push(parseInt(splitted[splitted.length - 3]));
        uid_array.push(parseInt(splitted[splitted.length - 1]));
        new AjaxGraphHandler().getUserGraphData(uid_array, this._address);

    } else {
        this._address = 'position';
        inputs.each(function () {
            uid_array.push(parseInt($(this).attr('id').substr(5)));
        });
        new AjaxGraphHandler().getUserGraphData(uid_array, this._address);
    }
};

/**
 * Callback if ajax request was successful.
 *
 * @param inputdata: unparsed data of request
 * @param addressUrl: step of discussion
 */
DiscussionBarometer.prototype.callbackIfDoneForGetDictionary = function (inputdata, addressUrl) {
    'use strict';
    this._address = addressUrl;
    try {
        this._mode = this._modeEnum[this._address];
    } catch (e) {
        setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(internalError));
        return;
    }

    if (inputdata.info.length !== 0) {
        setGlobalInfoHandler('Hey', inputdata.info);
        return;
    }

    // fetch zero users
    if (this.isEverythingZero(inputdata)) {
        setGlobalInfoHandler('Hey', _t_discussion(otherParticipantsDontHaveOpinionForThis));
        return -1;
    }

    this._data = inputdata;

    this.removeContentOfModal();

    // change status of toggle
    $('#chart-btn').toggle('off');
    // add listener for buttons to change the type of chart
    this.addListenerForChartButtons();
    // create bar chart as default view
    this.getD3BarometerBarChart();

    $('#' + popupBarometerId).modal('show').on('hidden.bs.modal', function () {
        clearAnchor();
    });

    $('#' + popupBarometerAcceptBtn).show().click(function () {
        $('#' + popupBarometerId).modal('hide');
    }).removeClass('btn-success');
    $('#' + popupBarometerRefuseBtn).hide();

    $('#' + popupBarometerId).find('.modal-title').html(this._data.title).css({'line-height': '1.0'});
};

/**
 * Remove content of barometer-modal.
 */
DiscussionBarometer.prototype.removeContentOfModal = function () {
    'use strict';
    $('#modal-body-chart-place').empty();
    $('#' + popupBarometerId).find('.col-md-5').empty();
};

/**
 * Add listeners for chart-buttons.
 */
DiscussionBarometer.prototype.addListenerForChartButtons = function () {
    'use strict';
    // show chart which refers to state of toggle-button
    var _this = this;
    $('#chart-btn-div').click(function () {
        // bar chart icon is visible
        if ($('#chart-btn').is(':checked')) {
            _this.getD3BarometerBarChart();
        }
        // doughnut chart icon is visible
        else {
            _this.getD3BarometerDoughnutChart();
        }
    });
};

/**
 * Create barometer.
 */
DiscussionBarometer.prototype.getD3BarometerBarChart = function () {
    'use strict';
    this.removeContentOfModal();

    // create div for barometer
    $('#modal-body-chart-place').append('<div id="barometer-div"></div>');
    // width and height of chart
    var width = 400;
    var height = this._mode === this._modeEnum.attitude ? 300 : 400;
    var barChartSvg = this.getSvg(width + 70, height + 50).attr("id", "barometer-svg");

    var usersDict = this.getUsersDict([]);

    // create bars of chart
    // selector = inner-rect: clicks on statement relative to seen_by value
    this.createBar(usersDict, width, height - 50, barChartSvg, "inner-rect");
    if (this._address !== 'argument' && this._address !== 'attitude') {
        this.createBar(usersDict, width, height - 50, barChartSvg, "outer-rect");
    }

    // create axis
    if (this._address === 'argument' || this._address === 'attitude') {
        this.createXAxis(usersDict, barChartSvg, width, height + 10);
    } else {
        this.createYAxis(barChartSvg, height - 50);
    }

    // if length of usersDict is greater then 0 add legend and tooltip
    if (usersDict.length > 0) {
        // create legend for chart
        this.createLegend(usersDict);
        // tooltip
        this.addListenerForTooltip(usersDict, barChartSvg, "rect");
    }
};

/**
 *
 * @param usersDict
 */
DiscussionBarometer.prototype.isEverythingZero = function (usersDict) {
    'use strict';
    // counting depends on address
    this._is_attitude = this._address === 'attitude';
    var count = 0;
    if (this._is_attitude) {
        count = usersDict.agree.seenBy + usersDict.disagree.seenBy;
    } else {
        $.each(usersDict.opinions, function (index, value) {
            count += value.seenBy;
        });
    }
    return count === 0;
};

/**
 * Create users dict depending on address
 *
 * @param usersDict
 * @returns {Array}
 */
DiscussionBarometer.prototype.getUsersDict = function (usersDict) {
    'use strict';
    // create dictionary depending on address
    this._is_attitude = this._address === 'attitude';
    if (this._is_attitude) {
        usersDict = this.createDictForAttitude(usersDict);
    } else {
        usersDict = this.createDictForArgumentAndStatement(usersDict);
    }
    return usersDict;
};

/**
 * Create svg-element.
 *
 * @param width: width of container, which contains barometer
 * @param height: height of container
 * @return scalable vector graphic
 */
DiscussionBarometer.prototype.getSvg = function (width, height) {
    'use strict';
    return d3.select('#barometer-div').append('svg').attr({width: width, height: height});
};

/**
 * Create x-axis for barometer.
 *
 * @param usersDict
 * @param svg
 * @param width
 * @param height
 */
DiscussionBarometer.prototype.createXAxis = function (usersDict, svg, width, height) {
    'use strict';
    var maxUsersNumber = this.getMaximum(usersDict);
    // add offset on scale
    var offset = 5 / 100 * maxUsersNumber;

    var xScale = d3.scale.linear().domain([0, maxUsersNumber + offset]).range([0, width]);

    // create y-axis
    var xAxis = d3.svg.axis().scale(xScale).orient("bottom");
    svg.append("g")
        .attr({id: "xAxis", transform: "translate(50," + height + ")"})
        .call(xAxis);
};

/**
 * Find maximum of userNumber-values.
 *
 * @param usersDict
 */
DiscussionBarometer.prototype.getMaximum = function (usersDict) {
    'use strict';
    var maxUsersNumber = 0;
    $.each(usersDict, function (key, value) {
        if (value.usersNumber > maxUsersNumber) {
            maxUsersNumber = value.usersNumber;
        }
    });
    return maxUsersNumber;
};

/**
 * Create y-axis for barometer.
 *
 * @param svg
 * @param height
 */
DiscussionBarometer.prototype.createYAxis = function (svg, height) {
    'use strict';
    var yScale = d3.scale.linear().domain([0, 100]).range([height, 0]);

    // create y-axis
    var yAxis = d3.svg.axis().scale(yScale).orient("left");
    svg.append("g")
        .attr({id: "yAxis", transform: "translate(50,50)"})
        .call(yAxis)
        .append("text")
        .attr({dx: "0.5em", dy: "-1.5em"})
        .style("text-anchor", "end")
        .text("%");
};

/**
 * Add length of each user-dictionary and value of key seen_by to array.
 * @param usersDict
 * @returns usersDict
 */
DiscussionBarometer.prototype.createDictForAttitude = function (usersDict) {
    'use strict';
    usersDict.push({
        usersNumber: this._data.agree.users.length,
        seenBy: this._data.seen_by,
        text: this._data.agree.text,
        users: this._data.agree.users,
        message: this._data.agree.message
    });
    usersDict.push({
        usersNumber: this._data.disagree.users.length,
        seenBy: this._data.seen_by,
        text: this._data.disagree.text,
        users: this._data.disagree.users,
        message: this._data.disagree.message
    });
    return usersDict;
};

/**
 * Add length of each user-dictionary and value of key seen_by to array.
 * @param usersDict
 * @returns usersDict
 */
DiscussionBarometer.prototype.createDictForArgumentAndStatement = function (usersDict) {
    'use strict';
    $.each(this._data.opinions, function (key, value) {
        usersDict.push({
            usersNumber: value.users.length,
            seenBy: value.seen_by,
            text: value.text,
            message: value.message,
            users: value.users
        });
    });
    return usersDict;
};

/**
 * Create bars for chart.
 *
 * @param usersDict
 * @param width
 * @param height
 * @param barChartSvg
 * @param selector
 */
DiscussionBarometer.prototype.createBar = function (usersDict, width, height, barChartSvg, selector) {
    'use strict';
    // if the chart is a bar chart, subtract offset on scale from width
    if (this._address === "argument" || this._address === "attitude") {
        var maxUsersNumber = this.getMaximum(usersDict);
        var offset = 5 / 100 * maxUsersNumber;
        width = width - (width / (maxUsersNumber + offset) * offset);
    }
    // width of one bar
    // width/height - left padding to y-Axis - space between bars
    var tmp = this._address === "argument" || this._address === "attitude" ? height : width;
    this._barWidth = (tmp - 10 - (usersDict.length - 1) * 10) / usersDict.length;

    var y_offset_height = 60;
    // set max-width of bar
    if (this._barWidth > 100) {
        this._barWidth = 100;
        y_offset_height = height - usersDict.length * this._barWidth;
    }

    this.testNoArgumentsCreateRects(usersDict, barChartSvg, width, height, y_offset_height, selector);
    this.createRects(usersDict, barChartSvg, width, height, y_offset_height, selector);
};

/**
 * If there are no arguments create one thin bar.
 *
 * @param usersDict
 * @param barChartSvg
 * @param width
 * @param height
 * @param y_offset_height
 * @param selector
 */
DiscussionBarometer.prototype.testNoArgumentsCreateRects = function (usersDict, barChartSvg, width, height, y_offset_height, selector) {
    'use strict';
    // if there are no arguments show one thin bar
    var maxUsersNumber = this.getMaximum(usersDict);
    if (usersDict.length === 0) {
        barChartSvg.append("rect")
            .attr({
                width: this.getRectWidth(0, width, maxUsersNumber),
                height: this.getRectHeight(0, 0, height, selector),
                x: this.getRectX(0),
                y: this.getRectY(0, 0, 0, y_offset_height, height, selector),
                fill: this.getRectColor(0, selector),
                id: selector + "-" + 0
            });
    }
};

/**
 * Create bars.
 *
 * @param usersDict
 * @param barChartSvg
 * @param width
 * @param height
 * @param y_offset_height
 * @param selector
 */
DiscussionBarometer.prototype.createRects = function (usersDict, barChartSvg, width, height, y_offset_height, selector) {
    'use strict';
    var maxUsersNumber = this.getMaximum(usersDict);
    var _this = this;
    barChartSvg.selectAll(selector)
        .data(usersDict)
        .enter().append("rect")
        .attr({
            width: function (d) {
                return _this.getRectWidth(d.usersNumber, width, maxUsersNumber);
            },
            height: function (d) {
                return _this.getRectHeight(d.usersNumber, d.seenBy, height, selector);
            },
            x: function (d, i) {
                return _this.getRectX(i);
            },
            y: function (d, i) {
                return _this.getRectY(d.usersNumber, d.seenBy, i, y_offset_height, height, selector);
            },
            fill: function (d, i) {
                return _this.getRectColor(i, selector);
            },
            id: function (d, i) {
                return selector + "-" + i;
            }
        });
};

/**
 * Calculate width of one bar.
 *
 * @param usersNumber
 * @param width
 * @param maxUsersNumber
 * @returns {*}
 */
DiscussionBarometer.prototype.getRectWidth = function (usersNumber, width, maxUsersNumber) {
    'use strict';
    // height in percent: length/seen_by = x/height
    if (this._address === "argument" || this._address === "attitude") {
        return this.divideWrapperIfZero(usersNumber, maxUsersNumber) * width;
    } else {
        return this._barWidth;
    }
};

/**
 * Calculate height of one bar.
 *
 * @param usersNumber
 * @param seenBy
 * @param height
 * @param selector
 * @returns {*}
 */
DiscussionBarometer.prototype.getRectHeight = function (usersNumber, seenBy, height, selector) {
    'use strict';
    // number of bar * width of bar + padding-left + space between to bars
    if (this._address === "argument" || this._address === "attitude") {
        return this._barWidth;
    }
    if (selector === 'inner-rect') {
        return this.divideWrapperIfZero(usersNumber, seenBy) * height;
    }
    return height - (this.divideWrapperIfZero(usersNumber, seenBy) * height);
};

/**
 * Calculate x coordinate of bar.
 *
 * @param i
 * @returns {number}
 */
DiscussionBarometer.prototype.getRectX = function (i) {
    'use strict';
    if (this._address === "argument" || this._address === "attitude") {
        return 50;
    }
    return i * this._barWidth + 60 + i * 10;
};

/**
 * Calculate y coordinate of bar.
 *
 * @param usersNumber
 * @param seenBy
 * @param i
 * @param y_offset_height
 * @param height
 * @param selector
 * @returns {*}
 */
DiscussionBarometer.prototype.getRectY = function (usersNumber, seenBy, i, y_offset_height, height, selector) {
    'use strict';
    // y: height - barLength, because d3 starts to draw in left upper corner
    if (this._address === "argument" || this._address === "attitude") {
        return i * this._barWidth + y_offset_height + i * 10;
    }
    if (selector === 'inner-rect') {
        return height - (this.divideWrapperIfZero(usersNumber, seenBy) * height - 50);
    }
    return 50;
};

/**
 * Get color of one bar.
 *
 * @param i
 * @param selector
 * @returns {*}
 */
DiscussionBarometer.prototype.getRectColor = function (i, selector) {
    'use strict';
    if (selector === 'inner-rect') {
        return this.getBaseColorFor(i);
    }
    return this.getLightColorFor(i);
};

/**
 * Wrapper for division
 *
 * @param numerator int
 * @param denominator int
 * @returns {number}
 */
DiscussionBarometer.prototype.divideWrapperIfZero = function (numerator, denominator) {
    'use strict';
    return denominator === 0 || numerator === 0 ? 0.005 : numerator / denominator;
};

/**
 * Create doughnut chart.
 *
 * @param doughnutChartSvg
 * @param usersDict
 */
DiscussionBarometer.prototype.createDoughnutChart = function (doughnutChartSvg, usersDict) {
    'use strict';
    var height = 400, width = 400,
        outerRadius = Math.min(width, height) / 2,
        innerRadius = 0.3 * outerRadius;

    var doughnut = this.getDoughnut(usersDict);

    var ldata = [];
    // if there is no argument create donut-chart with one sector with small radius
    if (usersDict.length === 0) {
        ldata.push({
            usersNumber: 0,
            seenBy: 0
        });
    } else {
        ldata = usersDict;
    }

    var innerCircle = this.getInnerCircle(innerRadius, outerRadius, ldata);
    var outerCircle = this.getOuterCircle(innerRadius, outerRadius);
    this.createOuterPath(doughnutChartSvg, outerCircle, doughnut, ldata);
    this.createInnerPath(doughnutChartSvg, innerCircle, doughnut, ldata);
};

/**
 * Choose layout of d3.
 *
 * @param data
 * @returns {*}
 */
DiscussionBarometer.prototype.getDoughnut = function (data) {
    'use strict';
    var sumUsersNumber = 0;
    $.each(data, function (key, value) {
        sumUsersNumber += value.usersNumber;
    });
    return d3.layout.pie()
        .sort(null)
        .value(function (d, i) {
            // if all arguments have not been seen by anyone,
            // then all sectors have the same angle
            if (sumUsersNumber === 0) {
                return 1;
            }
            // if the argument has not been seen by anyone,
            // then the height of the sector is 2% of the number of all users
            else if (data[i].usersNumber === 0) {
                return (sumUsersNumber * 2) / 100;
            }
            return data[i].usersNumber;
        });
};

/**
 * Create inner circle of chart.
 *
 * @param innerRadius
 * @param outerRadius
 * @param data
 * @returns {*}
 */
DiscussionBarometer.prototype.getInnerCircle = function (innerRadius, outerRadius, data) {
    'use strict';
    return d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(function (d, i) {
            // if the user can only decide between agree and disagree: the height of sector is not dependent on seen-by-value
            if (this._address === "attitude") {
                return (outerRadius - innerRadius) + innerRadius;
            }
            // if nobody has chosen the argument then the height of the sector is 2% of the difference between innerRadius and outerRadius
            if (data[i].usersNumber === 0) {
                return ((outerRadius - innerRadius) * 2) / 100 + innerRadius;
            }
            return (outerRadius - innerRadius) * (data[i].usersNumber / data[i].seenBy) + innerRadius;
        });
};

/**
 * Create outer circle of chart.
 *
 * @param innerRadius
 * @param outerRadius
 * @returns {*}
 */
DiscussionBarometer.prototype.getOuterCircle = function (innerRadius, outerRadius) {
    'use strict';
    return d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);
};

/**
 * Create inner path.
 *
 * @param doughnutChartSvg
 * @param innerCircle
 * @param doughnut
 * @param data
 */
DiscussionBarometer.prototype.createInnerPath = function (doughnutChartSvg, innerCircle, doughnut, data) {
    'use strict';
    var _this = this;
    doughnutChartSvg.selectAll(".innerCircle")
        .data(doughnut(data))
        .enter().append("path")
        .attr({
            'fill': function (d, i) {
                return _this.getBaseColorFor(i);
            },
            'stroke': "gray", d: innerCircle,
            'transform': "translate(240,230)",
            'id': function (d, i) {
                return "inner-path-" + i;
            },
            'class': "chart-sector"
        });
};

/**
 * Create outer path.
 *
 * @param doughnutChartSvg
 * @param outerCircle
 * @param doughnut
 * @param data
 */
DiscussionBarometer.prototype.createOuterPath = function (doughnutChartSvg, outerCircle, doughnut, data) {
    'use strict';
    var _this = this;
    doughnutChartSvg.selectAll(".outerCircle")
        .data(doughnut(data))
        .enter().append("path")
        .attr({
            'fill': function (d, i) {
                return _this.getLightColorFor(i);
            },
            'stroke': "gray", d: outerCircle,
            'transform': "translate(240,230)",
            'id': function (d, i) {
                return "outer-path-" + i;
            },
            'class': "chart-sector"
        });
};

/**
 * Create short tooltip for doughnut chart in middle of chart.
 *
 * @param doughnutChartSvg
 * @param usersDict
 * @param index
 */
DiscussionBarometer.prototype.createShortTooltipDoughnutChart = function (doughnutChartSvg, usersDict, index) {
    'use strict';
    // append tooltip in middle of doughnut chart
    // text of tooltip depends on address
    var tooltipText;
    if (this._address === "attitude") {
        tooltipText = usersDict[index].usersNumber;
    } else {
        tooltipText = usersDict[index].usersNumber + "/" + usersDict[index].seenBy;
    }
    doughnutChartSvg.append("text")
        .attr({
            'x': 240,
            'y': 230,
            'class': "doughnut-chart-text-tooltip", "font-weight": "bold", "font-size": "25px"
        })
        .text(tooltipText);

    tooltipText = _t(clickedOnThis);
    doughnutChartSvg.append("text").attr({
        'x': 240,
        'y': 250,
        'class': "doughnut-chart-text-tooltip"
    }).text(tooltipText);
};

// bar chart and doughnut chart
/**
 * Create tooltips for bar chart and doughnut chart.
 *
 * @param usersDict
 * @param chartSvg
 * @param selector: different selectors for bar chart and doughnut chart
 */
DiscussionBarometer.prototype.addListenerForTooltip = function (usersDict, chartSvg, selector) {
    'use strict';
    var isClicked = false;
    var tooltipIsVisible = false;
    // save index and id of object of last click event
    var elementIndex;
    var _index;
    var _this = this;

    // add listener for click event
    chartSvg.selectAll(selector).on('click', function (d, index) {
        // sector of doughnut chart and part which represents the seen-by-value should have the same index
        elementIndex = index % usersDict.length;
        if (isClicked) {
            if (_index !== elementIndex) {
                _this.hideTooltip(selector, _index);
                _this.showTooltip(usersDict, elementIndex, chartSvg, selector);
                isClicked = true;
                tooltipIsVisible = true;
            } else { // if the user clicks on the same tooltip for a second time hide the tooltip
                _this.hideTooltip(selector, elementIndex);
                isClicked = false;
                tooltipIsVisible = false;
            }
        } else {
            if (!tooltipIsVisible) {
                _this.showTooltip(usersDict, elementIndex, chartSvg, selector);
            }
            isClicked = true;
            tooltipIsVisible = true;
        }
        _index = elementIndex;
    }).on("mouseover", function (d, index) { // add listener for hover event
        if (!isClicked) {
            elementIndex = index % usersDict.length;

            _this.showTooltip(usersDict, elementIndex, chartSvg, selector);
            tooltipIsVisible = true;
        }
    }).on("mouseout", function (d, index) { // add listener for mouse out event
        if (!isClicked) {
            elementIndex = index % usersDict.length;

            _this.hideTooltip(selector, elementIndex);
            tooltipIsVisible = false;
        }
    });

    // add click-event-listener for avatar-icons
    $(document).on('click', '.img-circle', function () {
        window.location = $(this).attr('data-href');
    });

    // add click-event-listener for popup
    $('#' + popupBarometerId).on('click', function (d) {
        // select area of popup without tooltip and listen for click event
        // if tooltip is visible hide tooltip
        if (d.target.id.indexOf("path") === -1 && d.target.id.indexOf("rect") === -1 && tooltipIsVisible === true) {
            _this.hideTooltip(selector, elementIndex);
            isClicked = false;
            tooltipIsVisible = false;
        }
    });
};

/**
 * Show tooltip on mouse event.
 *
 * @param usersDict
 * @param index
 * @param chartSvg
 * @param selector
 */
DiscussionBarometer.prototype.showTooltip = function (usersDict, index, chartSvg, selector) {
    'use strict';
    this.getTooltip(usersDict, index);
    // if doughnut chart is selected add short tooltip in middle of chart
    var el = '';
    if (selector === ".chart-sector") {
        this.createShortTooltipDoughnutChart(chartSvg, usersDict, index);
        el = 'path'; // highlight whole sector on hover
    } else {
        el = 'rect'; // highlight sector on hover
    }
    d3.select('#inner-' + el + '-' + index).attr('fill', this.getDarkColorFor(index));
    d3.select('#outer-' + el + '-' + index).attr('fill', this.getNormalColorFor(index));
    $('#legendLi_' + index).css('background', '#CFD8DC');
};

/**
 * Hide tooltip on mouse event.
 *
 * @param selector
 * @param index
 */
DiscussionBarometer.prototype.hideTooltip = function (selector, index) {
    'use strict';
    var el = '';
    var chartTooltip = $('.chartTooltip');
    chartTooltip.remove();
    // hide tooltip with detailed information
    chartTooltip.css("opacity", 0);

    $('#legendLi_' + index).css('background', '');

    // if doughnut chart is selected hide text in middle of doughnut
    if (selector === ".chart-sector") {
        $('.doughnut-chart-text-tooltip').text("");
        el = 'path'; // fill chart element with originally color
    } else {
        el = 'rect'; // fill chart element with originally color
    }
    d3.select('#inner-' + el + '-' + index).attr('fill', this.getBaseColorFor(index));
    d3.select('#outer-' + el + '-' + index).attr('fill', this.getLightColorFor(index));
};

/**
 * Create tooltip.
 *
 * @param usersDict
 * @param index
 */
DiscussionBarometer.prototype.getTooltip = function (usersDict, index) {
    'use strict';
    var tooltip = $('<div>').attr("class", "chartTooltip");
    var append_left = $('#' + popupBarometerId).find('.col-md-5').outerHeight() > $('#' + popupBarometerId).find('.col-md-6').outerHeight() + 100;
    var col = append_left ? '.col-md-6' : '.col-md-5';
    $('#' + popupBarometerId).find(col).append(tooltip);

    // make tooltip visible
    tooltip.css("opacity", 1).css('border-radius', '0.2em');

    this.createTooltipContent(usersDict, index);

    // fill background of tooltip with color of selected sector of barometer
    tooltip.css('background-color', this.getVeryLightColorFor(index));
    // fill border of tooltip with the same color as the sector of barometer
    tooltip.css('border-color', this.getDarkColorFor(index));
};

/**
 * Create content of -div.
 *
 * @param usersDict
 * @param index: index of bar is selected
 */
DiscussionBarometer.prototype.createTooltipContent = function (usersDict, index) {
    'use strict';
    // append list elements to div

    var message_list = usersDict[index].message !== null ? $('<li>').html(usersDict[index].message) : '';
    var text_keyword = '';
    if (this._address === 'argument') {
        text_keyword = usersDict[index].seenBy === 1 ? participantSawArgumentsToThis : participantsSawArgumentsToThis;
    } else {
        text_keyword = usersDict[index].seenBy === 1 ? participantSawThisStatement : participantsSawThisStatement;
    }

    var seenByList = $('<li>').html(usersDict[index].seenBy + ' ' + _t_discussion(text_keyword));

    var list = !this._is_attitude ? seenByList.append(message_list) : message_list;

    // add images of avatars
    usersDict[index].users.forEach(function (e) {
        var avatarImage = $('<img>').attr({
            'data-href': e.public_profile_url, 'title': e.nickname,
            'class': 'img-circle', 'src': e.avatar_url
        });
        list.append(avatarImage);
    });

    $('.chartTooltip').append(list);
};

/**
 * Create legend for chart.
 *
 * @param usersDict
 */
DiscussionBarometer.prototype.createLegend = function (usersDict) {
    'use strict';
    var div, label, ul, _this = this;
    ul = $('<ul>').attr({'class': 'legendUl', 'style': 'padding-left: 0em; list-style-type: none;'});
    $.each(usersDict, function (key, value) {
        div = $('<div>').attr('class', 'legendSymbolDiv').css('background-color', _this.getBaseColorFor(key)).css('border-radius', '0.2em');
        label = $('<label>').attr('class', 'legendLabel').html(value.text);
        ul.append($('<li>').attr('id', 'legendLi_' + key).css('border-radius', '0.2em').append(div).append(label));
    });
    $('#' + popupBarometerId).find('.col-md-5').append(ul);
};
DiscussionBarometer.prototype.getBaseColorFor = function (index) {
    'use strict';
    return this.google_colors[index % this.google_colors.length][0];
};
DiscussionBarometer.prototype.getVeryLightColorFor = function (index) {
    'use strict';
    return this.google_colors[index % this.google_colors.length][1];
};
DiscussionBarometer.prototype.getLightColorFor = function (index) {
    'use strict';
    return this.google_colors[index % this.google_colors.length][2];
};
DiscussionBarometer.prototype.getNormalColorFor = function (index) {
    'use strict';
    return this.google_colors[index % this.google_colors.length][3];
};
DiscussionBarometer.prototype.getDarkColorFor = function (index) {
    'use strict';
    return this.google_colors[index % this.google_colors.length][9];
};

// doughnut chart

/**
 * Create barometer.
 */
DiscussionBarometer.prototype.getD3BarometerDoughnutChart = function () {
    'use strict';
    var usersDict = [];
    this.removeContentOfModal();

    // create div for barometer
    $('#modal-body-chart-place').append('<div id="barometer-div"></div>');

    // width and height of chart
    var width = 500, height = 410;
    var doughnutChartSvg = this.getSvg(width, height + 40).attr('id', "barometer-svg");

    this.getUsersDict(usersDict);

    // create doughnut of chart
    this.createDoughnutChart(doughnutChartSvg, usersDict);

    // if length of usersDict is greater then 0 add legend and tooltip
    if (usersDict.length > 0) {
        // create legend for chart
        this.createLegend(usersDict);
        // tooltip
        this.addListenerForTooltip(usersDict, doughnutChartSvg, ".chart-sector");
    }
};
