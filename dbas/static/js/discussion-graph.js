/**
 * @author Tobias Krauthoff, Abdullah Polat
 * @email krauthoff@cs.uni-duesseldorf.de, abdullah.polat@hhu.de
 * @copyright Krauthoff, Polat 2016
 */

function DiscussionGraph(){
	/**
	 * Displays a graph of current discussion
	 */
	this.showGraph = function(){
		var space = $('#' + graphViewContainerSpaceId),
			image = 'http://cdno.gettingsmart.com/wp-content/uploads/2013/09/Complex-Mind-Map.png';
		space.show().empty().append('<img src="' + image + '">');
		$('#' + graphViewContainerId).show();
	};
}