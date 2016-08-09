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
		//try {
		try {
			s = new DiscussionGraph().setDefaultViewParams(true, jsonData, null);
		} catch (err) {
			new DiscussionGraph().setDefaultViewParams(false, null, s);
			setGlobalErrorHandler(_t(ohsnap), _t(internalError));
		}
	};

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

		var container = $('#' + graphViewContainerSpaceId);
		container.empty();

		if (startD3){
			try {
				return this.getD3Graph(jsonData);
			} catch (err){
				new DiscussionGraph().setDefaultViewParams(false, null, d3);
				setGlobalErrorHandler('Oh Snap!', _t(internalError));
				console.log('D3: ' + err.message);
			}
		} else {
			container.empty();
		}
	};

	/**
	 * Create a graph.
	 * 
	 * @param jsonData
	 */
	this.getD3Graph = function(jsonData){
		var container = $('#' + graphViewContainerSpaceId);
		container.empty();
			
		var width = container.width();
		var height = container.outerHeight();

		// container for visualization
		var svg = d3.select('#' + graphViewContainerSpaceId).append("svg")
    		.attr("width", width)
    		.attr("height", height)
			.append('g')
			.attr("class", "zoom");

		// create force layout object and define properties
		var force = d3.layout.force()
    		.gravity(0.07)
    		.charge(-150)
    		.linkDistance(80)
    		.size([width, height]);

		// zoom and pan
		var zoom = d3.behavior.zoom().on("zoom", zoomed);
		d3.select("svg").call(zoom);

        function zoomed() {
            d3.select("g.zoom")
            .attr("transform", "translate(" + zoom.translate() + ")"
			+ " scale(" + zoom.scale() + ")")
        }

		// enable drag functionality, pan functionality overrides drag
        var drag = force.drag()
			.on("dragstart", function(d){
				d3.event.sourceEvent.stopPropagation();
			});

		var edges = [];

		jsonData.edges.forEach(function(e) {
    		// get source and target nodes
    		var sourceNode = jsonData.nodes.filter(function(d) { return d.id === e.source; })[0],
        		targetNode = jsonData.nodes.filter(function(d) { return d.id === e.target; })[0];
    		// add edge, color and size to array
    		edges.push({source: sourceNode, target: targetNode, color: e.color, size: e.size});
		});

		force.links(edges).nodes(jsonData.nodes).on("tick", forceTick);

        var marker = svg.append("defs").selectAll('marker').data(edges)
            .enter()
            .append("svg:marker")
            .attr("id", function(d) { return "marker_" + d.target.color + d.color })
			.attr("refX", function(d){
			    if(d.target.label == ''){ return 4; }
				else if(d.target.size == 8){ return 8; }
				else{ return 7; }
			})
            .attr("refY", 2.2)
            .attr("markerWidth", 10)
            .attr("markerHeight", 10)
            .attr("orient", "auto")
			.append("svg:path")
			.attr("d", "M 0,0 V 4 L 5,2 Z")
            .attr("fill", function(d) {
			    return d.color;
			});

		// links between nodes
		var link = svg.selectAll(".path")
    		.data(edges)
			// svg lines
    		.enter().append("line")
			.style("fill", "white")
      		.attr("class", "link")
			.style("stroke", function(d) { return d.color; })
			.style("stroke-width", '2px')
			.attr("marker-end", function(d) { return "url(#marker_" + d.target.color + d.color + ")" });

		// node: svg circle
   		var node = svg.selectAll(".node")
        	.data(force.nodes())
        	.enter().append("g")
            .attr("class", "node")
            .call(drag);

		// define properties for nodes
    	var circle = node.append("circle")
      		.attr("r", function(d){
				return d.size;
            })
			.attr("fill", function(d){
				return d.color;
			});

		// wrap text
		var label = node
			.append("text").each(function (d) {
            var node_text = d.label.split(" ");
            for (var i = 0; i < node_text.length; i++) {
                if((i % 4) == 0){
                    d3.select(this).append("tspan")
					.text(node_text[i])
                    .attr("dy", i ? '1.0em' : '0')
                    .attr("x", '0')
                    .attr("text-anchor", "middle")
                    .attr("class", "tspan" + i);
                }
                else{
                    d3.select(this).append("tspan")
                    .text(' ' + node_text[i]);
                }
            }
		});

		// show content
		$('#show-content').click(function() {
			label.style("display", "inline");
			$('#show-content').hide();
			$('#hide-content').show();
		});

		// hide content
		$('#hide-content').click(function() {
			label.style("display", "none");
			$('#show-content').show();
			$('#hide-content').hide();
		});

        force.start();

		// update force layout calculations
  		function forceTick() {
            // update position of edges
    		link
        		.attr("x1", function(d) { return d.source.x; })
        		.attr("y1", function(d) { return d.source.y; })
        		.attr("x2", function(d) { return d.target.x; })
        		.attr("y2", function(d) { return d.target.y; });

            // update position of nodes
			circle
        		.attr("cx", function(d) { return d.x; })
        		.attr("cy", function(d) { return d.y; });

            // update position of label
			label
				.attr("transform", function (d) {
        			return "translate(" + d.x + "," + (d.y - 50) + ")";
    			});
 		}
	}
}