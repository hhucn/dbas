// colors from https://www.google.com/design/spec/style/color.html#color-color-palette
var google_colors = [
    //0          1          2          3          4          5          6          7          8          9          10         11         12         13         14
    ['#f44336', '#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#ef5350', '#f44336', '#e53935', '#d32f2f', '#c62828', '#b71c1c', '#ff8a80', '#ff5252', '#ff1744', '#d50000'],  // red
    ['#4caf50', '#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50', '#43a047', '#388e3c', '#2e7d32', '#1b5e20', '#b9f6ca', '#69f0ae', '#00e676', '#00c853'],  // green
    ['#2196f3', '#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1e88e5', '#1976d2', '#1565c0', '#0d47a1', '#82b1ff', '#448aff', '#2979ff', '#2962ff'],  // blue
    ['#ffeb3b', '#fffde7', '#fff9c4', '#fff59d', '#fff176', '#ffee58', '#ffeb3b', '#fdd835', '#fbc02d', '#f9a825', '#f57f17', '#ffff8d', '#ffff00', '#ffea00', '#ffd600'],  // yellow
    ['#673ab7', '#ede7f6', '#d1c4e9', '#b39ddb', '#9575cd', '#7e57c2', '#673ab7', '#5e35b1', '#512da8', '#4527a0', '#311b92', '#b388ff', '#7c4dff', '#651fff', '#6200ea'],  // deep purple
    ['#3f51b5', '#e8eaf6', '#c5cae9', '#9fa8da', '#7986cb', '#5c6bc0', '#3f51b5', '#3949ab', '#303f9f', '#283593', '#1a237e', '#8c9eff', '#536dfe', '#3d5afe', '#304ffe'],  // indigo
    ['#03a9f4', '#e1f5fe', '#b3e5fc', '#81d4fa', '#4fc3f7', '#29b6f6', '#03a9f4', '#039be5', '#0288d1', '#0277bd', '#01579b', '#80d8ff', '#40c4ff', '#00b0ff', '#0091ea'],  // light blue
    ['#00bcd4', '#e0f7fa', '#b2ebf2', '#80deea', '#4dd0e1', '#26c6da', '#00bcd4', '#00acc1', '#0097a7', '#00838f', '#006064', '#84ffff', '#18ffff', '#00e5ff', '#00b8d4'],  // cyan
    ['#e91e63', '#fce4ec', '#f8bbd0', '#f48fb1', '#f06292', '#ec407a', '#e91e63', '#d81b60', '#c2185b', '#ad1457', '#880e4f', '#ff80ab', '#ff4081', '#f50057', '#c51162'],  // pink
    ['#9c27b0', '#f3e5f5', '#e1bee7', '#ce93d8', '#ba68c8', '#ab47bc', '#9c27b0', '#8e24aa', '#7b1fa2', '#6a1b9a', '#4a148c', '#ea80fc', '#e040fb', '#d500f9', '#aa00ff'],  // purple
    ['#009688', '#e0f2f1', '#b2dfdb', '#80cbc4', '#4db6ac', '#26a69a', '#009688', '#00897b', '#00796b', '#00695c', '#004d40', '#a7ffeb', '#64ffda', '#1de9b6', '#00bfa5'],  // teal
    ['#8bc34a', '#f1f8e9', '#dcedc8', '#c5e1a5', '#aed581', '#9ccc65', '#8bc34a', '#7cb342', '#689f38', '#558b2f', '#33691e', '#ccff90', '#b2ff59', '#76ff03', '#64dd17'],  // light green
    ['#cddc39', '#f9fbe7', '#f0f4c3', '#e6ee9c', '#dce775', '#d4e157', '#cddc39', '#c0ca33', '#afb42b', '#9e9d24', '#827717', '#f4ff81', '#eeff41', '#c6ff00', '#aeea00'],  // lime
    ['#ffc107', '#fff8e1', '#ffecb3', '#ffe082', '#ffd54f', '#ffca28', '#ffc107', '#ffb300', '#ffa000', '#ff8f00', '#ff6f00', '#ffe57f', '#ffd740', '#ffc400', '#ffab00'],  // amber
    ['#ff9800', '#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726', '#ff9800', '#fb8c00', '#f57c00', '#ef6c00', '#e65100', '#ffd180', '#ffab40', '#ff9100', '#ff6d00'],  // orange
    ['#ff5722', '#fbe9e7', '#ffccbc', '#ffab91', '#ff8a65', '#ff7043', '#ff5722', '#f4511e', '#e64a19', '#d84315', '#bf360c', '#ff9e80', '#ff6e40', '#ff3d00', '#dd2c00']   // deep orange
    ];


function DiscussionBarometer(){
    'use strict';

    /**
     * Displays barometer.
     */
    this.showBarometer = function(){
        var uid = 0, uid_array = [];
        var url = window.location.href;
        url = url.split('#')[0];
        url = url.split('?')[0];
        var splitted = url.split('/');
        var address = 'position';

        // parse url
        if (url.indexOf('/attitude/') != -1){
            address = 'attitude';
            uid = splitted[splitted.length-1];
            new AjaxGraphHandler().getUserGraphData(uid, address);
        } else if (url.indexOf('/justify/') != -1 || window.location.href.indexOf('/choose/') != -1) {
            address = 'justify';
            $('#discussions-space-list li:not(:last-child) input').each(function(){
                uid_array.push($(this).attr('id').substr(5));
            });
            new AjaxGraphHandler().getUserGraphData(uid_array, address);
        } else if (url.indexOf('/reaction/') != -1){
            address = 'argument';
            uid_array.push(splitted[splitted.length - 3]);
            uid_array.push(splitted[splitted.length - 1]);
            new AjaxGraphHandler().getUserGraphData(uid_array, address);
        } else {
            address = 'position';
            $('#discussions-space-list li:not(:last-child) label').each(function(){
                uid_array.push($(this).attr('id'));
            });
            new AjaxGraphHandler().getUserGraphData(uid_array, address);
        }

        new Helper().setAnchor('barometer');
    };

    /**
     * Callback if ajax request was successfull.
     *
     * @param data: unparsed data of request
     * @param address: step of discussion
     */
    this.callbackIfDoneForGetDictionary = function(data, address){
        var jsonData;
        var dialog = $('#' + popupConfirmRowDialogId);
        var _this = this;
        
        try{
            jsonData = JSON.parse(data);
            console.log(jsonData);
        } catch(e) {
            setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(internalError));
            alert('parsing-json: ' + e);
            return;
        }

        createButtons(jsonData, address);

        dialog.modal('show').on('hidden.bs.modal', function () {
            new Helper().clearAnchor();
        }).on('shown.bs.modal', function () {
            // display bar after the modal is shown, cause we need the width of the modal
            getD3BarometerBarChart(jsonData, address);
        });
        $('#' + popupConfirmRowDialogAcceptBtn).show().click( function () {
            $('#' + popupConfirmRowDialogId).modal('hide');
        }).removeClass('btn-success');
        $('#' + popupConfirmRowDialogRefuseBtn).hide();

        dialog.find('.modal-title').html(jsonData.title).css({'line-height': '1.0'});
        //getD3BarometerBarChart(jsonData, address);
    };

    /**
     * Create buttons to switch between charts.
     *
     * @param jsonData
     * @param address
     */
    function createButtons(jsonData, address){
        var dialog = $('#' + popupConfirmRowDialogId);
        dialog.find('.col-md-6').empty();
        dialog.find('.col-md-5').empty();
        dialog.find('#chart-buttons').empty();

        dialog.find('.modal-footer').append('<div id="chart-buttons"></div>');

        dialog.find('#chart-buttons').append('<button id="show-bar-chart-btn" type="button" class="btn btn-default">Bar Chart</button>');
        dialog.find('#chart-buttons').append('<button id="show-doughnut-chart-btn" type="button" class="btn btn-default">Doughnut Chart</button>');
        addListenerForChartButtons(jsonData, address);
    }

    /**
     * Add listeners for chart-buttons.
     *
     * @param jsonData
     * @param address
     */
    function addListenerForChartButtons(jsonData, address) {
        $('#show-bar-chart-btn').click(function() { getD3BarometerBarChart(jsonData, address); });
        $('#show-doughnut-chart-btn').click(function() { getD3BarometerDoughnutChart(jsonData, address, 0.3); });
    }

    /**
     * Create barometer.
     *
     * @param jsonData
     * @param address
     */
     function getD3BarometerBarChart(jsonData, address) {
        var dialog = $('#' + popupConfirmRowDialogId);
        dialog.find('.col-md-6').empty();
        dialog.find('.col-md-5').empty();

        // create div for barometer
        dialog.find('.col-md-6').append('<div id="barometer-div"></div>');
        // width and height of chart
        var width = dialog.find('.col-md-6').width();
        var height = 400;
        var barChartSvg = getSvg(width+50, height+20);

        createAxis(barChartSvg, height-50);

        var usersDict = [];
        // create dictionary depending on address
        if(address === 'attitude')
            usersDict = createDictForAttitude(jsonData, usersDict);
        else
            usersDict = createDictForArgumentAndStatement(jsonData, usersDict);

        // create bars of chart
        createBar(width, height-50, usersDict, barChartSvg);

        // tooltip
        createTooltip(usersDict, barChartSvg, width, address);

        // create legend for chart
        createLegend(usersDict);
    };

    /**
     * Create svg-element.
     *
     * @param width: width of container, which contains barometer
     * @param height: height of container
     * @return scalable vector graphic
     */
    function getSvg(width, height){
        return d3.select('#barometer-div').append('svg').attr({width: width, height: height, id: "barometer-svg"});
    }

    /**
     * Create axis for barometer.
     *
     * @param svg
     * @param height
     */
    function createAxis(svg, height){
        // create scale to map values
        var xScale = d3.scale.linear().range([0, height]);
        var yScale = d3.scale.linear().domain([0, 100]).range([height, 0]);

        // create x and y-axis
        var xAxis = d3.svg.axis().scale(xScale).orient("bottom");
        svg.append("g")
            .attr({id: "xAxis", transform: "translate(50,500)"})
            .call(xAxis);
        var yAxis = d3.svg.axis().scale(yScale).orient("left");
        svg.append("g")
            .attr({id: "yAxis", transform: "translate(50,50)"})
            .call(yAxis)
            .append("text")
            .attr({dx: "0.5em", dy: "-1.5em"})
            .style("text-anchor", "end")
            .text("%");
    }

    /**
     * Add length of each user-dictionary and value of key seen_by to array.
     *
     * @param jsonData
     * @param usersDict
     * @returns usersDict
     */
    function createDictForAttitude(jsonData, usersDict){
        usersDict.push({
            usersNumber: jsonData.agree_users.length,
            seenBy: jsonData.seen_by,
            text: jsonData.agree_text,
            users: jsonData.agree_users
        });
        usersDict.push({
            usersNumber: jsonData.disagree_users.length,
            seenBy: jsonData.seen_by,
            text: jsonData.disagree_text,
            users: jsonData.disagree_users
        });
        return usersDict;
    }

    /**
     * Add length of each user-dictionary and value of key seen_by to array.
     *
     * @param jsonData
     * @param usersDict
     * @returns usersDict
     */
    function createDictForArgumentAndStatement(jsonData, usersDict){
        $.each(jsonData.opinions, function(key, value) {
            usersDict.push({
                usersNumber: value.users.length,
                seenBy: value.seen_by,
                text: value.text,
                message: value.message,
                users: value.users
            });
        });
        return usersDict;
    }

    /**
     * Create bars for chart.
     *
     * @param width
     * @param height
     * @param usersDict
     * @param barChartSvg
     */
    function createBar(width, height, usersDict, barChartSvg){
        // width of one bar
        var barWidth = width/usersDict.length - 5;

        barChartSvg.selectAll('rect')
            .data(usersDict)
            .enter().append("rect")
            .attr({width: barWidth,
                   // height in percent: length/seen_by = x/height
                   height: function(d) {return divideWrapperIfZero(d.usersNumber, d.seenBy) * height;},
                   // number of bar * width of bar + padding-left + space between to bars
                   x: function(d,i) {return i*barWidth + 55 + i*5;},
                   // y: height - barLength, because d3 starts to draw in left upper corner
                   y: function(d) {return height - (divideWrapperIfZero(d.usersNumber, d.seenBy) * height - 50);},
                   fill: function (d, i) {return getNormalColorFor(i);}});
    }
    
    function divideWrapperIfZero(numerator, denominator){
        return denominator == 0 || numerator == 0 ? 0.005 : numerator / denominator;
    }

    /**
     * Create tooltips for bars.
     *
     * @param usersDict
     * @param barChartSvg
     * @param width
     * @param address
     */
    function createTooltip(usersDict, barChartSvg, width, address) {
        var div;
        var barWidth = width / usersDict.length - 5;
        var tooltipWith = width;
        var tmp;
        barChartSvg.selectAll("rect").on("mouseover", function (d, index) {
            var barLeft = index / 2 * barWidth + 70 + index * 5;
            tmp = index;
            while (tooltipWith + barLeft > $( window ).width()){
                if (tmp > 0){
                    // move one step to the left
                    tmp -= 1;
                    tooltipWith = tmp * barWidth + 70 + tmp * 5;
                } else {
                    tooltipWith = width / usersDict.length - 5;
                    barLeft = index * barWidth + 70 + index * 5;
                }
            }
            
            div = d3.select('#' + popupConfirmRowDialogId + ' .col-md-6').append("div");

            // set properties of div
            div.attr("class", "tooltip").style("opacity", 1)
                .style("left", 65 + "px")
                .style("top", 100 + "px")
                .style("width", tooltipWith);

            // append list elements to div
            if (d.message != null) {
                div.append('li').html(d.message);
            }
            var text_keyword = '';
            if (address == 'argument')
                text_keyword = d.seenBy == 1 ? participantSawArgumentsToThis : participantsSawArgumentsToThis;
            else
                text_keyword = d.seenBy == 1 ? participantSawThisStatement : participantsSawThisStatement;
            div.append('li').html(d.seenBy + ' ' + _t_discussion(text_keyword));
            div.append('li').html(_t_discussion(users) + ': ');

            // add images of avatars
            d.users.forEach(function (e) {
                div.append('img').attr('src', e.avatar_url);
            });
            $(this).attr('fill', getDarkColorFor(index));
        })
        .on("mouseout", function (d, index) {
            div.style("opacity", 0);
            $(this).attr('fill', getNormalColorFor(index));
        });
    }
    
    function getNormalColorFor(index){ return google_colors[index % google_colors.length][0]; }
    function getLightColorFor(index){ return google_colors[index % google_colors.length][2]; }
    function getDarkColorFor(index){ return google_colors[index % google_colors.length][10]; }

    /**
     * Create legend for chart.
     *
     * @param usersDict
     */
    function createLegend(usersDict){
        var div, label, element;
        $.each(usersDict, function(key, value) {
            div = $('<div>').attr('class', 'legendSymbolDiv').css('background-color', getNormalColorFor(key));
            label = $('<label>').attr('class', 'legendLabel').html(value.text);
            element = $('<ul>').attr('class', 'legendUl').append(div).append(label);
            $('#' + popupConfirmRowDialogId).find('.col-md-5').append(element);
        });
    }

    // Doughnut Chart

    /**
     * Create barometer.
     *
     * @param jsonData
     * @param address
     */
    function getD3BarometerDoughnutChart(jsonData, address) {
        var dialog = $('#' + popupConfirmRowDialogId);
        dialog.find('.col-md-6').empty();
        dialog.find('.col-md-5').empty();
        
        // create div for barometer
        dialog.find('.col-md-6').append('<div id="barometer-div"></div>');

        // width and height of chart
        var width = 500, height = 410;
        var doughnutChartSvg = getSvgDoughnutChart(width, height);

        var usersDict = [];
        // create dictionary depending on address
        if(address === 'attitude'){
            usersDict = createDictForAttitude(jsonData, usersDict);
        }
        else{
            usersDict = createDictForArgumentAndStatement(jsonData, usersDict);
        }

        // create bars of chart
        createDoughnutChart(usersDict, doughnutChartSvg);

        // create legend for chart
        createLegend(usersDict);
    };

    /**
     * Create svg-element.
     *
     * @param width: width of container, which contains barometer
     * @param height: height of container
     * @return scalable vector graphic
     */
    function getSvgDoughnutChart(width, height){
        return d3.select('#barometer-div').append('svg').attr({width: width, height: height, id: "barometer-svg"});
    }

    /**
     * Create doughnut chart.
     *
     * @param usersDict
     * @param doughnutChartSvg
     */
    function createDoughnutChart(usersDict, doughnutChartSvg) {
        var height = 400, width = 400,
            outerRadius = Math.min(width, height) / 2,
            innerRadius = 0.3 * outerRadius;

        var sumArrayLength = 0;
        $.each(usersDict, function(key, value) {
            sumArrayLength += value.usersNumber;
        });

        var doughnut = getDoughnut(usersDict);

        var innerCircle = getInnerCircle(usersDict, innerRadius, outerRadius, sumArrayLength);
        var outerCircle = getOuterCircle(innerRadius, outerRadius);

        createOuterPath(doughnutChartSvg, usersDict, outerCircle, doughnut);
        createInnerPath(doughnutChartSvg, usersDict, innerCircle, doughnut);
    }

    /**
     * Choose layout of d3.
     *
     * @param usersDict
     * @returns {*}
     */
    function getDoughnut(usersDict){
        return d3.layout.pie()
            .sort(null)
            .value(function (d, i) {
                return usersDict[i].seenBy;
            });
    }

    /**
     * Create inner circle of chart.
     *
     * @param usersDict
     * @param innerRadius
     * @param outerRadius
     * @param sumSeenBy
     * @returns {*}
     */
    function getInnerCircle(usersDict, innerRadius, outerRadius, sumArrayLength){
        return d3.svg.arc()
            .innerRadius(innerRadius)
            .outerRadius(function (d, i) {
                 return (outerRadius - innerRadius) * (usersDict[i].usersNumber/sumArrayLength) + innerRadius;
            });
    }

    /**
     * Create outer circle of chart.
     *
     * @param innerRadius
     * @param outerRadius
     * @returns {*}
     */
    function getOuterCircle(innerRadius, outerRadius){
        return d3.svg.arc()
            .innerRadius(innerRadius)
            .outerRadius(outerRadius);
    }

    /**
     * Create inner path.
     *
     * @param doughnutChartSvg
     * @param usersDict
     * @param innerCircle
     * @param doughnut
     */
    function createInnerPath(doughnutChartSvg, usersDict, innerCircle, doughnut){
        doughnutChartSvg.selectAll(".innerCircle")
            .data(doughnut(usersDict))
            .enter().append("path")
            .attr({fill: function (d, i) { return getNormalColorFor(i); },
                   stroke: "gray", d: innerCircle, transform: "translate(250,210)"});
    }

    /**
     * Create outer path.
     *
     * @param doughnutChartSvg
     * @param usersDict
     * @param outerCircle
     * @param doughnut
     */
    function createOuterPath(doughnutChartSvg, usersDict, outerCircle, doughnut){
        doughnutChartSvg.selectAll(".outerCircle")
            .data(doughnut(usersDict))
            .enter().append("path")
            .attr({'fill': function (d, i) { return getLightColorFor(i); },
                   stroke: "gray", d: outerCircle, transform: "translate(250,210)"});
    }
}