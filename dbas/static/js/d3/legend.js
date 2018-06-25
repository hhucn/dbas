function GraphLegend(colors) {
    'use strict';
    this.labelCircle = [_t_discussion("issue"), _t_discussion("position"), _t_discussion("statement")];
    this.labelRect = [_t_discussion("support"), _t_discussion("attack")];
    this.colorCircle = [colors.grey, colors.blue, colors.yellow];
    this.colorRect = [colors.green, colors.red];
}

GraphLegend.prototype.create = function (d3){
    'use strict';
    var _this = this;

    // set properties for legend
    d3.svg.legend = function () {
        function legend(selection) {
            _this.createNodeSymbols(selection, _this.labelCircle, _this.colorCircle);
            _this.createEdgeSymbols(selection, _this.labelRect, _this.colorRect);
            _this.createLabelsForSymbols(selection, _this.labelCircle, _this.labelRect);
        }

        return legend;
    };
};

/**
 * Create symbols for nodes.
 *
 * @param selection
 * @param legendLabelCircle: array with labels for circle
 * @param legendColorCircle: array with colors
 */
GraphLegend.prototype.createNodeSymbols = function(selection, legendLabelCircle, legendColorCircle) {
    'use strict';
    selection.selectAll(".circle")
    .data(legendLabelCircle)
    .enter().append("circle")
    .attr({
        fill: function (d, i) {
            return legendColorCircle[i];
        },
        r: 6,
        cy: function (d, i) {
            return i * 40;
        }
    });
};

/**
 * Create symbols for edges.
 *
 * @param selection
 * @param legendLabelRect: array with labels for rect
 * @param legendColorRect: array with colors
 */
GraphLegend.prototype.createEdgeSymbols = function(selection, legendLabelRect, legendColorRect) {
    'use strict';
    selection.selectAll(".rect")
        .data(legendLabelRect)
        .enter().append("rect")
        .attr({
            fill: function (d, i) {
                return legendColorRect[i];
            },
            width: 15,
            height: 5,
            x: -7, y: function (d, i) {
                return i * 40 + 118;
            }
        });
};

/**
 * Create labels for symbols.
 *
 * @param selection
 * @param legendLabelCircle: array with labels for circle
 * @param legendLabelRect: array with labels for rect
 */
GraphLegend.prototype.createLabelsForSymbols = function(selection, legendLabelCircle, legendLabelRect) {
    'use strict';
    selection.selectAll(".text")
        .data(legendLabelCircle.concat(legendLabelRect))
        .enter().append("text")
        .text(function (d) {
            return d;
        })
        .attr({
            x: 20, y: function (d, i) {
                return i * 40 + 5;
            }
        });
};
