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
		new AjaxGraphHandler().getDiscussionGraphData('/graph/d3');
	};


	/**
	 *
	 * @param data
	 */
	this.callbackIfDoneForDiscussionGraph = function (data) {
		var jsonData = $.parseJSON(data);
		try {
			s = new DiscussionGraph().setDefaultViewParams(true, jsonData, null);
		} catch (err) {
			new DiscussionGraph().setDefaultViewParams(false, null, s);
			setGlobalErrorHandler(_t(ohsnap), _t(internalError));
		}
	}

	/**
	 *
	 * @param startD3
	 * @param jsonData
	 * @param d3
	 */
	this.setDefaultViewParams = function (startD3, jsonData, d3) {
		$('#hide-content').hide();
		$('#show-content').show();
		$('#wide-view').show();
		$('#tight-view').hide();

		$('#' + graphViewContainerSpaceId).empty();

		if (startD3){
			try {
				return this.getD3Graph(jsonData);
			} catch (err){
				new DiscussionGraph().setDefaultViewParams(false, null, d3);
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
	this.getD3Graph = function(jsonData){
		$('#' + graphViewContainerSpaceId).empty();

		var width = 1500,
   			height = 600;

		// container for visualization
		var svg = d3.select('#' + graphViewContainerSpaceId).append("svg")
    		.attr("width", width)
    		.attr("height", height);

		// create force layout object and define properties
		var force = d3.layout.force()
    		.gravity(0.07)
    		.charge(-200)
    		.linkDistance(80)
    		.size([width, height]);

		var edges = [];

		jsonData.edges.forEach(function(e) {
    		// get source and target nodes
    		var sourceNode = jsonData.nodes.filter(function(d) { return d.id === e.source; })[0],
        		targetNode = jsonData.nodes.filter(function(d) { return d.id === e.target; })[0];
    		// add edge and color to array
    		edges.push({source: sourceNode, target: targetNode, color: e.color});
		});

		force
    		.links(edges)
			.nodes(jsonData.nodes)
    		.start();
		
		// links between nodes
		var link = svg.selectAll(".link")
    		.data(edges)
			// SVG lines
    		.enter().append("line")
			    .style("stroke", function(d) { return d.color; })
      			.attr("class", "link");

		// node: SVG circle
   		var node = svg.selectAll(".node")
        	.data(force.nodes())
        	.enter().append("g")
            	.attr("class", "node")
            	.call(force.drag);

		// define properties for nodes
    	var circle = node.append("circle")
      		.attr("r", function(d){
				return d.size;
            })
			.attr("fill", function(d){
				return d.color;
			});

		var helper = new Helper();

        var label = node.append("text").each(function (d) {
   	        var node_text = helper.cutTextOnChar(d.label, 50, ' ');
       		d3.select(this).append("tspan")
                .text(node_text)
                .attr("dy", "1.2em")
                .attr("x", '0')
                .attr("text-anchor", "middle")
                .attr("class", "tspan");
      		});

		// update force layout calculations
  		force.on("tick", function() {
    		link
				// transform x, y
        		.attr("x1", function(d) { return d.source.x; })
        		.attr("y1", function(d) { return d.source.y; })
        		.attr("x2", function(d) { return d.target.x; })
        		.attr("y2", function(d) { return d.target.y; });

			circle
        		.attr("cx", function(d) { return d.x; })
        		.attr("cy", function(d) { return d.y; });

			label
				.attr("transform", function (d) {
        			return "translate(" + d.x + "," + (d.y - 50) + ")";
    			});
  		});
	}
}
