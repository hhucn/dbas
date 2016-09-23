function DiscussionBarometer(){
    'use strict';

    /**
	 * Displays barometer.
	 */
	this.showBarometer = function(){
		var uid = 0, uid_array = [],
			url = window.location.href.split('?')[0],
			splitted = url.split('/'),
			adress = 'position';

		// parse url
		if (url.indexOf('/attitude/') != -1){
			adress = 'attitude';
			uid = splitted[splitted.length-1];
			new AjaxGraphHandler().getUserGraphData(uid, adress);
		} else if (url.indexOf('/justify/') != -1 || window.location.href.indexOf('/choose/') != -1) {
			adress = 'justify';
			$('#discussions-space-list li:not(:last-child) input').each(function(){
				uid_array.push($(this).attr('id').substr(5));
			});
			new AjaxGraphHandler().getUserGraphData(uid_array, adress);
		} else if (url.indexOf('/reaction/') != -1){
			adress = 'argument';
			uid_array.push(splitted[splitted.length-3]);
			uid_array.push(splitted[splitted.length-1]);
			new AjaxGraphHandler().getUserGraphData(uid_array, adress);
		} else {
			adress = 'position';
			$('#discussions-space-list li:not(:last-child) label').each(function(){
				uid_array.push($(this).attr('id'));
			});
			new AjaxGraphHandler().getUserGraphData(uid_array, adress);
		}
	};

	/**
	 * Callback if ajax request was successfull.
     * 
	 * @param data: unparsed data of request
	 * @param adress: step of discussion
	 */
	this.callbackIfDoneForGetDictionary = function(data, adress){
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

		this.getD3Barometer(jsonData);
	};

	/**
	 * Create barometer.
	 *
	 * @param jsonData
	 */
	this.getD3Barometer = function(jsonData) {
		$('#' + popupConfirmDialogId + ' div.modal-body').empty();

		var width = 500, height = 550;

		var svg = getSvg(width, height);

		createAxis(svg);
};

	/**
	 * Create svg-element.
	 *
	 * @param width: width of container, which contains barometer
     * @param height: height of container
	 * @return scalable vector graphic
     */
	function getSvg(width, height){
		return d3.select('#' + popupConfirmDialogId + ' div.modal-body').append("svg")
    		.attr({width: width, height: height, id: "barometer-svg"})
			.append("g");
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
}
