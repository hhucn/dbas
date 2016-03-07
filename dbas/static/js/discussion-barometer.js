/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionBarometer(){
	/**
	 * Displays the barometer
	 */
	this.showBarometer = function(){
		var txt = 'Hier wird bald ein Meinungsbarometer erscheinen.';
		txt += '<br><img src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Disk_usage_(Boabab).png">';
		displayConfirmationDialogWithoutCancelAndFunction('In progress', txt);
		/**
		 * TODO TERESA:
		 * 1. ajax request
		 * 2. structure like the ajaxhandler
		 * 3. callback in this class
		 * 4. using chartjs.org with doghnut
		 * 5. displayConfirmationDialogWithoutCancelAndFunction with html as text and suitable header
		 */

		getDictionary();
	};

	/**
	 * sends Ajax-Request to Server
	 * saves answer in array
	 * */
	getDictionary = function() {
		$.ajax({
			url: "ajax_get_user_with_same_opinion",
			type: 'GET',
			dataType: 'json',
			data: {
				uid: 0,
				is_argument: false
			},
			async: true
		}).done(function (data) {
			var obj = JSON.parse(data);
			var error = obj.error;
			var votes = [];
			var i = 0;
			$.each(obj.votes, function () {
				votes[i] = [];
				$.each(this, function (key, value) {
					votes[i].push("Key: " + key + ", Value:" + value);
				});
				i++;
			});
		}).fail(function () {
		});
	};
}
