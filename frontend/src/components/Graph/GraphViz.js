import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import './GraphViz.css'

class GraphViz extends Component {
	constructor(props){
		super(props)
		this.createGraph = this.createGraph.bind(this)
	}
	componentDidMount() {
		this.createGraph()
	}
	componentDidUpdate() {
		this.createGraph()
	}
	createGraph() {
		var d3 = require("d3");

		var svg = d3.select("svg")
			.call(d3.zoom().on("zoom", () => svg.attr("transform", d3.event.transform)))
			.on("click", onSvgClick)
			.append("g")


		var width = +svg.attr("width");
		var height = +svg.attr("height");

		// Define the div for the tooltip
		var div = d3.select("body").append("div")	
			.attr("class", "infoBlock")				
			.style("opacity", 0);

		var color = d3.scaleOrdinal(d3["schemeCategory10"]);

		var simulation = d3.forceSimulation()
			.force("link", d3.forceLink().id(function(d) { return d.id; }))
			.force("charge", d3.forceManyBody())
			.force("center", d3.forceCenter(width / 2, height / 2));

		fetch("http://localhost:8001/miserables.json")
			.then(response => response.json())
			.then(graph => {

				var link = svg.append("g")
					.attr("class", "links")
					.selectAll("line")
					.data(graph.links)
					.enter().append("line")
					.attr("opacity", function(d) { 
						var values = graph.links.map(function(element) {
							return element.value;
						});
						return 0.7 + 0.3 * d.value/d3.max(values); 
					})
					.on("click", onLinkClick);

				var node = svg.append("g")
					.attr("class", "nodes")
				
				var circle = node.selectAll("circle")
					.data(graph.nodes)
					.enter()
					.append("circle")
					.attr("r", 10)
					.attr("stroke", "black")
					.attr("fill", function(d, i) { return color(d.group); })
					.call(d3.drag()
						.on("start", dragstarted)
						.on("drag", dragged)
						.on("end", dragended))
					.on("mouseover", mouseOver(.2))
					.on("mouseout", mouseOut)
					.on("click", onCircleClick);
				
				var title = node.selectAll("title")
					.data(graph.nodes)
					.enter()
					.append("text")
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

				function ticked() {
					link
						.attr("x1", function(d) { return d.source.x; })
						.attr("y1", function(d) { return d.source.y; })
						.attr("x2", function(d) { return d.target.x; })
						.attr("y2", function(d) { return d.target.y; });

					circle
						.attr("cx", function(d) { return d.x; })
						.attr("cy", function(d) { return d.y; });

					title
						.attr("x", function(d) { return d.x; })
						.attr("y", function(d) { return d.y; });
				}

				var linkedByIndex = {};
				graph.links.forEach(function(d) {
					linkedByIndex[d.source.index + "," + d.target.index] = 1;
				});

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

						link.transition()
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
					
					link.transition()
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

				function onLinkClick(d) {
					div.transition()		
						.duration(200)		
						.style("opacity", 1);		
					div.html(d.source.id + "<br/>"  + d.target.id)	
						.style("left", (d3.event.pageX) + "px")		
						.style("top", (d3.event.pageY - 28) + "px");
					d3.event.stopPropagation();
				}
			});
		
		function onSvgClick(event) {
			div.transition()		
				.duration(500)		
				.style("opacity", 0);
		}

		function dragstarted(d) {
			if (!d3.event.active) simulation.alphaTarget(0.3).restart();
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
	}
	render() {
		return  <svg id="graph" height="665"  viewBox="-300 -300 665 665"></svg>
	}
}

export default GraphViz
