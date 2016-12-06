// colors from https://www.google.com/design/spec/style/color.html#color-color-palette
const google_colors = [
    //0          1          2          3          4          5          6          7          8          9          10         11         12         13         14
    ['#4caf50', '#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50', '#43a047', '#388e3c', '#2e7d32', '#1b5e20', '#b9f6ca', '#69f0ae', '#00e676', '#00c853'],  // green
    ['#f44336', '#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#ef5350', '#f44336', '#e53935', '#d32f2f', '#c62828', '#b71c1c', '#ff8a80', '#ff5252', '#ff1744', '#d50000'],  // red
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
    let is_attitude = false;

    /**
     * Displays barometer.
     */
    this.showBarometer = function(){
        let uid = 0, uid_array = [];
        let url = window.location.href;
        url = url.split('#')[0];
        url = url.split('?')[0];
        let splitted = url.split('/');
        let address = 'position';
        let inputs = $('#discussions-space-list').find('li:visible:not(:last-child) input');

        // parse url
        if (url.indexOf('/attitude/') != -1){
            address = 'attitude';
            uid = splitted[splitted.length-1];
            
            new AjaxGraphHandler().getUserGraphData(uid, address);
        } else if (url.indexOf('/justify/') != -1 || window.location.href.indexOf('/choose/') != -1) {
            address = 'justify';
            inputs.each(function(){
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
            inputs.each(function(){
                uid_array.push($(this).attr('id').substr(5));
            });
            new AjaxGraphHandler().getUserGraphData(uid_array, address);
        }
    };

    /**
     * Callback if ajax request was successfull.
     *
     * @param data: unparsed data of request
     * @param address: step of discussion
     */
    this.callbackIfDoneForGetDictionary = function(data, address){
        let jsonData;
        let dialog = $('#' + popupBarometerId);

        try{
            jsonData = JSON.parse(data);
            console.log(jsonData);
        } catch(e) {
            setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(internalError));
            alert('parsing-json: ' + e);
            return;
        }

        // remove content of modal
        dialog.find('.col-md-6').empty();
        dialog.find('.col-md-5').empty();
        
        // change status of toggle
        $('#chart-btn').bootstrapToggle('off');
        // create bar chart as default view
        getD3BarometerBarChart(jsonData, address);
        // add listener for buttons to change the type of chart
        addListenerForChartButtons(jsonData, address);

        dialog.modal('show').on('hidden.bs.modal', function () {
            clearAnchor();
        });
        
        $('#' + popupBarometerAcceptBtn).show().click( function () {
            $('#' + popupBarometerId).modal('hide');
        }).removeClass('btn-success');
        $('#' + popupBarometerRefuseBtn).hide();

        dialog.find('.modal-title').html(jsonData.title).css({'line-height': '1.0'});
    };


    /**
     * Add listeners for chart-buttons.
     *
     * @param jsonData
     * @param address
     */
    function addListenerForChartButtons(jsonData, address) {
        // show only button of chart which is currently not visible
        let i = 0;
        $('#chart-btn-div').click(function() {
            if (i % 2 == 0) {
                getD3BarometerDoughnutChart(jsonData, address);
            }
            else{
                getD3BarometerBarChart(jsonData, address);
            }
            i++;
        });
    }

    /**
     * Create barometer.
     *
     * @param jsonData
     * @param address
     */
     function getD3BarometerBarChart(jsonData, address) {
        let dialog = $('#' + popupBarometerId);
        dialog.find('.col-md-6').empty();
        dialog.find('.col-md-5').empty();

        // create div for barometer
        dialog.find('.col-md-6').append('<div id="barometer-div"></div>');
        // width and height of chart
        let width = 400;
        let height = 400;
        let barChartSvg = getSvg(width+70, height+50);

        let usersDict = [];
        // create dictionary depending on address
        is_attitude = address === 'attitude';
        if(address === 'attitude')
            usersDict = createDictForAttitude(jsonData, usersDict);
        else
            usersDict = createDictForArgumentAndStatement(jsonData, usersDict);

        // create bars of chart
        // selector = inner-rect: clicks on statement relative to seen_by value
        createBar(width, height-50, usersDict, barChartSvg, "inner-rect", address);
        if(address != 'argument' && address != 'attitude'){
            // selector = outer-rect: seen_by value
            createBar(width, height-50, usersDict, barChartSvg, "outer-rect", address);
        }

        // create axis
        if(address === 'argument' || address === 'attitude'){
            createXAxis(barChartSvg, width, height+10, usersDict);
        }
        else{
            createYAxis(barChartSvg, height-50);
        }

        // create legend for chart
        createLegend(usersDict);

        // tooltip
        addListenerForTooltip(usersDict, barChartSvg, address, "rect");
    }

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
     * Create x-axis for barometer.
     *
     * @param svg
     * @param width
     * @param height
     * @param usersDict
     */
     function createXAxis(svg, width, height, usersDict){
        let maxUsersNumber = getMaximum(usersDict);

        let xScale = d3.scale.linear().domain([0, maxUsersNumber]).range([0, width]);

        // create y-axis
        let xAxis = d3.svg.axis().scale(xScale).orient("bottom");
        svg.append("g")
            .attr({id: "xAxis", transform: "translate(50," + height + ")"})
            .call(xAxis);
    }

    /**
     * Find maximum of userNumber-values.
     *
     * @param usersDict
     */
    function getMaximum(usersDict) {
        let maxUsersNumber = 0;
        $.each(usersDict, function(key, value){
            if(value.usersNumber > maxUsersNumber){
                maxUsersNumber = value.usersNumber;
            }
        });
        return maxUsersNumber;
    }

    /**
     * Create y-axis for barometer.
     *
     * @param svg
     * @param height
     */
    function createYAxis(svg, height){
        let yScale = d3.scale.linear().domain([0, 100]).range([height, 0]);

        // create y-axis
        let yAxis = d3.svg.axis().scale(yScale).orient("left");
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
            users: jsonData.agree_users,
            message: jsonData.agree_message
        });
        usersDict.push({
            usersNumber: jsonData.disagree_users.length,
            seenBy: jsonData.seen_by,
            text: jsonData.disagree_text,
            users: jsonData.disagree_users,
            message: jsonData.disagree_message
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
     * @param selector
     * @param address
     */
    function createBar(width, height, usersDict, barChartSvg, selector, address) {
        // width of one bar
        // width/height - left padding to y-Axis - space between bars
        let barWidth;
        if(address === "argument" || address === "attitude"){
            barWidth = (height - 10 - (usersDict.length-1)*10) / usersDict.length;
        }
        else{
            barWidth = (width - 10 - (usersDict.length-1)*10) / usersDict.length;
        }

        // set max-width of bar
        if(barWidth > 150){
            barWidth = 150;
        }

        let maxUsersNumber = getMaximum(usersDict);

        barChartSvg.selectAll(selector)
            .data(usersDict)
            .enter().append("rect")
            .attr({
                width: function (d) {
                    if(address === "argument" || address === "attitude"){
                        return divideWrapperIfZero(d.usersNumber, maxUsersNumber) * width;
                    }
                    else{
                        return barWidth;
                    }
                },
                // height in percent: length/seen_by = x/height
                height: function (d) {
                        if(address === "argument" || address === "attitude"){
                            return barWidth;
                        }
                        if (selector === 'inner-rect')
                            return divideWrapperIfZero(d.usersNumber, d.seenBy) * height;
                        return height - (divideWrapperIfZero(d.usersNumber, d.seenBy) * height);
                },
                // number of bar * width of bar + padding-left + space between to bars
                x: function (d, i) {
                    if(address === "argument" || address === "attitude"){
                        return 50;
                    }
                    return i * barWidth + 60 + i * 10;
                },
                // y: height - barLength, because d3 starts to draw in left upper corner
                y: function (d, i) {
                    if(address === "argument" || address === "attitude"){
                        return i * barWidth + 60 + i * 10;
                    }
                    if (selector === 'inner-rect')
                        return height - (divideWrapperIfZero(d.usersNumber, d.seenBy) * height - 50);
                    return 50;
                },
                fill: function (d, i) {
                    if (selector === 'inner-rect')
                        return getNormalColorFor(i);
                    return getLightColorFor(i)
                },
                id: function (d, i) {
                    return selector + "-" + i;
                }
            });
    }

    function divideWrapperIfZero(numerator, denominator){
        return denominator == 0 || numerator == 0 ? 0.005 : numerator / denominator;
    }

    // doughnut chart

    /**
     * Create barometer.
     *
     * @param jsonData
     * @param address
     */
    function getD3BarometerDoughnutChart(jsonData, address) {
        let dialog = $('#' + popupBarometerId);
        dialog.find('.col-md-6').empty();
        dialog.find('.col-md-5').empty();

        // create div for barometer
        dialog.find('.col-md-6').append('<div id="barometer-div"></div>');

        // width and height of chart
        let width = 500, height = 410;
        let doughnutChartSvg = getSvgDoughnutChart(width, height + 40);

        let usersDict = [];
        // create dictionary depending on address
        if(address === 'attitude'){
            usersDict = createDictForAttitude(jsonData, usersDict);
        }
        else{
            usersDict = createDictForArgumentAndStatement(jsonData, usersDict);
        }
        // create doughnut of chart
        createDoughnutChart(usersDict, doughnutChartSvg, address);
        // create legend for chart
        createLegend(usersDict);
        // tooltip
        addListenerForTooltip(usersDict, doughnutChartSvg, address, ".chart-sector");
    }

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
     * @param address
     */
    function createDoughnutChart(usersDict, doughnutChartSvg, address) {
        let height = 400, width = 400,
            outerRadius = Math.min(width, height) / 2,
            innerRadius = 0.3 * outerRadius;

        let doughnut = getDoughnut(usersDict);

        let innerCircle = getInnerCircle(usersDict, innerRadius, outerRadius, address);
        let outerCircle = getOuterCircle(innerRadius, outerRadius);

        createOuterPath(doughnutChartSvg, usersDict, outerCircle, doughnut);
        createInnerPath(doughnutChartSvg, usersDict, innerCircle, doughnut);
    }

    /**
     * Choose layout of d3.
     *
     * @param usersDict
     * @param address
     * @returns {*}
     */
    function getDoughnut(usersDict){
        let sumUsersNumber = 0;
        $.each(usersDict, function (key, value) {
            sumUsersNumber += value.usersNumber;
        });
        return d3.layout.pie()
            .sort(null)
            .value(function (d, i) {
                // if all arguments have not been seen by anyone,
                // then all sectors have the same angle
                if(sumUsersNumber === 0){
                    return 1;
                }
                // if the argument has not been seen by anyone,
                // then the height of the sector is 2% of the number of all users
                else if(usersDict[i].usersNumber === 0){
                    return (sumUsersNumber*2)/100;
                }
                return usersDict[i].usersNumber;
            });
    }

    /**
     * Create inner circle of chart.
     *
     * @param usersDict
     * @param innerRadius
     * @param outerRadius
     * @param address
     * @returns {*}
     */
    function getInnerCircle(usersDict, innerRadius, outerRadius, address){
        return d3.svg.arc()
            .innerRadius(innerRadius)
            .outerRadius(function (d, i) {
                // if the user can only decide between agree and disagree: the height of sector is not dependent on seen-by-value
                if(address === "attitude"){
                    return (outerRadius - innerRadius) + innerRadius;
                }
                // if nobody has chosen the argument then the height of the sector is 2% of the difference between innerRadius and outerRadius
                if(usersDict[i].usersNumber === 0){
                    return ((outerRadius-innerRadius)*2)/100 + innerRadius;
                }
                return (outerRadius - innerRadius) * (usersDict[i].usersNumber/usersDict[i].seenBy) + innerRadius;
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
                   stroke: "gray", d: innerCircle, transform: "translate(240,230)",
                   id: function (d, i) {return "inner-path-" + i}, class: "chart-sector"});
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
                   stroke: "gray", d: outerCircle, transform: "translate(240,230)",
                   id: function (d, i) {return "outer-path-" + i}, class: "chart-sector"});
    }

    /**
     * Create short tooltip for doughnut chart in middle of chart.
     *
     * @param doughnutChartSvg
     * @param usersDict
     * @param index
     * @param address
     */
    function createShortTooltipDoughnutChart(doughnutChartSvg, usersDict, index, address){
        // append tooltip in middle of doughnut chart
        // text of tooltip depends on address
        let tooltipText;
        if(address === "attitude"){
            tooltipText = usersDict[index].usersNumber;
        }
        else{
            tooltipText = usersDict[index].usersNumber + "/" + usersDict[index].seenBy;
        }
        doughnutChartSvg.append("text")
            .attr({x: 240, y: 230,
                   class: "doughnut-chart-text-tooltip",
                   "font-weight": "bold", "font-size": "25px"})
            .text(tooltipText);

        tooltipText = _t(clickedOnThis);
        doughnutChartSvg.append("text").attr({x: 240, y: 250, class: "doughnut-chart-text-tooltip"}).text(tooltipText);
    }

    // bar chart and doughnut chart
    /**
     * Create tooltips for bar chart and doughnut chart.
     *
     * @param usersDict
     * @param chartSvg
     * @param address
     * @param selector: different selectors for bar chart and doughnut chart
     */
    function addListenerForTooltip(usersDict, chartSvg, address, selector) {
        let isClicked = false;
        let tooltipIsVisible = false;
        // save index and id of object of last click event
        let elementIndex;
        let _index;

        // add listener for click event
        chartSvg.selectAll(selector).on('click', function (d, index) {
            // sector of doughnut chart and part which represents the seen-by-value should have the same index
            elementIndex = index % usersDict.length;
            if (isClicked){
                if (_index != elementIndex){
                    hideTooltip(selector, _index);
                    showTooltip(usersDict, elementIndex, address, chartSvg, selector);
                    isClicked = true;
                    tooltipIsVisible = true;
                } else { // if the user clicks on the same tooltip for a second time hide the tooltip
                    hideTooltip(selector, elementIndex);
                    isClicked = false;
                    tooltipIsVisible = false;
                }
            } else {
                if (!tooltipIsVisible){
                    showTooltip(usersDict, elementIndex, address, chartSvg, selector);
                }
                isClicked = true;
                tooltipIsVisible = true;
            }
            _index = elementIndex;
        }).on("mouseover", function (d, index) { // add listener for hover event
            if(!isClicked){
                elementIndex = index % usersDict.length;

                showTooltip(usersDict, elementIndex, address, chartSvg, selector);
                tooltipIsVisible = true;
            }
        }).on("mouseout", function (d, index) { // add listener for mouse out event
            if(!isClicked){
                elementIndex = index % usersDict.length;

                hideTooltip(selector, elementIndex);
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
                hideTooltip(selector, elementIndex);
                isClicked = false;
                tooltipIsVisible = false;
            }
       });
    }

     /**
     * Show tooltip on mouse event.
     *
     * @param usersDict
     * @param index
     * @param address
     * @param chartSvg
     * @param selector
     */
    function showTooltip(usersDict, index, address, chartSvg, selector){
        getTooltip(usersDict, index, address);
        // if doughnut chart is selected add short tooltip in middle of chart
        if(selector === ".chart-sector"){
            createShortTooltipDoughnutChart(chartSvg, usersDict, index, address);
            // highlight whole sector on hover
            d3.select("#inner-path-" + index).attr('fill', getDarkColorFor(index));
            d3.select("#outer-path-" + index).attr('fill', google_colors[index % google_colors.length][3]);
        }
        else{
            // highlight sector on hover
            d3.select("#inner-rect-" + index).attr('fill', getDarkColorFor(index));
            d3.select("#outer-rect-" + index).attr('fill', google_colors[index % google_colors.length][3]);
        }
    }

    /**
     * Hide tooltip on mouse event.
     *
     * @param selector
     * @param index
     */
    function hideTooltip(selector, index){
        $('.chartTooltip').remove();
        // hide tooltip with detailed information
        $('.chartTooltip').css("opacity", 0);

        // if doughnut chart is selected hide text in middle of doughnut
        if(selector === ".chart-sector") {
            $('.doughnut-chart-text-tooltip').text("");
            // fill chart element with originally color
            d3.select("#inner-path-" + index).attr('fill', getNormalColorFor(index));
            d3.select("#outer-path-" + index).attr('fill', getLightColorFor(index));
        }
        else{
            // fill chart element with originally color
            d3.select("#inner-rect-" + index).attr('fill', getNormalColorFor(index));
            d3.select("#outer-rect-" + index).attr('fill', getLightColorFor(index));
        }
    }

     /**
     * Create tooltip.
     *
     * @param usersDict
     * @param index
     * @param address
     */
    function getTooltip(usersDict, index, address){
        let div = $('<div>').attr("class", "chartTooltip");
        $('#' + popupBarometerId).find('.col-md-5').append(div);

        let tooltip = $(".chartTooltip");

        // make tooltip visible
        tooltip.css("opacity", 1);

        createTooltipContent(usersDict, index, address);

        // fill background of tooltip with color of selected sector of barometer
        tooltip.css('background-color', getVeryLightColorFor(index));
        // fill border of tooltip with the same color as the sector of barometer
        tooltip.css('border-color', getDarkColorFor(index));
    }

    /**
     * Create content of -div.
     *
     * @param usersDict
     * @param index: index of bar is selected
     * @param address
     */
    function createTooltipContent(usersDict, index, address){
        // append list elements to div
        let messageList = '';
        if (usersDict[index].message != null) {
            messageList = $('<li>').html(usersDict[index].message);
        }
        let text_keyword = '';
        if (address == 'argument')
            text_keyword = usersDict[index].seenBy == 1 ? participantSawArgumentsToThis : participantsSawArgumentsToThis;
        else
            text_keyword = usersDict[index].seenBy == 1 ? participantSawThisStatement : participantsSawThisStatement;
        let seenByList = $('<li>').html(usersDict[index].seenBy + ' ' + _t_discussion(text_keyword));
        let userList = $('<li>').html(_t_discussion(users) + ': ');

        let list;
        if(usersDict[index].message != null){
            if (is_attitude)
                list = messageList.append(userList);
            else
                list = messageList.append(seenByList).append(userList);
        } else {
            if (is_attitude)
                list = userList;
            else
                list = seenByList.append(userList);
        }

        // add images of avatars
        usersDict[index].users.forEach(function (e) {
            let avatarImage = $('<img>').attr({'data-href': e.public_profile_url, 'title': e.nickname,
                'class': 'img-circle', 'src': e.avatar_url});
            list.append(avatarImage);
        });

        $('.chartTooltip').append(list);
    }

    /**
     * Create legend for chart.
     *
     * @param usersDict
     */
    function createLegend(usersDict){
        let div, label, element;
        $.each(usersDict, function(key, value) {
            div = $('<div>').attr('class', 'legendSymbolDiv').css('background-color', getNormalColorFor(key));
            label = $('<label>').attr('class', 'legendLabel').html(value.text);
            element = $('<ul>').attr('class', 'legendUl').append(div).append(label);
            $('#' + popupBarometerId).find('.col-md-5').append(element);
        });
    }

    function getNormalColorFor(index){ return google_colors[index % google_colors.length][0]; }
    function getVeryLightColorFor(index){ return google_colors[index % google_colors.length][1]; }
    function getLightColorFor(index){ return google_colors[index % google_colors.length][2]; }
    function getDarkColorFor(index){ return google_colors[index % google_colors.length][9]; }
}