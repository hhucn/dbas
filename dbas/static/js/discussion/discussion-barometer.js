/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionBarometer(){
	'use strict'

	/**
	 * Displays the barometer
	 */
	this.showBarometer = function(){
		var uid = 0, uid_array = [],
			splitted = window.location.href.split('/'),
			adress = 'position';

		if (window.location.href.indexOf('/attitude/') != -1){
			adress = 'attitude';
			uid = splitted[splitted.length-1];
			new DiscussionBarometer().ajaxRequest(uid, adress);
		} else if (window.location.href.indexOf('/justify/') != -1 || window.location.href.indexOf('/choose/') != -1) {
			adress = 'statement';
			$('#discussions-space-list li:not(:last-child) label').each(function(){
				uid_array.push($(this).attr('id'));
			});
			new DiscussionBarometer().ajaxRequest(uid_array, adress);
		} else if (window.location.href.indexOf('/reaction/') != -1){
			adress = 'argument';
			uid = splitted[splitted.length-3];
			new DiscussionBarometer().ajaxRequest(uid, adress);
		} else {
			adress = 'position';
			new DiscussionBarometer().ajaxRequest(uid, adress);
		}
	};

	this.ajaxRequest = function(uid, adress){
		var dataString;
		switch(adress){
			case 'attitude':
				dataString = {is_argument: 'false', is_attitude: 'true', is_reaction: 'false', uids: uid};
			break;
			case 'statement':
				var json_array = JSON.stringify(uid);
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', uids: json_array};
			break;
			case 'argument':
				dataString = {is_argument: 'true', is_attitude: 'false', is_reaction: 'true', uids: uid};
			break;
			default:
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', uids: uid};
		}

		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			type: 'GET',
			dataType: 'json',
			data: dataString,
			async: true
		}).done(function (data) {
			new DiscussionBarometer().callbackIfDoneForGetDictionary(data, adress);
		}).fail(function () {
			new DiscussionBarometer().callbackIfFailForGetDictionary();
		});
	}

	/**
	 * Callback if the ajax request was successfull
	 * @param data: unparsed data of the request
	 */
	this.callbackIfDoneForGetDictionary = function(data, adress){
		var obj;
        try{
	        obj = JSON.parse(data);
			console.log(obj);
        }catch(e){
	        // TODO: Um die Anzeige einer Fehlermeldung kümmern wir uns später.
			alert('parsing-json: ' + e);
	        return;
        }
		// TODO: Nun hier mit chart.js die votes passend darstellen. ich denke, eine pie-chart bietet sich an

		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' div.modal-body')
			.html('<canvas id="chartCanvas" width="400" height="400" style= "display: block; margin: 0 auto;"></canvas>');
		// TODO: anstelle von txt kann der neue html code eingetragen werden
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		}).removeClass('btn-success');

		// create pie-Chart
		switch(adress){
			case 'attitude': new DiscussionBarometer().createAttituteBarometer(obj); break;
			case 'statement': new DiscussionBarometer().createStatementBarometer(obj); break;
		}

	};

	this.createAttituteBarometer = function(obj) {
		$('#' + popupConfirmDialogId + ' h4.modal-title').html(obj.text);
    	var ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d");

		var pieData = [
        {
			value: obj.agree_users.length,
        	color: "#41AF3D",
			highlight: "#8ADB87",
            label: 'agree'
        },
		{
			value: obj.disagree_users.length,
        	color: "#E04F5F",
			highlight: "#EFA5AC",
			label: 'disagree'
		}
		];

		var chart = new Chart(ctx).Pie(pieData);
	};

	this.createStatementBarometer = function(obj) {
		var ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d");
		var chart = new Chart(ctx).Pie();
		for(var i = 0; i < obj.opinions.length; i++){
			if(obj.opinions[i].text != null){
				var randomColor = '#' + (Math.random().toString(16) + '0000000').slice(2,8);
				chart.addData({
					value: obj.opinions[i].users.length,
					color: randomColor,
					label: obj.opinions[i].text
				});
			}
		}
	};

	/**
	 * Callback if the ajax request failed
	 */
	this.callbackIfFailForGetDictionary = function(){
		alert('ajax-request: some error');
		// TODO: Um die Anzeige einer Fehlermeldung kümmern wir uns später.
	};
}
