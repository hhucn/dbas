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
		 * todo:
		 * 1. ajax request
		 * 2. structure like the ajaxhandler
		 * 3. callback into this class
		 * 4. using chartjs.org with doghnut
		 * 5. displayConfirmationDialogWithoutCancelAndFunction with html as text and suitable header
		 * hint: example of a module is in discussion-island
		 */
	};
}
