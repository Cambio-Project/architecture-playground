String.prototype.format = function () {
    let i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

var width     = window.innerWidth - 50;
var height    = window.innerHeight - 100;
var node_size = 5;
var color     = d3.scaleOrdinal(d3.schemeCategory10);
var zoom_level;

var simulation = d3
    .forceSimulation(graph.nodes)
    .force("charge", d3.forceManyBody().strength(-3000))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("x", d3.forceX(width / 2).strength(1))
    .force("y", d3.forceY(height / 2).strength(1))
    .force("link", d3.forceLink(graph.links).id(function (d) {return d.id; }).distance(25).strength(1))
    .on("tick", ticked);

var svg = d3
    .select("body")
    .append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("width", width)
    .attr("height", height)
    .style("border", "1px solid black");

var container = svg.append("g");
container
    .append("svg:defs")
    .selectAll("marker")
    .data(["end"])
    .enter()
    .append("svg:marker")
    .attr("id", String)
    .attr("viewBox", "0 -3 6 7")
    .attr("refX", 13)
    .attr("fill", "#555555")
    .attr("markerWidth", node_size)
    .attr("markerHeight", node_size)
    .attr("orient", "auto")
    .append("svg:path")
    .attr("d", "M 0,-3 L 7,0 L 0,3");

var link = container
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("path")
    .attr("stroke", "#AAAAAA")
    .attr("fill", "transparent")
    .attr("stroke-width", "1px")
    .attr("marker-end", "url(#end)");

var node = container
    .append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter()
    .append("circle")
    .attr("r", node_size)
    .attr("fill", function (d) { return color(d.group); })

var node_labels = container
    .append("g")
    .attr("class", "node-labels")
    .selectAll("g")
    .data(graph.nodes)
    .enter()
    .append("text")
    .text(function (d) { return d.label; });

var link_labels = container
    .append("g")
    .attr("class", "link-labels")
    .selectAll("g")
    .data(graph.links)
    .enter()
    .append("text")
    .text(function (d) { return d.label; });

zoom_level = d3
    .zoom()
    .scaleExtent([.1, 4])
    .on("zoom", function () {
        container.attr("transform", d3.event.transform);
        d3.select("#zoom").property("value", d3.event.transform.k);
    });
svg.call(zoom_level);

node.call(
    d3.drag()
      .on("start", function (d) {
          d3.event.sourceEvent.stopPropagation();
          if (!d3.event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
      })
      .on("drag", function (d) {
          d.fx = d3.event.x;
          d.fy = d3.event.y;
      })
      .on("end", function (d) {
          if (!d3.event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
      })
);

function ticked() {
    link.attr("d", function (d) {
        let x1 = d.source.x,
            y1 = d.source.y,
            x2 = d.target.x,
            y2 = d.target.y;

        if (d.source !== d.target) {
            let dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = Math.sqrt(dx * dx + dy * dy);
            return "M {} {} A {} {} 0 0 1 {} {}".format(x1, y1, dr, dr, x2, y2);
            // return "M {} {} L {} {}".format(x1, y1, x2, y2)
        }
        let scale = d.label.length * 3; // TODO size of the curve
        return "M {} {} C {} {} {} {} {} {}".format(x1, y1, x1 - scale, y1 - scale, x1 - scale, y1 + scale, x1, y1);
    })

    node.attr("cx", function (d) { return d.x; })
        .attr("cy", function (d) { return d.y; });

    node_labels
        .attr("x", function (d) { return d.x + 10; })
        .attr("y", function (d) { return d.y + 10; });

    link_labels
        .attr("x", function (d) { return d.source.x + (d.target.x - d.source.x) * 0.5 + 10; })
        .attr("y", function (d) { return d.source.y + (d.target.y - d.source.y) * 0.5 + 10; });
}

function hidenodes(checkbox) {
    node.style('visibility', checkbox.checked ? 'visible' : 'hidden');
}

function hidelinks(checkbox) {
    link.style('visibility', checkbox.checked ? 'visible' : 'hidden');
}

function hidenodelabels(checkbox) {
    node_labels.style('visibility', checkbox.checked ? 'visible' : 'hidden');
}

function hidelinklabels(checkbox) {
    link_labels.style('visibility', checkbox.checked ? 'visible' : 'hidden');
}

function zoom(slider) {
    zoom_level.scaleTo(svg, Math.round(slider.value * 10) / 10)
}