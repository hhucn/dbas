/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionGraph() {
	var s;

	/**
	 * Displays a graph of current discussion
	 */
	this.showGraph = function () {
		$.ajax({
			url: '/graph/sigma',
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
			s = this.getSigmaGraph(jsonData);
			s.addRenderer({
				type: 'canvas',
				container: graphViewContainerSpaceId
			});
		} catch (err){
			new DiscussionGraph().setDefaultViewParams(false, null, s);
			new GuiHandler().showDiscussionError(_t(internalError));
			return;
		}

		// dragging
        var dragListener = sigma.plugins.dragNodes(s, s.renderers[0]);
		dragListener.bind('startdrag', function(event) {
            s.stopForceAtlas2();
        });
		dragListener.bind('drop', function(event) {});

		// hack
		$('#graph-view-container-space').attr('style', 'height:95%; float: left;');

		// buttons
		$('#start-view').click(function() {
			new DiscussionGraph().setDefaultViewParams(true, jsonData, s);
		});

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

		$('#wide-view').click(function() {
			if (!s.isForceAtlas2Running()){
                s.startForceAtlas2({
					worker: true,
	                linLogMode: false,
					strongGravityMode: true,
					barnesHutTheta: 10,
					scalingRatio: 20
                });
			}
			$('#wide-view').hide();
			$('#tight-view').show();
            s.configForceAtlas2({
	            strongGravityMode: false,
	            linLogMode:true,
	            outboundAttractionDistribution:false
            });
		});

		$('#tight-view').click(function() {
            s.configForceAtlas2({outboundAttractionDistribution:true});
			$('#wide-view').show();
			$('#tight-view').hide();
		});

		$('#snapshot-graph').click(function() {
			var now = new Date(Date.now());
			var formatted = now.getYear + '-' + now.getMonth + '-' + now.getHours();
			formatted += '_' + now.getMinutes() + '-' + now.getSeconds();
			formatted += '_' + new Helper().getCurrentIssueId();
			window.open(s.renderers[0].snapshot({
				format: 'png',
				background: 'white',
				filename: formatted + '.png',
				labels: false
            }));
		});

		// empty graphViewContainerSpaceId after closing
		$('#' + closeGraphViewContainerId).click(function(){
			new DiscussionGraph().setDefaultViewParams(false, null, s);
		});
	};

	/**
	 *
	 * @param startSigma
	 * @param jsonData
	 * @param sigma
	 */
	this.setDefaultViewParams = function (startSigma, jsonData, sigma) {
		$('#hide-content').hide();
		$('#show-content').show();
		$('#wide-view').show();
		$('#tight-view').hide();
		sigma.stopForceAtlas2();
		sigma.killForceAtlas2();
		sigma.graph.clear();
		sigma.graph.kill();

            $('#' + graphViewContainerSpaceId).empty();

		if (startSigma){
			try {
				sigma = this.getSigmaGraph(jsonData);
			} catch (err){
				new DiscussionGraph().setDefaultViewParams(false, null, sigma);
				new GuiHandler().showDiscussionError(_t(internalError));
			}
		} else {
			$('#'+ graphViewContainerSpaceId).empty();
		}
	};

	/**
	 *
	 * @param jsonData
	 */
	this.getSigmaGraph = function(jsonData){
		return new sigma({
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
				doubleClickEnabled: false,
				hideEdgesOnMove: false,
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
		}).bind('doubleClickNode', function(e){
			var tmp = '<br><br><ul><li>edit</li><li>supportes</li><li>author</li></ul>';
			displayConfirmationDialogWithoutCancelAndFunction('Edit Node: ' + e.data.node.id, 'Content: ' + e.data.node.label + tmp);
        }).refresh();
	}
}
