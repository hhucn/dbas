/**
 * @author Teresa Uebber, Tobias Krauthoff
 * @email teresa.uebber@hhu.de, krauthoff@cs.uni-duesseldorf.de
 */

function DiscussionGraph() {
    var s;
    var isPositionVisible = false;
    var isContentVisible = false;
    var isStatementVisible = false;
    var isSupportVisible = false;
    var isAttackVisible = false;

    /**
     * Displays a graph of current discussion
     */
    this.showGraph = function () {
        new AjaxGraphHandler().getDiscussionGraphData('/graph/d3');
    };

    /**
     * Callback if ajax request was successful.
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
     * If ajax request was successful show modal with data for jump into discussion.
     *
     * @param data
     */
    this.callbackIfDoneForGetJumpDataForGraph = function (data){
        var jsonData = $.parseJSON(data);
        var popup = $('#popup-jump-graph');
        if (jsonData.error.length === 0) {
            var list = $('<ul>');
            popup.find('div.modal-body div').empty();
            createContentOfModalBody(jsonData, list);
            popup.find('div.modal-body div').append(list);

            // jump to url
            popup.find('input').click(function () {
                window.location = $(this).attr('value');
            });
        } else {
            popup.modal('hide');
        }

        // add hover effects
        new GuiHandler().hoverInputListOf(popup.find('div.modal-body div'));
    };

    /**
     * Create content for modal to jump into discussion.
     *
     * @param jsonData
     * @param list
     */
    function createContentOfModalBody(jsonData, list) {
        var label, input, element, counter = 0;

        $.each(jsonData.arguments, function(key, value) {
            input = $('<input>').attr('type', 'radio').attr('value', value.url).attr('id', 'jump_' + counter);
            label = $('<label>').html(value.text).attr('for', 'jump_' + counter);
            element = $('<li>').append(input).append(label);
            list.append(element);
            counter += 1;
        });
    }

    /**
     * Set parameters for default view of graph.
     *
     * @param startD3
     * @param jsonData
     * @param d3
     */
    this.setDefaultViewParams = function (startD3, jsonData, d3) {
        new DiscussionGraph().setButtonDefaultSettings();
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
     * Set default settings of buttons.
     */
    this.setButtonDefaultSettings = function(){
        $('#show-labels').show();
        $('#hide-labels').hide();
        $('#show-attacks-on-my-statements').show();
        $('#hide-attacks-on-my-statements').hide();
        $('#show-my-statements').show();
        $('#hide-my-statements').hide();
        $('#show-supports-on-my-statements').show();
        $('#hide-supports-on-my-statements').hide();
        $('#show-positions').show();
        $('#hide-positions').hide();
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

        var svg = getGraphSvg(width, height),
            force = getForce(width, height+100);

        // zoom and pan
        zoomAndPan();
        var drag = enableDrag(force);

        // resize
        resizeGraph(container, force);

        // edge
        var edges = createEdgeDict(jsonData);
        // create arrays of links, nodes and move layout forward one step
        force.links(edges).nodes(jsonData.nodes).on("tick", forceTick);
        var edgesTypeArrow = createArrowDict(edges),
            marker = createArrows(svg, edgesTypeArrow),
            link = createLinks(svg, edges, marker);

        // node
        var node = createNodes(svg, force, drag),
            circle = setNodeProperties(node);

        // tooltip
        // rect as background of label
        var rect = node.append("rect").attr('class', 'labelBox'),
            label = createLabel(node);
        setRectProperties(rect);

        // legend
        createLegend();
        // call updated legend
        var legend = d3.svg.legend();
        // create div for legend
        container.append("<div id = 'graphViewLegendId'></div>");
        getLegendSvg().call(legend);

        // buttons of sidebar
        addListenersForSidebarButtons(jsonData, label, rect, edges, force);

        moveToBack(circle);

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
        addListenerForNodes(circle, edges);
    };

    /**
     * Create svg-element.
     *
     * @param width: width of container, which contains graph
     * @param height: height of container
     * @return scalable vector graphic
     */
    function getGraphSvg(width, height){
        return d3.select('#' + graphViewContainerSpaceId).append("svg")
            .attr({width: width, height: height, id: "graph-svg"})
            .append('g')
            .attr("class", "zoom");
    }

    /**
     * Create force-directed network diagram and define properties.
     *
     * @param width: width of container, which contains graph
     * @param height: height of container
     * @return force layout
     */
    function getForce(width, height){
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

    /**
     * Enable zoom and pan functionality on graph.
     */
    function zoomAndPan(){
        var zoom = d3.behavior.zoom().on("zoom", redraw);
        d3.select("#graph-svg").call(zoom).on("dblclick.zoom", null);
        function redraw() {
            d3.selectAll("g.zoom")
            .attr("transform", "translate(" + zoom.translate() + ")"
            + " scale(" + zoom.scale() + ")");
        }
    }

    /**
     * Enable drag functionality, because pan functionality overrides drag.
     *
     * @param force
     * @return drag functionality
     */
    function enableDrag(force){
        return force.drag()
            .on("dragstart", function(){
                d3.event.sourceEvent.stopPropagation();
            });
    }

    /**
     * Resize graph on window event.
     *
     * @param container
     * @param force
     */
    function resizeGraph(container, force){
        d3.select(window).on("resize", resize);
        function resize() {
            var graphSvg = $('#graph-svg');
            graphSvg.width(container.width());
            // height of space between header and bottom of container
            graphSvg.height(container.outerHeight()-$('#graph-view-container-header').height() + 20);
            force.size([container.width(), container.outerHeight()]).resume();
        }
    }

    /**
     * Create dictionary for edges.
     *
     * @param jsonData: dict with data for nodes and edges
     * @return edges: array, which contains dicts for edges
     */
    function createEdgeDict(jsonData) {
        var edges = [];
        jsonData.edges.forEach(function(e) {
            // get source and target nodes
            var sourceNode = jsonData.nodes.filter(function(d) { return d.id === e.source; })[0],
                targetNode = jsonData.nodes.filter(function(d) { return d.id === e.target; })[0];
            // add edge, color, type, size and id to array
            edges.push({source: sourceNode, target: targetNode, color: e.color, edge_type: e.edge_type, size: e.size, id: e.id});
        });
        return edges;
    }

    /**
     * Select edges with type of arrow.
     *
     * @param edges: edges of graph
     * @return edgesTypeArrow: array, which contains edges of type arrow
     */
    function createArrowDict(edges){
        var edgesTypeArrow = [];
        edges.forEach(function(d){
            if(d.edge_type === 'arrow'){
                return edgesTypeArrow.push(d);
            }
        });
        return edgesTypeArrow;
    }

    /**
     * Create arrows for edges.
     *
     * @param svg
     * @param edgesTypeArrow
     * @return marker: arrow
     */
    function createArrows(svg, edgesTypeArrow) {
        return svg.append("defs").selectAll('marker').data(edgesTypeArrow)
            .enter().append("svg:marker")
            .attr({id: function(d) { return "marker_" + d.edge_type + d.id; },
                   refX: function(d){
                             if(d.target.label === ''){ return 6; }
                             if(d.target.label === ''){ return 6; }
                             else if(d.target.id === 'issue'){ return 10; }
                             else{ return 9; }},
                   refY: 0,
                   markerWidth: 10, markerHeight: 10,
                   viewBox: '0 -5 10 10',
                   orient: "auto",
                   fill: function(d) { return d.color; }
            })
            .append("svg:path")
            .attr("d", "M0,-3L7,0L0,3");
    }

    /**
     * Create links between nodes.
     *
     * @param svg
     * @param marker: arrow
     * @param edges
     * @return links
     */
    function createLinks(svg, edges, marker) {
        return svg.selectAll(".path")
            .data(edges)
            // svg lines
            .enter().append("line")
            .attr({class: "link",
                   id: function(d) { return 'link-' + d.id; }})
            .style("stroke", function(d) { return d.color; })
            // assign marker to line
            .attr("marker-end", function(d) { return "url(#marker_" + d.edge_type + d.id + ")"; });
    }

    /**
     * Create node as svg circle and enable drag functionality.
     *
     * @param svg
     * @param force
     * @param drag
     * @return nodes
     */
    function createNodes(svg, force, drag) {
        return svg.selectAll(".node")
            .data(force.nodes())
            .enter().append("g")
            .attr({class: "node",
                   id: function(d){
                       return 'node_' + d.id;}})
            .call(drag);
    }

    /**
     * Define properties for nodes.
     *
     * @param node
     * @return circle
     */
    function setNodeProperties(node){
        return node.append("circle")
            .attr({r: function(d){ return d.size; },
                   fill: function(d){ return d.color; },
                   id: function (d) { return 'circle-' + d.id; }
            });
    }

    /**
     * Wrap text.
     *
     * @param node
     * @return label
     */
    function createLabel(node){
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

    /**
     * Set properties for rect.
     *
     * @param rect: background of label
     */
    function setRectProperties(rect){
        rect.each(function (d) {
            var element = $("#label-" + d.id),
                width = element.width() + 24,
                height = element.height() + 10;
            if(d.size === 0){
                width = 0;
                height = 0;
            }
            d3.select(this)
            .attr({width: width, height: height,
                   x: -width/2, y: -height+36,
                   id: 'rect-' + d.id});
        });
    }

    /**
     * Create svg for legend.
     */
    function getLegendSvg() {
        d3.select('#graphViewLegendId').append("svg")
            .attr({width: 200, height: 200, id: "graph-legend-svg"});
        return d3.select("#graph-legend-svg").append("g")
            .attr({id: "graphLegend",
                   transform: "translate(10,20)"});
    }

    /**
     * Listen whether a node is clicked.
     *
     * @param circle
     * @param edges
     */
    function addListenerForNodes(circle, edges){
        var selectedCircleId;
        circle.on("click", function(d)
        {
            // distinguish between click and drag event
            if(d3.event.defaultPrevented) return;
            // show modal when node clicked twice
            if(d.id === selectedCircleId){
                showModal(d);
            }
            var circleId = this.id;
            showPartOfGraph(edges, circleId);
            selectedCircleId = d.id;
        });
    }

    /**
     * Create legend and update legend.
     */
    function createLegend(){
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

    /**
     * Create symbols for nodes.
     *
     * @param selection
     * @param legendLabelCircle: array with labels for circle
     * @param legendColorCircle: array with colors
     */
    function createNodeSymbols(selection, legendLabelCircle, legendColorCircle) {
        selection.selectAll(".circle")
        .data(legendLabelCircle)
        .enter().append("circle")
        .attr({fill: function (d,i) {return legendColorCircle[i];},
               r: function (d,i) {
                   if(i === 0) { return 8; }
                   else { return 6; }},
               cy: function (d,i) {return i*40;}});
    }

    /**
     * Create symbols for edges.
     *
     * @param selection
     * @param legendLabelRect: array with labels for rect
     * @param legendColorRect: array with colors
     */
    function createEdgeSymbols(selection, legendLabelRect, legendColorRect) {
        selection.selectAll(".rect")
        .data(legendLabelRect)
        .enter().append("rect")
        .attr({fill: function (d,i) {return legendColorRect[i];},
               width: 15, height: 5,
               x: -7, y: function (d,i) {return i*40+118;}});
    }

    /**
     * Create labels for symbols.
     *
     * @param selection
     * @param legendLabelCircle: array with labels for circle
     * @param legendLabelRect: array with labels for rect
     */
    function createLabelsForSymbols(selection, legendLabelCircle, legendLabelRect) {
        selection.selectAll(".text")
        .data(legendLabelCircle.concat(legendLabelRect))
        .enter().append("text")
        .text(function(d) {return d;})
        .attr({x: 20, y: function (d,i) {return i*40+5;}});
    }

    /**
     * Add listeners for buttons of sidebar.
     *
     * @param jsonData
     * @param label
     * @param rect
     * @param edges
     * @param force
     */
    function addListenersForSidebarButtons(jsonData, label, rect, edges, force){
        showDefaultView(jsonData);
        $('#show-labels').click(function() {showLabels(label, rect);});
        $('#hide-labels').click(function() {hideLabels(label, rect);});
        $('#show-positions').click(function() {showPositions();});
        $('#hide-positions').click(function() {hidePositions();});
        $('#show-my-statements').click(function() {showMyStatements(edges, force);});
        $('#hide-my-statements').click(function() {hideMyStatements(edges, force);});
        $('#show-supports-on-my-statements').click(function() {showSupportsOnMyStatements(edges, force);});
        $('#hide-supports-on-my-statements').click(function() {hideSupportsOnMyStatements(edges, force);});
        $('#show-attacks-on-my-statements').click(function() {showAttacksOnMyStatements(edges, force);});
        $('#hide-attacks-on-my-statements').click(function() {hideAttacksOnMyStatements(edges, force);});
    }

    /**
     * Restore initial state of graph.
     *
     * @param jsonData
     */
    function showDefaultView (jsonData){
        $('#start-view').click(function() {
            new DiscussionGraph().setDefaultViewParams(true, jsonData, s);
        });
    }

    /**
     * Show all labels of graph.
     *
     * @param label
     * @param rect
     */
    function showLabels(label, rect){
        isContentVisible = true;
        label.style("display", "inline");
        rect.style("display", "inline");
        $('#show-labels').hide();
        $('#hide-labels').show();
        // also show content of positions
        $('#show-positions').hide();
        $('#hide-positions').show();
    }

    /**
     * Hide all labels of graph.
     *
     * @param label
     * @param rect
     */
    function hideLabels(label, rect) {
        isContentVisible = false;
        label.style("display", "none");
        rect.style("display", "none");
        $('#show-labels').show();
        $('#hide-labels').hide();
        if (isPositionVisible){
            setDisplayStyleOfNodes('inline');
        } else {
            $('#show-positions').show();
            $('#hide-positions').hide();
        }
    }

    /**
     * Show labels for positions.
     */
    function showPositions() {
        isPositionVisible = true;
        // select positions
        setDisplayStyleOfNodes('inline');
        $('#show-positions').hide();
        $('#hide-positions').show();
    }

    /**
     * Hide labels for positions.
     */
    function hidePositions() {
        isPositionVisible = false;
        // select positions
        setDisplayStyleOfNodes('none');
        $('#show-positions').show();
        $('#hide-positions').hide();
    }

    /**
     * Show all statements, which the current user has created.
     *
     * @param edges
     * @param force
     */
    function showMyStatements(edges, force){
        isStatementVisible = true;
        isSupportVisible = true;
        isAttackVisible = true;

        // graying all elements of graph
        edges.forEach(function(d){
            grayingElements(d);
        });
        // highlight incoming and outgoing edges of all statements, which the current user has created
        force.nodes().forEach(function(d){
            if(d.author.name === $('#header_nickname')[0].innerText){
                d3.select('#circle-' + d.id).attr({fill: d.color, stroke: 'black'});
                showPartOfGraph(edges, d.id);
            }
        });

        $('#show-my-statements').hide();
        $('#hide-my-statements').show();
        // also show supports and attacks on statements
        $('#show-supports-on-my-statements').hide();
        $('#hide-supports-on-my-statements').show();
        $('#show-attacks-on-my-statements').hide();
        $('#hide-attacks-on-my-statements').show();
    }

    /**
     * Hide all statements, which the current user has created.
     *
     * @param edges
     * @param force
     */
    function hideMyStatements(edges, force){
        isStatementVisible = false;
        if(isSupportVisible){
            $('#show-supports-on-my-statements').show();
            $('#hide-supports-on-my-statements').hide();
            isSupportVisible = false;
        }
        if(isAttackVisible){
            $('#show-attacks-on-my-statements').show();
            $('#hide-attacks-on-my-statements').hide();
            isAttackVisible = false;
        }

        // highlight all elements of graph
        edges.forEach(function(d){
            highlightElements(d);
        });
        // delete border of nodes
        force.nodes().forEach(function(d) {
            d3.select('#circle-' + d.id).attr('stroke', 'none');
        });

        $('#show-my-statements').show();
        $('#hide-my-statements').hide();
    }

    /**
     * Show all supports on the statements, which the current user has created.
     *
     * @param edges
     * @param force
     */
    function showSupportsOnMyStatements(edges, force){
        isSupportVisible = true;

        // if attacks on statements of current user are visible, highlight additionally the supports
        if(!isAttackVisible) {
            // graying all elements of graph
            edges.forEach(function (d) {
                grayingElements(d);
            });
        }
        force.nodes().forEach(function(d){
            if(d.author.name === $('#header_nickname')[0].innerText){
                d3.select('#circle-' + d.id).attr({fill: d.color, stroke: 'black'});
                showPartOfGraph(edges, d.id);
            }
        });
        $('#show-supports-on-my-statements').hide();
        $('#hide-supports-on-my-statements').show();
    }

    /**
     * Hide all supports on the statements, which the current user has created.
     *
     * @param edges
     * @param force
     */
    function hideSupportsOnMyStatements(edges, force){
        isSupportVisible = false;

        // if attacks are not visible, show the default view of the graph
        // else let them visible
        if(!isAttackVisible){
            // highlight all elements of graph
            edges.forEach(function(d){
                highlightElements(d);
            });
            // delete border of nodes
            force.nodes().forEach(function(d) {
                d3.select('#circle-' + d.id).attr('stroke', 'none');
            });
        }
        else{
            if(isStatementVisible){
                $('#show-my-statements').show();
                $('#hide-my-statements').hide();
                isStatementVisible = false;
            }
            showAttacksOnMyStatements(edges, force);
        }
        $('#show-supports-on-my-statements').show();
        $('#hide-supports-on-my-statements').hide();
    }

    /**
     * Show all attacks on the statements, which the current user has created.
     *
     * @param edges
     * @param force
     */
    function showAttacksOnMyStatements(edges, force){
        isAttackVisible = true;

        // if supports on statements of current user are visible, highlight additionally the attacks
        if(!isSupportVisible) {
            // graying all elements of graph
            edges.forEach(function (d) {
                grayingElements(d);
            });
        }
        force.nodes().forEach(function(d){
            if(d.author.name === $('#header_nickname')[0].innerText){
                d3.select('#circle-' + d.id).attr({fill: d.color, stroke: 'black'});
                showPartOfGraph(edges, d.id);
            }
        });
        $('#show-attacks-on-my-statements').hide();
        $('#hide-attacks-on-my-statements').show();
    }

    /**
     * Hide all attacks on the statements, which the current user has created.
     *
     * @param edges
     * @param force
     */
    function hideAttacksOnMyStatements(edges, force){
        isAttackVisible = false;

        if(!isSupportVisible){
            // highlight all elements of graph
            edges.forEach(function(d){
                highlightElements(d);
            });
            // delete border of nodes
            force.nodes().forEach(function(d) {
                d3.select('#circle-' + d.id).attr('stroke', 'none');
            });
        }
        else{
            if(isStatementVisible){
                $('#show-my-statements').show();
                $('#hide-my-statements').hide();
                isStatementVisible = false;
            }
            showSupportsOnMyStatements(edges, force);
        }
        $('#show-attacks-on-my-statements').show();
        $('#hide-attacks-on-my-statements').hide();
    }

    /**
     * Set display style of nodes.
     *
     * @param style
     */
    function setDisplayStyleOfNodes(style) {
        // select edges with position as source and issue as target
        d3.selectAll(".node").each(function(d) {
            d3.selectAll(".link").each(function(e) {
                if (e.source.id === d.id && e.target.id === 'issue') {
                    // set display style of positions
                    d3.select('#label-' + d.id).style("display", style);
                    d3.select("#rect-" + d.id).style("display", style);
                }
            });
        });
    }

    /**
     * Hide nodes on mouse event.
     *
     * @param circle
     */
    function moveToBack(circle){
        circle.on("mouseover", function(d) {
            d3.selectAll('.node')
            .sort(function(a, b) {
                if (a.id === d.id) {
                    return 1;
                }
                else if (b.id === d.id) {
                    return -1;
                }
                return 0;
            })
        });
    }

    /**
     * Show modal.
     */
    function showModal(d){
        var popup = $('#popup-jump-graph');
        if(d.id != 'issue'){
            popup.modal('show');
            var splitted = d.id.split('_'),
                uid = splitted[splitted.length - 1];
            new AjaxGraphHandler().getJumpDataForGraph(uid);
        }
    }

    /**
     * Select uid.
     */
    function selectUid(id) {
        var splitted = id.split('-');
        return splitted[splitted.length - 1];
    }

    /**
     * Highlight incoming and outgoing edges of selected node.
     *
     * @param edges: all edges of graph
     * @param circleId: id of selected node
     */
    function showPartOfGraph(edges, circleId) {
        // edges with selected circle as source or as target
        var edgesCircleId = [];
        // select all incoming and outgoing edges of selected circle
        edges.forEach(function(d){
            var circleUid = selectUid(circleId);
            if(isSupportVisible && selectUid(d.target.id) === circleUid && d.color === '#64DD17'){
                edgesCircleId.push(d);
            }
            else if(isAttackVisible && selectUid(d.target.id) === circleUid && d.color === '#F44336'){
                edgesCircleId.push(d);
            }
            else if((selectUid(d.source.id) === circleUid || selectUid(d.target.id) === circleUid)
                      && ((!isAttackVisible && !isSupportVisible) || isStatementVisible)){
                edgesCircleId.push(d);
            }
        });

        // if isMyStatementsClicked is false gray all elements at each function call,
        // else the graph is colored once gray
        if(!isStatementVisible && !isSupportVisible && !isAttackVisible){
            edges.forEach(function(d){
                grayingElements(d);
            });
        }
        edgesCircleId.forEach(function (d) {
            highlightElements(d);
        });

        highlightElementsVirtualNodes(edges, edgesCircleId);
    }

    /**
     * Highlight incoming and outgoing edges of virtual node.
     *
     * @param edges
     * @param edgesVirtualNodes
     */
    function highlightElementsVirtualNodes(edges, edgesVirtualNodes) {
        // array with edges from last loop pass
        var edgesVirtualNodesLast = edgesVirtualNodes;
        do {
            // virtual nodes
            var virtualNodes = createVirtualNodesArray(edgesVirtualNodes);
            // edges with a virtual node as source or as target
            edgesVirtualNodes = createVirtualNodesEdgesArray(edges, virtualNodes);
            var isVirtualNodeLeft = testVirtualNodesLeft(edgesVirtualNodes, edgesVirtualNodesLast);
            // save array with edges for next loop pass
            edgesVirtualNodesLast = edgesVirtualNodes;

        }
        while(isVirtualNodeLeft);
    }

    /**
     * Create array with virtual nodes.
     *
     * @param edgesVirtualNodes
     * @return Array
     */
    function createVirtualNodesArray(edgesVirtualNodes) {
        var virtualNodes = [];
        edgesVirtualNodes.forEach(function (d) {
            if (d.source.label === '') {
                virtualNodes.push(d.source);
            }
            if (d.target.label === '') {
                virtualNodes.push(d.target);
            }
        });
        return virtualNodes;
    }

    /**
     * Create array which contains edges with virtual node as source or as target.
     *
     * @param edges
     * @param virtualNodes
     * @return Array
     */
    function createVirtualNodesEdgesArray(edges, virtualNodes) {
        var edgesVirtualNodes = [];
        edges.forEach(function (d) {
            virtualNodes.forEach(function (e) {
                if (d.source.id === e.id || d.target.id === e.id) {
                    // if button supports or attacks is clicked do not highlight supports or attacks on premise groups
                    if(!((isSupportVisible || isAttackVisible) && (d.edge_type === 'arrow') && !isStatementVisible)){
                        edgesVirtualNodes.push(d);
                    }
                }
            });
        });
        edgesVirtualNodes.forEach(function (d) {
            highlightElements(d);
        });
        return edgesVirtualNodes;
    }

    /**
     * Test whether virtual nodes are left, where not all incoming and outgoing edges are highlighted.
     *
     * @param edgesVirtualNodes
     * @param edgesVirtualNodesLast
     * @return boolean
     */
    function testVirtualNodesLeft(edgesVirtualNodes, edgesVirtualNodesLast) {
        var isVirtualNodeLeft = false;
        edgesVirtualNodes.forEach(function (d) {
            if (d.source.label === '') {
                isVirtualNodeLeft = true;
                // if the edge is already highlighted terminate loop
                edgesVirtualNodesLast.forEach(function (e) {
                    if(d.id === e.id){
                        isVirtualNodeLeft = false;
                    }
                });
            }
        });
        return isVirtualNodeLeft;
    }

    /**
     * Highlighting components of graph.
     *
     * @param edge: edge that should be highlighted
     */
    function highlightElements(edge){
        // edges
        d3.select('#link-' + edge.id).style('stroke', edge.color);
        // nodes
        d3.select('#circle-' + edge.source.id).attr('fill', edge.source.color);
        d3.select('#circle-' + edge.target.id).attr('fill', edge.target.color);
        // arrows
        d3.select("#marker_" + edge.edge_type + edge.id).attr('fill', edge.color);
    }

    /**
     * Graying components of graph.
     *
     * @param edge: edge that should be gray
     */
    function grayingElements(edge) {
        // edges
        d3.select('#link-' + edge.id).style('stroke', '#E0E0E0');
        // nodes
        d3.select('#circle-' + edge.source.id).attr('fill', '#E0E0E0');
        d3.select('#circle-' + edge.target.id).attr('fill', '#E0E0E0');
        // arrows
        d3.select("#marker_" + edge.edge_type + edge.id).attr('fill', '#E0E0E0');
    }
}