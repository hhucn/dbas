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
		$('#show-positions').show();
		$('#hide-positions').hide();

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

		var svg = getSvg(width, height);

		var force = getForce(width, height);

		// zoom and pan
		var zoom = d3.behavior.zoom().on("zoom", redraw);
		d3.select("svg").call(zoom);

        function redraw() {
            d3.select("g.zoom")
            .attr("transform", "translate(" + zoom.translate() + ")"
			+ " scale(" + zoom.scale() + ")");
        }

		// enable drag functionality, because pan functionality overrides drag
        var drag = force.drag()
			.on("dragstart", function(d){
				d3.event.sourceEvent.stopPropagation();
			});

		var edges = createEdgeDict(jsonData);

		// create arrays of links, nodes and move layout forward one step
		force.links(edges).nodes(jsonData.nodes).on("tick", forceTick);

		// select edges with type of arrow 
		var edgesTypeArrow = [];
		edges.forEach(function(d){
			if(d.edge_type == 'arrow'){
			    return edgesTypeArrow.push(d);
			}
		});

		// arrows for edges
        var marker = svg.append("defs").selectAll('marker').data(edgesTypeArrow)
            .enter()
            .append("svg:marker")
            .attr("id", function(d) { return "marker_" + d.edge_type + d.color + d.target.color})
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
      		.attr("class", "link")
			.style("stroke", function(d) { return d.color; })
			.attr("marker-end", function(d) { return "url(#marker_" + d.edge_type + d.color + d.target.color + ")" });

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

		// background of labels
		var rect = node.append("rect");

		// wrap text
		var label = node.append("text").each(function (d) {
            var node_text = d.label.split(" ");
            for (var i = 0; i < node_text.length; i++) {
                if((i % 4) == 0){
                    d3.select(this).append("tspan")
					.text(node_text[i])
                    .attr("dy", i ? '1.2em' : '0')
                    .attr("x", '0')
                    .attr("text-anchor", "middle");
                }
                else{
                    d3.select(this).append("tspan")
                    .text(' ' + node_text[i]);
				}
            }
			d3.select(this).attr("id", 'label-' + d.id);
			// set position of label
			var height = $("#label-" + d.id).height();
			d3.select(this).attr("y", -height+45);
		});

		// set properties for rect
		rect.each(function (d) {
		    var width = $("#label-" + d.id).width()+10,
			    height = $("#label-" + d.id).height()+10;
			if(d.size == 0){
				width = 0;
				height = 0;
			}
			d3.select(this)
			.attr("width", width)
			.attr("height", height)
			.attr("y", -height+38)
			.attr("x", -width/2)
			.attr("id", 'rect-' + d.id);
		});

		// labels and colors for legend
		var legendLabelCircle = [_t_discussion("issue"), _t_discussion("position"), _t_discussion("statement")];
		var legendLabelRect = [_t_discussion("support"), _t_discussion("attack")];

        var legendColorCircle = ["#3D5AFE", "#3D5AFE", "#FFC107"];
		var legendColorRect = ["#64DD17", "#F44336"];

		// set properties for legend
		d3.svg.legend = function() {
            function legend(selection) {
				// symbols for nodes
                selection.selectAll(".circle")
                .data(legendLabelCircle)
                .enter()
                .append("circle")
				.attr("fill", function (d,i) {return legendColorCircle[i]})
                .attr("r", function (d,i) {
	                if(i == 0) { return 8; }
                    else { return 6; }
				})
				.attr("cy", function (d,i) {return i*40});

				// symbols for edges
				selection.selectAll(".rect")
                .data(legendLabelRect)
                .enter()
                .append("rect")
				.attr("fill", function (d,i) {return legendColorRect[i]})
                .attr("width", 15)
				.attr("height", 5)
				.attr("x", -7)
				.attr("y", function (d,i) {return i*40+118});

				// labels for symbols
                selection.selectAll(".text")
                .data(legendLabelCircle.concat(legendLabelRect))
                .enter()
                .append("text")
                .text(function(d) {return d;})
				.attr("x", 20)
				.attr("y", function (d,i) {return i*40+5});

				return this;
            }
            return legend;
        };

		// create legend
        var legend = d3.svg.legend();
        d3.select("svg").append("g")
            .attr("transform", "translate(30, 330)")
            .call(legend);

		// show content
		$('#show-content').click(function() {
			label.style("display", "inline");
			rect.style("display", "inline");
			$('#show-content').hide();
			$('#hide-content').show();
		});

		// hide content
		$('#hide-content').click(function() {
			label.style("display", "none");
			rect.style("display", "none");
			$('#show-content').show();
			$('#hide-content').hide();
		});
		
		// show positions
		$('#show-positions').click(function() {
			// select positions
			d3.selectAll(".node").each(function(d) {
				if(d.color == '#3D5AFE' && d.size == '6') {
					d3.select('#label-' + d.id).style("display", "inline");
					d3.select("#rect-" + d.id).style("display", "inline");
				}
			});
			$('#show-positions').hide();
			$('#hide-positions').show();
		});
		
		// hide positions
		$('#hide-positions').click(function() {
			// select positions
			d3.selectAll(".node").each(function(d) {
				if(d.color == '#3D5AFE' && d.size == '6') {
					d3.select('#label-' + d.id).style("display", "none");
					d3.select("#rect-" + d.id).style("display", "none");
				}
			});
			$('#show-positions').show();
			$('#hide-positions').hide();
		});

        force.start();

		d3.select(window).on("resize", resize);

		// update force layout calculations
		function forceTick() {
		    // update position of edges
			link
                .attr("x1", function(d) { return d.source.x; })
        	    .attr("y1", function(d) { return d.source.y; })
        	    .attr("x2", function(d) { return d.target.x; })
        	    .attr("y2", function(d) { return d.target.y; });

		    // update position of rect
		    rect
			    .attr("transform", function (d) {
				    return "translate(" + d.x + "," + (d.y - 50) + ")";
    		    });

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

		function resize() {
			$('#graph-svg').width(container.width());
			// Height of space between header and bottom of container
			$('#graph-svg').height(container.outerHeight()-$('#graph-view-container-header').height() + 20);

   		    force.size([container.width(), container.outerHeight()]).resume();
		}
	};

	function getSvg(width, height){
		/**
		 * Create svg-element.
		 *
		 * @param width: width of container, which contains graph
		 * @param height: height of container
		 * @return scalable vector graphic
		 */
		return d3.select('#' + graphViewContainerSpaceId).append("svg")
    		.attr({width: width, height: height, id: "graph-svg"})
			.append('g')
			.attr("class", "zoom");
	}

	function getForce(width, height){
		/**
		 * Create force-directed network diagram and define properties.
		 *
		 * @param width: width of container, which contains graph
		 * @param height: height of container
		 * @return force layout
		 */
		return d3.layout.force()
			.size([width, height])
			// pull nodes toward layout center
    		.gravity(0.11)
			// nodes push each other away
			.charge(-350)
    		.linkDistance(function (d) {
				return d.size;
			});
	}

	function createEdgeDict(jsonData) {
		/**
		 * Create dictionary for edges
		 *
		 * @param jsonData: dict with data for nodes and edges
		 * @return edges: array, which contains dicts for edges
         */
		var edges = [];

		jsonData.edges.forEach(function(e) {
    		// get source and target nodes
    		var sourceNode = jsonData.nodes.filter(function(d) { return d.id === e.source; })[0],
        		targetNode = jsonData.nodes.filter(function(d) { return d.id === e.target; })[0];
    		// add edge, color and type to array
    		edges.push({source: sourceNode, target: targetNode, color: e.color, edge_type: e.edge_type, size: e.size});
		});

		return edges;
	}
}