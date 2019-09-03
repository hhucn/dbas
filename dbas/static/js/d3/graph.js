function DiscussionGraph(box_sizes_for_rescaling, is_partial_graph_mode) {
    'use strict';
    var isPartialGraphMode = is_partial_graph_mode;
    /**
     * isVisible.content: whether all graph labels are shown (implies isVisible.statements and isVisible.positions)
     * isVisible.statements: whether statement labels are shown
     * isVisible.positions: whether position labels are shown
     */
    var isVisible;
    var colors;
    var rescaleGraph;
    var box_sizes = box_sizes_for_rescaling; // needed for rescaling
    var force;
    var size;
    var change;

    // edges
    var edges;
    var link;
    var rect;
    var label;

    // nodes
    var node;
    var circle;
    var selectedCircleId;
    var circleIds;
    var currentColorOfCircle;

    /**
     * Displays a graph of current discussion
     */
    this.showGraph = function (override_cases) {
        initialDicts();
        var url = window.location.href.split('?')['0'];
        url = url.split('#')[0];
        var is_argument = null;
        var uid = null;
        isPartialGraphMode = override_cases;
        if (!override_cases) {
            var tmp = url.split('/');
            var keys = {
                'attitude': false,
                'justify': false,
                'reaction': true,
                'support': true,
                'finish': true,
                'jump': true
            };
            $.each(keys, function (key, bool) {
                if (url.indexOf(key) !== -1) {
                    uid = tmp[tmp.indexOf(key) + 1];
                    is_argument = bool;
                    isPartialGraphMode = true;
                    return false;
                }
                return true;
            });
        }
        new AjaxGraphHandler().getDiscussionGraphData(this, uid, is_argument, isPartialGraphMode);
        return true;
    };

    /**
     * Initialize global dictionaries.
     */
    function initialDicts() {
        setIsVisibleDict();
        setColorsDict();
        setRescaleGraphDict();
        setSizeDict();
    }

    /**
     * Initialize dict "isVisible".
     */
    function setIsVisibleDict() {
        isVisible = {
            'position': false,
            'statements': false,
            'content': false,
            'my_statements': false,
            'support': false,
            'attack': false,
            'defaultView': false
        };
    }

    /**
     * Initialize dict "colors".
     */
    function setColorsDict() {
        var c = new Colors();
        colors = {
            'light_grey': c.get_grey()[300],
            'grey': c.get_blueGrey()[600],
            'yellow': c.get_amber()[500],
            'red': c.get_red()[500],
            'green': c.get_green()[300],
            'blue': c.get_blue()[600],
            'black': '#000000',
            'dark_grey': c.get_grey()[800]
        };
    }

    /**
     * Initialize dict "rescaleGraph".
     */
    function setRescaleGraphDict() {
        rescaleGraph = {
            'font_size': 14, // needed for rescaling
            'line_height': 1.5, // needed for rescaling
            'node_id_prefix': 'node_', // needed for rescaling
            'old_scale': 1.0, // needed for rescaling
            'zoom_scale': 0
        };
    }

    /**
     * Initialize dict "size".
     */
    function setSizeDict() {
        size = {
            'statement': 6, // base node size of an statement
            'node_factor': 10, // additional size for the doj, which is in [0,1]
            'node': 6,
            'issue': 8,
            'rel_node_factor': {},
            'edge': 90,
            'edge_virtual_node': 45
        };
    }

    function setSlider() {
        var slider = $('#graph-slider');
        var start_date_ms = slider.data('start-ms');
        slider.slider({
            formatter: function (value) {
                var add_ms = value * 3600 * 1000;
                var cval = start_date_ms + add_ms;
                var date = new Date(cval);
                return date.toLocaleString();
            }
        }).on('slideStop', function (value) {
            resetButtons();
            if (typeof start_date_ms !== 'undefined') {
                var add_ms = value.value * 3600 * 1000;
                add_ms += value.value === 0 ? 1800 : 0;
                showNodesUntilMoment(start_date_ms + add_ms);
            }
        });
        var w = $('#graph-view-container-space').width() - 24;
        w -= slider.parent().width();
        w += slider.parent().find('.slider').width();
        slider.prev().css('width', w);
    }

    /**
     * Callback if ajax request was successful.
     *
     * @param data
     * @param request_for_complete
     */
    this.callbackIfDoneForDiscussionGraph = function (data, request_for_complete) {
        if (data.error.length !== 0) {
            setGlobalErrorHandler('Ohh!', data.error);
            new GuiHandler().setDisplayStyleAsDiscussion();
            return;
        }
        new DiscussionGraph(box_sizes, isPartialGraphMode).setDefaultViewParams(true, data, null, request_for_complete);

    };

    /**
     * If ajax request was successful show modal with data for jump into discussion.
     *
     * @param data
     */
    this.callbackIfDoneForGetJumpDataForGraph = function (data) {
        var popup = $('#popup-jump-graph');
        popup.find('div.modal-body div').empty();
        var list = createContentOfModalBody(data);
        popup.find('div.modal-body div').append(list);

        // jump to url
        popup.find('input').click(function () {
            window.location = $(this).attr('value');
        });

        // add hover effects
        new GuiHandler().hoverInputListOf(popup.find('div.modal-body div'));
    };

    /**
     * Create content for modal to jump into discussion.
     *
     * @param jsonData
     */
    function createContentOfModalBody(jsonData) {
        var label, input, element, counter = 0;
        var list = $('<ul>');

        $.each(jsonData.arguments, function (key, value) {
            input = $('<input>').attr('type', 'radio').attr('value', value.url).attr('id', 'jump_' + counter);
            label = $('<label>').html(value.text).attr('for', 'jump_' + counter);
            element = $('<li>').append(input).append(label);
            list.append(element);
            counter += 1;
        });
        return list;
    }

    /**
     * Set parameters for default view of graph.
     *
     * @param startD3
     * @param jsonData
     * @param d3
     * @param request_for_complete
     */
    this.setDefaultViewParams = function (startD3, jsonData, d3, request_for_complete) {
        var dg = new DiscussionGraph(box_sizes, isPartialGraphMode);
        $('#global-view').attr('data-global-view-loaded', jsonData.type === 'complete');
        dg.setButtonDefaultSettings(jsonData, request_for_complete);
        initialDicts();
        var container = $('#' + graphViewContainerSpaceId);
        container.empty();

        if (startD3) {
            if (!this.getD3Graph(jsonData)) {
                dg.setDefaultViewParams(false, null, d3, request_for_complete);
            }
        } else {
            container.empty();
        }
        $("html, body").animate({scrollTop: $(document).height()}, "slow");
    };

    /**
     * Set default settings of buttons in sidebar.
     *
     * @param jsonData
     * @param request_for_complete
     */
    this.setButtonDefaultSettings = function (jsonData, request_for_complete) {
        $('#graph-view-container').find('.sidebar').find('li').each(function () {
            $(this).removeClass('hidden');
        });

        if ((request_for_complete || typeof request_for_complete === 'undefined') && !isPartialGraphMode) {
            $('#global-view').hide();
        } else {
            $('#global-view').show();
        }

        // show or hide my path
        $('#hide-my-path').hide();
        if (jsonData.path.length === 0) {
            $('#show-my-path').addClass('hidden');
        } else {
            $('#show-my-path').show();
        }
    };

    /**
     * Create a graph.
     *
     * @param jsonData
     */
    this.getD3Graph = function (jsonData) {
        var container = $('#' + graphViewContainerSpaceId);
        container.empty();
        size.rel_node_factor = {};

        var width = container.width();
        var height = container.outerHeight();

        var svg = getGraphSvg(width, height);
        force = getForce(jsonData, width, height);

        // zoom and pan
        var zoom = d3.behavior.zoom();
        zoomAndPan(zoom);
        var drag = enableDrag();

        // resize
        resizeGraph(container);

        setEdges(jsonData, svg);

        // node
        node = createNodes(svg, drag);
        circle = setNodeProperties().attr('class', 'circle');

        setTooltip();

        setLegend();

        setSlider();

        // buttons of sidebar
        addListenersForSidebarButtons(jsonData, zoom);
        // add listener to show/hide tooltip on mouse over
        addListenerForTooltip();

        force.start();

        // highlight nodes and edges
        addListenerForNodes();

        return true;
    };

    /**
     * Set edges of graph.
     *
     * @param jsonData
     * @param svg
     */
    function setEdges(jsonData, svg) {
        // edge
        edges = createEdgeDict(jsonData);
        setNodeColorsForData(jsonData);
        setPositionOfGraphElements(jsonData);
        var edgesTypeArrow = createArrowDict();
        var marker = createArrows(svg, edgesTypeArrow);
        link = createLinks(svg, marker);
    }

    /**
     * Create tooltip.
     */
    function setTooltip() {
        // tooltip
        // rect as background of label
        var tooltip = node.append('g');
        rect = tooltip.append('rect').attr('class', 'labelBox');
        label = createLabel(tooltip);

        // reorder the elements so that the tooltips appear in front of the nodes
        tooltip.order();
        setRectProperties();
    }

    /**
     * Create legend.
     */
    function setLegend() {
        var container = $('#' + graphViewContainerSpaceId);

        // legend
        new GraphLegend(colors).create(d3);
        // call updated legend
        var legend = d3.svg.legend();
        // create div for legend
        container.append("<div id = 'graphViewLegendId'></div>");
        getLegendSvg().call(legend);

    }

    /**
     * Set position of graph elements.
     *
     * @param jsonData
     */
    function setPositionOfGraphElements(jsonData) {
        // create arrays of links, nodes and move layout forward one step
        force.links(edges).nodes(jsonData.nodes).on("tick", forceTick);

        // update force layout calculations
        function forceTick() {
            // update position of nodes
            setPositionOfCircles(jsonData);
            // update position of edges
            setPositionOfLinks();
            // update position of rect
            rect.attr("transform", function (d) {
                return "translate(" + d.x + "," + (d.y - 50) + ")";
            });
            // update position of label
            label.attr("transform", function (d) {
                return "translate(" + d.x + "," + (d.y - 50) + ")";
            });
        }
    }

    /**
     * Calculate position of circles.
     *
     * @param jsonData
     */
    function setPositionOfCircles(jsonData) {
        circle.attr({
            cx: function (d) {
                return getCirclePosition(jsonData, d, 'x');
            },
            cy: function (d) {
                return getCirclePosition(jsonData, d, 'y');
            }
        });
    }

    /**
     * Calculate position of links.
     */
    function setPositionOfLinks() {
        link.attr({
            x1: function (d) {
                return d3.select('#circle-' + d.source.id).attr('cx');
            },
            y1: function (d) {
                return d3.select('#circle-' + d.source.id).attr('cy');
            },
            x2: function (d) {
                return d3.select('#circle-' + d.target.id).attr('cx');
            },
            y2: function (d) {
                return d3.select('#circle-' + d.target.id).attr('cy');
            }
        });
    }

    /**
     * Get position of nodes.
     *
     * @param jsonData
     * @param d: circle
     * @param coordinate
     */
    function getCirclePosition(jsonData, d, coordinate) {
        // virtual nodes
        if ((d.label === "") && (d.edge_source.length === 1)) {
            var edge_source = jsonData.nodes.filter(function (node) {
                return node.id === d.edge_source[0];
            })[0];
            var edge_target = jsonData.nodes.filter(function (node) {
                return node.id === d.edge_target;
            })[0];
            if (coordinate === 'x') {
                return (edge_source.x + edge_target.x) / 2;
            }
            return (edge_source.y + edge_target.y) / 2;
        }

        if (coordinate === 'x') {
            return d.x;
        }
        return d.y;
    }

    /**
     * Create svg-element.
     *
     * @param width: width of container, which contains graph
     * @param height: height of container
     * @return scalable vector graphic
     */
    function getGraphSvg(width, height) {
        return d3.select('#' + graphViewContainerSpaceId).append("svg")
            .attr({width: width, height: height, id: "graph-svg"})
            .append('g')
            .attr("class", "zoom");
    }

    /**
     * Create force-directed network diagram and define properties.
     *
     * @param jsonData
     * @param width: width of container, which contains graph
     * @param height: height of container
     * @return force layout
     */
    function getForce(jsonData, width, height) {
        // set chargeFactor dependent on number of nodes
        var chargeFactor = jsonData.nodes.length <= 10 ? 1200 : 700;
        return d3.layout.force()
            .size([width, height])
            // nodes push each other away
            .charge(-chargeFactor)
            .gravity(0.2)
            .linkDistance(function (d) {
                if ((d.source.label === '') || ((d.target.label === '') && (d.edge_type === ''))) {
                    return size.edge_virtual_node;
                }
                return size.edge;
            });
    }

    /**
     * Enable zoom and pan functionality on graph.
     */
    function zoomAndPan(zoom) {
        zoom.on("zoom", redraw).scaleExtent([0.5, 5]);

        d3.select("#graph-svg").call(zoom).on("dblclick.zoom", null);

        // if default view button is clicked redraw graph once
        if (isVisible.defaultView) {
            redraw();
        }

        function redraw() {
            var change_scale = true;
            if (isVisible.defaultView) {
                rescaleGraph.zoom_scale = 1;
                isVisible.defaultView = false;
            } else {
                rescaleGraph.zoom_scale = zoom.scale();
                change_scale = Math.abs(rescaleGraph.old_scale - rescaleGraph.zoom_scale) > 0.02;
            }

            rescaleGraph.old_scale = rescaleGraph.zoom_scale;

            d3.selectAll("g.zoom").attr("transform", "translate(" + zoom.translate() + ")" + " scale(" + rescaleGraph.zoom_scale + ")");

            if (change_scale) {
                var svg = $('#graph-svg');
                // resizing of font size, line height and the complete rectangle
                svg.find('.node').each(function () {
                    var id = $(this).attr('id').replace(rescaleGraph.node_id_prefix, '');
                    if (id.indexOf('statement') !== -1 || id.indexOf('issue') !== -1) {
                        $('#label-' + id).css({
                            'font-size': rescaleGraph.font_size / rescaleGraph.zoom_scale + 'px',
                            'line-height': rescaleGraph.line_height / rescaleGraph.zoom_scale
                        });
                        var width = box_sizes[id].width / rescaleGraph.zoom_scale;
                        var height = box_sizes[id].height / rescaleGraph.zoom_scale;
                        var pos = calculateRectPos(box_sizes[id].width, box_sizes[id].height);
                        $('#rect-' + id).attr({
                            'width': width,
                            'height': height,
                            'x': pos[0] / rescaleGraph.zoom_scale,
                            'y': pos[1] / rescaleGraph.zoom_scale
                        });
                    }
                });

                // dirty hack to accept new line height and label position
                svg.css({'line-height': '1.0'});
                setTimeout(function () {
                    $('#graph-svg').css({'line-height': '1.5'});
                    $('#' + graphViewContainerSpaceId).find('.node').each(function () {
                        var id = $(this).attr('id').replace(rescaleGraph.node_id_prefix, '');
                        var label = $('#label-' + id);
                        label.attr({
                            'y': -label.height() / rescaleGraph.zoom_scale + 45 / rescaleGraph.zoom_scale
                        });
                    });
                }, 300);
            }
        }
    }

    /**
     * Enable drag functionality, because pan functionality overrides drag.
     *
     * @return drag functionality
     */
    function enableDrag() {
        return force.drag()
            .on("dragstart", function () {
                d3.event.sourceEvent.stopPropagation();
            });
    }

    /**
     * Resize graph on window event.
     *
     * @param container
     */
    function resizeGraph(container) {
        d3.select(window).on("resize", resize);

        function resize() {
            var graphSvg = $('#graph-svg');
            graphSvg.width(container.width());
            // height of space between header and bottom of container
            graphSvg.height(container.outerHeight() - $('#graph-sidebar').height());
            force.size([container.width(), container.outerHeight()]).resume();
        }
    }

    /**
     * Sets the color in the json Data
     *
     * @param jsonData
     */
    function setNodeColorsForData(jsonData) {
        jsonData.nodes.forEach(function (e) {
            if (e.type === 'position') {
                e.color = colors.blue;
            } else if (e.type === 'statement') {
                e.color = colors.yellow;
            } else if (e.type === 'issue') {
                e.color = colors.grey;
            } else {
                e.color = colors.black;
            }
        });
    }

    /**
     * Create dictionary for edges.
     *
     * @param jsonData: dict with data for nodes and edges
     * @return Array array, which contains dicts for edges
     */
    function createEdgeDict(jsonData) {
        var edges = [];
        jsonData.edges.forEach(function (e) {
            // get source and target nodes
            var sourceNode = jsonData.nodes.filter(function (d) {
                    return d.id === e.source;
                })[0],
                targetNode = jsonData.nodes.filter(function (d) {
                    return d.id === e.target;
                })[0];
            // add edge, color, type, size and id to array
            edges.push({
                source: sourceNode,
                target: targetNode,
                color: colors[e.color],
                edge_type: e.edge_type,
                id: e.id
            });
        });
        return edges;
    }

    /**
     * Select edges with type of arrow.
     *
     * @return Array array, which contains edges of type arrow
     */
    function createArrowDict() {
        var edgesTypeArrow = [];
        edges.forEach(function (d) {
            if (d.edge_type === 'arrow') {
                edgesTypeArrow.push(d);
                return edgesTypeArrow;
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
            .attr({
                id: function (d) {
                    return "marker_" + d.edge_type + d.id;
                },
                refX: function (d) {
                    if (d.is_undercut === true) {
                        return 6;
                    }
                    return 6 + calculateNodeSize(d.target) / 2;
                },
                refY: 0,
                markerWidth: 10,
                markerHeight: 10,
                viewBox: '0 -5 10 10',
                orient: "auto",
                fill: function (d) {
                    return d.color;
                }
            })
            .append("svg:path")
            .attr("d", "M0,-3L7,0L0,3");
    }

    /**
     * Create links between nodes.
     *
     * @param svg
     * @param marker: arrow
     * @return links
     */
    function createLinks(svg, marker) {
        return svg.selectAll(".path")
            .data(edges)
            // svg lines
            .enter().append("line")
            .attr({
                'class': "link",
                'id': function (d) {
                    return 'link-' + d.id;
                }
            })
            .style("stroke", function (d) {
                return d.color;
            })
            // assign marker to line
            .attr("marker-end", function (d) {
                return "url(#marker_" + d.edge_type + d.id + ")";
            });
    }

    /**
     * Create node as svg circle and enable drag functionality.
     *
     * @param svg
     * @param drag
     * @return nodes
     */
    function createNodes(svg, drag) {
        return svg.selectAll(".node")
            .data(force.nodes())
            .enter().append("g")
            .attr({
                'class': "node",
                'id': function (d) {
                    return rescaleGraph.node_id_prefix + d.id;
                }
            })
            .call(drag);
    }

    /**
     * Define properties for nodes.
     *
     * @return circle
     */
    function setNodeProperties() {
        return node.append("circle")
            .attr({
                'r': function (d) {
                    return calculateNodeSize(d);
                },
                'fill': function (d) {
                    return d.color;
                },
                'id': function (d) {
                    return 'circle-' + d.id;
                }
            });
    }

    /**
     * Calculates the node size in respect to the DOJ
     *
     * @param node
     * @returns {*}
     */
    function calculateNodeSize(node) {
        if (node.id.indexOf('statement_') !== -1) {
            var id = node.id.replace('statement_', '');
            if (id in size.rel_node_factor) {
                return size.node + size.node_factor * size.rel_node_factor[id];
            } else {
                return size.node;
            }
        }
        if (node.id.indexOf('argument_') !== -1) {
            return 0;
        }
        return size.issue;
    }

    /**
     * Wrap text.
     *
     * @param node
     * @return label
     */
    function createLabel(node) {
        return node.append("text").each(function (d) {
            var text = $("<div>").html(d.label).text();
            var node_text = text.split(" ");
            for (var i = 0; i < node_text.length; i++) {
                var attr = {};
                if (i % 4 === 0) {
                    attr = {'dy': '1.2em', 'x': '0', 'text-anchor': "middle"};
                }
                d3.select(this).append("tspan")
                    .text(' ' + node_text[i])
                    .attr(attr);
            }
            // set position of label
            var height = $("#label-" + d.id).length > 0 ? 45 - $("#label-" + d.id).height() : -20;
            d3.select(this).attr({'id': 'label-' + d.id, 'y': height});
        });
    }

    /**
     * Set properties for rect.
     */
    function setRectProperties() {
        rect.each(function (d) {
            var width = 0;
            var height = 0;
            var pos = calculateRectPos(width, height);

            d3.select(this).attr({
                'width': width,
                'height': height,
                'x': pos[0],
                'y': pos[1],
                'id': 'rect-' + d.id
            });

            if (d.id.indexOf('statement') !== -1 || d.id.indexOf('issue') !== -1) {
                box_sizes[d.id] = {'width': width, 'height': height};
            }
        });
    }

    /**
     * Calculate the rectangle position depending on the rectangle width and height
     *
     * @param width int
     * @param height int
     * @returns {*[]} [x, y]
     */
    function calculateRectPos(width, height) {
        return [-width / 2, -height + 36];
    }

    /**
     * Create svg for legend.
     */
    function getLegendSvg() {
        d3.select('#graphViewLegendId').append("svg")
            .attr({
                'width': 200,
                'height': 200,
                'id': "graph-legend-svg"
            });
        return d3.select("#graph-legend-svg").append("g")
            .attr({
                'id': "graphLegend",
                'transform': "translate(10,20)"
            });
    }

    /**
     * Listen whether a node is clicked.
     */
    function addListenerForNodes() {
        circle.on("click", function (d) {
            // distinguish between click and drag event
            if (d3.event.defaultPrevented) {
                return;
            }
            var circleId = this.id;
            showArgumentsOfIdInGraph(circleId);
            selectedCircleId = d.id;
        });
        circle.on("dblclick", function (d) {
            // distinguish between click and drag event
            if (d3.event.defaultPrevented) {
                return;
            }
            // show modal when node clicked twice
            showModal(d);
            var circleId = this.id;
            showArgumentsOfIdInGraph(circleId);
            selectedCircleId = d.id;
        });
    }

    /**
     * Add listeners for buttons of sidebar.
     *
     * @param jsonData
     * @param zoom
     */
    function addListenersForSidebarButtons(jsonData, zoom) {
        $('#default-view').off('click').click(function () {
            resetSlider();
            if ($('#global-view').attr('data-global-view-loaded') === 'true' && $('#global-view:hidden').length === 0) {
                new DiscussionGraph(box_sizes, isPartialGraphMode).showGraph(false);
            } else {
                showDefaultView(jsonData, zoom);
            }
        });
        $('#global-view').off('click').click(function () {
            if ($(this).attr('data-global-view-loaded') === 'true') {
                showDefaultView(jsonData, zoom);
            } else {
                new DiscussionGraph(box_sizes, isPartialGraphMode).showGraph(true);
            }
        });

        var mapper = {
            'labels': [showLabels, hideLabels],
            'positions': [showPositions, hidePositions],
            'statements': [showStatements, hideStatements],
            'my-statements': [showMyStatements, hideMyStatements],
            'supports-on-my-statements': [showSupportsOnMyStatements, hideSupportsOnMyStatements],
            'attacks-on-my-statements': [showAttacksOnMyStatements, hideAttacksOnMyStatements]
        };

        // get all buttons in the sidebar
        $('#graph-sidebar').find('li').each(function (index, element) {
            var id = $(element).attr('id');
            // check if the button is mentioned in mapper array
            if (id in mapper) {
                $('#' + id).off('click').click(function () {
                    if ($(this).hasClass('reset-slider')) {
                        resetSlider();
                    }
                    if ($(this).find('i').attr('class') === "fa fa-square-o") {
                        $(this).find('i').removeClass().addClass("fa fa-check-square-o");
                        mapper[id][0]();
                    } else {
                        $(this).find('i').removeClass().addClass("fa fa-square-o");
                        mapper[id][1]();
                    }
                });
            }
        });

        $('#show-my-path').click(function () {
            showPath(jsonData);
        });

        $('#hide-my-path').click(function () {
            hidePath();
        });
    }

    /**
     * Restore initial state of graph.
     *
     * @param jsonData
     * @param zoom
     */
    function showDefaultView(jsonData, zoom) {
        isVisible.defaultView = true;

        // reset buttons
        new DiscussionGraph(box_sizes, isPartialGraphMode).setButtonDefaultSettings(jsonData);

        // set position of graph and set scale
        d3.selectAll("g.zoom").attr("transform", "translate(" + 0 + ")" + " scale(" + 1 + ")");

        // stop zoom event
        zoom.on("zoom", null);

        // create new zoom event listener
        var zoomDefaultView = d3.behavior.zoom();
        zoomAndPan(zoomDefaultView);

        resetButtons();
    }

    /**
     * Reset graph if button default view is clicked.
     */
    function resetButtons() {
        isVisible.position = true;
        isVisible.content = true;
        isVisible.support = true;
        isVisible.attack = true;

        hideLabels();
        hidePositions();
        hidePath();
        hideMyStatements();
        hideSupportsOnMyStatements();
        hideAttacksOnMyStatements();
    }

    function resetSlider() {
        var slider = $('#graph-slider');
        slider.slider('setValue', slider.data('slider-max'));
    }

    /**
     * Show all labels of graph.
     */
    function showLabels() {
        isVisible.content = true;
        isVisible.position = true;
        isVisible.statements = true;

        label.style("display", 'inline');
        rect.style("display", 'inline');

        hideLabelsOfNotSelectedNodes();

        // also show content of positions and statements
        $('#positions').find('i').removeClass().addClass("fa fa-check-square-o");
        $('#statements').find('i').removeClass().addClass("fa fa-check-square-o");
    }

    /**
     * Hide labels of not selected nodes
     */
    function hideLabelsOfNotSelectedNodes() {
        // hide labels of nodes which are not selected
        d3.selectAll(".node").each(function (d) {
            if (d3.select('#circle-' + d.id).attr('fill') === colors.light_grey) {
                d3.select('#label-' + d.id).style("display", 'none');
                d3.select("#rect-" + d.id).style("display", 'none');
            }
        });
    }

    /**
     * Hide all labels of graph.
     */
    function hideLabels() {
        isVisible.content = false;
        label.style("display", 'none');
        rect.style("display", 'none');
        addListenerForTooltip();
        if (isVisible.position || isVisible.statements) {
            $('#positions').find('i').removeClass().addClass("fa fa-square-o");
            $('#statements').find('i').removeClass().addClass("fa fa-square-o");
        }
        isVisible.position = false;
        isVisible.statements = false;
    }

    /**
     * Show labels for positions.
     */
    function showPositions() {
        isVisible.position = true;
        // select positions
        if (isVisible.statements) {
            $('#labels').find('i').removeClass().addClass("fa fa-check-square-o");
            setDisplayStyleOfNodes('inline', 'inline');
        } else {
            $('#labels').find('i').removeClass().addClass("fa fa-minus-square-o");
            setDisplayStyleOfNodes('inline', 'none');
        }
    }

    /**
     * Hide labels for positions.
     */
    function hidePositions() {
        isVisible.position = false;
        addListenerForTooltip();
        if (!isVisible.statements) {
            $('#labels').find('i').removeClass().addClass("fa fa-square-o");
            setDisplayStyleOfNodes('none', 'none');
        } else {
            $('#labels').find('i').removeClass().addClass("fa fa-minus-square-o");
            setDisplayStyleOfNodes('none', 'inline');
        }
    }

    /**
     * Show labels for statements.
     */
    function showStatements() {
        isVisible.statements = true;
        if (isVisible.position) {
            $('#labels').find('i').removeClass().addClass("fa fa-check-square-o");
            setDisplayStyleOfNodes('inline', 'inline');
        } else {
            $('#labels').find('i').removeClass().addClass("fa fa-minus-square-o");
            setDisplayStyleOfNodes('none', 'inline');
        }
    }

    /**
     * Hide labels for statements.
     */
    function hideStatements() {
        isVisible.statements = false;
        addListenerForTooltip();
        if (!isVisible.position) {
            $('#labels').find('i').removeClass().addClass("fa fa-square-o");
            setDisplayStyleOfNodes('none', 'none');
        } else {
            $('#labels').find('i').removeClass().addClass("fa fa-minus-square-o");
            setDisplayStyleOfNodes('inline', 'none');
        }
    }

    /**
     * Get id of node.
     *
     * @param node
     * @returns {*}
     */
    function getId(node) {
        if (node === "issue") {
            return node;
        }
        return "statement_" + node;
    }

    /**
     * Show all statements, which the current user has created.
     */
    function showMyStatements() {
        isVisible.attack = true;
        isVisible.support = true;

        // show supports and attacks on statements
        if (isVisible.support) {
            $('#supports-on-my-statements').find('i').removeClass().addClass("fa fa-check-square-o");
            isVisible.support = true;
        }
        if (isVisible.attack) {
            $('#attacks-on-my-statements').find('i').removeClass().addClass("fa fa-check-square-o");
            isVisible.attack = true;
        }

        // graying all elements of graph
        edges.forEach(function (d) {
            grayingElements(d);
        });

        selectSupportsAttacks();
    }

    /**
     * Hide all statements, which the current user has created.
     */
    function hideMyStatements() {
        isVisible.attack = false;
        isVisible.support = false;

        // hide supports and attacks on statements
        $('#supports-on-my-statements').find('i').removeClass().addClass("fa fa-square-o");
        $('#attacks-on-my-statements').find('i').removeClass().addClass("fa fa-square-o");

        highlightAllElements();

        // delete border of nodes
        deleteBorderOfCircle();
    }

    /**
     * Show all supports on the statements, which the current user has created.
     */
    function showSupportsOnMyStatements() {
        isVisible.support = true;

        // hide statements
        // delete border of nodes
        deleteBorderOfCircle();

        // if attacks on statements of current user are visible, highlight additionally the supports
        if (!isVisible.attack) {
            $('#my-statements').find('i').removeClass().addClass("fa fa-minus-square-o");
            // graying all elements of graph
            edges.forEach(function (d) {
                grayingElements(d);
            });
        } else {
            $('#my-statements').find('i').removeClass().addClass("fa fa-check-square-o");
        }

        selectSupportsAttacks();
    }

    /**
     * Hide all supports on the statements, which the current user has created.
     */
    function hideSupportsOnMyStatements() {
        isVisible.support = false;

        deleteBorderOfCircle();

        // if attacks are not visible, show the default view of the graph
        // else make them visible
        if (!isVisible.attack) {
            $('#my-statements').find('i').removeClass().addClass("fa fa-square-o");
            highlightAllElements();
        } else {
            $('#my-statements').find('i').removeClass().addClass("fa fa-minus-square-o");
            showAttacksOnMyStatements();
        }
    }

    /**
     * Show all attacks on the statements, which the current user has created.
     */
    function showAttacksOnMyStatements() {
        isVisible.attack = true;

        // hide statements
        // delete border of nodes
        deleteBorderOfCircle();

        // if supports on statements of current user are visible, highlight additionally the attacks
        if (!isVisible.support) {
            $('#my-statements').find('i').removeClass().addClass("fa fa-minus-square-o");
            // graying all elements of graph
            edges.forEach(function (d) {
                grayingElements(d);
            });
        } else {
            $('#my-statements').find('i').removeClass().addClass("fa fa-check-square-o");
        }

        selectSupportsAttacks();
    }

    /**
     * Hide all attacks on the statements, which the current user has created.
     */
    function hideAttacksOnMyStatements() {
        isVisible.attack = false;

        deleteBorderOfCircle();

        if (!isVisible.support) {
            $('#my-statements').find('i').removeClass().addClass("fa fa-square-o");
            highlightAllElements();
        } else {
            $('#my-statements').find('i').removeClass().addClass("fa fa-minus-square-o");
            showSupportsOnMyStatements();
        }
    }

    /**
     *
     * @param new_limit
     */
    function showNodesUntilMoment(new_limit) {
        var tmp_edges = edges;
        edges.forEach(function (edge) {
            var edge_source_timestamp = parseInt(edge.source.timestamp) * 1000;
            var edge_target_timestamp = parseInt(edge.target.timestamp) * 1000;
            new_limit = parseInt(new_limit);
            if (edge_source_timestamp >= new_limit || edge_target_timestamp >= new_limit) {
                tmp_edges = $.grep(tmp_edges, function (value) {
                    return value !== edge;
                });
                highlightElements(edge);
            }
        });
        edges.forEach(function (edge) {
            grayingElements(edge);
        });
        tmp_edges.forEach(function (edge) {
            highlightElements(edge);
        });
    }

    /**
     * Select supports or attacks on statements of current user.
     */
    function selectSupportsAttacks() {
        circleIds = [];
        force.nodes().forEach(function (d) {
            var nick = $('#header_nickname').data('public-nickname');
            var author = d.author.name;
            nick = typeof nick === 'undefined' ? nick : nick.toLocaleLowerCase();
            author = typeof author === 'undefined' ? author : author.toLocaleLowerCase();
            if (author === nick) {
                circleIds.push(selectUid(d.id));
            }
        });

        showPartOfGraph(circleIds);
    }

    /**
     * Show current path.
     *
     * @param jsonData
     */
    function showPath(jsonData) {
        $('#show-my-path').hide();
        $('#hide-my-path').show();

        edges.forEach(function (d) {
            grayingElements(d);
        });

        if (jsonData.path.length !== 0) { // if jsonData.path is not empty highlight path
            highlightPath(jsonData);
        } else { // if jsonData.path is empty color issue
            d3.select('#circle-issue').attr('fill', colors.grey);
        }
    }

    /**
     * Hide current path.
     */
    function hidePath() {
        $('#show-my-path').show();
        $('#hide-my-path').hide();
        edges.forEach(function (d) {
            highlightElements(d);
        });
    }

    /**
     * Highlight path.
     *
     * @param jsonData
     */
    function highlightPath(jsonData) {
        var edgesCircleId = [];

        // run through all values in jsonData.path
        jsonData.path.forEach(function (d) {
            edges.forEach(function (edge) {
                // edge without virtual node
                if ((edge.source.id === getId(d[0])) && (edge.target.id === getId(d[1]))) {
                    edgesCircleId.push(edge);
                }
                // edge with virtual node
                else if (edge.source.id === getId(d[0]) && edge.target.label === '') {
                    findEdgesVirtualNode(edge, edgesCircleId, d);
                }
            });
        });

        // highlight path
        edgesCircleId.forEach(function (d) {
            highlightElements(d);
        });
    }

    /**
     * Find two edges which connect source and target.
     *
     * @param edge
     * @param edgesCircleId
     * @param d
     */
    function findEdgesVirtualNode(edge, edgesCircleId, d) {
        // edge from virtual node to statement
        edges.forEach(function (e) {
            if (e.source.id === edge.target.id && e.target.id === getId(d[1])) {
                edgesCircleId.push(edge);
                edgesCircleId.push(e);
            }
        });
    }

    /**
     * Highlight all elements of graph.
     */
    function highlightAllElements() {
        edges.forEach(function (d) {
            highlightElements(d);
        });
    }

    /**
     * Delete border of circle.
     */
    function deleteBorderOfCircle() {
        // delete border of nodes
        force.nodes().forEach(function (d) {
            d3.select('#circle-' + d.id).attr('stroke', 'none');
        });
    }

    /**
     * Set display style of nodes.
     *
     * @param positionStyle
     * @param statementStyle
     */
    function setDisplayStyleOfNodes(positionStyle, statementStyle) {
        // select edges with position as source and issue as target
        d3.selectAll(".node").each(function (d) {
            // set display style of statements
            if (d3.select('#circle-' + d.id).attr('fill') !== colors.light_grey) {
                d3.select('#label-' + d.id).style("display", statementStyle);
                d3.select("#rect-" + d.id).style("display", statementStyle);
            }
            d3.selectAll(".link").each(function (e) {
                // only show labels of highlighted nodes
                if (e.source.id === d.id && e.target.id === 'issue' && d3.select('#circle-' + d.id).attr('fill') !== colors.light_grey) {
                    // set display style of positions
                    d3.select('#label-' + d.id).style("display", positionStyle);
                    d3.select("#rect-" + d.id).style("display", positionStyle);
                }
            });
        });
    }

    /**
     * Show/hide tooltips on mouse event.
     */
    function addListenerForTooltip() {
        d3.selectAll('.node').on("mouseover", function (d) {
            determineShowOrHideTooltip(d, true);
        }).on("mouseout", function (d) {
            determineShowOrHideTooltip(d, false);
        });
    }

    /**
     * Show or hide tooltip of node dependent on selected side-bar buttons.
     *
     * @param d: current node
     * @param mouseover
     */
    function determineShowOrHideTooltip(d, mouseover) {
        const isPosition = testNodePosition(d);
        if ((!isVisible.position && isPosition) || (!isVisible.statements && !isPosition)) {
            showHideTooltip(d, mouseover);
        }
    }

    /**
     * Test whether the selected node is a position.
     *
     * @param d
     */
    function testNodePosition(d) {
        var isPosition = false;
        d3.selectAll(".link").each(function (e) {
            if (e.source.id === d.id && e.target.id === 'issue') {
                isPosition = true;
            }
        });
        return isPosition;
    }

    /**
     * Show or hide tooltip of node dependent on mouse event.
     *
     * @param d
     * @param mouseover
     */
    function showHideTooltip(d, mouseover) {
        // if there is a mouseover-event show the tooltip
        if (mouseover) {
            d3.select('#label-' + d.id).style('display', 'inline');
            d3.select('#rect-' + d.id).style('display', 'inline');
            // determine color of circle before mouse over
            // to restore color on mouse out
            currentColorOfCircle = d3.select('#circle-' + d.id).attr('fill');
            d3.select('#circle-' + d.id).attr('fill', new Colors().grey);
        }
        // otherwise there is a mouseout-out, then hide the tooltip
        else {
            d3.select('#label-' + d.id).style('display', 'none');
            d3.select('#rect-' + d.id).style('display', 'none');
            // if circle d is currently clicked restore originally color of circle
            if (d.id === selectedCircleId) {
                d3.select('#circle-' + d.id).attr('fill', d.color);
            } else {
                d3.select('#circle-' + d.id).attr('fill', currentColorOfCircle);
            }
        }
    }

    /**
     * Show modal.
     */
    function showModal(d) {
        var popup = $('#popup-jump-graph');
        if (d.id !== 'issue') {
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
     * @param circleId: id of selected node
     */
    function showArgumentsOfIdInGraph(circleId) {
        // edges with selected circle as source or as target
        var edgesCircleId = [];
        // select all incoming and outgoing edges of selected circle
        edges.forEach(function (d) {
            var circleUid = selectUid(circleId);
            // supports
            if ((isVisible.support || isVisible.attack) && selectUid(d.target.id) === circleUid) {
                edgesCircleId.push(d);
            } else if ((selectUid(d.source.id) === circleUid || selectUid(d.target.id) === circleUid) && (!isVisible.attack && !isVisible.support)) {
                edgesCircleId.push(d);
            }
        });

        // if isMyStatementsClicked is false gray all elements at each function call,
        // else the graph is colored once gray
        if (!isVisible.my_statements && !isVisible.support && !isVisible.attack) {
            edges.forEach(function (d) {
                grayingElements(d);
            });
        }
        highlightElementsVirtualNodes(edges, edgesCircleId, true);
        edgesCircleId.forEach(function (d) {
            if (isVisible.attack && d.color === colors.red) {
                highlightElements(d);
            }
            if (isVisible.support && d.color === colors.green) {
                highlightElements(d);
            } else if (!isVisible.attack && !isVisible.support) {
                highlightElements(d);
            }
        });
    }

    /**
     * Highlight incoming and outgoing edges of selected node.
     *
     * @param circleIds: ids of selected node
     */
    function showPartOfGraph(circleIds) {
        // edges with selected circle as source or as target
        var edgesIds = [];
        var nodeId = [];
        // select all incoming and outgoing edges of selected circle
        edges.forEach(function (d) {
            // add source for supports/attacks
            var relation = isVisible.support || isVisible.attack;
            var selected = $.inArray(d.source.id, circleIds) !== -1;
            if (relation && selected) {
                edgesIds.push(d);
            }
            // get all targets of the edges without the edge itself
            relation = !(isVisible.support || isVisible.attack) || d.target.type === 'position';
            selected = $.inArray(d.target.id, circleIds) !== -1;
            if (relation && selected) {
                nodeId.push(d);
            }
        });

        // if isMyStatementsClicked is false gray all elements at each function call,
        // else the graph is colored once gray
        var nothing = !isVisible.my_statements && !isVisible.support && !isVisible.attack;
        if (nothing) {
            edges.forEach(function (d) {
                grayingElements(d);
            });
        }
        highlightElementsVirtualNodes(edges, edgesIds, false);
        edgesIds.forEach(function (d) {
            var attack = isVisible.attack && d.color === colors.red;
            var support = isVisible.support && d.color === colors.green;
            var other = !isVisible.attack && !isVisible.support;
            if (attack || support || other) {
                hightlghtEdge(d);
                highlightEdgeSource(d);
            }
        });
        nodeId.forEach(function (d) {
            var attack = isVisible.attack && d.color === colors.red;
            var support = isVisible.support && d.color === colors.green;
            var other = !isVisible.attack && !isVisible.support;
            if (attack || support || other) {
                hightlightEdgeTarget(d);
            }
        });
    }

    /**
     * Highlight incoming and outgoing edges of virtual node.
     *
     * @param edges
     * @param edgesCircleId
     * @param highlightCompleteArgument
     */
    function highlightElementsVirtualNodes(edges, edgesCircleId, highlightCompleteArgument) {
        var virtualNodes = [];
        var virtualNodesIds = [];
        do {
            change = false;
            // virtual nodes
            createVirtualNodesArray(edgesCircleId, virtualNodes, virtualNodesIds);
            // edges with a virtual node as source or as target
            createVirtualNodesEdgesArray(edges, virtualNodes, edgesCircleId, highlightCompleteArgument);
        }
        while (change);
    }

    /**
     * Create array with virtual nodes.
     *
     * @param edgesCircleId
     * @param virtualNodes
     * @param virtualNodesIds
     */
    function createVirtualNodesArray(edgesCircleId, virtualNodes, virtualNodesIds) {
        edgesCircleId.forEach(function (d) {
            if (d.source.label === '') {
                if ($.inArray(d.source.id, virtualNodesIds) === -1) {
                    change = true;
                    virtualNodesIds.push(d.source.id);
                    virtualNodes.push(d.source);
                }
            }
            if (d.target.label === '') {
                if ($.inArray(d.target.id, virtualNodesIds) === -1) {
                    change = true;
                    virtualNodesIds.push(d.target.id);
                    virtualNodes.push(d.target);
                }
            }
        });
    }

    /**
     * Create array which contains edges with virtual node as source or as target.
     *
     * @param edges
     * @param virtualNodes
     * @param edgesCircleId
     * @param highlightCompleteArgument
     */
    function createVirtualNodesEdgesArray(edges, virtualNodes, edgesCircleId, highlightCompleteArgument) {
        edges.forEach(function (d) {
            virtualNodes.forEach(function (e) {
                if (d.source.id === e.id || (d.target.id === e.id && highlightCompleteArgument)) {
                    edgesCircleId.push(d);
                }
            });
        });
    }

    /**
     * Highlighting components of graph.
     *
     * @param edge: edge that should be highlighted
     */
    function highlightElements(edge) {
        hightlghtEdge(edge);
        highlightEdgeSource(edge);
        hightlightEdgeTarget(edge);
    }

    /**
     *
     * @param edge
     */
    function hightlghtEdge(edge) {
        d3.select('#link-' + edge.id).style('stroke', edge.color);
        d3.select("#marker_" + edge.edge_type + edge.id).attr('fill', edge.color);
    }

    /**
     *
     * @param edge
     */
    function highlightEdgeSource(edge) {
        d3.select('#circle-' + edge.source.id).attr('fill', edge.source.color);
        if ((isVisible.support || isVisible.attack) && $.inArray(edge.source.id, circleIds) !== -1) {
            d3.select('#circle-' + edge.source.id).attr({fill: edge.source.color, stroke: 'black'});
        }
    }

    /**
     *
     * @param edge
     */
    function hightlightEdgeTarget(edge) {
        d3.select('#circle-' + edge.target.id).attr('fill', edge.target.color);
        if ((isVisible.support || isVisible.attack) && $.inArray(edge.target.id, circleIds) !== -1) {
            d3.select('#circle-' + edge.target.id).attr({fill: edge.target.color, stroke: 'black'});
        }
    }

    /**
     * Graying components of graph.
     *
     * @param edge: edge that should be gray
     */
    function grayingElements(edge) {
        // edges
        d3.select('#link-' + edge.id).style('stroke', colors.light_grey);
        // nodes
        d3.select('#circle-' + edge.source.id).attr('fill', colors.light_grey);
        d3.select('#circle-' + edge.target.id).attr('fill', colors.light_grey);
        // arrows
        d3.select("#marker_" + edge.edge_type + edge.id).attr('fill', colors.light_grey);
    }
}
