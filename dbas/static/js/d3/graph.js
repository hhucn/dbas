/**
 * @author Teresa Uebber, Tobias Krauthoff
 * @email teresa.uebber@hhu.de, krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionGraph() {
    var s;
	var isPositionVisible = false;
	var isContentVisible = false;
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

		var width = container.width(), height = container.outerHeight();

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
		var drag = enableDrag(force);

		// resize graph on window event
		d3.select(window).on("resize", resize);
		function resize() {
			var graphsvg = $('#graph-svg');
			graphsvg.width(container.width());
			// height of space between header and bottom of container
			graphsvg.height(container.outerHeight()-$('#graph-view-container-header').height() + 20);
			force.size([container.width(), container.outerHeight()]).resume();
		}

		// edge
		var edges = createEdgeDict(jsonData);
		// create arrays of links, nodes and move layout forward one step
		force.links(edges).nodes(jsonData.nodes).on("tick", forceTick);
		var edgesTypeArrow = createArrowDict(edges);
        var marker = createArrows(svg, edgesTypeArrow);
		var link = createLinks(svg, edges, marker);

		// node
   		var node = createNodes(svg, force, drag);
    	var circle = setNodeProperties(node);

		// tooltip
		// rect as background of label
		var rect = node.append("rect");
		var label = createLabel(node);
		setRectProperties(rect/*, label*/);

		// legend
        createLegend();
		// call updated legend
        var legend = d3.svg.legend();
		// set position of legend
        d3.select("svg").append("g")
            .attr("transform", "translate(30, 280)")
            .call(legend);

		// buttons of sidebar
        showContent(label, rect);
		hideContent(label, rect);
		showPositions();
		hidePositions();

        force.start();
		
		// update force layout calculations
		function forceTick() {
		    // update position of edges
			link.attr({x1: function(d) { return d.source.x; }, y1: function(d) { return d.source.y; },
        	           x2: function(d) { return d.target.x; }, y2: function(d) { return d.target.y; }});

		    // update position of rect
		    rect.attr("transform", function (d) {
				    return "translate(" + d.x + "," + (d.y - 50) + ")";});

            // update position of nodes
		    circle.attr({cx: function(d) { return d.x; },
       		             cy: function(d) { return d.y; }});

            // update position of label
		    label.attr("transform", function (d) {
  			        return "translate(" + d.x + "," + (d.y - 50) + ")";});
		}

		//////////////////////////////////////////////////////////////////////////////
		// highlight nodes and edges
		circle.on("click", function()
		{
			var circleId = this.id;
            showPartOfGraph(edges, circleId);
			showEdgesWithTwoLinks(edges, circleId);

		});
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
		 * Create dictionary for edges.
		 *
		 * @param jsonData: dict with data for nodes and edges
		 * @return edges: array, which contains dicts for edges
         */
		var edges = [];

		jsonData.edges.forEach(function(e) {
    		// get source and target nodes
    		var sourceNode = jsonData.nodes.filter(function(d) { return d.id === e.source; })[0],
        		targetNode = jsonData.nodes.filter(function(d) { return d.id === e.target; })[0];
    		// add edge, color, type and idto array
    		edges.push({source: sourceNode, target: targetNode, color: e.color, edge_type: e.edge_type, size: e.size, id: e.id});
		});

		return edges;
	}

	function createArrowDict(edges){
		/**
		 * Select edges with type of arrow.
		 *
		 * @param edges: edges of graph
		 * @return edgesTypeArrow: array, which contains edges of type arrow
         */
		var edgesTypeArrow = [];
		edges.forEach(function(d){
			if(d.edge_type == 'arrow'){
			    return edgesTypeArrow.push(d);
			}
		});
		return edgesTypeArrow;
	}

	function createArrows(svg, edgesTypeArrow) {
		/**
		 * Create arrows for edges.
		 *
		 * @param svg
		 * @param edgesTypeArrow
		 * @return marker: arrow
         */
		return svg.append("defs").selectAll('marker').data(edgesTypeArrow)
            .enter().append("svg:marker")
            .attr({id: function(d) { return "marker_" + d.edge_type + d.id },
			       refX: function(d){
			                 if(d.target.label == ''){ return 4; }
				             else if(d.target.size == 8){ return 8; }
				             else{ return 7; }}, refY: 2.2,
                   markerWidth: 10, markerHeight: 10,
                   orient: "auto"})
			.attr("fill", function(d) { return d.color; })
			.append("svg:path")
			.attr("d", "M 0,0 V 4 L 5,2 Z");
	}

	function createLinks(svg, edges, marker) {
		/**
		 * Create links between nodes.
		 *
		 * @param svg
		 * @param marker: arrow
		 * @param edges
		 * @return links
		 */
		return svg.selectAll(".path")
    		.data(edges)
			// svg lines
    		.enter().append("line")
      		.attr("class", "link")
			.style("stroke", function(d) { return d.color; })
			.attr("id", function(d) { return d.id; })
			// assign marker to line
			.attr("marker-end", function(d) { return "url(#marker_" + d.edge_type + d.id + ")" });
	}

	function enableDrag(force){
		/**
		 * Enable drag functionality, because pan functionality overrides drag.
		 *
		 * @param force
		 * @return drag functionality
		 */
		return force.drag()
			.on("dragstart", function(d){
				d3.event.sourceEvent.stopPropagation();
			});
	}

	function createNodes(svg, force, drag) {
		/**
		 * Create node as svg circle and enable drag functionality.
		 *
		 * @param svg
		 * @param force
		 * @param drag
		 * @return nodes
		 */
		return svg.selectAll(".node")
        	.data(force.nodes())
        	.enter().append("g")
            .attr("class", "node")
            .call(drag);
	}

	function setNodeProperties(node){
		/**
		 * Define properties for nodes.
         *
		 * @param node
		 * @return circle
		 */
		return node.append("circle")
      		.attr({r: function(d){ return d.size; },
				   fill: function(d){ return d.color},
				   id: function (d) { return d.id;}
			});
	}

	function createLabel(node){
		/**
		 * Wrap text.
		 *
		 * @param node
		 * @return label
		 */
		return node.append("text").each(function (d) {
            var node_text = d.label.split(" ");
            for (var i = 0; i < node_text.length; i++) {
                if((i % 4) == 0){
                    d3.select(this).append("tspan")
					.text(node_text[i])
                    .attr({dy: i ? '1.2em' : '0', x: '0',
                           "text-anchor": "middle"});
                }
                else{
                    d3.select(this).append("tspan").text(' ' + node_text[i]);
				}
            }
			d3.select(this).attr("id", 'label-' + d.id);
			// set position of label
			var height = $("#label-" + d.id).height();
			d3.select(this).attr("y", -height+45);
		});
	}

	function setRectProperties(rect){
		/**
		 * Set properties for rect.
		 *
		 * @param rect: background of label
 		 */
		rect.each(function (d) {
			var element = $("#label-" + d.id);
		    var width = element.width() + 10;
			var height = element.height() + 10;
			if(d.size == 0){
				width = 0;
				height = 0;
			}
			d3.select(this)
			.attr({width: width, height: height,
			       y: -height+38, x: -width/2,
			       id: 'rect-' + d.id});
		});
	}

	function createLegend(){
		/**
		 * Create legend and update legend.
		 */
		// labels and colors for legend
		var legendLabelCircle = [_t_discussion("issue"), _t_discussion("position"), _t_discussion("statement")],
		    legendLabelRect = [_t_discussion("support"), _t_discussion("attack")],
            legendColorCircle = ["#3D5AFE", "#3D5AFE", "#FFC107"],
		    legendColorRect = ["#64DD17", "#F44336"];

		// set properties for legend
		return d3.svg.legend = function() {
            function legend(selection) {
                createNodeSymbols(selection, legendLabelCircle, legendColorCircle);
                createEdgeSymbols(selection, legendLabelRect, legendColorRect);
                createLabelsForSymbols(selection, legendLabelCircle, legendLabelRect);
				return this;
            }
            return legend;
        };
	}

	function createNodeSymbols(selection, legendLabelCircle, legendColorCircle) {
		/**
		 * Create symbols for nodes.
		 *
		 * @param selection
		 * @param legendLabelCircle: array with labels for circle
		 * @param legendColorCircle: array with colors
		 */
		selection.selectAll(".circle")
        .data(legendLabelCircle)
        .enter().append("circle")
		.attr("id", 1)
		.attr({fill: function (d,i) {return legendColorCircle[i]},
               r: function (d,i) {
	               if(i == 0) { return 8; }
				   else { return 6; }},
			   cy: function (d,i) {return i*40}});
	}

	function createEdgeSymbols(selection, legendLabelRect, legendColorRect) {
		/**
		 * Create symbols for edges.
		 *
		 * @param selection
		 * @param legendLabelRect: array with labels for rect
		 * @param legendColorRect: array with colors
		 */
		selection.selectAll(".rect")
		.data(legendLabelRect)
        .enter().append("rect")
		.attr({fill: function (d,i) {return legendColorRect[i]},
               width: 15, height: 5,
			   x: -7, y: function (d,i) {return i*40+118}});
	}

	function createLabelsForSymbols(selection, legendLabelCircle, legendLabelRect) {
		/**
		 * Create labels for symbols.
		 *
		 * @param selection
		 * @param legendLabelCircle: array with labels for circle
		 * @param legendLabelRect: array with labels for rect
		 */
		selection.selectAll(".text")
		.data(legendLabelCircle.concat(legendLabelRect))
        .enter().append("text")
        .text(function(d) {return d;})
		.attr({x: 20, y: function (d,i) {return i*40+5}});
	}

	function showContent (label, rect){
        /**
	     * Show all labels of graph.
		 *
		 * @param label
		 * @param rect
		 */
		$('#show-content').click(function() {
			label.style("display", "inline");
			rect.style("display", "inline");
			$('#show-content').hide();
			$('#hide-content').show();
			// also show content of positions
			$('#show-positions').hide();
			$('#hide-positions').show();
			isContentVisible = true;
		});
	}

	function hideContent(label, rect) {
        /**
	     * Hide all labels of graph.
		 *
		 * @param label
		 * @param rect
		 */
		$('#hide-content').click(function() {
			label.style("display", "none");
			rect.style("display", "none");
			$('#show-content').show();
			$('#hide-content').hide();
			isContentVisible = false;
			if (isPositionVisible){
				setDisplayStyleOfNodes('inline');
			} else {
				$('#show-positions').show();
				$('#hide-positions').hide();
			}
		});
	}

	function showPositions() {
        /**
	     * Show labels for positions.
		 */
		$('#show-positions').click(function() {
			// select positions
			setDisplayStyleOfNodes('inline');
			$('#show-positions').hide();
			$('#hide-positions').show();
			isPositionVisible = true;
		});
	}

	function hidePositions() {
        /**
	     * Hide labels for positions.
		 */
		$('#hide-positions').click(function() {
			// select positions
			setDisplayStyleOfNodes('none');
			$('#show-positions').show();
			$('#hide-positions').hide();
			isPositionVisible = false;
		});
	}

	function setDisplayStyleOfNodes(style) {
		d3.selectAll(".node").each(function(d) {
			if(d.color == '#3D5AFE' && d.size == '6') {
				d3.select('#label-' + d.id).style("display", style);
				d3.select("#rect-" + d.id).style("display", style);
			}
		});
	}

    function showPartOfGraph(edges, circleId) {
		edges.forEach(function(d){
			if(d.source.id === circleId || d.target.id === circleId){
				// edges
                d3.select('#' + d.id).style('stroke', d.color);
				// nodes
				d3.select('#' + d.source.id).attr('fill', d.source.color);
				d3.select('#' + d.target.id).attr('fill', d.target.color);
				// arrows
				d3.select("#marker_" + d.edge_type + d.id).attr('fill', d.color);
			}
			else{
				// edges
                d3.select('#' + d.id).style('stroke', '#E0E0E0');
				// nodes
				d3.select('#' + d.source.id).attr('fill', '#E0E0E0');
				// arrows
				d3.select("#marker_" + d.edge_type + d.id).attr('fill', '#E0E0E0');
			}
		});
	}

	function showEdgesWithTwoLinks(edges, circleId){
		var edge;
		var idOfNextEdge;
		edges.forEach(function(d) {
			if(d.source.id === circleId || d.target.id === circleId){
				if (d.source.label === '' || d.target.label === ''){
				    if(d.id.charAt(d.id.length-1) === '0') {
					    idOfNextEdge = (d.id.substring(0, d.id.length - 1) + '1');
						edges.forEach(function (selected) {
							if(selected.id === idOfNextEdge){
								edge = selected;
							}
						});
						if(edge != null){
							// edge
							d3.select('#' + idOfNextEdge).style('stroke', d.color);
						    // node
				            d3.select('#' + edge.source.id).attr('fill', edge.source.color);
							// arrow
					        d3.select("#marker_" + edge.edge_type + edge.id).attr('fill', edge.color);
						}
					}
					else if(d.id.charAt(d.id.length-1) === '1') {
						idOfNextEdge = (d.id.substring(0, d.id.length - 1) + '0');
						edges.forEach(function (selected) {
							if(selected.id === idOfNextEdge){
								edge = selected;
							}
						});
						if(edge != null) {
							//edge
							d3.select('#' + idOfNextEdge).style('stroke', d.color);
							//node
							d3.select('#' + edge.target.id).attr('fill', edge.target.color);
							// arrow
							d3.select("#marker_" + edge.edge_type + edge.id).attr('fill', edge.color);
						}
					}
				}
			}
		});
	}
}