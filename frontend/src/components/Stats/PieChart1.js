import React, { Component } from 'react';
import { LabeledArc } from './Arc.js';

class Piechart extends Component {
    constructor() {
        super();

        var d3 = require("d3");

        this.pie = d3.pie().value((d) => d.value);
        this.colors = d3.schemeCategory10;
        this.state = {x: 200, y: 100, outerRadius: 130, innerRadius: 50,
          data: [  {value: 12, label: 'John'},
                   {value: 13, label: 'Peter'},
                   {value: 21, label: 'Anna'},
                   {value: 11, label: 'Maria'},
                   {value: 27, label: 'Vlad'}
                   ]};

    }

    arcGenerator(d, i) {
         return (
            <LabeledArc key={`arc-${i}`}
                        data={d}
                        innerRadius={this.state.innerRadius}
                        outerRadius={this.state.outerRadius}
                        color={this.colors[i]} />
        );
    }

    render() {
        let pie = this.pie(this.state.data),
            translate = `translate(${this.state.x}, ${this.state.y})`;

        return (
            <div id="svg2">
                <svg width="350" height="300" viewBox="100 -50 300 300">
                    <g transform={translate}>
                        {pie.map((d, i) => this.arcGenerator(d, i))}
                    </g>
                    <text x="100" y="250" font-family="sans-serif" font-size="20px" fill="black">The most active users</text>
                </svg>
            </div>
        )
    }
}

export default Piechart;
