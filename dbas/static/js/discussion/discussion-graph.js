/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionGraph() {

	/**
	 * Displays a graph of current discussion
	 */

	this.showGraph = function () {

		//get datastructure of current issue
		$.ajax({
			url: '/export/sigma',
			type: 'GET',
			dataType: 'json',
			async: true

			// if ajax request done, parse data or if failed, error
		}).done(function (data) {
			new DiscussionGraph().callbackIfDoneForDiscussionGraph(data);
		}).fail(function () {
			new DiscussionGraph().callbackIfFailForDiscussionGraph();
		});
	};

	this.callbackIfDoneForDiscussionGraph = function (data) {
		var jsonData = $.parseJSON(data);

		s = new sigma({
			graph: jsonData,
			renderer: {
				type: 'canvas',
				container: graphViewContainerSpaceId
			},
			settings: {

				// default settings for edge
				edgeColor: 'default',
				defaultEdgeColor: '#666',

				// default settings for edge label
				defaultEdgeLabelColor: '#848484',
				defaultEdgeLabelSize: 8,
				edgeLabelSize: 'proportional',
				edgeLabelSizePowRatio: 1,
				edgeLabelThreshold:0,

				// default settings for node label
				defaultLabelHoverColor: 'node',
				defaultHoverLabelBGColor: '#EBEBEB',
				defaultLabelSize: 13,

				// default settings for node border
				defaultNodeType: 'border',
				defaultNodeBorderColor: '#000',
				borderSize: 3,

				// default settings for edges
				enableEdgeHovering: true,
				edgeHoverColor: 'edge',
				defaultEdgeHoverColor: '#000',
				edgeHoverSizeRatio: 1,
				edgeHoverExtremities: true,

				// other default settings
				doubleClickEnabled: true,
				hideEdgesOnMove: true,
				zoomMin: 0.2,
				zoomMax: 1,
				minArrowSize: 10,
				maxEdgeSize: 2,
				sideMargin: 1

			}
		}).startForceAtlas2({
			worker: true,
			strongGravityMode: true,
			barnesHutTheta: 10,
			scalingRatio: 20
		}).bind('clickNode', function(e){
			displayConfirmationDialogWithoutCancelAndFunction('Edit Node: ' + e.data.node.id, e.data.node.label);
		}).refresh();

		$('#graph-view-container-space').attr('style', 'height:95%; float: left;');


		$('#show-content').click(function() {
			s.settings({labelThreshold: 0, defaultLabelColor: '#2E2E2E'});
			$('#show-content').hide();
			$('#hide-content').show();
		});
		$('#hide-content').click(function() {
			s.settings({labelThreshold: 8});
			$('#show-content').show();
			$('#hide-content').hide();
		});

		// empty graphViewContainerSpaceId after closing
		$('#' + closeGraphViewContainerId).click(function(){
			s.stopForceAtlas2();
			s.killForceAtlas2();
			s.graph.clear();
			s.graph.kill();
			$('#'+ graphViewContainerSpaceId).empty();
		});
	};

	/**
	 * Callback for graph - if ajax request failed!
	 */

	this.callbackIfFailForDiscussionGraph = function () {
		alert('ajax-request failed');
	};
}
