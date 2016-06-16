/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionGraph() {

	/**
	 * Displays a graph of current discussion
	 */
	this.showGraph = function () {
		$.ajax({
			url: '/graph/d3',
			type: 'GET',
			dataType: 'json',
			data: {issue: new Helper().getCurrentIssueId()},
			async: true
		}).done(function (data) {
			new DiscussionGraph().callbackIfDoneForDiscussionGraph(data);
		}).fail(function () {
			new GuiHandler().showDiscussionError(_t(internalError));
		});
	};


	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForDiscussionGraph = function (data) {
		var jsonData = $.parseJSON(data);

		try {
			alert('do something');
		} catch (err) {
			new DiscussionGraph().setDefaultViewParams(false, null, s);
			new GuiHandler().showDiscussionError(_t(internalError));
		}
	}
}
