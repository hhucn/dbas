// colors from https://www.google.com/design/spec/style/color.html#color-color-palette
var colors = [
	'#4CAF50', //  0 green
	'#F44336', //  1 red
	'#2196F3', //  2 blue
	'#FFEB3B', //  3 yellow
	'#673AB7', //  4 deep purple
	'#03A9F4', //  5 light blue
	'#FF5722', //  6 deep orange
	'#607D8B', //  7 blue grey
	'#E91E63', //  8 pink
	'#3F51B5', //  9 indigo
	'#00BCD4', //  10 cyan
	'#8BC34A', // 11 light green
	'#FFC107', // 12 amber
	'#795548', // 13 brown
	'#000000', // 14 black
	'#9C27B0', // 15 purple
	'#009688', // 16 teal
	'#CDDC39', // 17 lime
	'#FF9800', // 18 orange
	'#9E9E9E'  // 19 grey
	];

function DiscussionBarometer(){
    'use strict';

    /**
	 * Displays barometer.
	 */
	this.showBarometer = function(){
		var uid = 0, uid_array = [],
			url = window.location.href.split('?')[0],
			splitted = url.split('/'),
			address = 'position';

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
			uid_array.push(splitted[splitted.length-3]);
			uid_array.push(splitted[splitted.length-1]);
			new AjaxGraphHandler().getUserGraphData(uid_array, address);
		} else {
			address = 'position';
			$('#discussions-space-list li:not(:last-child) label').each(function(){
				uid_array.push($(this).attr('id'));
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
		var jsonData;
        try{
	        jsonData = JSON.parse(data);
        } catch(e) {
	        setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(internalError));
			alert('parsing-json: ' + e);
	        return;
        }
		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		}).removeClass('btn-success');
		$('#' + popupConfirmDialogRefuseBtn).hide();

		$('#' + popupConfirmDialogId).find('.modal-title').text(jsonData.title).css({'line-height': '1.0'});
		this.getD3Barometer(jsonData, address);
	};

	/**
	 * Create barometer.
	 *
	 * @param jsonData
	 * @param address
	 */
	this.getD3Barometer = function(jsonData, address) {
		$('#' + popupConfirmDialogId + ' div.modal-body').empty();

		// create div for barometer
		$('#' + popupConfirmDialogId + ' div.modal-body').append('<div id="barometer-div"></div>');
		// width and height of chart
		var width = 450, height = 500;
		var barChartSvg = getSvg(width+50, height+50);

		createAxis(barChartSvg);

		var usersDict = [];
		// create dictionary depending on address
		if(address === 'attitude'){
			usersDict = createDictForAttitude(jsonData, usersDict);
		}
		else{
			usersDict = createDictForArgumentAndStatement(jsonData, usersDict);
		}

        // create bars of chart
		createBar(width, height-50, usersDict, barChartSvg);

		// tooltip
        createTooltip(usersDict, barChartSvg, width);

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
	 */
	function createAxis(svg){
	    // create scale to map values
		var xScale = d3.scale.linear().range([0, 450]);
        var yScale = d3.scale.linear().domain([0, 100]).range([450, 0]);

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
			       height: function(d) {if(d.seenBy === 0){
					                        return d.usersNumber/100 * height;
				                        }
					                    return d.usersNumber/d.seenBy * height;},
			       // number of bar * width of bar + padding-left + space between to bars
			       x: function(d,i) {return i*barWidth + 55 + i*5;},
			       // y: height - barLength, because d3 starts to draw in left upper corner
			       y: function(d) {if(d.seenBy === 0){
					                   return height - (d.usersNumber/100 * height - 50);
				                   }
					               return height - (d.usersNumber/d.seenBy * height - 50);},
			       fill: function (d, i) {return colors[i % colors.length];}});
	}

	/**
	 * Create tooltips for bars.
	 *
	 * @param usersDict
	 * @param barChartSvg
	 * @param width
     */
	function createTooltip(usersDict, barChartSvg, width) {
		var div;
		var barWidth = width / usersDict.length - 5;
		barChartSvg.selectAll("rect").on("mouseover", function (d, index) {
			div = d3.select('#' + popupConfirmDialogId + ' div.modal-body').append("div");

			// set properties of div
			div.attr("class", "tooltip").style("opacity", 1)
				.style("left", index * barWidth + 70 + index * 5 + "px")
				.style("top", 200 + "px")
				.style("width", barWidth);

			// append list elements to div
			div.append('li').html(d.text + '.');
			if (d.message != null) {
				div.append('li').html(d.message);
			}
			div.append('li').html(d.seenBy + ' ' + _t_discussion("participantsSawThisStatement"));
			div.append('li').html(_t_discussion("users") + ': ');

			// add images of avatars
			d.users.forEach(function (e) {
				div.append('img').attr('src', e.avatar_url);
			});
		})
		.on("mouseout", function (d) {
			div.style("opacity", 0);
		});
	}

	/**
	 * Create legend for chart.
	 *
	 * @param usersDict
	 */
	function createLegend(usersDict){
		var div, label, element;
		$('#' + popupConfirmDialogId + ' div.modal-body').append('<div id="legend-div"></div>');
		$.each(usersDict, function(key, value) {
			div = $('<div>').attr('class', 'legendSymbolDiv').css('background-color', colors[key]);
            label = $('<label>').attr('class', 'legendLabel').html(value.text);
			element = $('<ul>').attr('class', 'legendUl').append(div).append(label);
			$('#legend-div').append(element);
		});
	}
}