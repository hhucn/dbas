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
		$('#' + graphViewContainerId).show();

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
				//edgeLabelThreshold:0,

				// default settings for node label
				defaultLabelHoverColor: 'node',
				defaultHoverLabelBGColor: '#1C1C1C',
				defaultLabelSize: 13,

				// default settings for node border
				defaultNodeType: 'border',
				defaultNodeBorderColor: '#000000',
				borderSize: 3,

				// default settings for edges
				enableEdgeHovering: true,
				edgeHoverColor: 'edge',
				defaultEdgeHoverColor: '#000',
				edgeHoverSizeRatio: 1,
				edgeHoverExtremities: true,

				// other default settings
				doubleClickEnabled: false,
				hideEdgesOnMove: true,
				zoomMin: 0.2, zoomMax: 1,
				minArrowSize: 7, maxEdgeSize: 1.7,
				sideMargin: 1

			}
		});

		// start startForceAtlas2
		s.startForceAtlas2({worker: true, strongGravityMode: true,barnesHutTheta:10,scalingRatio:20}).refresh();

		/*
		// empty graphViewContainerSpaceId after closing
		$('#' + closeGraphViewContainerId).click(function(){
			$('#'+ graphViewContainerSpaceId).empty();
		});

		// separate the groups of startpoints each other
		$('#' + 'separateView').click(function() {
			s.configForceAtlas2({strongGravityMode: false,linLogMode:true,outboundAttractionDistribution:false});
		});

		// optimize the positions of nodes
		$('#' + 'strechView').click(function() {
			s.configForceAtlas2({outboundAttractionDistribution:true});
		});

		// return to start Graph
		$('#' + 'startView').click(function() {
			s.configForceAtlas2({worker: true,linLogMode:false,strongGravityMode: true,
			barnesHutTheta:10,scalingRatio:20,outboundAttractionDistribution:false});
		});

		// show all contents
		var clicks = 0;
			$('#' + 'showAllContents').click(function() {
			if(clicks == 0){
				s.settings({ labelThreshold: 0, defaultLabelColor: '#2E2E2E' });
			} else {
				s.settings({ labelThreshold: 8 });
			}
			++clicks;
		});
		*/
	};

	/**
	 * Callback for graph - if ajax request failed!
	 */

	this.callbackIfFailForDiscussionGraph = function () {
		alert('ajax-request failed');
	};
}
