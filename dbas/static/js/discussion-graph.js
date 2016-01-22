/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 05.01.16
 */

function DiscussionGraph(){
	/**
	 * Displays a graph of current discussion
	 */
	this.showGraph = function(){
		var space = $('#' + graphViewContainerSpaceId),
			image = 'http://cdno.gettingsmart.com/wp-content/uploads/2013/09/Complex-Mind-Map.png';
		space.show().empty().append('<img style="width: ' + space.width()+ 'px" src="' + image + '">');
		$('#' + graphViewContainerId).show();
	};
}