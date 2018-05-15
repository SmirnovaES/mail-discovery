const GraphV = {};

var d3, svg, width, height, color, div, simulation, links, line, title, node, nodes, circle, linkedByIndex;

function loadData(loadGraph, readyToLoad, onChangeLoading) {
    if (!readyToLoad.graph) {
        return false;
    }
    loadGraph()
        .then(graph => {
            // // transition
            // var t = d3.transition()
            //     .duration(750);
            var lineData = links
                .selectAll("line")
                .data(graph.links);
            lineData.exit().remove();
            line = lineData
                .enter().append("line")
                .merge(lineData)
                .attr("opacity", function(d) { 
                    var values = graph.links.map(function(element) {
                        return element.value;
                    });
                    return 0.7 + 0.3 * d.value/d3.max(values); 
                })
                .on("click", onLineClick);
            
            var nodeData = nodes.selectAll("g.node")
                .data(graph.nodes);
            nodeData.exit().remove();
            node = nodeData.enter().append("g")
                .attr("class", "node")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));  

            circle = node.append("circle")
                .attr("r", 10)
                .attr("stroke", "black")
                .attr("fill", function(d, i) { return color(d.group); })
                .on("mouseover", mouseOver(.2))
                .on("mouseout", mouseOut)
                .on("click", onCircleClick);

            title = node.append("text")
                .attr("class", "textClass")
                .attr("dx", 12)
                .attr("dy", ".35em")
                .text(function(d) {
                    return d.id.slice(0,4);
                })
                .style("stroke", "black")
                .style("pointer-events", "none")
                .style("stroke-width", 0.5)
                .style("fill", function(d) {
                    return color(d.group);
                });

            simulation
                .nodes(graph.nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(graph.links);

            simulation.alphaTarget(1).restart();

            linkedByIndex = {};
            graph.links.forEach(function(d) {
                linkedByIndex[d.source.index + "," + d.target.index] = 1;
            });

            line = line.merge(lineData);
            node = node.merge(nodeData);
            circle = node.selectAll("circle");
            title = node.selectAll("text"); 

            readyToLoad.graph = false;
            onChangeLoading(readyToLoad);
        })
        .catch(function(error) {
            console.log(error);
        });
}
GraphV.create = (el, loadGraph, readyToLoad, onChangeLoading) => {
    // D3 Code to create the chart
    d3 = require("d3"); 
    svg = d3.select("svg")
        .call(d3.zoom().on("zoom", () => svg.attr("transform", d3.event.transform)))
        .on("click", onSvgClick)
        .append("g")


    width = +svg.attr("width");
    height = +svg.attr("height");

    // Define the div for the tooltip
    div = d3.select("body").append("div")	
        .attr("class", "infoBlock")				
        .style("opacity", 0);

    color = d3.scaleOrdinal(d3["schemeCategory10"]);

    simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; })
            .distance(30).strength(0.1))
        .force("charge", d3.forceManyBody())
        .force('x', d3.forceX())
        .force('y', d3.forceY())
        .force("center", d3.forceCenter(width / 2, height / 2));


    links = svg.append("g")
        .attr("class", "links");

    nodes = svg.append("g")
        .attr("class", "nodes");

    loadData(loadGraph, readyToLoad, onChangeLoading);
    
};

GraphV.update = (el, loadGraph, readyToLoad, onChangeLoading, chart) => {
    // D3 Code to update the chart
    loadData(loadGraph, readyToLoad, onChangeLoading);
};

GraphV.destroy = () => {
    // Cleaning code here
};

export default GraphV;

function ticked() {
    line
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
}


function isConnected(a, b) {
    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index === b.index;
}

function mouseOver(opacity) {
    return function(d) {
        circle.transition()
            .duration(500)
            .style("stroke-opacity", function(o) {
                var thisOpacity = isConnected(d, o) ? 1 : opacity;
                return thisOpacity;
            })
            .style("fill-opacity", function(o) {
                var thisOpacity = isConnected(d, o) ? 1 : opacity;
                return thisOpacity;
            });	

        line.transition()
            .duration(500)
            .style("stroke-opacity", function(o) {
                return o.source === d || o.target === d ? 1 : opacity;
            })
            .style("stroke", function(o){
                return o.source === d || o.target === d ? color(o.source.group) : "#ddd";
            });
    };
}

function mouseOut() {
    circle.transition()
        .duration(500)
        .style("stroke-opacity", 1)
        .style("fill-opacity", 1);
    
    line.transition()
        .duration(500)
        .style("stroke-opacity", 1)
        .style("fill-opacity", 1)
        .style("stroke", "#999");	
}

function onCircleClick(d) {
    div.transition()		
        .duration(200)		
        .style("opacity", 1);		
    div.html(d.id + "<br/>"  + d.group)	
        .style("left", (d3.event.pageX) + "px")		
        .style("top", (d3.event.pageY - 28) + "px");
    d3.event.stopPropagation();
}

function onLineClick(d) {
    div.transition()		
        .duration(200)		
        .style("opacity", 1);		
    div.html(d.source.id + "<br/>"  + d.target.id)	
        .style("left", (d3.event.pageX) + "px")		
        .style("top", (d3.event.pageY - 28) + "px");
    d3.event.stopPropagation();
}


function onSvgClick(event) {
    div.transition()		
        .duration(500)		
        .style("opacity", 0);
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}
