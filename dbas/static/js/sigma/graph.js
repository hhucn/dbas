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
		new AjaxGraphHandler().getDiscussionGraphData('/graph/sigma');
	};


	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForDiscussionGraph = function (data) {
		var jsonData = $.parseJSON(data);

		try {
			s = new DiscussionGraph().setDefaultViewParams(true, jsonData, null);
		} catch (err){
			new DiscussionGraph().setDefaultViewParams(false, null, null);
			setGlobalErrorHandler(_t(ohsnap), _t(internalError));
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

		// restore default view
		$('#start-view').click(function() {
			new DiscussionGraph().setDefaultViewParams(true, jsonData, s);
		});

		// show content
		$('#show-content').click(function() {
			s.settings({labelThreshold: 0, defaultLabelColor: '#2E2E2E'});
			$('#show-content').hide();
			$('#hide-content').show();
		});

		// hide content
		$('#hide-content').click(function() {
			s.settings({labelThreshold: 8});
			$('#show-content').show();
			$('#hide-content').hide();
		});

		// increase distance between nodes
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

		// decrease distance between nodes
		$('#tight-view').click(function() {
            s.configForceAtlas2({outboundAttractionDistribution:true});
			$('#wide-view').show();
			$('#tight-view').hide();
		});

		// make a snapshow
		$('#snapshot-graph').click(function() {
			var now = new Date(Date.now());
			var formatted = now.getYear + '-' + now.getMonth + '-' + now.getHours();
			formatted += '_' + now.getMinutes() + '-' + now.getSeconds();
			formatted += '_' + getCurrentIssueId();
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
		if (sigma != null) {
			sigma.stopForceAtlas2();
			sigma.killForceAtlas2();
			sigma.graph.clear();
			sigma.graph.kill();
		}

		$('#' + graphViewContainerSpaceId).empty();

		if (startSigma){
			try {
				return this.getSigmaGraph(jsonData);
			} catch (err){
				new DiscussionGraph().setDefaultViewParams(false, null, sigma);
				setGlobalErrorHandler(_t(ohsnap), _t(internalError));
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
		$('#' + graphViewContainerSpaceId).empty();
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
			var uid = e.data.node.id.substr(e.data.node.id.indexOf('_') + 1);
			var img_modifier = '';
			var img_author = '<img class="preload-image" style="height: 20pt; margin-right: 1em;" src="' + jsonData.extras[uid].author_gravatar + '">';
			var a_modifier = '<a target="_blank" href="' + mainpage + 'user/' + jsonData.extras[uid].author + '">';
			var a_author = '<a target="_blank" href="' + mainpage + 'user/' + jsonData.extras[uid].modifier + '">';
			var tmp = '<ul>';

			tmp += '<li>Content: ' + e.data.node.label + '</li>';
			tmp += '<li>Node: ' + e.data.node.id + '</li>';
			tmp += '<li>Supporters: ' + jsonData.extras[uid].votes + '</li>';
			tmp += '<li>Author: ' + a_author + jsonData.extras[uid].author + ' ' + img_author + '</a></li>';

			if (jsonData.extras[uid].was_modified === 'true') {
				img_modifier = '<img class="preload-image" style="height: 20pt; margin-right: 1em;" src="' + jsonData.extras[uid].modifier_gravatar + '">';
				tmp += '<li>Edit by: ' + a_modifier + jsonData.extras[uid].modifier + ' ' + img_modifier + '</a></li>';
			}
			tmp += '</ul>';
			displayConfirmationDialogWithoutCancelAndFunction('Statement ' + uid, tmp);
        }).refresh();
	}
}
