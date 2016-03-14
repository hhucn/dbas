/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionBarometer(){
	/**
	 * Displays the barometer
	 */
	this.showBarometer = function(){
		/**
		 * TODO TERESA:
		 * 1. ajax request
		 * 2. structure like the ajaxhandler
		 * 3. callback in this class
		 * 4. using chartjs.org with doghnut
		 * 5. displayConfirmationDialogWithoutCancelAndFunction with html as text and suitable header
		 */

		$.ajax({
			url: "ajax_get_user_with_same_opinion",
			type: 'GET',
			dataType: 'json',
			data: {uid: 0, is_argument: false},
			async: true
		}).done(function (data) {
			new DiscussionBarometer().callbackIfDoneForGetDictionary(data);
		}).fail(function () {
			new DiscussionBarometer().callbackIfFailForGetDictionary();
		});
	};

	/**
	 * Callback if the ajax request was successfull
	 * @param data: unparsed data of the request
	 */
	this.callbackIfDoneForGetDictionary = function(data){
		var obj,
			votes = [],
			i = 0;

        try{
	        obj = JSON.parse(data);
        }catch(e){
	        // TODO: Um die Anzeige einer Fehlermeldung kümmern wir uns später.
			alert('parsing-json: ' + e);
	        return;
        }

		$.each(obj.votes, function () {
			votes[i] = [];
			$.each(this, function (key, value) {
				votes[i].push("Key: " + key + ", Value:" + value);
			});
			i++;
		});
		// TODO: Nun hier mit chart.js die votes passend darstellen. ich denke, eine pie-chart bietet sich an
		
		var txt = 'Hier wird bald ein Meinungsbarometer erscheinen.';
		txt += '<br><img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Disk_usage_(Boabab).png">';

		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' h4.modal-title').html('In progress');
		$('#' + popupConfirmDialogId + ' div.modal-body').html(txt); // TODO: anstelle von txt kann der neue html code eingetragen werden
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		}).removeClass('btn-success');
		$('#' + popupConfirmDialogRefuseBtn).hide();
	};


	/**
	 * Callback if the ajax request failed
	 */
	this.callbackIfFailForGetDictionary = function(){
		alert('ajax-request: some error');
		// TODO: Um die Anzeige einer Fehlermeldung kümmern wir uns später.
	};
}
